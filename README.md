# SDSF Result Card Portal 🎓

> **Backend Developer**: Joyobrata Das ([@holycompile](https://github.com/holycompile))  
> **Frontend Designer**: Gemini (*lol xd — being 100% honest with my learning journey!*) 

---

An academic portal built for the **School of Data Science and Forecasting (SDSF)**, **Devi Ahilya Vishwavidyalaya (DAVV)**, to manage student records and result cards.

---

## Project Overview

The **SDSF Result Card Portal** streamlines student record management and grade-sheet lookups. The backend handles data persistence, schema creation, duplicate detection, and request routing with Python and SQLite, while the UI is styled cleanly with Tailwind CSS and powered by Jinja2 template inheritance.

---

## 🛠️ Tech Stack

- **Backend**: Python 3, Flask
- **Database**: SQLite3
- **Frontend**: HTML5, Tailwind CSS, Jinja2 Template Inheritance
- **Client Scripting**: Vanilla JavaScript (ES6)

---

## ✨ Features Implemented So Far

### 1. Unified Portal Branding & Navigation
- Official DAVV and transparent SDSF department logos integrated via Flask static serving.
- Clean, minimal, mobile-friendly header and footer.
- Sub-navigation for administrative tasks (`Admin Home`, `Insert Student`).

### 2. Base Admin Layout & Template Inheritance
- Base dashboard view (`admin.html`) acting as the foundation layout.
- Child views seamlessly inject their content via Jinja's `{% extends %}` and `{% block content %}` without reloading or duplicating header/footer markup.

### 3. Student Record Registration (`/insert_student`)
- **Dynamic Program Logic**: JavaScript config dynamically updates duration and semesters based on selected course:
  - **M.Tech (Dual Degree) AI & Data Science**: 5 years / 10 Semesters.
  - **M.Tech Data Science / Big Data / Executive**: 2 years / 4 Semesters.
  - **M.Sc. Data Science & Analytics**: 2 years / 4 Semesters.
  - **MBA (Business Analytics)**: 2 years / 4 Semesters.
- **Batch Auto-Calculation**: End batch is calculated on the fly from the start batch and course duration.
- **Strict Input Validation**:
  - Enrollment Number regex validation (`[A-Z]{2}[0-9]{7}`).
  - Roll Number regex validation (`[A-Z0-9]{4}-[0-9]{4}`).
- **Two-Column Responsive Form**: Clean Tailwind card layout with input focus states and clear labels.

### 4. Database Integration & Duplicate Detection
- Automated table creation (`create_table()` initializes `studenttable`).
- Parameterized SQLite queries in `databases/query.py` to prevent SQL injection.
- Duplicate detection helper (`checking_enroll_no()`) queries `studenttable` to prevent duplicate student enrollment entries.

### 5. Status Feedback UI (`/insert_student/info_hit`)
- Responsive feedback card that displays:
  - ✅ **Success View**: Confirms successful student registration.
  - ❌ **Conflict View**: Alerts when a student with the enrollment number already exists.
- Quick navigation buttons to return home or insert another student.

---

## 📁 Project Structure

```text
SDSF_Result_Card_Portal/
│
├── app.py                     # Main Flask server, route controllers & duplicate checking
│
├── databases/
│   ├── query.py               # Table creation & parameterized insert queries
│   └── student_info.db        # SQLite database (stores studenttable)
│
├── static/                    # Public static assets served by Flask
│   ├── davvLogo.png           # DAVV University logo
│   └── departmentlogo_transparent.png  # SDSF Department transparent logo
│
├── photo/                     # Raw image assets
│
└── templates/                 # Jinja2 template views
    ├── admin.html             # Base admin layout (header, subbar, footer, block content)
    ├── home.html              # Public landing page with result check card
    ├── info_hit.html          # Submission status card (Success / Already Exists)
    └── forms/
        └── insert_student.html # Student registration form with dynamic JS logic
```

---

## 🏃 Running the Project Locally

1. **Clone the repository**:
   ```bash
   git clone https://github.com/holycompile/SDSF_Result_Card_Portal.git
   cd SDSF_Result_Card_Portal
   ```

2. **Install requirements**:
   ```bash
   pip install flask
   ```

3. **Start the Flask development server**:
   ```bash
   python app.py
   ```

4. **Open in browser**:
   - Public Home: [http://127.0.0.1:5000/](http://127.0.0.1:5000/)
   - Admin Panel: [http://127.0.0.1:5000/admin](http://127.0.0.1:5000/admin)
   - Insert Student: [http://127.0.0.1:5000/insert_student](http://127.0.0.1:5000/insert_student)

---

## 📌 Upcoming Milestones
- [ ] Student marks & subject-wise grade entry form.
- [ ] Dynamic result card generation and PDF download.
- [ ] Public result lookup query integration by Roll Number and Semester.
