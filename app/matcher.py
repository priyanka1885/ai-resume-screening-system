"""
matcher.py - Resume-to-JD matching using TF-IDF and Cosine Similarity.

This module implements the core matching logic that compares a resume
against a job description and returns a similarity score along with
skill overlap analysis.
"""

from typing import Dict, List, Tuple

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from app.skills import extract_skills


def calculate_similarity(job_description: str, resume_text: str) -> Dict:
    """
    Calculate the match between a job description and a resume.

    Uses TF-IDF vectorization and cosine similarity to compute a
    semantic similarity score, then performs skill-based analysis
    for detailed feedback.

    Args:
        job_description: The job description text.
        resume_text: The extracted resume text.

    Returns:
        A dictionary containing:
            - match_score (int): Similarity score from 0 to 100
            - matched_skills (List[str]): Skills found in both texts
            - missing_skills (List[str]): Skills in JD but not in resume
    """
    # --- TF-IDF Cosine Similarity ---
    vectorizer = TfidfVectorizer(stop_words="english")
    tfidf_matrix = vectorizer.fit_transform([job_description, resume_text])

    # Cosine similarity between JD (index 0) and resume (index 1)
    similarity = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])
    raw_score = float(similarity[0][0])

    # --- Skill-Based Analysis ---
    jd_skills: List[str] = extract_skills(job_description)
    resume_skills: List[str] = extract_skills(resume_text)

    matched_skills: List[str] = [s for s in jd_skills if s in resume_skills]
    missing_skills: List[str] = [s for s in jd_skills if s not in resume_skills]

    # --- Combined Score ---
    # Blend TF-IDF similarity with skill overlap ratio for a balanced score
    if jd_skills:
        skill_ratio = len(matched_skills) / len(jd_skills)
    else:
        skill_ratio = 0.0

    # Weighted combination: 60% TF-IDF similarity + 40% skill match ratio
    combined_score = (raw_score * 0.6) + (skill_ratio * 0.4)
    match_score = min(100, max(0, int(combined_score * 100)))

    return {
        "match_score": match_score,
        "matched_skills": matched_skills,
        "missing_skills": missing_skills,
    }
