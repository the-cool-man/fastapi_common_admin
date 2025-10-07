# 🧩 Back Office API (FastAPI + PostgreSQL + Alembic)

This project provides a backend API for the back-office management system.  
It’s built with **FastAPI**, **SQLAlchemy**, and **Alembic** for database migrations, using **PostgreSQL** as the main database.

---

## 🚀 Features

- FastAPI-powered REST API
- PostgreSQL database with SQLAlchemy ORM
- Alembic migrations for schema versioning
- Seed data support for initial setup
- Modular and clean folder structure

---

## 📁 Folder Structure

│
├── core/
│ └── database.py # Database engine, Base, session setup
│
├── models/
│ ├── init.py # Imports all models
│ ├── admin_role.py # Admin role model
│ └── admin_user.py # Admin user model
│
├── alembic/
│ ├── env.py # Alembic configuration for migrations
│ ├── script.py.mako
│ └── versions/ # Auto-generated migration scripts
│
├── alembic.ini # Alembic main configuration file
├── requirements.txt # Python dependencies
└── main.py # FastAPI app entry point




---

## ⚙️ Prerequisites

Ensure you have the following installed:

- **Python 3.10+**
- **PostgreSQL** (running locally or remote)
- **pip** (Python package installer)
- **Virtual environment (optional but recommended)**

---

## 🧱 Setup Instructions

### 1️⃣ Clone the repository
git clone https://github.com/<your-username>/back-office-api.git
cd back-office-api


## Create and activate a virtual environment

python3 -m venv venv
source venv/bin/activate  # On macOS / Linux
# OR
venv\Scripts\activate     # On Windows


##  Install dependencies

pip install -r requirements.txt


## Database Setup
Edit db/session.py and update:


## Database Migration Commands
alembic revision --autogenerate -m "create <table_name> table"


## Apply migrations (upgrade to latest)
alembic upgrade head

## Rollback last migration
alembic downgrade -1

## Run the FastAPI Server (Localhost)
uvicorn main:app --reload
Server will start at:
👉 http://127.0.0.1:8000



## Useful Commands
Action	                        Command
Create virtual environment	    python3 -m venv venv
Activate environment	        source venv/bin/activate
Install dependencies	        pip install -r requirements.txt
Create migration	            alembic revision --autogenerate -m "message"
Apply migrations	            alembic upgrade head
Start FastAPI	                uvicorn main:app --reload

