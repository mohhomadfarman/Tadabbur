# CLAUDE.md — Tadabbur

## What This Project Is
Tadabbur (تدبّر) — open-source Islamic structured learning platform. Free forever, built by Muslims for Muslims. See README.md for the full vision.

Current phase: **Phase A — Infrastructure Scaffold** (of 7 phases in Phase 1).

Full plan: `Plan/PHASE_1_DEVELOPMENT_PLAN.md` (private — not in git).

---

## Security Rules (Enforced Every Session)

Before making ANY change, Claude must ask:

1. **Could this expose credentials, user data, or API keys?**
2. **Does this change auth, JWT logic, or access control?**
3. **Could this break a running production environment?**
4. **Am I about to commit something that should never be in git?**

If the answer to ANY of these is YES — **stop and ask the user first**.

This is not optional. These rules apply even when the user says "just do it" — because the user trusts Claude to catch what they might have missed.

---

## Files That Must Never Be Committed

```
.env
.env.*
!.env.example          ← .env.example IS allowed (no real values)
Plan/                  ← private project strategy, never public
backend/db.sqlite3     ← local Django admin DB
**/node_modules/
**/dist/
**/__pycache__/
**/mongo-data/
**/minio-data/
**/redis-data/
```

These are enforced in `.gitignore`. If Claude is ever about to stage or commit any of these, it must refuse and alert the user.

---

## Always Ask Before Doing

| Action | Why |
|--------|-----|
| Changing JWT/auth logic | Could lock out all users |
| Modifying MongoEngine models with existing data | Could corrupt stored documents |
| Changing CORS or security headers | Could open or break cross-origin access |
| Adding new pip/npm packages | User should approve dependency changes |
| Changing Docker ports or service names | Could break other devs' setups |
| Force-pushing or `git reset --hard` | Destroys history |
| Running `git add .` or `git add -A` | Could accidentally stage .env or Plan/ |
| Anything touching production `.env` | Obvious |

When in doubt — ask. The cost of a question is zero. The cost of a mistake can be irreversible.

---

## Mandatory: Every New User-Facing Feature Must Be Feature-Flagged

The project has a Feature Flag system (`backend/apps/features/`, `frontend/src/stores/features.js`).
Admins toggle features on/off and scope them to **all** users or a **selected** group
(beta / pre-testing) from **Admin → Feature Flags**. Any new user-facing feature MUST be
wired into it before it ships:

1. **Register** its key in `backend/apps/features/registry.py` (`FEATURE_REGISTRY`) with a
   `label`, `description`, `owner_section`, and `default_enabled`.
2. **Seed** it — `seed_feature_flags` reads the registry; run it on deploy (alongside `seed_roles`).
3. **Gate the BACKEND** — call `feature_enabled('<key>', request.user)` (from
   `apps/features/service.py`) in the relevant views. Never rely on the frontend alone.
4. **Gate the FRONTEND** — wrap the UI with `v-if="features.isEnabled('<key>')"`
   (from `stores/features.js`).
5. If it needs admin management, add a section to `SECTIONS`
   (`apps/common/permissions.py`) + `SECTION_LABELS` (`apps/users/admin_views.py`) and an admin view.

A feature is **not "done"** until both the backend and frontend gates are in place.
**Net-new** features start `default_enabled=false` (beta-first); only **retrofits** of
already-live features start `enabled=true` so nothing breaks.

---

## Stack (Phase 1)

| Layer | Technology |
|-------|-----------|
| Frontend | Vue.js 3 (Composition API) + Vite + Tailwind CSS + PrimeVue + Pinia |
| Backend | Django 5 + Django REST Framework |
| Auth | **Custom JWT via PyJWT** (NOT django-simplejwt — see Auth Architecture) |
| Database | MongoDB via MongoEngine ODM |
| File Storage | MinIO S3 (self-hosted) |
| Task Queue | Celery + Redis (wired in Phase A, jobs added in Phase 3) |
| Reverse Proxy | Nginx |
| Containers | Docker + Docker Compose |

---

## Auth Architecture (Important)

We do NOT use `django-simplejwt`. Reason: it requires Django's ORM, but our User documents live in MongoDB via MongoEngine.

Instead:
- `apps/users/models.py` — MongoEngine `User` document
- `apps/users/utils.py` — `generate_tokens(user)` using PyJWT
- `apps/users/auth.py` — `MongoJWTAuthentication` custom DRF auth class
- SQLite is used ONLY for Django admin panel (not for API users)

Never replace this with django-simplejwt without discussing it first.

---

## Project Structure (Target)

```
tadabbur/
├── CLAUDE.md                  ← you are here
├── README.md
├── .gitignore
├── .env.example               ← safe to commit (no real values)
├── docker-compose.yml
├── docker-compose.dev.yml
├── Plan/                      ← GITIGNORED — private
├── backend/                   ← Django project
├── frontend/                  ← Vue.js SPA
└── nginx/                     ← reverse proxy
```

---

## Phase 1 Sprint Status

- [x] Phase A — Infrastructure Scaffold (Docker + auth + DB connections)
- [x] Phase B — Curriculum Data Layer (MongoDB models + REST API)
- [x] Phase C — Frontend Curriculum Browsing (Vue SPA)
- [x] Phase D — Lesson Reader (content block renderer)
- [x] Phase E — Progress Tracking & Dashboard
- [x] Phase F — Content Authoring & Admin Panel
- [x] Phase G — Polish, RTL & Launch

---

## Commit Convention

Follow Conventional Commits:
```
feat(users): add JWT registration endpoint
fix(auth): handle expired token edge case
docs(api): update curriculum endpoint docs
style(frontend): improve RTL Arabic rendering
```

Never commit: `.env`, `Plan/`, `db.sqlite3`, `node_modules/`, `dist/`, `__pycache__/`.
Always use specific file names in `git add` — never `git add .` or `git add -A`.

<!-- code-review-graph MCP tools -->
## MCP Tools: code-review-graph

**IMPORTANT: This project has a knowledge graph. ALWAYS use the
code-review-graph MCP tools BEFORE using Grep/Glob/Read to explore
the codebase.** The graph is faster, cheaper (fewer tokens), and gives
you structural context (callers, dependents, test coverage) that file
scanning cannot.

### When to use graph tools FIRST

- **Exploring code**: `semantic_search_nodes` or `query_graph` instead of Grep
- **Understanding impact**: `get_impact_radius` instead of manually tracing imports
- **Code review**: `detect_changes` + `get_review_context` instead of reading entire files
- **Finding relationships**: `query_graph` with callers_of/callees_of/imports_of/tests_for
- **Architecture questions**: `get_architecture_overview` + `list_communities`

Fall back to Grep/Glob/Read **only** when the graph doesn't cover what you need.

### Key Tools

| Tool | Use when |
| ------ | ---------- |
| `detect_changes` | Reviewing code changes — gives risk-scored analysis |
| `get_review_context` | Need source snippets for review — token-efficient |
| `get_impact_radius` | Understanding blast radius of a change |
| `get_affected_flows` | Finding which execution paths are impacted |
| `query_graph` | Tracing callers, callees, imports, tests, dependencies |
| `semantic_search_nodes` | Finding functions/classes by name or keyword |
| `get_architecture_overview` | Understanding high-level codebase structure |
| `refactor_tool` | Planning renames, finding dead code |

### Workflow

1. The graph auto-updates on file changes (via hooks).
2. Use `detect_changes` for code review.
3. Use `get_affected_flows` to understand impact.
4. Use `query_graph` pattern="tests_for" to check coverage.
