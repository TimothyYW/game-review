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

## Project Overview

- Create account
- Update profile
- Posting about other topic such as IT topic in general.
- Share detailed reviews of games they've played.
- Browse reviews from other gamers.
- Manage their profile and review history.
- Search for specific games or reviews.
- Up vote or Down vote the review that are left.

[Live Site](https://game-review-jg6a.onrender.com)

## UX Design

### Wireframe

Wireframe landing page

![Wireframe Landing Page](./assets/images/wireframe-landing-page.png)

Wireframe login page

![Wireframe Login Page](./assets/images/wireframe-login-page.png)

Wireframe edit profile

![Wireframe Edit Profile](./assets/images/wireframe-edit-profile.png)

## Agile development

## Features

### Existing Features
1. User Authentication
   - Registration
   - Login/Logout
   - Password Reset

2. Review Management
   - Create Reviews
   - View Reviews

3. Profile Management
   - Update Profile
   - View Review History
   - Profile Picture Upload

4. Search Functionality
   - Search by Gaming
   - Search by Filter

%. Miscellenious 

### Future Feature


## Technologies Used

### Languages
- HTML5
- CSS3
- JavaScript
- Python 3.8

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
## Deployment

- Create Render Account

- Click New

- Click "Web Service"

- Search for repo and click connect

- Name the app

- Ensure root empty

- Enviornment Python 3

- Region Frankfurt Central Europe

- Branch have to be Main

- Set build in command  pip install -r requirements.txt && npm install

- start command gunicorn core.wsgi:application

- Ensure free plan

- Scroll to advance

- Click Add enviornment variable
    ALLOWED_HOSTS
    DATABASE_URL
    DEBUG = False
    SUPABASE_KEY 
    SUPABASE_SERVICE_KEY
    SUPABASE_URL

- Click Deploy

## Credits
