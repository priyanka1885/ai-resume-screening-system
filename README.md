# Smart Resume Screening System

An AI-powered backend system that matches resumes against job descriptions using **TF-IDF**, **Cosine Similarity**, and **skill extraction**. Built with Python, FastAPI, and scikit-learn.

## Features

- **Resume Parsing** — Extracts text from PDF, DOCX, and TXT files
- **Skill Extraction** — Identifies technical and soft skills from text
- **TF-IDF + Cosine Similarity** — Computes semantic similarity between JD and resume
- **Match Scoring** — Returns a combined score (0–100) blending text similarity and skill overlap
- **Explanation Generation** — Produces human-readable match summaries
- **Multiple Resume Support** — Upload and rank multiple resumes at once
- **Swagger Documentation** — Interactive API docs at `/docs`

## Project Structure

```
smart_resume_screening/
│
├── app/
│   ├── __init__.py
│   ├── main.py          # FastAPI app and endpoints
│   ├── parser.py        # Resume text extraction (PDF/DOCX/TXT)
│   ├── matcher.py       # TF-IDF matching logic
│   ├── skills.py        # Predefined skill list and extraction
│   ├── schemas.py       # Pydantic response models
│   └── utils.py         # Helpers (validation, explanation)
│
├── resumes/             # Directory for uploaded resumes (gitignored)
├── requirements.txt
├── README.md
└── .gitignore
```

## Quick Start

### 1. Clone and navigate

```bash
cd smart_resume_screening
```

### 2. Create a virtual environment

```bash
python -m venv venv

# Windows
venv\Scripts\activate

# macOS/Linux
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Run the server

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

The API will be available at: **http://localhost:8000**

Interactive docs: **http://localhost:8000/docs**

## API Endpoints

### `GET /`
Health check. Returns system status.

### `POST /match-resume/`
Match a single resume against a job description.

**Parameters (form-data):**
| Field | Type | Description |
|-------|------|-------------|
| `job_description` | string | The job description text |
| `resume` | file | Resume file (.pdf, .docx, or .txt) |

**Response:**
```json
{
  "filename": "resume.pdf",
  "match_score": 82,
  "matched_skills": ["python", "sql", "machine learning"],
  "missing_skills": ["docker", "aws"],
  "explanation": "The resume shows excellent alignment with the job description, with strong overlap in Python, Sql, Machine Learning. However, experience in Docker, Aws appears to be missing."
}
```

### `POST /match-resumes/`
Match and rank multiple resumes against a job description.

**Parameters (form-data):**
| Field | Type | Description |
|-------|------|-------------|
| `job_description` | string | The job description text |
| `resumes` | file[] | One or more resume files |

**Response:**
```json
{
  "job_description": "Looking for a Python developer...",
  "results": [
    {
      "filename": "alice_resume.pdf",
      "match_score": 88,
      "matched_skills": ["python", "fastapi", "docker"],
      "missing_skills": ["aws"],
      "explanation": "..."
    },
    {
      "filename": "bob_resume.docx",
      "match_score": 65,
      "matched_skills": ["python"],
      "missing_skills": ["fastapi", "docker", "aws"],
      "explanation": "..."
    }
  ]
}
```

## Testing with cURL

### Single resume:
```bash
curl -X POST http://localhost:8000/match-resume/ \
  -F "job_description=Looking for a Python developer with experience in machine learning, SQL, Docker, and AWS" \
  -F "resume=@resumes/sample_resume.pdf"
```

### Multiple resumes:
```bash
curl -X POST http://localhost:8000/match-resumes/ \
  -F "job_description=Looking for a Python developer with experience in machine learning, SQL, Docker, and AWS" \
  -F "resumes=@resumes/resume1.pdf" \
  -F "resumes=@resumes/resume2.docx"
```

## Testing with Python (requests)

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

## How Scoring Works

The match score is a weighted combination of two signals:

1. **TF-IDF Cosine Similarity (60%)** — Measures overall textual similarity between the job description and resume content.
2. **Skill Match Ratio (40%)** — Proportion of JD-required skills found in the resume.

```
final_score = (tfidf_similarity * 0.6) + (skill_overlap_ratio * 0.4)
```

This blended approach ensures that both semantic content and specific skill keywords contribute to the final score.

## Extending the Skill List

Edit `app/skills.py` to add or remove skills from the `SKILL_LIST`. The system performs case-insensitive substring matching, so multi-word skills like "machine learning" work out of the box.

## Tech Stack

| Component | Technology |
|-----------|-----------|
| Web Framework | FastAPI |
| ML/NLP | scikit-learn (TF-IDF + Cosine Similarity) |
| PDF Parsing | pdfplumber |
| DOCX Parsing | python-docx |
| Validation | Pydantic |
| Server | Uvicorn |

## License

MIT
