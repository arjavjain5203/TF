# API Documentation

The backend exposes a REST API built with FastAPI.

## endpoints

### `POST /webhook`
This is the primary endpoint used by Twilio to communicate with the bot.

-   **Description**: Receives incoming WhatsApp messages.
-   **Request Body**: `Form Data` (standard Twilio format).
    -   `From`: The sender's WhatsApp number (e.g., `whatsapp:+1234567890`).
    -   `Body`: The text content of the message.
    -   `AccountSid`: Twilio Account ID (used for validation).
-   **Response**: `application/xml` (TwiML).
    -   Contains the bot's response message to be sent back to the user.

### `GET /` (Health Check)
-   **Description**: Simple root endpoint to verify the server is running.
-   **Response**: `{"message": "Family Tree Bot is running!"}`

## Authentication
-   **Webhook Validation**: The `webhook` endpoint validates the request signature using the `TwilioRequestValidator` to ensure requests originate from Twilio.
