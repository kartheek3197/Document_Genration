"""
Pydantic models for request payloads.
"""
from pydantic import BaseModel, Field
from datetime import date

class DocumentRequest(BaseModel):
    """
    Schema for document generation requests.
    """
    project_name: str = Field(..., description="Name of the project")
    project_type: str = Field("Commercial", description="Type of the project (e.g., Commercial or Residential)")
    location: str | None = Field(None, description="Location of the project")
    meeting_date: date = Field(default_factory=date.today, description="Meeting date for the review")

    class Config:
        schema_extra = {
            "example": {
                "project_name": "New Office Building",
                "project_type": "Commercial",
                "location": "123 Maple Street, Springfield",
                "meeting_date": "2025-04-27"
            }
        }
