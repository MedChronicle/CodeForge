# AlgoForge

**AlgoForge** is a personalized Data Structures and Algorithms (DSA) learning platform designed to help learners build problem-solving skills through structured practice, adaptive study plans, revision scheduling, and progress analytics.

Instead of treating coding practice as a simple list of questions, AlgoForge brings topic-based learning, curated problem metadata, personalized recommendations, spaced repetition, learning resources, and performance insights into one workspace.

## Table of Contents

1. [Project Overview](#project-overview)
2. [Objectives](#objectives)
3. [Key Features](#key-features)
4. [Technology Stack](#technology-stack)
5. [System Architecture](#system-architecture)
6. [Project Structure](#project-structure)
7. [Prerequisites](#prerequisites)
8. [Installation and Setup](#installation-and-setup)
9. [Running the Application](#running-the-application)
10. [API Documentation](#api-documentation)
11. [Database and Seed Data](#database-and-seed-data)
12. [Machine Learning](#machine-learning)
13. [Testing and Verification](#testing-and-verification)
14. [Environment Variables](#environment-variables)
15. [Security Notes](#security-notes)
16. [Limitations and Future Improvements](#limitations-and-future-improvements)

## Project Overview

AlgoForge provides a single environment in which learners can explore DSA topics, work through curated problems, maintain learning notes, follow revision schedules, and review progress. The frontend communicates with a FastAPI backend, which manages authentication, learning data, progress tracking, analytics, and machine-learning-assisted recommendations.

## Objectives

- Organize DSA learning into clear topics and problem categories.
- Help learners plan and maintain consistent practice.
- Support revision through spaced-repetition scheduling.
- Track learning progress and provide understandable performance insights.
- Use a machine-learning model as an additional signal for estimating skill and supporting recommendations.
- Provide a responsive, interactive interface for daily learning.

## Key Features

- **Authentication:** registration, login, token-based authentication, and protected routes.
- **Learning dashboard:** a central view of learning activity and progress.
- **Topic and problem exploration:** curated topic catalog and problem metadata with filters.
- **Adaptive study sheets:** generate or manage practice sheets using learner-related signals.
- **Revision planner:** schedule and review previously studied material.
- **Progress analytics:** visual summaries of progress, mastery estimates, difficulty, and streak activity.
- **Learning resources:** links and notes associated with topics.
- **Code workspace:** browser-based coding scratchpad with language selection and Monaco Editor integration.
- **Administration:** administrative endpoints and a dashboard for platform management.
- **Rate limiting and configuration:** backend controls for request handling and environment-based settings.

Feature availability depends on the implemented API routes and the current database/model state.

## Technology Stack

| Layer | Technologies | Purpose |
|---|---|---|
| Frontend | React 18, TypeScript, Vite | User interface and development/build tooling |
| Styling and interaction | Tailwind CSS, Framer Motion, GSAP | Styling and interface animations |
| Visualization | Recharts, React Three Fiber, Drei, Three.js | Charts and 3D visual elements |
| State and HTTP | Zustand, Axios | Client state and API communication |
| Code and notes | Monaco Editor, React Markdown | Code workspace and rendered notes |
| Backend API | FastAPI, Uvicorn, Pydantic | HTTP API and request/response validation |
| Persistence | SQLAlchemy, SQLite by default | Database models and data access |
| Authentication | JWT, bcrypt | Token-based authentication and password hashing |
| Machine learning | scikit-learn, NumPy, pandas, joblib | Skill estimation and recommendation support |
| Testing | pytest, HTTPX, Vitest, Testing Library | Backend and frontend tests |
| Optional deployment | Docker, Docker Compose | Container-based development/deployment |

## System Architecture

```text
Learner / Administrator
          |
          v
React + TypeScript frontend (Vite)
          |
          | HTTP requests / JSON
          v
FastAPI backend
  |-- Authentication and user services
  |-- Topics, problems, resources and sheets
  |-- Progress, analytics and revision
  |-- Administration and health endpoints
  |-- ML recommendation / skill-estimation routes
          |
          v
SQLAlchemy data layer ---> SQLite by default
          |
          v
scikit-learn model artifact for ML-assisted estimates
```

The frontend and backend run as separate development services. The frontend uses the configured API origin to communicate with the backend.

## Project Structure

```text
algoforge/
├── README.md
├── .env.example
├── .gitignore
├── docker-compose.yml
├── backend/
│   ├── app/
│   │   ├── main.py                 # FastAPI application entry point
│   │   ├── api/
│   │   │   ├── router.py           # API router registration
│   │   │   ├── deps.py             # Shared API dependencies
│   │   │   └── routes/             # Auth, users, topics, problems, sheets,
│   │   │                           # resources, progress, revision, admin, ML
│   │   ├── core/                   # Settings, database, security, logging,
│   │   │                           # rate limiting and exceptions
│   │   ├── models/                 # SQLAlchemy database models
│   │   ├── schemas/                # Pydantic request/response schemas
│   │   └── services/               # Application and business logic
│   ├── ml/
│   │   ├── artifacts/              # Saved estimator and metadata
│   │   ├── features.py             # ML feature preparation
│   │   ├── skill_estimator.py      # Skill-estimation logic
│   │   ├── recommender.py          # Recommendation logic
│   │   ├── sheet_generator.py      # Adaptive sheet generation
│   │   ├── synthetic_data.py       # Synthetic training data
│   │   ├── train.py                # Model training
│   │   ├── evaluate.py             # Model evaluation
│   │   └── model_card.md           # Model purpose and limitations
│   ├── seed/
│   │   ├── problem_catalog.py      # Curated problem metadata
│   │   ├── topic_catalog.py        # DSA topic catalog
│   │   ├── resource_catalog.py    # Learning resources and notes
│   │   └── seed_data.py            # Database initialization/seeding
│   ├── tests/                      # Backend tests
│   ├── requirements.txt
│   ├── pyproject.toml
│   └── Dockerfile
├── frontend/
│   ├── public/                     # Public static assets
│   ├── src/
│   │   ├── main.tsx                # Frontend entry point
│   │   ├── App.tsx                 # Application routes/layout composition
│   │   ├── api/                    # API client modules
│   │   ├── components/
│   │   │   ├── analytics/          # Progress and mastery charts
│   │   │   ├── auth/               # Authentication layouts and guards
│   │   │   ├── common/             # Loading, empty and error states
│   │   │   ├── editor/              # Code editor and language selector
│   │   │   ├── layout/              # Sidebar, topbar and application shell
│   │   │   ├── problems/            # Problem cards, filters and topic sections
│   │   │   ├── resources/           # Markdown notes
│   │   │   ├── three/               # 3D hero and skill visualization
│   │   │   └── ui/                  # Reusable interface components
│   │   ├── pages/                  # Landing, auth, dashboard, sheets,
│   │   │                           # revision, resources, admin and workspace
│   │   ├── styles/                 # Global styles, tokens and animations
│   │   ├── types/                  # TypeScript API and app types
│   │   ├── lib/                    # Shared utilities and constants
│   │   ├── test/                   # Test setup and utilities
│   │   └── __tests__/               # Frontend component/store tests
│   ├── package.json
│   ├── package-lock.json
│   ├── vite.config.ts
│   ├── vitest.config.ts
│   └── tailwind.config.ts
├── migrations/                     # Database migration configuration/files
└── scripts/
    ├── start-dev.sh                # Start backend and frontend locally
    ├── seed.sh                     # Seed helper
    ├── train_model.sh              # Model-training helper
    └── verify.sh                   # Verification helper
```

### Main folder responsibilities

| Folder/file | Responsibility |
|---|---|
| `frontend/src/pages/` | Full pages for the user-facing application |
| `frontend/src/components/` | Reusable UI, layout, problem, editor and analytics components |
| `frontend/src/api/` | Frontend API integration modules |
| `frontend/src/types/` | TypeScript definitions for API data and app state |
| `backend/app/api/routes/` | HTTP endpoint definitions |
| `backend/app/models/` | Database table models |
| `backend/app/schemas/` | Validated API data structures |
| `backend/app/services/` | Business logic used by API routes |
| `backend/app/core/` | Configuration, database connection and security utilities |
| `backend/ml/` | Model features, training, evaluation and recommendation code |
| `backend/seed/` | Initial topics, problems, resources and database seed routine |
| `backend/tests/` | Automated backend tests |
| `scripts/` | Development, seeding, training and verification helpers |

## Prerequisites

Install the following before setup:

- Python 3.12 (recommended for this project configuration)
- Node.js and npm
- Git (optional, for version control)
- Docker and Docker Compose (optional)

Check the installed versions:

```bash
python3 --version
node --version
npm --version
```

## Installation and Setup

Run these commands from the directory that contains the `algoforge` folder.

### 1. Enter the project

```bash
cd algoforge
```

### 2. Create a Python virtual environment

```bash
python3.12 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
pip install -r backend/requirements.txt
```

If your system uses a different Python executable name, use the equivalent Python 3.12 command.

### 3. Install frontend dependencies

```bash
cd frontend
npm install
cd ..
```

### 4. Configure environment variables

```bash
cp .env.example .env
```

Open `.env` and replace the example secret and administrator password before using the application beyond local development. Do not commit `.env` to source control.

### 5. Initialize the database and seed starter data

From the project root, with the virtual environment active:

```bash
python -m backend.seed.seed_data
```

The seed process is intended to create the initial administrator and populate the topic, problem-metadata, and resource catalog. The README's default catalog description is 18 topics and 180 curated problem metadata records; verify the seed output if the catalog has been changed.

### 6. Train the ML model if needed

```bash
python -m backend.ml.train
```

A model artifact is already included in `backend/ml/artifacts/`. Retraining is optional unless you change the training data or feature logic.

## Running the Application

### Recommended: start both services

From the project root:

```bash
./scripts/start-dev.sh
```

The helper expects dependencies to be installed and `.venv` to exist. It starts the API and Vite development server in separate background processes. Press `Ctrl+C` to stop them.

### Alternative: run services in separate terminals

Terminal 1 — backend:

```bash
source .venv/bin/activate
uvicorn backend.app.main:app --reload --host 127.0.0.1 --port 8000
```

Terminal 2 — frontend:

```bash
cd frontend
npm run dev
```

Open the frontend URL printed by Vite, normally `http://localhost:5173`.

Do not open `frontend/index.html` directly from Finder. Vite must serve the application so TypeScript modules, routing, and API requests work correctly.

## API Documentation

When the backend is running:

- API base URL: `http://localhost:8000`
- Interactive Swagger documentation: `http://localhost:8000/docs`
- Alternative ReDoc documentation: `http://localhost:8000/redoc`
- Health endpoint: see the health route registered by the backend.

Exact endpoints and available operations are defined in `backend/app/api/routes/`.

## Database and Seed Data

The example configuration uses SQLite:

```env
DATABASE_URL=sqlite:///./algoforge.db
```

SQLAlchemy provides the persistence layer. The backend includes models for users, profiles, topics, problems, sheets, progress, resources, and refresh tokens. The database is initialized and populated using the seed module. A PostgreSQL-compatible URL can be configured if the database driver and deployment configuration are also set up appropriately.

## Machine Learning

The ML subsystem contains feature preparation, synthetic data generation, a skill estimator, recommendation logic, adaptive sheet generation, training and evaluation scripts. The saved model is loaded from the path configured by `ML_MODEL_PATH`.

The model is intended to provide an additional learning signal. Its predictions are not a guarantee of interview readiness, a formal assessment, or a replacement for learner judgment or instructor feedback. Because the training data is synthetic, model performance on real learners should be validated before making high-impact decisions.

## Testing and Verification

Backend checks:

```bash
source .venv/bin/activate
pytest -q backend/tests
python -m compileall backend/app backend/ml backend/seed
```

Frontend checks:

```bash
cd frontend
npm run typecheck
npm run test -- --run
npm run build
```

Run these checks after changing routes, schemas, database models, ML features, UI components, or configuration. A passing test suite does not replace end-to-end testing with a freshly seeded database.

## Environment Variables

| Variable | Purpose | Example/default |
|---|---|---|
| `APP_NAME` | Application display/name setting | `AlgoForge` |
| `ENVIRONMENT` | Runtime environment | `development` |
| `SECRET_KEY` | Secret used by security/token configuration | Replace with a long random secret |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | Access-token lifetime | `30` |
| `REFRESH_TOKEN_EXPIRE_DAYS` | Refresh-token lifetime | `14` |
| `DATABASE_URL` | SQLAlchemy database connection URL | `sqlite:///./algoforge.db` |
| `FRONTEND_ORIGIN` | Allowed frontend origin/configuration | `http://localhost:5173` |
| `RATE_LIMIT_REQUESTS` | Request limit for the configured window | `120` |
| `RATE_LIMIT_WINDOW_SECONDS` | Rate-limit window duration | `60` |
| `ML_MODEL_PATH` | Path to the saved estimator | `backend/ml/artifacts/skill_estimator.joblib` |
| `ADMIN_EMAIL` | Email used for the seeded administrator | `admin@algoforge.local` |
| `ADMIN_PASSWORD` | Password used for the seeded administrator | Change before first use |

These values are examples. Check `backend/app/core/config.py` for the application's actual settings behavior and defaults.

## Security Notes

- Replace `SECRET_KEY` and `ADMIN_PASSWORD` before deployment.
- Do not commit real credentials, tokens, or production environment files.
- Use HTTPS, secure deployment secrets, and an appropriately configured database in production.
- Review CORS, token expiry, password hashing, rate limits, and administrative authorization before public deployment.
- Do not use the seeded development administrator credentials on a public server.
