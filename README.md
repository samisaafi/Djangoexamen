# Run an Existing Django Project with Pipenv

This guide explains how to set up and run an existing Django project using **Pipenv**.

---

## 📦 Prerequisites

- Python 3.x installed  
- Pipenv installed (`pip install pipenv`)  
- Django project files present (with `manage.py`, `Pipfile`, etc.)

---

## 🚀 Setup Steps

### 1. Install Pipenv (if not installed)

```bash
pip install pipenv
```

---

### 2. Navigate to the Project Directory

```bash
cd path/to/your/project
```

---

### 3. Install Dependencies from Pipfile

```bash
pipenv install
```

---

### 4. Activate the Pipenv Shell

```bash
pipenv shell
```

---

### 5. Apply Migrations

```bash
python manage.py migrate
```

---

### 6. Run the Development Server

```bash
python manage.py runserver
```

---

## ✅ Done

Your Django project is now running. Open `http://127.0.0.1:8000/` in your browser to see it in action.
