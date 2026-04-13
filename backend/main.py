from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from openai import OpenAI
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
        # The prompt forces the LLM to act as a marketer and output strict JSON
        system_prompt = f"""
        You are a Cuemath social media marketer. Convert the user's idea into a {user_input.format}.
        Output ONLY valid JSON in this exact structure:
        {{
            "slides": [
                {{
                    "slide_number": 1,
                    "text": "Catchy hook text here",
                    "image_prompt": "A detailed DALL-E prompt for the background image"
                }}
            ]
        }}
        Create between 3 to 5 slides.
        """

        response = client.chat.completions.create(
            model="gpt-4o", # Or claude-3-haiku via Anthropic
            response_format={ "type": "json_object" },
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_input.idea}
            ]
        )
        
        # In a full build, you would parse this JSON and pass the 'image_prompt's 
        # to an image generation API here before returning the final payload.
        
        return {"status": "success", "data": response.choices[0].message.content}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Run locally using: uvicorn main:app --reload