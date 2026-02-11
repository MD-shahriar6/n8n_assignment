from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import httpx
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

app = FastAPI(title="n8n AI Agent Proxy")

# Define the input schema
class ChatRequest(BaseModel):
    sessionId: str
    chatInput: str

# n8n Webhook URL - loaded from environment variable
WEBHOOK_URL = os.getenv("WEBHOOK_URL", "http://localhost:5678/webhook/f85204fb-9fd0-42b8-946c-26ac99c03a08")

@app.post("/chat")
async def chat_endpoint(request: ChatRequest):
    """
    Receives sessionId and chatInput, forwards to n8n, 
    and returns the agent's response.
    """
    payload = {
        "sessionId": request.sessionId,
        "chatInput": request.chatInput
    }

    async with httpx.AsyncClient() as client:
        try:
            # Forwarding the request to n8n
            response = await client.post(WEBHOOK_URL, json=payload, timeout=60.0)
            
            # Check if n8n returned a successful status
            response.raise_for_status()
            
            # Return the JSON response directly from n8n
            # This matches your requirement: {{ $node["Respond to Webhook"].json }}
            return response.json()

        except httpx.HTTPStatusError as e:
            raise HTTPException(status_code=e.response.status_code, detail=f"n8n Error: {e.response.text}")
        except httpx.RequestError as e:
            raise HTTPException(status_code=500, detail=f"Connection to n8n failed: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8005)