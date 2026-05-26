"""
main.py - FastAPI application entry point.

Defines the API endpoints for the Smart Resume Screening System.
Supports single and multiple resume uploads matched against a job description.
"""

from typing import List

from fastapi import FastAPI, File, Form, HTTPException, UploadFile
from fastapi.responses import JSONResponse

from app.matcher import calculate_similarity
from app.parser import extract_text
from app.schemas import MatchResult, MultiMatchResponse
from app.utils import generate_explanation, validate_file_extension

# --- Application Setup ---
app = FastAPI(
    title="Smart Resume Screening System",
    description=(
        "AI-powered resume screening API that matches resumes against "
        "job descriptions using TF-IDF, Cosine Similarity, and skill extraction."
    ),
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
)


# --- Health Check ---
@app.get("/", tags=["Health"])
async def root():
    """Health check endpoint."""
    return {
        "status": "running",
        "message": "Smart Resume Screening System is live. Visit /docs for API documentation.",
    }


# --- Single Resume Match ---
@app.post("/match-resume/", response_model=MatchResult, tags=["Matching"])
async def match_resume(
    job_description: str = Form(
        ..., description="The job description to match against"
    ),
    resume: UploadFile = File(..., description="Resume file (PDF, DOCX, or TXT)"),
):
    """
    Match a single resume against a job description.

    Accepts a job description and a resume file, then returns:
    - Match score (0-100)
    - Matched skills
    - Missing skills
    - Human-readable explanation

    Supported file formats: PDF, DOCX, TXT
    """
    # Validate job description
    if not job_description.strip():
        raise HTTPException(
            status_code=400, detail="Job description cannot be empty."
        )

    # Validate file type
    if not resume.filename or not validate_file_extension(resume.filename):
        raise HTTPException(
            status_code=400,
            detail="Invalid file type. Accepted formats: .pdf, .docx, .txt",
        )

    # Read and extract text from resume
    try:
        file_bytes = await resume.read()
        if not file_bytes:
            raise HTTPException(
                status_code=400, detail="Uploaded file is empty."
            )
        resume_text = extract_text(file_bytes, resume.filename)
    except ValueError as e:
        raise HTTPException(status_code=422, detail=str(e))
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error processing resume: {str(e)}"
        )

    # Calculate match
    result = calculate_similarity(job_description, resume_text)

    # Generate explanation
    explanation = generate_explanation(
        match_score=result["match_score"],
        matched_skills=result["matched_skills"],
        missing_skills=result["missing_skills"],
    )

    return MatchResult(
        filename=resume.filename,
        match_score=result["match_score"],
        matched_skills=result["matched_skills"],
        missing_skills=result["missing_skills"],
        explanation=explanation,
    )


# --- Multiple Resume Match & Ranking ---
@app.post("/match-resumes/", response_model=MultiMatchResponse, tags=["Matching"])
async def match_multiple_resumes(
    job_description: str = Form(
        ..., description="The job description to match against"
    ),
    resumes: List[UploadFile] = File(
        ..., description="One or more resume files (PDF, DOCX, or TXT)"
    ),
):
    """
    Match multiple resumes against a job description and rank them.

    Accepts a job description and multiple resume files, then returns
    ranked results sorted by match score (highest first).

    Supported file formats: PDF, DOCX, TXT
    """
    # Validate job description
    if not job_description.strip():
        raise HTTPException(
            status_code=400, detail="Job description cannot be empty."
        )

    if not resumes:
        raise HTTPException(
            status_code=400, detail="At least one resume file is required."
        )

    results: List[MatchResult] = []
    errors: List[str] = []

    for resume in resumes:
        # Validate file type
        if not resume.filename or not validate_file_extension(resume.filename):
            errors.append(
                f"Skipped '{resume.filename}': unsupported file type."
            )
            continue

        # Read and extract text
        try:
            file_bytes = await resume.read()
            if not file_bytes:
                errors.append(f"Skipped '{resume.filename}': file is empty.")
                continue
            resume_text = extract_text(file_bytes, resume.filename)
        except ValueError as e:
            errors.append(f"Skipped '{resume.filename}': {str(e)}")
            continue
        except Exception as e:
            errors.append(f"Skipped '{resume.filename}': processing error.")
            continue

        # Calculate match
        result = calculate_similarity(job_description, resume_text)

        # Generate explanation
        explanation = generate_explanation(
            match_score=result["match_score"],
            matched_skills=result["matched_skills"],
            missing_skills=result["missing_skills"],
        )

        results.append(
            MatchResult(
                filename=resume.filename,
                match_score=result["match_score"],
                matched_skills=result["matched_skills"],
                missing_skills=result["missing_skills"],
                explanation=explanation,
            )
        )

    # Sort results by match score (highest first) for ranking
    results.sort(key=lambda r: r.match_score, reverse=True)

    return MultiMatchResponse(
        job_description=job_description[:200] + "..."
        if len(job_description) > 200
        else job_description,
        results=results,
    )


# --- Run with Uvicorn ---
if __name__ == "__main__":
    import uvicorn

    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
