# tAhIni

## Project Structure

``` Plaintext
tAhIni/
│
├── backend/                    # Python FastAPI/Django app (APIs, DB models, agents)
│   ├── src/
│   │   ├── agents/            # AI exam agents, grading, NLP pipelines
│   │   ├── api/               # REST/GraphQL routes
│   │   ├── core/              # Config, settings, constants
│   │   ├── db/                # SQLAlchemy/Prisma/ORM models, migrations
│   │   ├── services/          # Business logic (exam creation, scoring, etc.)
│   │   ├── schemas/           # Pydantic (request/response validation)
│   │   └── utils/             # Helpers (logging, security, common funcs)
│   │
│   ├── migrations/            # Database migrations
│   ├── alembic.ini
│   ├── tests/                 # pytest/unit + integration tests
│   └── main.py                # FastAPI entrypoint
│
├── frontend/                  # React/Next.js (later if needed)
│   ├── src/
│   │   ├── components/        # UI pieces (buttons, modals, question cards)
│   │   ├── pages/             # Route-based views
│   │   ├── hooks/             # Custom hooks
│   │   └── utils/
│   └── package.json
│
├── infra/                     # Deployment & infra-as-code
│   ├── docker/                # Dockerfiles for backend, frontend, db
│   ├── k8s/                   # Kubernetes manifests (optional later)
│   └── compose.yml            # docker-compose for local dev
│
├── scripts/                   # One-off scripts (data seeding, maintenance)
├── docs/                      # Architecture diagrams, roadmap, ADRs
├── .env.example               # Sample env vars
├── .gitignore
├── pyproject.toml             # Python deps (if using poetry) OR requirements.txt
└── README.md
```

## 1. Overview
### AI-Driven EdTech Platform for Secure Digital Assessments
tAhIni is a robust exam management system designed to deliver secure, timed, and reliable assessments. It features a strict separation between the Authoring Environment (for Instructors/Teachers) and the Candidate Environment (for Students), backed by a stateless JWT authentication system and a resilient autosaving engine.

## 2. System Architecture
The application is built on a Service-Repository pattern, ensuring business logic is decoupled from API routes and database models.
```markdown
### Getting Started

### Prerequisites
- Python 3.11+
- Node.js 18+ (for frontend)
- Docker & Docker Compose

### Installation
1. Clone the repository
2. Copy `.env.example` to `.env`

### Backend
cd backend
source venv/bin/activate
uvicorn src.main:app --reload

### Frontend
cd frontend
npm install
npm run dev
```

```markdown
### Tech Stack

### Backend (`/backend`)
FastAPI-based REST API handling all business logic, AI agents, and data persistence.

### Frontend (`/frontend`)
React (Vite), Tailwind CSS

### Infrastructure (`/infra`)
Containerization and deployment configurations.

### Auth
Stateless JWT (JSON Web Tokens) with custom payload scopes

### Database 
PostgreSQL with SQLAlchemy ORM

### Serialization
Pydantic V2 (Strict Mode)
```

## 3. **Core**
The system is divided into distinct functional domains:
### 1. Candidate Session Engine (src/services/candidate_exam.py)

    Handles the lifecycle of an exam attempt: Enter -> Start -> Interact -> Submit.

    Enforces strict UTC Timezone validation for started_at and ends_at.

    Manages Status Transitions (IN_PROGRESS -> SUBMITTED | TIMED_OUT).

### 2. Authentication Guard (src/auth/dependencies.py)

    Verifies JWTs with specific scopes (candidate_session).

    Injects active sessions into routes, preventing access to expired or submitted exams.

### 3 .Frontend Renderers (src/pages/student/)

    Dynamic question rendering (MCQ, MultiResponse, Code).

    Debounced Autosave mechanism to minimize network load while preventing data loss.


## 4. **Features & Flows**

### 1. Secure Exam Entry

    Code-Based Access: Candidates enter a unique exam_code.

    Session Initialization: The system generates a session_id and issues a strictly scoped JWT.

    Token Security: Tokens contain exp (Expiration) claims derived from the exam duration, ensuring the token dies exactly when the exam ends.

### 2. The Exam Interface

    Real-time Autosave: Answers are pushed to the backend (/autosave) using a debounced queue.

    Multi-Type Questions: Support for Single Choice (Radio) and Multiple Response (Checkbox) with strictly typed schemas.

    Resiliency: The frontend checks for an existing session on load (bootstrap), restoring the student's progress if they accidentally refresh.
