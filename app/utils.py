"""
utils.py - Utility functions for the Smart Resume Screening System.

Contains helper functions for explanation generation, file validation,
and other shared logic.
"""

from typing import List

# Allowed file extensions for resume uploads
ALLOWED_EXTENSIONS = {".pdf", ".docx", ".txt"}


def validate_file_extension(filename: str) -> bool:
    """
    Check if the uploaded file has an allowed extension.

    Args:
        filename: The original filename of the upload.

    Returns:
        True if the extension is allowed, False otherwise.
    """
    filename_lower = filename.lower()
    return any(filename_lower.endswith(ext) for ext in ALLOWED_EXTENSIONS)


def generate_explanation(
    match_score: int,
    matched_skills: List[str],
    missing_skills: List[str],
) -> str:
    """
    Generate a human-readable explanation of the match result.

    Args:
        match_score: The calculated match score (0-100).
        matched_skills: Skills found in both JD and resume.
        missing_skills: Skills in JD but not in resume.

    Returns:
        A short explanation string summarizing the match.
    """
    # Determine match quality
    if match_score >= 80:
        quality = "excellent"
    elif match_score >= 60:
        quality = "good"
    elif match_score >= 40:
        quality = "moderate"
    else:
        quality = "low"

    # Build explanation parts
    parts: List[str] = []

    if matched_skills:
        skills_str = ", ".join(s.title() for s in matched_skills[:5])
        if len(matched_skills) > 5:
            skills_str += f" and {len(matched_skills) - 5} more"
        parts.append(
            f"The resume shows {quality} alignment with the job description, "
            f"with strong overlap in {skills_str}."
        )
    else:
        parts.append(
            f"The resume shows {quality} alignment with the job description. "
            "No specific skill matches were identified from the predefined skill list."
        )

    if missing_skills:
        missing_str = ", ".join(s.title() for s in missing_skills[:5])
        if len(missing_skills) > 5:
            missing_str += f" and {len(missing_skills) - 5} more"
        parts.append(f"However, experience in {missing_str} appears to be missing.")

    if not missing_skills and matched_skills:
        parts.append("The candidate covers all identified required skills.")

    return " ".join(parts)
