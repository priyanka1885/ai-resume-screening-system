"""
schemas.py - Pydantic models for request/response validation.

Defines the data structures used by the API endpoints.
"""

from typing import List
from pydantic import BaseModel, Field


class MatchResult(BaseModel):
    """Response model for a single resume match result."""

    filename: str = Field(..., description="Name of the uploaded resume file")
    match_score: int = Field(
        ..., ge=0, le=100, description="Similarity score from 0 to 100"
    )
    matched_skills: List[str] = Field(
        default_factory=list, description="Skills found in both JD and resume"
    )
    missing_skills: List[str] = Field(
        default_factory=list, description="Skills in JD but not in resume"
    )
    explanation: str = Field(
        ..., description="Short human-readable explanation of the match"
    )


class MultiMatchResponse(BaseModel):
    """Response model when multiple resumes are submitted."""

    job_description: str = Field(..., description="The job description provided")
    results: List[MatchResult] = Field(
        default_factory=list, description="List of match results, ranked by score"
    )
