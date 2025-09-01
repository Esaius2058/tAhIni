# tAhIni

## Project Structure
tAhIni/
│
├── backend/               # Python FastAPI/Django app (APIs, DB models, agents)
│   ├── app/
│   │   ├── api/           # REST/GraphQL routes
│   │   ├── core/          # config, settings, constants
│   │   ├── db/            # SQLAlchemy/Prisma/ORM models, migrations
│   │   ├── agents/        # AI exam agents, grading, NLP pipelines
│   │   ├── services/      # business logic (exam creation, scoring, etc.)
│   │   ├── schemas/       # Pydantic (request/response validation)
│   │   └── utils/         # helpers (logging, security, common funcs)
│   │
│   ├── tests/             # pytest/unit + integration tests
│   ├── alembic/           # migrations (if SQLAlchemy)
│   └── main.py            # FastAPI entrypoint
│
├── frontend/              # React/Next.js (later if needed)
│   ├── src/
│   │   ├── components/    # UI pieces (buttons, modals, question cards)
│   │   ├── pages/         # route-based views
│   │   ├── hooks/         # custom hooks
│   │   └── utils/
│   └── package.json
│
├── infra/                 # deployment & infra-as-code
│   ├── docker/            # Dockerfiles for backend, frontend, db
│   ├── k8s/               # Kubernetes manifests (optional later)
│   └── compose.yml        # docker-compose for local dev
│
├── scripts/               # one-off scripts (data seeding, maintenance)
├── docs/                  # architecture diagrams, roadmap, ADRs
├── .env.example           # sample env vars
├── .gitignore
├── pyproject.toml         # python deps (if using poetry) OR requirements.txt
└── README.md
