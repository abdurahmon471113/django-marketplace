# Django Project like OLX

## 📋 Project Overview 
**OLX Clone** is a full-featured marketplace platform built with Django.
It allows users to publish classified advertisements, browse product categories, and connect with buyers or sellers.
The application features robust user authentication, dynamic product filtering, and a secure relational database architecture.
 


## 🛠️ Tech Stack
#### Framework: Django(Python) 

#### Database: PostgreSQL

#### Frontend: Django Templates (HTML5, CSS3, Bootstrap5.3)

#### Configuration: django-environ  (.env)



---

## Setup Instructions

1. **Clone the repository:**
```bash
git clone https://github.com/abdurahmon471113/django-marketplace.git
```
2. **Install new python package installer uv instead of pip:**
```bash
pip install uv
# On Windows
```
3. **Create a virtual environment and activate it with uv command:**
```bash
py -m uv venv
# Creation of venv with uv command on Windows

.venv\Scripts\activate 
# Activation of venv with uv command on Windows
```
4. **Install dependencies:**
**Install all required python packages.**
```bash
uv add -r requirements.txt 
# This command will change requirements.txt file to pyproject.toml, this file for all required py packages on Windows
``` 
5. **Create a .env file in the root folder.**
**THEN: Copy variables from .env.example and update them as needed.**
```bash
Example .env:

DEBUG=True
SECRET_KEY=your_secret_key
DB_NAME=learning_django
DB_USER=your_db_user
DB_PASSWORD=your_db_password
DB_HOST=localhost
DB_PORT=5432
```
6. **Create the PostgreSQL database:**

7. **CREATE DATABASE  buysell_db;**
**Run migrations:**
```bash
uv run python manage.py makemigrations
uv run python manage.py migrate
```
8. **Create a superuser (for Django admin):**
```bash
uv run python manage.py createsuperuser
```
9. **Run the development server:**
```bash
uv run python manage.py runserver
```
      
 


