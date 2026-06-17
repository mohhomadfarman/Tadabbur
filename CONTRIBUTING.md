# Contributing to Tadabbur

> *"Whoever guides someone to goodness will have a reward like the one who did it."*
> — Prophet Muhammad ﷺ (Muslim)

Thank you for wanting to contribute. Tadabbur is built by Muslims for Muslims, and every contribution — code, translation, content, or design — is a form of sadaqah jariyah (ongoing charity).

---

## Table of Contents

- [Code of Conduct](#code-of-conduct)
- [Ways to Contribute](#ways-to-contribute)
- [Getting Started (Development)](#getting-started-development)
- [Project Structure](#project-structure)
- [Workflow](#workflow)
- [Commit Convention](#commit-convention)
- [Pull Request Guidelines](#pull-request-guidelines)
- [Reporting Bugs](#reporting-bugs)
- [Suggesting Features](#suggesting-features)
- [Security Issues](#security-issues)
- [Contact](#contact)

---

## Code of Conduct

All contributors are expected to:

- Communicate with respect and Islamic adab (etiquette)
- Focus discussions on the work, not the person
- Welcome contributors of all backgrounds and experience levels
- Treat Islamic content with the reverence it deserves

Any behavior that is harassing, discriminatory, or harmful will result in removal from the project.

---

## Ways to Contribute

### 💻 Developers
- **Frontend** — Vue.js 3, Vite, Tailwind CSS, PrimeVue
- **Backend** — Django 5, Django REST Framework, MongoEngine
- **Infrastructure** — Docker, Nginx, Celery, Redis, MinIO
- **AI/ML** (Phase 3+) — RAG pipelines, LLM fine-tuning on Islamic corpus

### 🌍 Translators
Arabic, Urdu, Indonesian, Malay, Turkish, French, Bengali, Swahili, and more.
UI strings live in `frontend/src/i18n/`.

### 📖 Islamic Scholars & Educators
- Review and verify curriculum content for accuracy
- Identify missing topics, weak explanations, or scholarly disagreements
- Write or review lesson content

### 🎨 Designers
- UI/UX improvements
- RTL layout refinement
- Visual learning assets and illustrations

### 📝 Documentation
- Improve guides, add missing docs, fix broken links
- Write tutorials for setting up the dev environment on different OSes

---

## Getting Started (Development)

### Prerequisites

- [Docker Desktop](https://www.docker.com/products/docker-desktop/) (required — all services run in containers)
- Git

### Setup

```bash
# 1. Fork and clone the repo
git clone https://github.com/your-username/tadabbur.git
cd tadabbur

# 2. Copy the environment template
cp .env.example .env
# Edit .env and fill in values for your local environment

# 3. Start all services in development mode
docker compose -f docker-compose.dev.yml up --build
```

| Service     | URL                      |
|-------------|--------------------------|
| Frontend    | http://localhost:5173    |
| Backend API | http://localhost:8000    |
| MinIO UI    | http://localhost:9001    |

### Running Without Docker (Backend only)

```bash
cd backend
python -m venv venv
source venv/bin/activate      # Windows: venv\Scripts\activate
pip install -r requirements.txt
python manage.py runserver
```

> Note: MongoDB and Redis must still be running (via Docker or locally).

---

## Project Structure

```
tadabbur/
├── backend/            # Django 5 + DRF
│   ├── apps/
│   │   ├── users/      # Auth (custom JWT via PyJWT + MongoEngine)
│   │   └── ...
│   ├── config/         # Django settings, URLs, WSGI
│   └── requirements.txt
├── frontend/           # Vue.js 3 + Vite + Tailwind + PrimeVue
│   ├── src/
│   │   ├── components/
│   │   ├── views/
│   │   ├── stores/     # Pinia
│   │   └── i18n/       # Translation files
│   └── package.json
├── nginx/              # Reverse proxy config
├── docker-compose.yml
└── docker-compose.dev.yml
```

### Auth Architecture

We use a **custom JWT implementation** (PyJWT + MongoEngine), not `django-simplejwt`. This is intentional — simplejwt requires Django's ORM, but our users live in MongoDB.

- `backend/apps/users/models.py` — MongoEngine `User` document
- `backend/apps/users/utils.py` — `generate_tokens(user)`
- `backend/apps/users/auth.py` — `MongoJWTAuthentication` DRF auth class

Do not replace this with simplejwt without opening an issue first.

---

## Workflow

1. **Find or open an issue** before writing code — discuss the approach first
2. **Fork** the repo and create a branch from `main`
3. **Name your branch** clearly: `feat/lesson-progress-api`, `fix/rtl-sidebar`, `docs/setup-guide`
4. **Write your changes** — keep PRs focused on one thing
5. **Test your changes** locally before opening a PR
6. **Open a Pull Request** against `main` with a clear description

---

## Commit Convention

We follow [Conventional Commits](https://www.conventionalcommits.org/):

```
<type>(<scope>): <short description>
```

| Type | When to use |
|------|-------------|
| `feat` | New feature |
| `fix` | Bug fix |
| `docs` | Documentation only |
| `style` | Formatting, RTL, CSS (no logic change) |
| `refactor` | Code restructuring (no new feature or bug fix) |
| `test` | Adding or updating tests |
| `chore` | Build process, dependencies, tooling |

**Examples:**

```
feat(users): add JWT registration endpoint
fix(auth): handle expired token edge case
docs(api): update curriculum endpoint docs
style(frontend): improve RTL Arabic text rendering
```

---

## Pull Request Guidelines

- PRs should be **focused** — one feature or fix per PR
- Include a **description** of what changed and why
- Reference the related issue: `Closes #42`
- Ensure the app runs without errors after your change
- For frontend changes: test in both LTR and RTL layouts
- For backend changes: test the API endpoint manually or with tests

---

## Reporting Bugs

Open a GitHub Issue and include:

1. What you were trying to do
2. What actually happened (error message, screenshot)
3. Steps to reproduce
4. Your environment (OS, browser, Docker version)

---

## Suggesting Features

Open a GitHub Issue with the label `enhancement`. Describe:

1. The problem it solves
2. Your proposed solution
3. How it fits the project's mission and current phase

Major features should be discussed before implementation.

---

## Security Issues

**Do not open a public GitHub issue for security vulnerabilities.**

Email us privately at: mohhomadfarman@gmail.com

Include:
- A description of the vulnerability
- Steps to reproduce
- Potential impact
- Any suggested fix (optional)

We will respond within 72 hours and credit you in the fix if you wish.

---

## Contact

- **GitHub Discussions:** Join the conversation on the repo
- **Email:** mohhomadfarman@gmail.com

---

<div align="center">

*Jazakumullah khairan for contributing to this project.*

*May Allah accept it as a good deed from all of us.*

</div>
