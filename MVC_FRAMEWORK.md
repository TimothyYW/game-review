# 🏗️ MVC Framework — Game News Django App

> Dokumen ini menjelaskan bagaimana proyek **Game News** mengimplementasikan pola arsitektur **MVC (Model–View–Controller)** menggunakan Django.

---

## Apa Itu MVC?

**MVC** adalah cara kita mengorganisir kode agar tidak campur aduk. Setiap bagian punya tanggung jawabnya sendiri:

```
┌─────────────┐     request      ┌─────────────┐     query      ┌─────────────┐
│             │ ───────────────► │             │ ─────────────► │             │
│   Browser   │                  │  Controller │                │    Model    │
│  (User)     │ ◄─────────────── │  (View.py)  │ ◄───────────── │ (models.py) │
│             │    response       │             │     data        │             │
└─────────────┘                  └──────┬──────┘                └─────────────┘
                                        │ render
                                        ▼
                                 ┌─────────────┐
                                 │    View     │
                                 │  (Template) │
                                 │   .html     │
                                 └─────────────┘
```

> ⚠️ **Catatan Django:** Di Django, istilahnya **MVT** (Model–View–Template), bukan MVC. Yang Django sebut "View" = Controller, dan "Template" = View. Tapi konsepnya sama persis.

| MVC Klasik | Django | Tanggung Jawab |
|---|---|---|
| **Model** | `models.py` | Definisi data & aturan database |
| **Controller** | `views.py` | Logika bisnis, ambil data, proses request |
| **View** | `templates/*.html` | Tampilan yang dilihat user di browser |

---

## 📁 Struktur Folder Proyek

```
game-news/
│
├── news/                    ← App utama (berita)
│   ├── models.py            ← [M] Model: struktur data
│   ├── views.py             ← [C] Controller: logika bisnis
│   ├── urls.py              ← Routing: URL → View
│   ├── forms.py             ← Validasi input
│   └── templates/
│       ├── list.html        ← [V] View: halaman daftar berita
│       ├── detail.html      ← [V] View: halaman detail berita
│       └── form.html        ← [V] View: form buat/edit berita
│
├── accounts/                ← App autentikasi
│   ├── views.py             ← [C] Login, Register, Profile
│   ├── decorator.py         ← Helper: cek apakah user sudah login
│   └── templates/
│       ├── login.html       ← [V] Halaman login
│       └── register.html    ← [V] Halaman register
│
├── core/                    ← Konfigurasi utama
│   ├── settings.py          ← Pengaturan Django
│   ├── urls.py              ← Root URL dispatcher
│   └── supabase.py          ← Koneksi ke Supabase
│
└── templates/
    └── base.html            ← [V] Template induk (navbar, footer)
```

---

## 🗃️ MODEL — `news/models.py`

**Model = Cetak biru data.** Model mendefinisikan seperti apa bentuk data yang disimpan di database.

```python
# news/models.py

class News(models.Model):
    id         = models.UUIDField(primary_key=True)  # ID unik tiap berita
    author_id  = models.UUIDField()                  # Siapa yang nulis
    title      = models.TextField()                  # Judul berita
    content    = models.TextField()                  # Isi berita
    image_url  = models.TextField(null=True)         # Gambar (opsional)
    votes      = models.IntegerField(default=0)      # Jumlah vote
    views      = models.IntegerField(default=0)      # Jumlah view
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "news"   # Nama tabel di Supabase PostgreSQL
        managed  = False    # Django tidak buat/ubah tabel ini (sudah ada di Supabase)
        ordering = ["-created_at"]  # Urutan default: terbaru dulu
```

> 💡 **Kenapa `managed = False`?**
> Karena tabelnya sudah dibuat duluan di Supabase. Kita hanya "memetakan" kelas Python ke tabel yang sudah ada — Django tidak perlu sentuh strukturnya.

**Model kedua — `Profile`:**

```python
class Profile(models.Model):
    id         = models.UUIDField(primary_key=True)
    username   = models.TextField()
    avatar_url = models.TextField(null=True)
    bio        = models.TextField(null=True)
```

> Model ini merepresentasikan data pengguna. Satu `News` ditulis oleh satu `Profile`.

---

## 🎮 CONTROLLER — `news/views.py`

**Controller = Otak aplikasi.** View di Django bertindak sebagai controller: menerima request, mengambil/memanipulasi data dari Model, lalu mengirim hasilnya ke Template.

### 1. Menampilkan Daftar Berita (`news_list`)

```python
# news/views.py

def news_list(request):
    # 1. AMBIL DATA dari Supabase (Model layer)
    res = (
        get_supabase_client()
        .table("news")
        .select("*, profiles(username)")   # JOIN dengan tabel profiles
        .order("created_at", desc=True)
        .execute()
    )

    # 2. AMBIL DATA KATEGORI
    categories = get_supabase_client().table("categories").select("*").execute()

    # 3. PROSES DATA (bisnis logik)
    news = []
    for item in res.data or []:
        profile = item.pop("profiles", None)
        item["author_username"] = profile["username"] if profile else "Unknown"
        # ... konversi tanggal, dll
        news.append(item)

    # 4. KIRIM KE TEMPLATE (View layer)
    return render(request, "list.html", {
        "news":       news,
        "categories": categories.data
    })
```

**Alurnya:**
```
Browser minta "/"
   → urls.py arahkan ke news_list()
   → news_list() ambil data dari Supabase
   → proses data
   → render("list.html", data)
   → HTML dikirim balik ke browser
```

---

### 2. CRUD — Create, Read, Update, Delete

| Operasi | Function | URL | HTTP Method |
|---|---|---|---|
| **Read** (list) | `news_list` | `/` | GET |
| **Read** (detail) | `news_detail` | `/<uuid>/` | GET |
| **Create** | `news_create` | `/create/` | GET + POST |
| **Update** | `news_update` | `/edit/<uuid>/` | GET + POST |
| **Delete** | `news_delete` | `/delete/<uuid>/` | POST |

**Contoh Create:**

```python
@supabase_auth_required          # ← Autorisasi: harus login dulu
def news_create(request):
    if request.method == 'POST': # ← User submit form
        form = NewsForm(request.POST)
        if form.is_valid():      # ← Validasi input
            user_id = request.session.get('supabase_user_id')

            # INSERT data ke Supabase
            get_supabase_client().table('news').insert({
                'title':     form.cleaned_data['title'],
                'content':   form.cleaned_data['content'],
                'author_id': user_id,
            }).execute()

            return redirect('news_list')  # ← Redirect setelah sukses

    else:                        # ← User buka halaman form (GET)
        form = NewsForm()

    return render(request, 'form.html', {'form': form})
```

**Contoh Delete:**

```python
@supabase_auth_required
def news_delete(request, pk):
    if request.method == "POST":
        get_supabase_client().table("news").delete().eq("id", str(pk)).execute()
    return redirect("news_list")
```

---

### 3. API Endpoint untuk Infinite Scroll

Proyek ini juga punya **REST API** untuk dipakai oleh JavaScript di frontend:

```python
def news_api(request):
    # Baca parameter dari URL: /news/api/?filter=hot&page=2
    filter_type = request.GET.get("filter", "new")
    page        = int(request.GET.get("page", 1))
    page_size   = 10

    # Terapkan filter
    if filter_type == "new":
        query = query.order("created_at", desc=True)
    elif filter_type == "top":
        query = query.order("votes", desc=True)
    elif filter_type == "hot":
        query = query.order("views", desc=True)

    # Kembalikan JSON (bukan HTML)
    return JsonResponse({
        "news":     news,
        "page":     page,
        "has_more": (offset + page_size) < total,
    })
```

> 💡 Ini yang membedakan **Traditional View** (kembalikan HTML) vs **API View** (kembalikan JSON).
> JavaScript di `list.html` memanggil endpoint ini untuk infinite scroll tanpa reload halaman.

---

## 🖼️ VIEW (TEMPLATE) — `templates/`

**Template = Tampilan yang dilihat user.** Template menerima data dari Controller lalu merendernya menjadi HTML.

### Hirarki Template

```
templates/
└── base.html          ← Template induk (berisi navbar, footer, <head>)
    └── list.html      ← extends base.html → override block content
    └── detail.html    ← extends base.html → override block content
    └── form.html      ← extends base.html → override block content
```

### Template Inheritance

```html
<!-- base.html — Template Induk -->
<!DOCTYPE html>
<html>
  <head>
    <title>{% block title %}Default{% endblock %}</title>
  </head>
  <body>
    <nav>...</nav>
    {% block content %}{% endblock %}  ← Slot untuk konten anak
  </body>
</html>
```

```html
<!-- list.html — Template Anak -->
{% extends "base.html" %}          ← "warisi" base.html
{% block title %}News Feed{% endblock %}
{% block content %}
  <!-- Konten khusus halaman list di sini -->
  {% for item in news %}
    <h2>{{ item.title }}</h2>
  {% endfor %}
{% endblock %}
```

### Django Template Language (DTL)

Template punya sintaks khusus untuk menampilkan data dari Controller:

| Sintaks | Fungsi | Contoh |
|---|---|---|
| `{{ variabel }}` | Tampilkan nilai variabel | `{{ item.title }}` |
| `{% for x in list %}` | Perulangan | `{% for news in news_list %}` |
| `{% if kondisi %}` | Percabangan | `{% if user.is_authenticated %}` |
| `{% url 'nama' %}` | Generate URL | `{% url 'news_detail' pk=item.id %}` |
| `{% csrf_token %}` | Keamanan form | Wajib ada di setiap `<form>` |
| `{% extends %}` | Warisi template lain | `{% extends "base.html" %}` |
| `{% block %}` | Slot konten | `{% block content %}{% endblock %}` |

### Template List + JavaScript (Hybrid Rendering)

Halaman `list.html` menggunakan pendekatan **hybrid**:
- HTML awal di-render oleh Django (server-side)
- Konten berita di-load oleh JavaScript via AJAX (client-side)

```html
<!-- list.html — Bagian yang dirender Django -->
<select name="category_id">
  {% for c in categories %}           ← Data dari Controller
    <option value="{{ c.id }}">{{ c.name }}</option>
  {% endfor %}
</select>

<!-- Kontainer kosong — akan diisi oleh JavaScript -->
<div id="news-container">
  <!-- Skeleton loader awal -->
</div>

<script>
  // JavaScript fetch data dari /news/api/ dan render kartu berita
  async function loadFeed(filter, page) {
    const res = await fetch(`/news/api/?filter=${filter}&page=${page}`);
    const data = await res.json();
    // ... bangun HTML dan masukkan ke #news-container
  }
  loadFeed('hot', 1);  // Muat pertama kali
</script>
```

---

## 🔗 ROUTING — `urls.py`

URL dispatcher menghubungkan URL dengan function Controller:

```python
# core/urls.py — Root URL
urlpatterns = [
    path('',       include('news.urls')),      # Semua URL berita
    path('auth/',  include('accounts.urls')),  # Login, register, dst
    path('todos/', include('todos.urls')),      # App todos
]

# news/urls.py — URL spesifik berita
urlpatterns = [
    path('',                  views.news_list,    name='news_list'),
    path('create/',           views.news_create,  name='news_create'),
    path('<uuid:pk>/',        views.news_detail,  name='news_detail'),
    path('edit/<uuid:pk>/',   views.news_update,  name='news_update'),
    path('delete/<uuid:pk>/', views.news_delete,  name='news_delete'),

    # API Endpoints (kembalikan JSON)
    path('api/',                               views.news_api,        name='news_api'),
    path('api/create/',                        views.news_api_create, name='news_api_create'),
    path('api/<uuid:pk>/vote/',                views.news_vote,       name='news_vote'),
    path('<uuid:pk>/comment/',                 views.comment_create,  name='comment_create'),
    path('api/comment/<uuid:comment_id>/vote/', views.comment_vote,   name='comment_vote'),
]
```

---

## 🔄 Alur Lengkap: User Membuat Berita Baru

```
1. User buka /create/
   └─► urls.py → news_create(request) [GET]
       └─► Cek: sudah login? (decorator @supabase_auth_required)
           ├─► Belum login → redirect ke /auth/login/
           └─► Sudah login → render form.html (kosong)

2. User isi form dan klik "Post"
   └─► Browser kirim POST /news/api/create/ (via JavaScript fetch)
       └─► urls.py → news_api_create(request) [POST]
           ├─► Validasi: title & content tidak boleh kosong
           ├─► Upload gambar ke Supabase Storage (jika ada)
           ├─► INSERT data ke tabel "news" di Supabase
           └─► Return JSON {"success": true}

3. JavaScript terima response sukses
   └─► Reset form
   └─► Panggil loadFeed() → tampilkan berita terbaru
```

---

## 🎯 Ringkasan MVC di Proyek Ini

| Layer | File Utama | Yang Dilakukan |
|---|---|---|
| **Model** | `news/models.py` | Definisi tabel `News` dan `Profile` |
| **Controller** | `news/views.py` | CRUD berita, voting, komentar, API |
| **Controller** | `accounts/views.py` | Login, register, profil, settings |
| **View** | `news/templates/list.html` | UI feed berita + infinite scroll JS |
| **View** | `news/templates/detail.html` | UI detail berita + komentar nested |
| **View** | `accounts/templates/login.html` | UI form login |
| **Routing** | `news/urls.py` | Mapping URL ke Controller |
| **Config** | `core/settings.py` | Pengaturan Django, DB, Supabase |
| **Database** | Supabase PostgreSQL | Penyimpanan data sesungguhnya |

---

*Dokumen ini dibuat sebagai referensi belajar MVC Framework menggunakan proyek Game News — Django + Supabase.*
