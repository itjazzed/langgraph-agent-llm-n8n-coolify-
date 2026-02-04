from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional
import os

app = FastAPI(title="LangGraph Agent API")


class Message(BaseModel):
    role: str
    content: str


class ChatRequest(BaseModel):
    messages: List[Message]
    model: Optional[str] = "gpt-4o-mini"
    user_id: Optional[str] = "default"


class ChatResponse(BaseModel):
    response: str
    thought_process: List[str]
    tokens_used: int


@app.get("/")
def root():
    return {"status": "LangGraph Agent is running", "version": "1.0.0"}


@app.get("/health")
def health():
    return {"status": "healthy"}


@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """Simple echo endpoint for testing"""
    
    user_message = request.messages[-1].content if request.messages else "No message"
    
    return ChatResponse(
        response=f"Echo: {user_message}",
        thought_process=["Received message", "Processing", "Sending response"],
        tokens_used=100
    )
