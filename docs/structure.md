# Project Structure

This document explains the organization of the codebase and the purpose of each file/directory.

## Root Directory
-   `app/`: Contains the main application source code.
-   `alembic/`: Database migration scripts and configuration.
-   `tests/`: Automated tests.
-   `scripts/`: Utility scripts for setup and maintenance.
-   `docs/`: Project documentation.
-   `.env` / `.env.example`: Environment configuration.
-   `requirements.txt`: Python dependencies.
-   `render.yaml`: Deployment configuration for Render.com.
-   `alembic.ini`: Configuration file for Alembic migrations.

## `app/` Directory
The core logic resides here.

### `app/models/`
Defines the database schema using SQLAlchemy ORM.
-   `user.py`: `User` model (WhatsApp users, state management).
-   `tree.py`: `Tree`, `TreeAccess` models (Family trees, permissions).
-   `member.py`: `Member`, `Relationship` models (Individuals in the tree, connections).
-   `__init__.py`: Exports models for Alembic.

### `app/services/`
Contains business logic, separating it from API routes.
-   `chatbot_service.py`: The brain of the bot. Handles message parsing, state transitions, and generating responses.
-   `user_service.py`: CRUD operations for Users and state updates.
-   `tree_service.py`: Logic for creating trees, adding members, locking members, and sharing access.
-   `member_service.py`: Logic for creating members and defining relationships (parent/child).

### `app/routers/`
Defines API endpoints.
-   `webhook.py`: The main entry point for Twilio webhooks. Validates requests and delegates to `ChatbotService`.

### `app/utils/`
Helper functions.
-   `validators.py`: Input validation for dates, gender, etc.
-   `logging.py`: Logging configuration.

### Other Files
-   `main.py`: FastAPI application entry point. Configures routes and middleware.
-   `database.py`: Database connection setup (Async Engine, Session).
-   `config.py`: Application settings loading (Pydantic).

## `scripts/`
-   `setup_user.py`: Script to manually create users/trees for testing or admin purposes.

## `tests/`
-   `conftest.py`: Test fixtures (Async client, in-memory DB setup).
-   `test_webhook.py`: Integration tests for the chatbot flows.
