"""
skills.py - Predefined skill list and skill extraction logic.

This module contains a curated list of technical skills and a function
to extract matching skills from any given text (resume or job description).
"""

import re
from typing import List

# Predefined list of technical skills to match against.
# Extend this list as needed for your domain.
SKILL_LIST: List[str] = [
    "python",
    "machine learning",
    "deep learning",
    "sql",
    "tensorflow",
    "pytorch",
    "pandas",
    "numpy",
    "fastapi",
    "flask",
    "django",
    "docker",
    "kubernetes",
    "aws",
    "azure",
    "gcp",
    "nlp",
    "natural language processing",
    "data analysis",
    "data science",
    "data engineering",
    "computer vision",
    "scikit-learn",
    "sklearn",
    "java",
    "javascript",
    "typescript",
    "react",
    "node.js",
    "html",
    "css",
    "git",
    "linux",
    "mongodb",
    "postgresql",
    "mysql",
    "redis",
    "spark",
    "hadoop",
    "tableau",
    "power bi",
    "excel",
    "r programming",
    "scala",
    "golang",
    "rust",
    "c++",
    "c#",
    "api development",
    "rest api",
    "graphql",
    "microservices",
    "ci/cd",
    "agile",
    "scrum",
    "jira",
    "communication",
    "teamwork",
    "problem solving",
    "leadership",
]

# Skills that are short or common words need word-boundary matching
# to avoid false positives (e.g., "sql" in "result")
_SHORT_SKILLS = {s for s in SKILL_LIST if len(s) <= 3}


def extract_skills(text: str) -> List[str]:
    """
    Extract skills from the given text by matching against the predefined skill list.

    Uses word-boundary regex for short skill names to avoid false positives.

    Args:
        text: The input text (resume or job description) to scan for skills.

    Returns:
        A deduplicated list of matched skills found in the text.
    """
    if not text:
        return []

    # Normalize text to lowercase for case-insensitive matching
    text_lower = text.lower()

    # Find all skills present in the text
    matched_skills: List[str] = []
    for skill in SKILL_LIST:
        if skill in _SHORT_SKILLS:
            # Use word-boundary matching for short skills to avoid false positives
            pattern = r"\b" + re.escape(skill) + r"\b"
            if re.search(pattern, text_lower):
                matched_skills.append(skill)
        else:
            if skill in text_lower:
                matched_skills.append(skill)

    # Remove duplicates while preserving order
    seen = set()
    unique_skills: List[str] = []
    for skill in matched_skills:
        if skill not in seen:
            seen.add(skill)
            unique_skills.append(skill)

    return unique_skills
