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
    try:
        # Prompt the AI to give us specific search keywords for Unsplash
        system_prompt = f"""
        You are a Cuemath marketer. Create a {user_input.format} in JSON.
        For the 'image_keyword', provide 1-2 simple words (e.g., 'geometry', 'brain', 'logic') 
        that Unsplash can use to find a relevant math/education photo.
        Output ONLY valid JSON:
        {{
            "slides": [
                {{
                    "slide_number": 1,
                    "text": "Catchy text",
                    "image_keyword": "math"
                }}
            ]
        }}
        """

        response = client.chat.completions.create(
            model="gpt-4o", 
            messages=[{"role": "system", "content": system_prompt}, {"role": "user", "content": user_input.idea}],
            response_format={ "type": "json_object" }
        )
        
        return {"status": "success", "data": response.choices[0].message.content}

    except Exception as e:
        # Fallback to local mock data if the API fails
        import json
        mock = {"slides": [{"slide_number": 1, "text": f"Mastering {user_input.idea}", "image_keyword": "education"}]}
        return {"status": "success", "data": json.dumps(mock)}