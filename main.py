from fastapi import FastAPI, HTTPException, Path, Depends
from pydantic import BaseModel, Field
from typing import Dict, Any, Optional
import uuid
import time
from datetime import datetime, timedelta
import asyncio
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="Model Context Manager",
              description="API for managing model-specific context")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# In-memory storage for contexts
# Structure: {model_id: {session_id: {"context": context_data, "timestamp": last_accessed}}}
context_storage = {}

# Expiry time in seconds (10 minutes)
EXPIRY_TIME = 600

# Pydantic models for request/response validation
class ContextInput(BaseModel):
    session_id: str = Field(..., description="Unique identifier for the user session")
    context_data: Dict[str, Any] = Field(..., description="Context data to be stored")

class ContextResponse(BaseModel):
    message: str
    context_id: str

class PredictInput(BaseModel):
    session_id: str = Field(..., description="User session ID")
    query: str = Field(..., description="Query text for prediction")

class PredictResponse(BaseModel):
    response: str
    model_id: str
    session_id: str

class DeleteResponse(BaseModel):
    message: str

# Helper function to check if model exists
def get_model_contexts(model_id: str):
    if model_id not in context_storage:
        context_storage[model_id] = {}
    return context_storage[model_id]

# Background task to clean expired contexts
async def clean_expired_contexts():
    while True:
        current_time = time.time()
        for model_id in list(context_storage.keys()):
            for session_id in list(context_storage[model_id].keys()):
                if current_time - context_storage[model_id][session_id]["timestamp"] > EXPIRY_TIME:
                    del context_storage[model_id][session_id]
            # Remove empty model entries
            if not context_storage[model_id]:
                del context_storage[model_id]
        await asyncio.sleep(60)  # Check every minute

@app.on_event("startup")
async def startup_event():
    asyncio.create_task(clean_expired_contexts())

# Endpoints
@app.post("/models/{model_id}/context", response_model=ContextResponse)
async def store_context(
    model_id: str = Path(..., description="ID of the AI model"),
    context_input: ContextInput = None
):
    model_contexts = get_model_contexts(model_id)
    context_id = str(uuid.uuid4())
    
    model_contexts[context_input.session_id] = {
        "context": context_input.context_data,
        "timestamp": time.time(),
        "context_id": context_id
    }
    
    return ContextResponse(
        message=f"Context stored successfully for model {model_id} and session {context_input.session_id}",
        context_id=context_id
    )

@app.get("/models/{model_id}/context/{session_id}")
async def get_context(
    model_id: str = Path(..., description="ID of the AI model"),
    session_id: str = Path(..., description="User session ID")
):
    model_contexts = get_model_contexts(model_id)
    
    if session_id not in model_contexts:
        raise HTTPException(status_code=404, detail=f"Context not found for session {session_id}")
    
    # Update timestamp to prevent expiry
    model_contexts[session_id]["timestamp"] = time.time()
    
    return {"context": model_contexts[session_id]["context"]}

@app.post("/models/{model_id}/predict", response_model=PredictResponse)
async def predict(
    model_id: str = Path(..., description="ID of the AI model"),
    predict_input: PredictInput = None
):
    model_contexts = get_model_contexts(model_id)
    
    if predict_input.session_id not in model_contexts:
        raise HTTPException(status_code=404, detail=f"Context not found for session {predict_input.session_id}")
    
    # Update timestamp to prevent expiry
    model_contexts[predict_input.session_id]["timestamp"] = time.time()
    context_data = model_contexts[predict_input.session_id]["context"]
    
    # Simulate model prediction using the stored context
    # In a real application, this would call the actual model API
    response = f"Simulated response for query: '{predict_input.query}' using context: {context_data}"
    
    return PredictResponse(
        response=response,
        model_id=model_id,
        session_id=predict_input.session_id
    )

@app.delete("/models/{model_id}/context/{session_id}", response_model=DeleteResponse)
async def delete_context(
    model_id: str = Path(..., description="ID of the AI model"),
    session_id: str = Path(..., description="User session ID")
):
    if model_id not in context_storage or session_id not in context_storage[model_id]:
        raise HTTPException(status_code=404, detail=f"Context not found for model {model_id} and session {session_id}")
    
    del context_storage[model_id][session_id]
    
    # Remove empty model entries
    if not context_storage[model_id]:
        del context_storage[model_id]
    
    return DeleteResponse(message=f"Context deleted successfully for model {model_id} and session {session_id}")
