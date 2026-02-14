# Service Architecture

The application logic is modularized into services, located in `app/services/`.

## 1. ChatbotService (`chatbot_service.py`)
This is the core orchestration service. It handles the conversation flow with the user.
-   **Role**: Manages the Finite State Machine (FSM) for user interactions.
-   **Key Methods**:
    -   `handle_message(from_number, body)`: Entry point. Identify user, determine state, and Route to specific handlers.
    -   `handle_main_menu`: Processes main menu selections (1-7).
    -   `finalize_add_member`: Completes the multi-step "Add Member" flow.
    -   `show_main_menu`: Helper to display the main menu options.

## 2. UserService (`user_service.py`)
Handles all User-related database operations.
-   **Role**: Create, retrieve, and update users.
-   **Key Methods**:
    -   `get_or_create_user(phone)`: Finds a user by phone or creates a new one.
    -   `update_state(user_id, state, data)`: Updates the user's current conversational state (e.g., from `MAIN_MENU` to `ADD_MEMBER_NAME`).
    -   `clear_state(user_id)`: Resets the user to the default state.

## 3. TreeService (`tree_service.py`)
Manages the `Tree` entity and permissions.
-   **Role**: Create trees, manage ownership, and handle access control (Share/Transfer).
-   **Key Methods**:
    -   `create_tree(user)`: Creates a new tree for a user.
    -   `get_tree_by_owner(user_id)`: Retrieves a tree owned by the user.
    -   `grant_access(tree_id, user_id, role)`: allow another user to VIEW or EDIT the tree.
    -   `is_member_locked(member_id)`: concurrency check to see if a member is currently being edited by someone else.

## 4. MemberService (`member_service.py`)
Handles `Member` entities and their relationships.
-   **Role**: Add, update, and link members within a tree.
-   **Key Methods**:
    -   `create_member(tree_id, name, ...)`: Adds a new person to the tree.
    -   `add_relationship(tree_id, parent_id, child_id)`: Creates a parent-child link between two members.
    -   `get_members_by_tree(tree_id)`: Fetches all members in a specific tree.
    -   `update_member`: Modifies member details (Name, DOB, etc.).
