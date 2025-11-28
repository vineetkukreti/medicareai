# Refactoring Guide & Prompt for KisanAI/MediCareAI

This guide provides a blueprint for refactoring your application to improve scalability, maintainability, and "AI-friendliness". It is designed to be used as a prompt for an AI agent or a roadmap for human developers.

## 1. Core Philosophy

*   **Domain-Driven Design (DDD) Lite**: Organize code by **feature/domain** (e.g., `auth`, `appointments`, `patients`) rather than by technical layer (e.g., `controllers`, `models`, `views`). This keeps related logic together, making it easier for both humans and AI to understand a complete feature in one place.
*   **Colocation**: Keep things that change together, close together. Styles, tests, and logic for a component should be near each other.
*   **Explicit over Implicit**: Clear variable names, explicit type hints (Python type hints are crucial for AI), and documented interfaces.
*   **Separation of Concerns**: Backend handles data and logic; Frontend handles UI and state.

---

## 2. Proposed Folder Structure

### Backend (Python/FastAPI)

Current issues: Root is cluttered with scripts. `models.py` and `schemas.py` are likely to become monolithic.

**Proposed Structure:**

```text
backend/
├── app/
│   ├── __init__.py
│   ├── main.py              # App entry point, middleware setup
│   ├── core/                # Core functionality (config, security, db, logging)
│   │   ├── config.py
│   │   ├── database.py
│   │   ├── security.py
│   │   └── exceptions.py
│   ├── modules/             # FEATURE-BASED MODULES (The Heart of the App)
│   │   ├── auth/
│   │   │   ├── router.py    # API endpoints
│   │   │   ├── service.py   # Business logic
│   │   │   ├── models.py    # DB models for this module
│   │   │   └── schemas.py   # Pydantic models for this module
│   │   ├── appointments/
│   │   │   ├── router.py
│   │   │   ├── service.py
│   │   │   ├── models.py
│   │   │   └── schemas.py
│   │   └── patients/
│   │       └── ...
│   └── shared/              # Shared utilities/dependencies
│       ├── utils.py
│       └── dependencies.py
├── tests/                   # All tests go here
│   ├── conftest.py
│   ├── unit/
│   └── integration/
├── scripts/                 # Move all root scripts here (setup_*, update_*, etc.)
│   ├── setup_db.py
│   ├── seed_data.py
│   └── ...
├── alembic/                 # Database migrations
├── requirements.txt
└── .env
```

### Frontend (React/Vite)

Current issues: Standard but can be optimized for scaling.

**Proposed Structure:**

```text
frontend/src/
├── assets/                  # Static assets (images, fonts)
├── components/              # Shared/Generic UI components (Buttons, Inputs)
│   ├── ui/                  # Atomic UI elements
│   │   ├── Button.jsx
│   │   └── Input.jsx
│   └── layout/              # Layout components (Header, Sidebar)
├── features/                # FEATURE-BASED MODULES
│   ├── auth/
│   │   ├── components/      # Auth-specific components (LoginForm)
│   │   ├── hooks/           # Auth-specific hooks (useAuth)
│   │   ├── api.js           # Auth API calls
│   │   └── routes.jsx       # Auth routes
│   ├── appointments/
│   │   ├── components/
│   │   ├── hooks/
│   │   └── ...
│   └── dashboard/
├── lib/                     # Third-party library configurations (axios, utils)
│   ├── axios.js
│   └── utils.js
├── context/                 # Global state (Theme, AuthContext)
├── App.jsx
└── main.jsx
```

---

## 3. AI & Agent Optimization Tips

To make your codebase easy for AI agents (like me) to navigate and modify:

1.  **Type Hinting**: Use Python type hints (`def get_user(id: int) -> User:`) everywhere. It helps AI understand data structures instantly.
2.  **Docstrings**: Add a brief docstring to every function and class explaining *what* it does and *why*.
3.  **Context Files**: Create a `CONTEXT.md` or `ARCHITECTURE.md` in the root that explains the high-level system design. Agents can read this first to get oriented.
4.  **Standardized Error Handling**: Use a consistent pattern for returning errors from the API. This allows AI to write robust client code easily.
5.  **Small Files**: Avoid files larger than 300-400 lines. Break them down. AI context windows are large, but "reasoning" works better on focused chunks of code.

---

## 4. Refactoring Prompt for AI

You can use the following prompt to instruct an AI (or a human) to start the refactoring process:

> "I want to refactor our application to be more scalable and maintainable.
>
> **Goal**: Reorganize the codebase into a domain-driven structure.
>
> **Backend Instructions**:
> 1. Create a `scripts/` directory and move all root-level utility scripts (`setup_*.py`, `test_*.py`, etc.) into it.
> 2. Create a `tests/` directory and move all test files there.
> 3. Inside `backend/app`, create a `modules/` directory.
> 4. Refactor the monolithic `models.py` and `schemas.py` by splitting them into feature modules (e.g., `modules/auth/`, `modules/appointments/`).
> 5. Ensure `main.py` imports routers from these new modules.
>
> **Frontend Instructions**:
> 1. Adopt a feature-based structure in `src/features/`.
> 2. Move generic UI components to `src/components/ui`.
> 3. Group API calls by feature instead of a single `services` folder.
>
> **General**:
> - Ensure all imports are updated.
> - Verify that the application still runs after moving files.
> - Add type hints where missing."
