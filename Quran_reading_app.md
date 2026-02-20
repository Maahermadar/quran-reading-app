# 📘 Qur’an Reading Tracker — Implementation Plan

## ⚠️ Important — Read Before Starting

The UI is **already fully designed and implemented as HTML files**.

📁 The UI source is located in folder: **`(xx)`**

You must:

* Study the HTML in `(xx)` first.
* Follow the structure exactly.
* Use the existing markup as the frontend base.
* Connect logic to it — **do not redesign or recreate UI.**

> The UI is the source of truth.
> Development is only to make it functional.

---

## 🎯 Project Goal

Build a web application that allows users to track Qur’an reading progress using a simplified Mushaf model:

* Total Pages: **600**
* 30 Juz → **20 pages each**
* When a user reaches page **600**, it counts as **one full Qur’an completion**
* Track lifetime completions.

---

## 🧭 User Flow (Already Reflected in UI)

### Entry Flow

User lands on:
➡️ `login.html`

If new → Register
If authenticated → Enter main app.

---

### Main App Layout (Bottom Tabs — Already Built)

Tabs:

1. **Home**
2. **Insights**
3. **Tips**
4. **Profile**

These pages already exist in the UI folder — backend must power them.

---

## 🏠 Home Page — Functional Requirements

### 1️⃣ Current Progress

Display:

* Current Juz
* Page (X of 600)
* Completion %

### 2️⃣ Lifetime Qur’an Completions

Every time a user finishes page **600**:

```
lifetime_completions += 1
```

This value must persist.

---

### 3️⃣ Record Today’s Reading

User inputs:

* Start Page
* End Page

This drives:

* Progress calculation
* Insights data
* Goal tracking

---

### 4️⃣ Goals System

Already shown in UI.

Backend must support:

* `target_pages`
* `target_days`
* Remaining pages
* Remaining days
* Required pages/day

Only **one active goal per user**.

---

## 📊 Insights Page — Calculated Data

Backend must compute:

* Pages read per day
* Average pages/day
* Current streak
* Longest streak
* Best reading time (group logs by hour)

UI only displays → backend must calculate.

---

## 💡 Tips Page — Forecast Logic

Backend must generate:

* Estimated completion time based on user pace.
* Suggested reading plans:

  * 30 days → 20 pages/day
  * 60 days → 10 pages/day
  * 90 days → ~7 pages/day

---

## 👤 Profile Page

Simple:

* Show user info
* Logout

(No advanced settings in V1.)

---

## 🗄️ Data Model

### users

| Field         | Type            |
| ------------- | --------------- |
| id            | int (PK)        |
| name          | string          |
| email         | string (unique) |
| password_hash | string          |
| created_at    | datetime        |

---

### reading_logs

| Field      | Type     |
| ---------- | -------- |
| id         | int (PK) |
| user_id    | FK       |
| date       | date     |
| start_page | int      |
| end_page   | int      |
| created_at | datetime |

---

### goals

| Field        | Type                           |
| ------------ | ------------------------------ |
| id           | int (PK)                       |
| user_id      | FK                             |
| start_date   | date                           |
| target_pages | int                            |
| target_days  | int                            |
| status       | active / completed / cancelled |

---

### lifetime_stats (or derived table)

| Field             | Type |
| ----------------- | ---- |
| user_id           | FK   |
| total_completions | int  |

---

## ⚙️ Core Calculations

### Juz

```
juz = ((page - 1) // 20) + 1
```

### Pages Read

```
pages = abs(end - start) + 1
```

### Completion Trigger

```
if last_page >= 600:
    lifetime_completions += 1
```

### Streak

Count consecutive log days.

### Best Time

Group `created_at.hour` → find most frequent.

---

## 🧱 Technology Stack (Already Decided)

Backend:

* FastAPI
* SQLAlchemy
* Alembic
* JWT Authentication

Frontend:

* Existing HTML from `(xx)` folder
* Vanilla JS for API calls

Deployment:

* Railway (backend)
* Cloudflare Pages (frontend)

---

## 📁 Development Rule

You are **not building UI**.

You are:
✔ Wiring APIs to existing pages
✔ Returning data matching UI blocks
✔ Implementing calculations

You are NOT:
❌ Changing layouts
❌ Adding new UX
❌ Rebuilding components

---

## ✅ Milestones

| Step | Task                                   |
| ---- | -------------------------------------- |
| M1   | Authentication working with login.html |
| M2   | Reading logs stored + returned         |
| M3   | Progress calculations connected        |
| M4   | Goals logic → Home page                |
| M5   | Insights analytics endpoints           |
| M6   | Lifetime completion counter            |
| M7   | Deploy                                 |

---

## 🔧 DATABASE SETUP (LOCAL DEVELOPMENT REQUIREMENT)

Use a **local PostgreSQL database** for development.

### Database Details:

* Database Name: **Qurantracker**
* Username: *(use your local postgres user)*
* Password: **009988**
* Host: `localhost`
* Port: `5432`

### Instructions:

1️⃣ Create the database locally:

```sql
CREATE DATABASE "Qurantracker";
```

2️⃣ Connect the application to this database using SQLAlchemy.

Example connection string:

```
postgresql+psycopg2://postgres:009988@localhost:5432/Qurantracker
```

3️⃣ Use Alembic migrations to:

* Create all tables
* Manage schema changes
* Handle future updates

4️⃣ All schema creation must be done through migrations (not manual SQL).

You are free to structure migrations as needed — just ensure the database is fully initialized automatically when running:

```
alembic upgrade head
```

---

## 📌 Final Instruction

Open the `(xx)` folder first.
Understand what each page needs.
Then implement backend + JS to power it.

This is an **integration phase**, not a design phase.




## Folder Strucure 
uran-tracker/
  backend/
    app/
      main.py
      core/
        config.py
        security.py
      db/
        database.py
        models.py
        schemas.py
      routers/
        auth.py
        logs.py
        progress.py
        insights.py
        goals.py
      services/
        calc.py
        insights.py
      utils/
        deps.py
    alembic/
    alembic.ini
    requirements.txt
    .env.example

  frontend/
    index.html              # public landing
    login.html
    register.html

    app/
      home.html             # Tab 1
      insights.html         # Tab 2
      tips.html             # Tab 3
      profile.html          # Tab 4

    assets/
      css/
        styles.css
      js/
        api.js
        auth.js
        ui.js
        home.js
        insights.js
        tips.js
        profile.js

  README.md
  PLAN.md



Open the (xx) folder first.
Understand what each page needs.
Then implement backend + JS to power it.

This is an integration phase, not a design phase.