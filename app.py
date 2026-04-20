from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import requests

# -----------------------------
# FastAPI App Setup
# -----------------------------

app = FastAPI(
    title="TECEZE Outreach Engine",
    description="AI-powered enterprise outreach generator",
    version="1.0"
)

# Enable CORS

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# -----------------------------
# Request Model
# -----------------------------

class RequestModel(BaseModel):

    company_name: str
    industry: str
    geography: str

    contact_role: str
    contact_department: str

    pain_point: str
    transformation_focus: str

    service_towers: list[str]
    oem_partners: list[str]
    technology_stack: list[str]

    tone: str
    output_type: str

    include_statistics: bool
    include_use_cases: bool


# -----------------------------
# Root Route
# -----------------------------

@app.get("/")
def root():
    return {
        "status": "Backend running successfully"
    }


# -----------------------------
# Prompt Builder
# -----------------------------

def build_prompt(request: RequestModel):

    services = ", ".join(request.service_towers)
    oems = ", ".join(request.oem_partners)
    tech = ", ".join(request.technology_stack)

    stats_text = "Include relevant enterprise statistics." if request.include_statistics else ""
    usecase_text = "Include enterprise use cases." if request.include_use_cases else ""

    prompt = f"""
Create a structured enterprise outreach note.

Company: {request.company_name}
Industry: {request.industry}
Geography: {request.geography}

Contact Role: {request.contact_role}
Department: {request.contact_department}

Pain Point:
{request.pain_point}

Transformation Focus:
{request.transformation_focus}

Service Towers:
{services}

OEM Partners:
{oems}

Technology Stack:
{tech}

Tone:
{request.tone}

Output Type:
{request.output_type}

Instructions:

Structure output into:

1. Opening  
2. Industry Context  
3. Key Focus Areas  
4. How TECEZE + OEM Ecosystem Helps  
5. Business Outcomes  
6. Closing  

{stats_text}
{usecase_text}

Make it enterprise-grade, consultative, and industry-specific.
"""

    return prompt


# -----------------------------
# Email Generator Route
# -----------------------------

@app.post("/generate-email")
def generate_email(request: RequestModel):

    try:

        prompt = build_prompt(request)

        response = requests.post(
            "http://localhost:11434/api/generate",
            json={
                "model": "llama3",
                "prompt": prompt,
                "stream": False
            }
        )

        result = response.json()

        return {
            "output": result.get("response", ""),
            "status": "success"
        }

    except Exception as e:

        return {
            "output": str(e),
            "status": "error"
        }
