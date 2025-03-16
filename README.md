# Model Context Manager (MCM)

A FastAPI implementation for managing model-specific context in AI applications.

## Overview

The Model Context Manager (MCM) is a REST API service that allows storing and retrieving context data for AI models. It enables maintaining conversation history and other contextual information across multiple user sessions.

## Features

- Store model-specific context for different user sessions
- Retrieve stored context for a given model and session
- Generate responses using the stored context
- Clear context for specific user sessions
- Automatic expiry of unused contexts after 10 minutes

## Requirements

- Python 3.7+
- FastAPI
- Uvicorn (for serving the API)

## Installation

1. Clone this repository:
   ```
   git clone https://github.com/yourusername/model-context-manager.git
   cd model-context-manager
   ```

2. Create a virtual environment and install dependencies:
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install fastapi uvicorn
   ```

## Running the API

Start the server with:

```
uvicorn main:app --reload
```

The API will be available at `http://localhost:8000`.

## API Documentation

Once the server is running, you can access the auto-generated API documentation at:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## API Endpoints

### 1. Store Context

```
POST /models/{model_id}/context
```

Stores context for a specific AI model.

**Request Body:**
```json
{
  "session_id": "user-123",
  "context_data": {
    "conversation_history": ["Hello", "Hi there!"],
    "preferences": {"language": "en", "tone": "formal"}
  }
}
```

**Response:**
```json
{
  "message": "Context stored successfully for model gpt-4 and session user-123",
  "context_id": "550e8400-e29b-41d4-a716-446655440000"
}
```

### 2. Retrieve Context

```
GET /models/{model_id}/context/{session_id}
```

Retrieves the stored context for a given model and session.

**Response:**
```json
{
  "context": {
    "conversation_history": ["Hello", "Hi there!"],
    "preferences": {"language": "en", "tone": "formal"}
  }
}
```

### 3. Generate Response

```
POST /models/{model_id}/predict
```

Generates a response from a model using the stored context.

**Request Body:**
```json
{
  "session_id": "user-123",
  "query": "Tell me about machine learning"
}
```

**Response:**
```json
{
  "response": "Simulated response for query: 'Tell me about machine learning' using context: {...}",
  "model_id": "gpt-4",
  "session_id": "user-123"
}
```

### 4. Clear Context

```
DELETE /models/{model_id}/context/{session_id}
```

Clears the context for a specific user session.

**Response:**
```json
{
  "message": "Context deleted successfully for model gpt-4 and session user-123"
}
```

## Error Handling

The API returns appropriate HTTP status codes and error messages:

- 404: Context or model not found
- 422: Invalid input data
- 500: Server error

## Auto-Expiry Feature

Context data is automatically cleared if not accessed for 10 minutes to prevent memory leaks and maintain performance.
