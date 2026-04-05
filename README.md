# Game Review

A Django web application for writing and reading game reviews, with authentication powered by Supabase. Not just game any type of topic from IT, and user can up vote or down vote the post and leave comments.

![screenshot mock-up test](./assets/images/mock-up-test.png)

## Table of Contents
1. [Project Overview](#project-overview)
2. [UX Design](#ux-design)
4. [Features](#features)
5. [Technologies Used](#technologies-used)
6. [Testing](#testing)
7. [Tech Stack](#tech-Stack)
9. [Setup](#setup)
10. [Project Structure](#project-structure)
11. [Deployment](#deployment)
12. [Credits](#credits)

## Project Overview

- Create account
- Update profile
- Posting about other topic such as IT topic in general.
- Share detailed reviews of games they've played.
- Browse reviews from other gamers.
- Manage their profile and review history.
- Search for specific games or reviews.
- Up vote or Down vote the review that are left.

[Live Site](https://game-review-cqgo.onrender.com)

## UX Design

### Wireframe

Wireframe landing page

![Wireframe Landing Page](./assets/images/wireframe-landing-page.png)

Wireframe login page

![Wireframe Login Page](./assets/images/wireframe-login-page.png)

Wireframe edit profile

![Wireframe Edit Profile](./assets/images/wireframe-edit-profile.png)

## Features

### Existing Features

Review Management
- Create Reviews
- View Reviews

![Landing page screenshot](./assets/images/landing-page.png)

User Authentication
- Registration
- Login/Logout
- Password Reset

![Login/Register page screenshot](./assets/images/login/register-page.png)

Profile Management
- Update Profile
- View Review History
- Profile Picture Upload

![searching page screenshot](./assets/images/searching-page.png)

Search Functionality
- Search by Catagories
- Search by Filter

### Future Feature

1. Deleting Post

## Technologies Used

### Languages

- HTML5
- JavaScript
- Python 3.8

## Tech Stack

- Python 3 + Django 6
- Supabase (Auth + PostgreSQL)

---

## Testing



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
## Deployment

This guide walks through deploying this Django application to [Render](https://render.com).

### 1. Project Preparation

Install the required packages:

```bash
pip install gunicorn whitenoise psycopg2-binary python-dotenv
pip freeze > requirements.txt
```

### 2. Make executable a build script 

```bash
chmod a+x build.sh
```

### 3. Render Dashboard Setup

1. Go to [render.com](https://render.com) and create an account
2. Click **New** → **Web Service**
3. Connect your GitHub repository
4. Select **Environment: Python 3**

Set the following:

| Setting | Value |
|---|---|
| Build Command | `./build.sh` |
| Start Command | `gunicorn core.wsgi:application` |

### 4. Environment Variables

In the Render dashboard, scroll to **Advanced** and add the following environment variables:

```
SUPABASE_URL=
SUPABASE_KEY=
SUPABASE_SERVICE_KEY=
DATABASE_URL=
ALLOWED_HOSTS=
DEBUG=False
```

Click **Deploy**.

## Credits

- Website for Mock-up test
  https://techsini.com/multi-mockup/index.php
- Mock-up test solver
  https://techsini.com/unable-to-generate-mockup-of-your-website-here-is-the-quick-fix/
