import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from openai import OpenAI
from dotenv import load_dotenv

# Load local .env file (for local testing only)
load_dotenv()

app = FastAPI()

# Enable CORS so your Vercel frontend can talk to your Render backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize the OpenAI client correctly to avoid NameError
# Render will use the Environment Variable you set in the dashboard
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Define the data structure for the request
class IdeaInput(BaseModel):
    idea: str
    format: str

@app.post("/generate-creative")
async def generate_creative(user_input: IdeaInput):
    # This bypasses the AI and returns a successful response instantly
    import json
    mock_data = {
        "slides": [
            {
                "slide_number": 1, 
                "text": f"How to master {user_input.idea}", 
                "image_prompt": "A professional math classroom setting"
            },
            {
                "slide_number": 2, 
                "text": "Step 1: Spaced Repetition", 
                "image_prompt": "A clock and a brain icon"
            }
        ]
    }
    return {"status": "success", "data": json.dumps(mock_data)}