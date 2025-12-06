# **Event Platform (DXP Odin)**

[![Python](https://img.shields.io/badge/Python-3.12-3776AB?logo=python&logoColor=white)](https://www.python.org/)
[![Django](https://img.shields.io/badge/Django-5.2-092E20?logo=django&logoColor=white)](https://www.djangoproject.com/)
[![DRF](https://img.shields.io/badge/DRF-REST%20API-ff1709?logo=django&logoColor=white)](https://www.django-rest-framework.org/)
[![Redis](https://img.shields.io/badge/Redis-Cache-DC382D?logo=redis&logoColor=white)](https://redis.io/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Code style: Ruff](https://img.shields.io/badge/code%20style-ruff-000000.svg)](https://github.com/astral-sh/ruff)
[![Checked with mypy](https://img.shields.io/badge/mypy-checked-blue)](http://mypy-lang.org/)
[![Tests](https://img.shields.io/badge/tests-pytest-0A9EDC?logo=pytest&logoColor=white)](https://pytest.org/)

A high-performance event and marketing orchestration platform built with **Django**, designed for real-time campaigns, event workflows, CMS integrations, and external system orchestration.

----------

## **Table of Contents**

1. [Overview](#overview)
2. [Core Goals](#core-goals)
3. [Architecture](#architecture)
4. [System Architecture](#system-architecture)
5. [Tech Stack](#tech-stack)
6. [Project Structure](#project-structure)
7. [Development Workflow](#development-workflow)
8. [Quality & Tooling](#quality--tooling)
9. [Environment Setup](#environment-setup)
10. [Running the Application](#running-the-application)
11. [License](#license)

----------

## **Overview**

DXP Odin is a backend-driven platform for event management, campaign workflows, and marketing operations. Features include:

- Event scheduling, registration, and attendee management
- Campaign orchestration (email, SMS, automation hooks)
- CMS integration for content ingestion and sync
- API-driven design for headless frontend or React-based interfaces
- Integration layer for third-party services (CRM, analytics, automation)

----------

## **Core Goals**

### **1. Solid foundations**

- Strict linting (Ruff)
- Strict typing (Mypy + Django stubs)
- Test-first approach (Pytest & Coverage)
- Clear project structure

### **2. Modular, domain-driven apps**

Each domain lives in `apps/<domain>`, keeping things separated and maintainable.

### **3. API-first**

Everything is exposed through a REST API, ready for frontends, automation, or other consumers.

### **4. Production-ready**

- ASGI/WSGI support
- Whitenoise static handling
- Redis caching
- Gunicorn/Uvicorn for deployment
- Environment-based config using python-decouple

### **5. Extensible integrations**

Designed to grow into:

- CRM sync
- Email/SMS automation
- Webhook ingestion
- Cloud media pipelines
- CMS sync

----------

## **Architecture**

```
root
├─ config/              # Django configuration & settings
├─ apps/
│  ├─ core/             # Shared utilities, base models, mixins
│  ├─ accounts/         # Authentication & user domain
│  ├─ events/           # Event domain: schedules, speakers, registrations
│  ├─ campaigns/        # Campaign engine, messaging, automation
│  ├─ cms_integration/  # CMS connectors, sync logic
│  ├─ integrations/     # Third-party service integrations
│  └─ api/              # DRF endpoints & API routing
├─ static/
├─ templates/
└─ manage.py
```

----------

## **System Architecture**

```mermaid
flowchart LR
    subgraph Client
        U[User Browser]
    end

    subgraph Edge
        N[Nginx / Reverse Proxy]
    end

    subgraph DjangoApp[DXP Odin (Django)]
        D[ASGI/WSGI App<br/>Django + DRF + HTMX]
        CORE[apps.core<br/>Core domain & utilities]
        ACC[apps.accounts<br/>Users & auth]
        EVT[apps.events<br/>Events & schedules]
        CMP[apps.campaigns<br/>Campaigns & workflows]
        API[apps.api<br/>Public/Private APIs]
        CMSI[apps.cms_integration<br/>CMS connectors]
        INTS[apps.integrations<br/>3rd-party services]
    end

    subgraph DataLayer[Data & Services]
        DB[(PostgreSQL / SQL DB)]
        REDIS[(Redis<br/>cache + sessions)]
        MEDIA[Cloudinary<br/>images & video]
        EXT[External APIs<br/>(CRM, email, analytics)]
        CMS[External CMS<br/>(Wagtail / django CMS)]
    end

    U -->|HTTPS| N -->|Proxy / Static| D

    D --> CORE
    D --> ACC
    D --> EVT
    D --> CMP
    D --> API
    D --> CMSI
    D --> INTS

    CORE --> DB
    ACC --> DB
    EVT --> DB
    CMP --> DB

    D -->|Cache/Session| REDIS
    D -->|Media uploads| MEDIA

    CMSI --> CMS
    INTS --> EXT
```

----------

## **Tech Stack**

### **Backend**

- Python 3.12
- Django 5.2
- Django REST Framework (DRF)
- JWT Authentication (SimpleJWT)
- HTMX (lightweight interactivity)
- Redis (caching)
- Cloudinary (media)

### **Deployment**

- Gunicorn (production WSGI)
- Uvicorn (ASGI for async)
- Whitenoise (static serving)
- python-decouple (environment config)

### **Quality & Security**

- Ruff for linting
- Mypy for static typing
- Pytest for testing
- Coverage for test metrics
- Pre-commit hooks

----------

## **Development Workflow**

### **1. Install in editable mode**

```bash
pip install -e .[dev]
```

### **2. Set up tooling**

```bash
pre-commit install
pre-commit run --all-files
```

### **3. Run the server**

```bash
python manage.py migrate
python manage.py runserver
```

----------

## **Environment Setup**

Create a `.env` file (already in .gitignore):

```
DEBUG=True
SECRET_KEY=your-secret-key
DATABASE_URL=sqlite:///db.sqlite3
ALLOWED_HOSTS=127.0.0.1,localhost
```

More settings will be added as integrations grow.

----------

## **Running the Application**

```bash
python manage.py runserver
```

Open: **<http://127.0.0.1:8000/>**

----------

## **License**

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

```
MIT License

Copyright (c) 2024 DXP Odin

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```
