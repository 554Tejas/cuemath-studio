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
        # Create the prompt for Cuemath's brand voice
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

        # Call the OpenAI API using the correct client syntax
        response = client.chat.completions.create(
            model="gpt-4o", 
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_input.idea}
            ],
            response_format={ "type": "json_object" }
        )
        
        # Return the JSON data back to the React frontend
        return {"status": "success", "data": response.choices[0].message.content}

    except Exception as e:
        # This prints the error to Render logs so you can see it
        print(f"Deployment Error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)