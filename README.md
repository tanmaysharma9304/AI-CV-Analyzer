# AI CV Analyzer

A full-stack resume analyzer: upload PDF/DOCX resumes, parse candidate data, calculate transparent ATS/role scores, use Gemini for career feedback, inspect GitHub, validate public portfolio links, and download a PDF report.

## Architecture

- `backend/` FastAPI API, SQLite persistence, parsing/scoring/report services
- `frontend/` React + Vite dashboard
- `uploads/` persisted original resumes (created automatically)
- `reports/` generated PDF reports (created automatically)

## Install and run

### Backend

```bash
cd backend
python -m venv .venv
.venv\\Scripts\\activate
pip install -r requirements.txt
copy .env.example .env
uvicorn main:app --reload
```

The API listens on `http://localhost:8000`. Gemini is optional: set `GEMINI_API_KEY` in `.env` to enable AI-generated feedback. Without it, useful rule-based analysis remains available.

### Frontend

```bash
cd frontend
npm install
npm run dev
```

Open the Vite URL (normally `http://localhost:5173`). Optionally set `VITE_API_URL` in `frontend/.env`.

## Features

- PDF/DOCX uploads and text extraction
- Contact, skills, education, experience, projects, certifications extraction
- Explainable overall, ATS, skills, projects, experience scoring
- Role-based skills gap for QA Engineer, Python Developer, Data Analyst, and Full Stack Developer
- Gemini-powered strengths, weaknesses, career and ATS advice
- GitHub REST integration with repository/language summary and bonus
- LinkedIn/Tableau/Power BI public URL validation
- Chart.js pie/radar dashboard and downloadable ReportLab PDF
## Future improvements

- User authentication and ownership enforcement
- GitHub OAuth and richer contribution history
- LinkedIn OAuth (required to read full LinkedIn profile data)
- Background jobs/object storage for large files
