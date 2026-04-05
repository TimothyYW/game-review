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

[Live site](https://game-review-cqgo.onrender.com)

## UX Design

### Wireframe

This section show the draft and planning for the website.

Wireframe landing page

![Wireframe Landing Page](./assets/images/wireframe-landing-page.png)

Wireframe login page

![Wireframe Login Page](./assets/images/wireframe-login-page.png)

Wireframe edit profile

![Wireframe Edit Profile](./assets/images/wireframe-edit-profile.png)

## Features

### Existing Features

Navbar as can be seen on the left is the logo, in the middle user can search what they looking for, and on the right is the login to redirect user to login/register page.

![navbar screenshot](./assets/images/navbar.png)

Landing page is where the post page where user immidietly see the latest post, at very top there is a search bar for user to input what they like and post including pictures.

![Landing page screenshot](./assets/images/landing-page.png)

This is posting system, allowing user to input title, picture, choose category, and (optional) text

![post system screenshot](./assets/images/post.png)

This is the login page for user to login, and allowing new user to register

![Login/Register page screenshot](./assets/images/login-register-page.png)

This is the profile page, user can see the username and their posts. If user wish to edit their profile just simply click edit profile.

![profile page screenshot](./assets/images/profile-page.png)

This edit profile mode, user can input new username, view email, add information about them self if they want to, and delete their account.

![profile edit page screenshot](./assets/images/edit-profile.png)

### Future Feature

1. Deleting Post
2. Change password

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

### Test Results

| Test Case | Description                  | Expected Result                | Actual Result                  | Status |
|----------|------------------------------|--------------------------------|--------------------------------|--------|
| TC01     | Load homepage                | Page loads successfully        | Page loads correctly           | Pass |
| TC02     | Submit review                | Review is saved                | Review saved in database       | Pass |
| TC03     | Invalid input (empty form)   | Show error message             | Error message displayed        | Pass |
| TC04     | Open deployed link           | Website loads                  | Failed in mock-up environment  | Limited |
| TC05     | Upload picture               | Profile updated                | Profile updated                | Pass |
| TC06     | Login (Invalid user)         | User cannot login              | User cannot login              | Pass |
| TC07     | Login (Valid user)           | User login                     | User login                     | Pass |
| TC08     | Register new user            | User recieved an email confirmation then login | User recieved an email confirmation then login | Pass |
| TC09     | Update username              | New username appeared          | New username appeared          | Pass |
| TC09     | User deleting account        | Account deleted                | Account deleted                | Pass |
| TC010    | Upload profile picture       | Profile picture updated        | Profile picture updated        | Pass |

- All core features are working as expected.
- The deployed application runs successfully on Render.
- Note: The deployed link may not load in certain environments due to external access restrictions or because the render stop running the link.

### Unfixed bugs

- There is a bug where render decided to shut down the link that is deployed.
  note: if that occur please let me know ASAP.

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

- Website for Mock-up test:
  https://techsini.com/multi-mockup/index.php
- Mock-up test solver:
  https://techsini.com/unable-to-generate-mockup-of-your-website-here-is-the-quick-fix/
- Phto use in post is open source.
- The idea pprojcet come and inspired from Code Institute.
