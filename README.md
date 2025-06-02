# Django Project Setup with Pipenv

This guide outlines the steps to set up a Django project using **Pipenv** for dependency management.

---

## 📦 Prerequisites

- Python 3.x installed
- Pipenv installed (`pip install pipenv`)

---

## 🚀 Getting Started

### 1. Install Pipenv

If Pipenv is not already installed:

```bash
pip install pipenv
```

---

### 2. Create and Navigate to Project Directory

```bash
mkdir my_django_project
cd my_django_project
```

---

### 3. Initialize a Pipenv Environment

Replace `3.x` with your Python version:

```bash
pipenv --python 3.x
```

---

### 4. Install Django

```bash
pipenv install django
```

---

### 5. Create a New Django Project

```bash
pipenv run django-admin startproject myproject
```

> This will create a Django project inside the current directory.

---

### 6. Activate the Pipenv Shell

```bash
pipenv shell
```

---

### 7. Install Additional Dependencies (if needed)

If you have a `Pipfile` or `requirements.txt`:

```bash
pipenv install
```

To install a specific package:

```bash
pipenv install package_name
```

---

### 8. Run Migrations

```bash
python manage.py migrate
```

---

### 9. Start the Development Server

```bash
python manage.py runserver
```

---

## ✅ Summary

You now have a fully functional Django project set up with Pipenv! Use `pipenv shell` to activate your environment and continue development.
