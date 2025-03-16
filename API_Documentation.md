# API Documentation - Model Context Manager

This document provides detailed information about the request and response formats for the Model Context Manager API.

## Base URL

```
http://localhost:8000
```

## Authentication

Authentication is not implemented in this version. In a production environment, you would typically add authentication using OAuth2, API keys, or another secure method.

## Endpoints

### 1. Store Context

Stores context data for a specific AI model and user session.

```
POST /models/{model_id}/context
```

#### Path Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| model_id  | string | ID of the AI model (e.g., "gpt-4", "claude-3", etc.) |

#### Request Body

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| session_id | string | Yes | Unique identifier for the user session |
| context_data | object | Yes | JSON object containing context information |

#### Example Request

```json
POST /models/gpt-4/context
Content-Type: application/json

{
  "session_id": "user-123",
  "context_data": {
    "conversation_history": [
      {"role": "user", "content": "Hello, how are you?"},
      {"role": "assistant", "content": "I'm doing well, thank you! How can I help you today?"}
    ],
    "user_preferences": {
      "language": "en",
      "tone": "professional",
      "expertise_level": "beginner"
    },
    "metadata": {
      "last_topic": "AI basics",
      "session_start": "2025-03-13T10:30:00Z",
      "user_timezone": "UTC-5"
    }
  }
}
```

#### Example Response

```json
{
  "message": "Context stored successfully for model gpt-4 and session user-123",
  "context_id": "550e8400-e29b-41d4-a716-446655440000"
}
```

#### Status Codes

| Status Code | Description |
|-------------|-------------|
| 200 | Context stored successfully |
| 422 | Validation error (invalid request body) |
| 500 | Server error |

### 2. Retrieve Context

Retrieves the stored context for a specific model and user session.

```
GET /models/{model_id}/context/{session_id}
```

#### Path Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| model_id  | string | ID of the AI model |
| session_id | string | User session ID |

#### Example Request

```
GET /models/gpt-4/context/user-123
```

#### Example Response

```json
{
  "context": {
    "conversation_history": [
      {"role": "user", "content": "Hello, how are you?"},
      {"role": "assistant", "content": "I'm doing well, thank you! How can I help you today?"}
    ],
    "user_preferences": {
      "language": "en",
      "tone": "professional",
      "expertise_level": "beginner"
    },
    "metadata": {
      "last_topic": "AI basics",
      "session_start": "2025-03-13T10:30:00Z",
      "user_timezone": "UTC-5"
    }
  }
}
```

#### Status Codes

| Status Code | Description |
|-------------|-------------|
| 200 | Context retrieved successfully |
| 404 | Context not found for the specified model and session |
| 500 | Server error |

### 3. Generate Prediction

Generates a response from the model using the stored context.

```
POST /models/{model_id}/predict
```

#### Path Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| model_id  | string | ID of the AI model |

#### Request Body

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| session_id | string | Yes | User session ID |
| query | string | Yes | The user's query text |

#### Example Request

```json
POST /models/gpt-4/predict
Content-Type: application/json

{
  "session_id": "user-123",
  "query": "What are neural networks?"
}
```

#### Example Response

```json
{
  "response": "Neural networks are computational models inspired by the human brain's structure and function. They consist of interconnected nodes (neurons) organized in layers that process information. Each connection has a weight that adjusts as the network learns from data. Neural networks excel at pattern recognition, classification, and prediction tasks, making them fundamental to modern machine learning and AI applications.",
  "model_id": "gpt-4",
  "session_id": "user-123"
}
```

#### Status Codes

| Status Code | Description |
|-------------|-------------|
| 200 | Prediction generated successfully |
| 404 | Context not found for the specified session |
| 422 | Validation error (invalid request body) |
| 500 | Server error |

### 4. Delete Context

Clears the context for a specific model and user session.

```
DELETE /models/{model_id}/context/{session_id}
```

#### Path Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| model_id  | string | ID of the AI model |
| session_id | string | User session ID |

#### Example Request

```
DELETE /models/gpt-4/context/user-123
```

#### Example Response

```json
{
  "message": "Context deleted successfully for model gpt-4 and session user-123"
}
```

#### Status Codes

| Status Code | Description |
|-------------|-------------|
| 200 | Context deleted successfully |
| 404 | Context not found for the specified model and session |
| 500 | Server error |

## Error Responses

### Example Error Response (404)

```json
{
  "detail": "Context not found for session user-456"
}
```

### Example Error Response (422)

```json
{
  "detail": [
    {
      "loc": ["body", "session_id"],
      "msg": "field required",
      "type": "value_error.missing"
    }
  ]
}
```

## Auto-Expiry Feature

The API automatically removes context data that hasn't been accessed for 10 minutes. This behavior is built into the system and doesn't require any specific API calls.

## Request Validation

All requests are validated using Pydantic models:

### Context Input Schema
```python
class ContextInput(BaseModel):
    session_id: str
    context_data: Dict[str, Any]
```

### Predict Input Schema
```python
class PredictInput(BaseModel):
    session_id: str
    query: str
```

## Response Schemas

### Context Storage Response
```python
class ContextResponse(BaseModel):
    message: str
    context_id: str
```

### Predict Response
```python
class PredictResponse(BaseModel):
    response: str
    model_id: str
    session_id: str
```

### Delete Response
```python
class DeleteResponse(BaseModel):
    message: str
```

## Limitations

1. This implementation uses in-memory storage which does not persist across server restarts
2. There is no authentication or authorization mechanism
3. The response generation is simulated and does not use actual AI models
4. The system has not been optimized for high-volume traffic

## Next Steps for Production

For a production environment, consider:

1. Adding authentication and authorization
2. Implementing a persistent storage solution (Redis, MongoDB, PostgreSQL)
3. Adding robust logging and monitoring
4. Implementing rate limiting
5. Setting up proper error tracking
6. Integrating with actual AI model APIs
7. Adding compression for large context data
8. Implementing context pruning strategies for optimal performance
