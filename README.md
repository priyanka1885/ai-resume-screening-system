<p align="center">
  <img src="https://img.shields.io/badge/Python-3.11+-3776AB?style=for-the-badge&logo=python&logoColor=white" />
  <img src="https://img.shields.io/badge/FastAPI-0.104-009688?style=for-the-badge&logo=fastapi&logoColor=white" />
  <img src="https://img.shields.io/badge/scikit--learn-1.3-F7931E?style=for-the-badge&logo=scikit-learn&logoColor=white" />
  <img src="https://img.shields.io/badge/License-MIT-green?style=for-the-badge" />
</p>

# Smart Resume Screening System

> An AI-powered backend system that intelligently matches resumes against job descriptions using NLP and Machine Learning — built for recruiters, HR teams, and developers exploring AI in hiring.

---

## Overview

The **Smart Resume Screening System** automates the tedious process of manually reviewing resumes. Upload a job description and one or more resumes, and the system will:

- Extract text from PDF, DOCX, or TXT files
- Identify relevant technical and soft skills
- Compute a similarity score using TF-IDF and Cosine Similarity
- Return matched/missing skills with a human-readable explanation
- Rank multiple candidates by relevance

This project demonstrates production-style Python backend development with clean architecture, type hints, and modular design.

---

## Features

| Feature | Description |
|---------|-------------|
| Multi-format Parsing | Supports PDF, DOCX, and TXT resume uploads |
| AI-Powered Matching | TF-IDF Vectorization + Cosine Similarity scoring |
| Skill Extraction | Identifies 60+ technical and soft skills |
| Match Scoring | Weighted score (0–100) combining text similarity and skill overlap |
| Explanations | Auto-generated human-readable match summaries |
| Resume Ranking | Upload multiple resumes and get ranked results |
| Input Validation | File type checks, empty file handling, error responses |
| Swagger Docs | Interactive API documentation out of the box |

---

## Tech Stack

| Layer | Technology |
|-------|-----------|
| **Framework** | FastAPI |
| **ML/NLP** | scikit-learn (TF-IDF + Cosine Similarity) |
| **PDF Parsing** | pdfplumber |
| **DOCX Parsing** | python-docx |
| **Validation** | Pydantic v2 |
| **Server** | Uvicorn (ASGI) |
| **Language** | Python 3.11+ |

---

## Project Structure

```
smart_resume_screening/
│
├── app/
│   ├── __init__.py          # Package initializer
│   ├── main.py              # FastAPI app & API endpoints
│   ├── parser.py            # Resume text extraction (PDF/DOCX/TXT)
│   ├── matcher.py           # TF-IDF matching & scoring logic
│   ├── skills.py            # Predefined skill list & extraction
│   ├── schemas.py           # Pydantic request/response models
│   └── utils.py             # Helpers (validation, explanation generator)
│
├── resumes/                 # Upload directory (gitignored)
├── requirements.txt         # Python dependencies
├── README.md                # Project documentation
└── .gitignore               # Git ignore rules
```

---

## Installation & Setup

### Prerequisites

- Python 3.11 or higher
- pip (Python package manager)

### Steps

```bash
# 1. Clone the repository
git clone https://github.com/YOUR_USERNAME/ai-resume-screening-system.git
cd ai-resume-screening-system

# 2. Create a virtual environment
python -m venv venv

# Windows
venv\Scripts\activate

# macOS/Linux
source venv/bin/activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Start the server
uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```

---

## API Endpoints

### `GET /` — Health Check

Returns system status.

```json
{
  "status": "running",
  "message": "Smart Resume Screening System is live. Visit /docs for API documentation."
}
```

---

### `POST /match-resume/` — Single Resume Match

Match one resume against a job description.

**Parameters (multipart/form-data):**

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `job_description` | string | Yes | The job description text |
| `resume` | file | Yes | Resume file (.pdf, .docx, or .txt) |

---

### `POST /match-resumes/` — Multiple Resume Ranking

Upload multiple resumes and get ranked results.

**Parameters (multipart/form-data):**

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `job_description` | string | Yes | The job description text |
| `resumes` | file[] | Yes | One or more resume files |

---

## Example Request & Response

### cURL Request

```bash
curl -X POST http://localhost:8000/match-resume/ \
  -F "job_description=Looking for a Python developer with experience in machine learning, SQL, Docker, and AWS" \
  -F "resume=@resumes/sample_resume.pdf"
```

### Python Request

```python
import requests

url = "http://localhost:8000/match-resume/"
jd = "We need a Python developer skilled in machine learning, SQL, Docker, and AWS."

with open("resumes/sample_resume.pdf", "rb") as f:
    response = requests.post(
        url,
        data={"job_description": jd},
        files={"resume": ("resume.pdf", f, "application/pdf")},
    )

print(response.json())
```

### Response

```json
{
  "filename": "sample_resume.pdf",
  "match_score": 82,
  "matched_skills": ["python", "machine learning", "sql", "data analysis"],
  "missing_skills": ["docker", "aws"],
  "explanation": "The resume shows excellent alignment with the job description, with strong overlap in Python, Machine Learning, Sql, Data Analysis. However, experience in Docker, Aws appears to be missing."
}
```

---

## Screenshots

![Screenshot 1](screenshots/Screenshot%20(1814).png)

---

![Screenshot 2](screenshots/Screenshot%20(1815).png)

---

![Screenshot 3](screenshots/Screenshot%20(1816).png)

---

## How Scoring Works

The match score combines two signals:

```
final_score = (tfidf_cosine_similarity × 0.6) + (skill_match_ratio × 0.4)
```

| Component | Weight | Description |
|-----------|--------|-------------|
| TF-IDF Cosine Similarity | 60% | Semantic text overlap between JD and resume |
| Skill Match Ratio | 40% | Proportion of required skills found in resume |

This blended approach ensures both contextual relevance and specific keyword coverage contribute to the final score.

---

## Future Improvements

- [ ] **Sentence Transformers** — Use BERT/SBERT embeddings for deeper semantic matching
- [ ] **Experience Extraction** — Parse years of experience from resumes
- [ ] **Docker Support** — Containerize the application for easy deployment
- [ ] **Streamlit Frontend** — Build an interactive UI for non-technical users
- [ ] **Database Integration** — Store and retrieve past screening results
- [ ] **Batch Processing** — Handle large-scale resume uploads asynchronously
- [ ] **Custom Skill Lists** — Allow users to define domain-specific skills per job
- [ ] **Authentication** — Add API key or OAuth2 protection

---

## Contributing

Contributions are welcome! Feel free to:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

---

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

---

<p align="center">
  <b>If you found this project useful, give it a star on GitHub!</b>
</p>
