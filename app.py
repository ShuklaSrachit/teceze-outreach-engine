from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import requests

# -----------------------------
# FastAPI App Setup
# -----------------------------

app = FastAPI()

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

from pydantic import BaseModel
from typing import List


class RequestModel(BaseModel):

    # -----------------------------
    # Company Details
    # -----------------------------

    company_name: str
    industry: str
    geography: str

    # -----------------------------
    # Contact Details
    # -----------------------------

    contact_role: str
    contact_department: str

    # -----------------------------
    # Business Context
    # -----------------------------

    pain_point: str
    transformation_focus: str

    # -----------------------------
    # Service Towers (Multi-select)
    # -----------------------------

    service_towers: List[str]

    """
    Examples:

    Cloud
    Cybersecurity
    Infrastructure
    Managed Services
    Network Operations
    End User Computing
    Data Center
    IT Procurement
    Digital Transformation
    """

    # -----------------------------
    # OEM Ecosystem
    # -----------------------------

    oem_partners: List[str]

    """
    Examples:

    Microsoft
    AWS
    Cisco
    Palo Alto
    Fortinet
    CrowdStrike
    NetBrain
    VMware
    Dell
    HPE
    """

    # -----------------------------
    # Platform Environment
    # -----------------------------

    technology_stack: List[str]

    """
    Examples:

    SAP
    S/4HANA
    MES
    Active Directory
    Azure
    AWS
    Kubernetes
    VMware
    """

    # -----------------------------
    # Messaging Style
    # -----------------------------

    tone: str

    """
    Options:

    Consultative
    Strategic
    Technical
    Executive
    """

    # -----------------------------
    # Output Mode
    # -----------------------------

    output_type: str

    """
    Options:

    outreach_note
    email_sequence
    discovery_call_script
    partner_outreach
    """

    # -----------------------------
    # Optional Enhancers
    # -----------------------------

    include_statistics: bool = False
    include_use_cases: bool = False

# -----------------------------
# Root Route
# -----------------------------

@app.get("/")
def root():
    return {
        "status": "Backend running successfully"
    }


# -----------------------------
# Industry Templates
# -----------------------------

def get_industry_context(industry: str) -> str:

    industry = industry.lower()

    if "life" in industry or "pharma" in industry:

        return """
Industry Context (Life Sciences):

Organizations in life sciences environments are focusing on:

• Securing distributed manufacturing and lab environments
• Ensuring compliance readiness (ISO, GxP)
• Maintaining uptime across MES and SAP systems
• Managing IT/OT convergence across plants
• Standardizing IT operations across labs and sites
"""

    elif "bank" in industry or "fintech" in industry:

        return """
Industry Context (Banking & Financial Services):

Financial institutions are focusing on:

• Strengthening cybersecurity posture
• Ensuring regulatory compliance readiness
• Maintaining uptime of core banking systems
• Managing hybrid cloud securely
• Strengthening identity security
"""

    elif "manufacturing" in industry:

        return """
Industry Context (Manufacturing):

Manufacturing organizations are focusing on:

• Securing plant-level IT/OT infrastructure
• Ensuring uptime across production systems
• Standardizing IT across multiple plants
• Managing infrastructure vendors
• Supporting digital manufacturing initiatives
"""

    else:

        return """
Industry Context:

Organizations are focusing on:

• Improving IT visibility
• Strengthening cybersecurity posture
• Managing vendor complexity
• Supporting cloud transformation
"""


# -----------------------------
# Role Templates
# -----------------------------

def get_role_focus(role: str) -> str:

    role = role.lower()

    if "ciso" in role or "security" in role:

        return """
Role Focus:

Security leadership typically focuses on:

• Risk reduction
• Compliance readiness
• Threat visibility
• Incident response maturity
"""

    elif "cto" in role:

        return """
Role Focus:

Technology leadership typically focuses on:

• Architecture scalability
• Platform reliability
• Cloud modernization
• Operational resilience
"""

    elif "it" in role:

        return """
Role Focus:

IT leadership typically focuses on:

• Infrastructure reliability
• Vendor coordination
• Standardization
• Service uptime
"""

    else:

        return """
Role Focus:

Technology leadership typically focuses on:

• Stability
• Security
• Performance
• Governance
"""


# -----------------------------
# Generate Outreach Route
# -----------------------------

@app.post("/generate-email")
def generate_email(request: RequestModel):

    try:

        # Get Industry Context
        industry_context = get_industry_context(
            request.industry
        )

        # Get Role Context
        role_focus = get_role_focus(
            request.contact_role
        )

        # Build Prompt Safely
        prompt_text = f"""
Write a structured enterprise outreach note.

Target Company: {request.company_name}
Industry: {request.industry}
Target Role: {request.contact_role}
Services Offered: {request.services}
Pain Point: {request.pain_point}
Tone: {request.tone}

Opening:
Reference company priorities and transformation.

{industry_context}

{role_focus}

Key Focus Areas:
Use 4–6 bullet points relevant to the industry.

How TECEZE + OEM Ecosystem Helps:

• Cloud
• Cybersecurity
• Infrastructure
• Managed services

Business Outcomes:

• Improved visibility
• Standardized operations
• Reduced vendor complexity
• Optimized costs

Closing:
Would you be open to a 30-minute discussion sometime this week?

Rules:

• Professional consultative tone
• Use bullet points
• Avoid generic filler text
"""

        # Call Ollama
        response = requests.post(
            "http://localhost:11434/api/generate",
            json={
                "model": "llama3",
                "prompt": prompt_text,
                "stream": False
            }
        )

        data = response.json()

        return {
            "output": data.get("response", ""),
            "status": "success"
        }

    except Exception as e:

        return {
            "output": str(e),
            "status": "error"
        }

