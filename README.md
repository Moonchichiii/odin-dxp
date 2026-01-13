# Event Platform (DXP Odin)

[![Python](https://img.shields.io/badge/Python-3.12-3776AB?logo=python&logoColor=white)](https://www.python.org/)
[![Django](https://img.shields.io/badge/Django-5.2-092E20?logo=django&logoColor=white)](https://www.djangoproject.com/)
[![Wagtail](https://img.shields.io/badge/Wagtail-CMS-00403f?logo=wagtail&logoColor=white)](https://wagtail.org/)
[![Tailwind CSS](https://img.shields.io/badge/Tailwind-v4.0-38B2AC?logo=tailwind-css&logoColor=white)](https://tailwindcss.com/)
[![Bun](https://img.shields.io/badge/Bun-Fast-fbf0df?logo=bun&logoColor=black)](https://bun.sh/)

A high-performance event and marketing orchestration platform built with Django & Wagtail.

---

## Table of Contents

1. [Overview](#overview)
2. [Architecture](#architecture)
3. [Tech Stack](#tech-stack)
4. [Development Workflow](#development-workflow)
5. [Environment Setup](#environment-setup)
6. [License](#license)

---

## Overview

DXP Odin is a CMS-driven platform for event management.

**Key Features:**

- Tailwind v4 (CSS-First): Design tokens in `assets/css/input.css`.
- Wagtail CMS: Control over Hero sections, Speakers, Sponsors, and content blocks.
- HTMX & Alpine.js: Lightweight interactivity.
- Cloudinary: Optimized media delivery.

---

## Architecture

```bash
root
├─ config/              # Django settings & URL routing
├─ apps/
│  ├─ core/             # Shared utilities & base models
│  ├─ accounts/         # Authentication & User domain
│  ├─ admin_branding/   # Custom Wagtail Admin styling
│  ├─ cms_integration/  # Blocks, Pages, Snippets, Settings
│  ├─ campaigns/        # Marketing automation logic
│  └─ events/           # Core Event logic
├─ assets/
│  └─ css/              # Tailwind source (input.css)
├─ static/              # Compiled assets
├─ templates/           # Django/Wagtail HTML templates
└─ manage.py
```

---

## Tech Stack

### Backend

- Python 3.12
- Django 5.2
- Wagtail 6.x
- Redis
- Cloudinary

### Frontend

- Tailwind CSS v4
- Alpine.js
- HTMX
- Bun

---

## Development Workflow

### 1. Install Dependencies

**Python:**

```bash
pip install -e .[dev]
```

**Frontend (Bun):**

```bash
bun install
```

### 2. Run the Application

**Terminal 1 (Django Server):**

```bash
python manage.py runserver
```

**Terminal 2 (Tailwind/JS Watcher):**

```bash
bun run dev
```

### 3. Building for Production

```bash
bun run build
```

---

## Environment Setup

Create a `.env` file in the root:

```bash
DEBUG=True
SECRET_KEY=your-secret-key-here
DATABASE_URL=sqlite:///db.sqlite3
ALLOWED_HOSTS=127.0.0.1,localhost
```

---

## License

This project is licensed under the MIT License.
