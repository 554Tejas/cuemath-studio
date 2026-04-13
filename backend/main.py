from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from openai import OpenAI
import os
from dotenv import load_dotenv

api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    # This prevents a 500 error by giving a clear message
    print("CRITICAL ERROR: OPENAI_API_KEY is not set in environment variables.")

client = OpenAI(api_key=api_key)

load_dotenv()

# Initialize FastAPI
app = FastAPI()

# Allow frontend to communicate with backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # In production, replace with your Vercel URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Set your API key in a .env file (OPENAI_API_KEY=your_key_here)
client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Define the expected input from the frontend
class IdeaInput(BaseModel):
    idea: str
    format: str # e.g., "carousel", "story"

@app.post("/generate-creative")
async def generate_creative(user_input: IdeaInput):
    try:
        # 2. Use 'client.chat.completions', NOT 'openai.ChatCompletion'
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "You are a Cuemath social media expert."},
                {"role": "user", "content": user_input.idea}
            ],
            response_format={ "type": "json_object" }
        )
        return {"status": "success", "data": response.choices[0].message.content}
    except Exception as e:
        print(f"Error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# Run locally using: uvicorn main:app --reload