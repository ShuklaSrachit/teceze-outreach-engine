from fastapi import FastAPI
from pydantic import BaseModel
import google.generativeai as genai
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure Google API
genai.configure(
    api_key=os.getenv("GOOGLE_API_KEY")
)

# Your exact model ID
MODEL_ID = "gemma-4-31b-it"

# Initialize model
model = genai.GenerativeModel(MODEL_ID)

app = FastAPI()


# Request Model
class RequestModel(BaseModel):

    company_name: str
    contact_name: str
    industry: str
    pain_point: str
    service: str


# Prompt Builder
def build_prompt(request):

    return f"""
Write a highly personalized B2B cold outreach email.

Company Name: {request.company_name}
Contact Name: {request.contact_name}
Industry: {request.industry}
Pain Point: {request.pain_point}
Service Offered: {request.service}

Instructions:
- Keep email length between 120–180 words
- Professional tone
- Avoid generic phrases
- Include strong CTA
- Make it personalized
"""


# Core generation function
def generate_email(prompt):

    try:

        response = model.generate_content(
            prompt,
            generation_config={
                "temperature": 0.7,
                "max_output_tokens": 800
            }
        )

        if hasattr(response, "text"):
            return response.text

        return "No response generated."

    except Exception as e:

        return f"Generation Error: {str(e)}"


# API Route
@app.post("/generate-email")
def generate_email_api(request: RequestModel):

    try:

        prompt = build_prompt(request)

        output = generate_email(prompt)

        return {
            "output": output,
            "status": "success"
        }

    except Exception as e:

        return {
            "output": str(e),
            "status": "error"
        }
