from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import httpx
from dotenv import load_dotenv
import os
import uuid

# Load environment variables
load_dotenv()

app = FastAPI(title="n8n AI Agent Proxy")

# Input schema
class ChatRequest(BaseModel):
    email: str
    article_url: str

# n8n Webhook URL
WEBHOOK_URL = os.getenv(
    "WEBHOOK_URL",
    "http://localhost:5678/webhook/f85204fb-9fd0-42b8-946c-26ac99c03a08"
)

@app.post("/process-article")
async def process_article(request: ChatRequest):

    # Generate session ID
    session_id = str(uuid.uuid4())

    payload = {
        "session_id": session_id,
        "email": request.email,
        "article_url": request.article_url
    }

    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(
                WEBHOOK_URL,
                json=payload,
                timeout=60.0
            )

            response.raise_for_status()

            return {
                "message": "Request sent to n8n successfully",
                "session_id": session_id,
                "n8n_response": response.json()
            }

        except httpx.HTTPStatusError as e:
            raise HTTPException(
                status_code=e.response.status_code,
                detail=f"n8n Error: {e.response.text}"
            )

        except httpx.RequestError as e:
            raise HTTPException(
                status_code=500,
                detail=f"Connection to n8n failed: {str(e)}"
            )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8005)