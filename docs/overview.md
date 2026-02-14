# Family Tree WhatsApp Chatbot - Project Overview

## Introduction
The Family Tree WhatsApp Chatbot is an automated service that allows users to create, manage, and explore their family trees directly through WhatsApp. It leverages the Twilio API for messaging and a robust Python backend for logic and data management.

## Architecture

### High-Level Components
1.  **WhatsApp Interface (User)**: The user interacts with the bot via WhatsApp messages.
2.  **Twilio (Messaging Provider)**: Receives messages from WhatsApp and forwards them to our backend via Webhooks. It also sends our responses back to the user.
3.  **FastAPI Backend (Application Server)**: 
    -   Receives webhooks from Twilio.
    -   Processes user intent and state.
    -   Executes business logic (e.g., adding members, querying trees).
    -   Generates TwiML (Twilio Markup Language) responses.
4.  **PostgreSQL Database (Data Storage)**: Stores user data, family tree structures, member details, and relationships.
5.  **Alembic (Migrations)**: Manages database schema changes.

### Key Workflows
-   **Onboarding**: When a user messages for the first time, a `User` record is created.
-   **State Management**: The bot uses a Finite State Machine (FSM) approach. The user's current activity (e.g., `ADD_MEMBER_NAME`, `EDIT_SELECT_MEMBER`) is stored in the `users` table (`current_state`, `state_data`). This allows multi-step conversations.
-   **Tree Management**: Users can create a tree, add members, define relationships (Parent/Child/Spouse), and view the tree structure.
-   **Concurrency**: The system is designed to handle multiple concurrent users using Python's `asyncio` and `asyncpg` for non-blocking database operations.

## Technologies Used
-   **Language**: Python 3.12+
-   **Web Framework**: FastAPI
-   **Database ORM**: SQLAlchemy (Async)
-   **Database**: PostgreSQL
-   **Migrations**: Alembic
-   **Messaging**: Twilio API
-   **Testing**: Pytest
