from pydantic import BaseModel, HttpUrl, Field
from typing import Any

class IntegrationRequest(BaseModel):
    github_username: str | None = None
    linkedin_url: str | None = None
    tableau_or_powerbi_url: str | None = None

class AnalyzeRequest(BaseModel):
    role: str = "Python Developer"
    integrations: IntegrationRequest = Field(default_factory=IntegrationRequest)

class ResumeResponse(BaseModel):
    id: int
    filename: str
    parsed: dict[str, Any]

class AnalysisResponse(BaseModel):
    resume_id: int
    parsed: dict[str, Any]
    scores: dict[str, Any]
    gap: dict[str, Any]
    ai: dict[str, Any]
    integrations: dict[str, Any]
