# Timely Backend

A Python-based backend application for the Timely platform(an attendenace application that utilises Geolocation and facial recognision), built with Django and designed for scalable, efficient API services.

## Overview

Timely Backend is the server-side component of the Timely platform. It provides robust APIs and backend services for managing lessons, user data, and application configuration.

## Project Structure
timely-backend/
├── config/ # Configuration files and settings
├── lesson/ # Lesson-related models, views, and APIs
├── my_models/ # Custom models and database schemas
├── manage.py # Django management script
├── app.yaml # App deployment configuration
├── requirements.txt # Python dependencies
├── req.txt # Additional requirements
└── README.md # This file

## Technology Stack

- **Language:** Python
- **Framework:** Django
- **Database:** Django ORM with supported databases

## Getting Started

### Prerequisites

- Python 3.9+
- pip (Python package manager)
- Virtual environment (recommended)

### Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/WaleX-projects/timely-backend.git
   cd timely-backend
   ```
2. **Create and activate a virtual environment:**
   ```bash
   python -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate
   
3. **Install dependencies:**
   ```bash
    pip install -r requirements.txt

### Running the Application

1. **Apply database migrations:**
   ```bash
      python manage.py makemigrations
      python manage.py migrate
2. **Create a superuser (optional)**
    ```bash
       python manage.py createsuperuser
3. **Start the development server:**
   ```bash
      python manage.py runserver

**The application will be available at http://127.0.0.1:8000/**
