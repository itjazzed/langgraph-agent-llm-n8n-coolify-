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
        "features": ["LangGraph", "Composio", "LiteLLM"]
    }


@app.get("/health")
def health():
    return {"status": "healthy"}


@app.get("/tools")
def available_tools():
    """List available Composio tools"""
    try:
        from composio_langgraph import Action
        
        tools = [
            "GMAIL_SEND_EMAIL",
            "SLACK_SEND_MESSAGE",
            "GITHUB_CREATE_ISSUE",
            "NOTION_CREATE_PAGE",
            "TAVILY_SEARCH"
        ]
        
        return {
            "available_tools": tools,
            "total": len(tools),
            "status": "Composio initialized"
        }
    except Exception as e:
        return {"error": str(e), "status": "Composio not available"}


@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """Chat endpoint with optional Composio tools"""
    
    user_message = request.messages[-1].content if request.messages else "No message"
    
    tools_used = []
    if request.use_tools:
        tools_used = ["composio_demo"]
    
    return ChatResponse(
        response=f"Processed with Composio support: {user_message}",
        thought_process=[
            "Received message",
            "Checked for tool usage",
            "Processing with LangGraph",
            "Sending response"
        ],
        tokens_used=150,
        tools_used=tools_used
    )
