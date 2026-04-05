# Game Review

A Django web application for writing and reading game reviews, with authentication powered by Supabase.

![Landing page screenshot](./assets/images/landing-page.png)

## Table of Contents
1. [Project Overview](#project-overview)
2. [UX Design](#ux-design)
3. [Agile Development](#agile-development)
4. [Features](#features)
5. [Technologies Used](#technologies-used)
6. [Testing](#testing)
7. [Tech Stack](#tech-Stack)
9. [Setup](#setup)
10. [Project Structure](#project-structure)
11. [Deployment](#deployment)
12. [Credits](#credits)

## Tech Stack

- Python 3 + Django 6
- Supabase (Auth + PostgreSQL)

---

## Setup

### 1. Clone the repository

```bash
git clone https://github.com/TimothyYW/game-review.git
cd game-review
```

### 2. Create and activate virtual environment

```bash
python -m venv .venv
source .venv/bin/activate        # macOS/Linux
.venv\Scripts\activate           # Windows
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure environment variables

Create a `.env` file in the root directory:

```env
SUPABASE_URL=
SUPABASE_KEY=
SUPABASE_SERVICE_KEY=

# For Django ORM (standard Postgres connection)
DATABASE_URL="postgresql://postgres:[PASSWORD]@db.[PROJECT_REF].supabase.co:5432/postgres"

ALLOWED_HOSTS=
DEBUG='True'
```

> Get these values from your Supabase project: **Settings → API** and **Settings → Database**.

### 5. Set up the Supabase database

In the Supabase dashboard, go to **SQL Editor** and run the contents of:

```
assets/schema.sql
```

### 6. Run database migrations

```bash
python manage.py migrate
```


### 7. Start the development server

```bash
python manage.py runserver
```

Open [http://127.0.0.1:8000](http://127.0.0.1:8000) in your browser.

---

## Project Structure

```
game-review/
├── accounts/       # Auth views, middleware, decorators
├── news/           # Game review CRUD
├── core/           # Settings, URLs, Supabase client
├── templates/      # Base and app-level templates
├── assets/         # schema.sql
└── manage.py
```
