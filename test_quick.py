"""Quick smoke test for the matching pipeline."""
from app.matcher import calculate_similarity
from app.skills import extract_skills
from app.utils import generate_explanation

jd = """
We are looking for a Python developer with experience in machine learning,
SQL, Docker, AWS, and data analysis. Familiarity with FastAPI and pandas is a plus.
"""

resume = """
John Doe - Software Engineer
Skills: Python, Machine Learning, SQL, Pandas, NumPy, Data Analysis, Git
Experience: 3 years building ML pipelines and REST APIs using Flask and FastAPI.
"""

# Test skill extraction
jd_skills = extract_skills(jd)
resume_skills = extract_skills(resume)
print(f"JD Skills: {jd_skills}")
print(f"Resume Skills: {resume_skills}")

# Test matching
result = calculate_similarity(jd, resume)
print(f"\nMatch Score: {result['match_score']}")
print(f"Matched Skills: {result['matched_skills']}")
print(f"Missing Skills: {result['missing_skills']}")

# Test explanation
explanation = generate_explanation(
    result["match_score"], result["matched_skills"], result["missing_skills"]
)
print(f"\nExplanation: {explanation}")
print("\n--- All tests passed! ---")
