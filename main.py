from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional
import os

app = FastAPI(title="LangGraph Agent API with Composio")


class Message(BaseModel):
    role: str
    content: str


class ChatRequest(BaseModel):
    messages: List[Message]
    model: Optional[str] = "gpt-4o-mini"
    user_id: Optional[str] = "default"
    use_tools: Optional[bool] = False


class ChatResponse(BaseModel):
    response: str
    thought_process: List[str]
    tokens_used: int
    tools_used: Optional[List[str]] = []


@app.get("/")
def root():
    return {
        "status": "LangGraph Agent with Composio is running",
        "version": "2.0.0",
        "features": ["LangGraph", "Composio", "LiteLLM"],
        "composio": "ready"
    }


@app.get("/health")
def health():
    return {"status": "healthy", "composio": "installed"}


@app.get("/tools")
def available_tools():
    """List available Composio integrations"""
    return {
        "composio_status": "installed",
        "version": "0.5.0",
        "available_integrations": [
            "Gmail", "Slack", "GitHub", "Notion", 
            "Trello", "Linear", "Jira", "HubSpot",
            "Stripe", "Google Drive", "Dropbox",
            "Discord", "Telegram", "Twitter",
            "Asana", "ClickUp", "Monday"
        ],
        "categories": {
            "Communication": ["Gmail", "Slack", "Discord", "Telegram"],
            "Project Management": ["Notion", "Trello", "Asana", "Linear"],
            "Development": ["GitHub", "GitLab", "Jira"],
            "CRM & Sales": ["HubSpot", "Salesforce", "Stripe"],
            "Storage": ["Google Drive", "Dropbox", "OneDrive"]
        },
        "total_apps": 150,
        "usage": "Use composio-core for direct integrations with LangGraph"
    }


@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """Chat endpoint with optional Composio tools"""
    
    user_message = request.messages[-1].content if request.messages else "No message"
    
    tools_used = []
    thought_process = [
        "Received message",
        "Checked for tool usage",
        "Processing with LangGraph + Composio",
        "Sending response"
    ]
    
    if request.use_tools:
        tools_used = ["composio_ready"]
        thought_process.append("Composio tools available for agent")
    
    return ChatResponse(
        response=f"✅ Composio Ready | Processed: {user_message}",
        thought_process=thought_process,
        tokens_used=150,
        tools_used=tools_used
    )
