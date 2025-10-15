
from typing import List, Optional
from typing import Optional, List
from datetime import datetime
from pydantic import BaseModel
import os

from agents import Agent,ItemHelpers,AsyncOpenAI,OpenAIChatCompletionsModel,RunContextWrapper, Runner,set_tracing_disabled, function_tool
from dotenv import load_dotenv, find_dotenv
from openai.types.responses import ResponseTextDeltaEvent

load_dotenv(find_dotenv())
gemini_api_key: str | None = os.environ.get("GOOGLE_API_KEY")

set_tracing_disabled(disabled=True)
external_client: AsyncOpenAI = AsyncOpenAI(api_key=gemini_api_key, base_url="https://generativelanguage.googleapis.com/v1beta/openai/")
llm_provider : OpenAIChatCompletionsModel = OpenAIChatCompletionsModel(model='gemini-2.5-flash', openai_client=external_client) 


class Education(BaseModel):
    degree: str
    institution: str
    graduation_year: int
    gpa: Optional[float] = None

class Experience(BaseModel):
    position: str
    company: str
    start_year: int
    end_year: Optional[int] = None  # None if current job
    responsibilities: List[str]

class Resume(BaseModel):
    full_name: str
    email: str
    phone: str
    summary: str
    education: List[Education]
    experience: List[Experience]
    skills: List[str]
    languages: List[str]

# Create resume parser
resume_parser = Agent(
    name="ResumeParser",
    instructions="Extract structured information from resume text.",
    output_type=Resume
    ,model= llm_provider
)

# Test with sample resume
sample_resume = """
John Smith
Email: john.smith@email.com, Phone: (555) 123-4567

Professional Summary:
Experienced software developer with 5 years in web development and team leadership.

Education:
- Bachelor of Computer Science, MIT, 2018, GPA: 3.8
- Master of Software Engineering, Stanford, 2020

Experience:
- Senior Developer at Google (2020-present): Led team of 5 developers, implemented microservices architecture
- Junior Developer at Startup Inc (2018-2020): Built React applications, maintained CI/CD pipelines

Skills: Python, JavaScript, React, Docker, Kubernetes
Languages: English (native), Spanish (conversational), French (basic)
"""

result = Runner.run_sync(resume_parser, sample_resume)

print("=== Parsed Resume ===")
print(f"Name: {result.final_output.full_name}")
print(f"Email: {result.final_output.email}")
print(f"Phone: {result.final_output.phone}")
print(f"Summary: {result.final_output.summary}")

print("\nEducation:")
for edu in result.final_output.education:
    gpa_str = f", GPA: {edu.gpa}" if edu.gpa else ""
    print(f" • {edu.degree} from {edu.institution} ({edu.graduation_year}){gpa_str}")

print("\nExperience:")
for exp in result.final_output.experience:
    end_year = exp.end_year if exp.end_year else "present"
    print(f"  • {exp.position} at {exp.company} ({exp.start_year}-{end_year})")
    for resp in exp.responsibilities:
        print(f"    - {resp}")

print(f"\nSkills: {', '.join(result.final_output.skills)}")
print(f"Languages: {', '.join(result.final_output.languages)}")