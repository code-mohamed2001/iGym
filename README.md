# iGym

A gym management backend built with **Django** and **Django REST Framework**. It helps staff manage members, memberships, check-ins, and payments from a single API.

> **Work in progress** — core features are in place; reporting, auth hardening, and a frontend are still planned.

## What it does

- **Customers** — Register members with barcode, phone, and national ID; search and browse profiles.
- **Subscriptions** — Monthly plans, session packs, and single visits; track dates, sessions used, and lifecycle status (active / expired).
- **Check-ins** — Record gym visits and validate access against the member’s subscription.
- **Invoices & payments** — Invoices linked to subscriptions; support payment type, status, discounts, and references (e.g. Instapay, Vodafone Cash, cash).

Creating a subscription also creates a matching invoice (shared invoice number) via a shared service layer in `core`.

## Tech stack

| Layer | Technology |
|-------|------------|
| Framework | Django 6, Django REST Framework |
| Database | MySQL |
| Filtering / search | django-filter, DRF search filters |
| Tooling | Pipenv, django-debug-toolbar (development) |

## Project structure

```
iGym/
├── core/          # Custom user model (roles), shared services & utilities
├── customers/     # Customers & subscriptions API
├── checkins/      # Check-in API
├── payments/      # Invoices API
└── iGym/          # Project settings & URL routing
```

## API overview

Base path examples (when running locally):

| Area | Path prefix |
|------|-------------|
| Customers & subscriptions | `/BackEnd/BrowseCustomers/` |
| Check-ins | `/BackEnd/BrowseCheckIns/` |
| Invoices | `/BackEnd/BrowsePayments/` |
| Admin | `/admin/` |

Subscriptions support filtering by kind, status, customer, date ranges, and more (see `customers/filters.py`).

## Getting started

**Requirements:** Python 3.14+, Pipenv, MySQL

1. Clone the repository and install dependencies:

   ```bash
   pipenv install
   pipenv shell
   ```

2. Configure the database in `iGym/settings.py` (or use environment variables if you add them).

3. Run migrations and start the server:

   ```bash
   python manage.py migrate
   python manage.py runserver
   ```

4. Open the browsable API (e.g. `http://127.0.0.1:8000/BackEnd/BrowseCustomers/customers/`) or use a REST client.

## User roles

Staff accounts use a custom `User` model with roles: **Owner**, **Receptionist**, and **Trainer**.

## License

Not specified yet — add a license file if you plan to open-source the project.

## Author

Personal / learning project — gym operations management for a real-world use case.
