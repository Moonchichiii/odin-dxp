# **Event Platform (DXP Odin)**

A high-performance, enterprise-grade event and marketing orchestration platform built with **Django**, designed for real-time campaigns, event workflows, CMS integrations, and external system orchestration.
The system is engineered to be scalable, API-first, and modular — suitable for enterprise use cases and future AI-augmented automation.

----------

## **Table of Contents**

1. Overview

2. Core Goals

3. Architecture

4. Tech Stack

5. Project Structure

6. Development Workflow

7. Quality & Tooling

8. Environment Setup

9. Running the Application

10. License

----------

## **Overview**

DXP Odin is an extensible, backend-driven platform for powering event management, campaign workflows, and marketing operations.
It is designed with a **modular application layout**, enabling features such as:

- Event scheduling, registration, and attendee management

- Campaign orchestration (email, SMS, automation hooks)

- CMS integration for content ingestion and synchronization

- API-driven UX for headless frontend or React-based interfaces

- Integration layer for third-party services (CRM, analytics, automation systems)

The goal is to provide a clean foundation that scales while remaining maintainable, typed, and testable.

----------

## **Core Goals**

### **1. Enterprise-grade foundations**

- Strict linting (Ruff)

- Strict typing (Mypy + Django stubs)

- Test-first mindset (Pytest & Coverage)

- Clear, predictable project structure

### **2. Modular, domain-driven applications**

Each domain lives in `apps/<domain>`, ensuring separation of concerns and long-term maintainability.

### **3. API-first by default**

The platform exposes all core functionality through a structured REST API, ready for frontend frameworks, automation tasks, or microservice consumers.

### **4. Production-ready deployment path**

- ASGI/WSGI hybrid support

- Whitenoise static handling

- Redis caching

- Gunicorn/Uvicorn for deployment

- Environment-based configuration using python-decouple

### **5. Scalable integration layer**

Designed to expand into:

- CRM sync

- Email/SMS automation

- Webhook ingestion

- Cloud media pipelines

- CMS synchronization

----------

## **Architecture**

`root
├─ config/ # Django configuration & settings ├─ apps/
│  ├─ core/ # Shared utilities, base models, mixins │  ├─ accounts/ # Authentication & user domain │  ├─ events/ # Event domain: schedules, speakers, registrations │  ├─ campaigns/ # Campaign engine, messaging, automation │  ├─ cms_integration/ # CMS connectors, synchronization logic │  ├─ integrations/ # Third-party service integrations │  └─ api/ # DRF endpoints & API routing ├─ static/
├─ templates/
└─ manage.py`

This structure follows clean boundaries, enabling long-term scale and developer clarity.

----------

## **Tech Stack**

### **Backend**

- **Python 3.12**

- **Django 5.2**

- **Django REST Framework (DRF)**

- **JWT Authentication (SimpleJWT)**

- **HTMX (lightweight interactivity)**

- **Redis (caching layer)**

- **Cloudinary (media layer)**

### **Deployment**

- **Gunicorn** (production WSGI)

- **Uvicorn** (ASGI for realtime/async use cases)

- **Whitenoise** (static serving)

- **Environment-based settings (python-decouple)**

### **Quality & Security**

- **Ruff** for linting & code style

- **Mypy** for static typing

- **Pytest** for testing

- **Coverage** for test metrics

- **Pre-commit hooks** for guaranteed quality gates

----------

## **Development Workflow**

### **1. Install project in editable mode**

`pip install -e .[dev]`

### **2. Initialize tooling**

`pre-commit install
pre-commit run --all-files`

### **3. Run the server**

`python manage.py migrate
python manage.py runserver`

----------

## **Environment Setup**

Create a `.env` file (already ignored via .gitignore):

`DEBUG=True  SECRET_KEY=your-secret-key DATABASE_URL=sqlite:///db.sqlite3 ALLOWED_HOSTS=127.0.0.1,localhost`

More environment settings will be added as integrations grow.

----------

## **Running the Application**

`python manage.py runserver`

Open:

**[http://127.0.0.1:8000/](http://127.0.0.1:8000/)**
