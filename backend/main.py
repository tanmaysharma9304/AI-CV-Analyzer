import json, os, shutil, uuid
from pathlib import Path
from fastapi import FastAPI, UploadFile, File, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
from database import Base, engine, get_db
from models import Resume, Score, Report
from schemas import ResumeResponse, AnalyzeRequest, AnalysisResponse
from services.parser import extract_text, parse_resume
from services.scoring import score, ROLE_SKILLS
from services.ai import analyze
from services.integrations import github, validate_urls
from services.report import create_report

ROOT = Path(__file__).resolve().parent.parent; UPLOADS = ROOT / "uploads"; REPORTS = ROOT / "reports"; UPLOADS.mkdir(exist_ok=True); REPORTS.mkdir(exist_ok=True)
Base.metadata.create_all(bind=engine)
app = FastAPI(title="AI CV Analyzer", version="1.0.0")
app.add_middleware(CORSMiddleware, allow_origins=os.getenv("CORS_ORIGINS", "http://localhost:5173").split(","), allow_credentials=True, allow_methods=["*"], allow_headers=["*"])

@app.get("/api/health")
def health(): return {"status": "ok", "roles": list(ROLE_SKILLS)}

@app.post("/api/resumes", response_model=ResumeResponse)
async def upload_resume(file: UploadFile = File(...), db: Session = Depends(get_db)):
    suffix = Path(file.filename or "").suffix.lower()
    if suffix not in {".pdf", ".docx"}: raise HTTPException(400, "Only PDF and DOCX files are supported")
    path = UPLOADS / f"{uuid.uuid4()}{suffix}"
    with path.open("wb") as out: shutil.copyfileobj(file.file, out)
    try: text = extract_text(path)
    except Exception as e: path.unlink(missing_ok=True); raise HTTPException(400, f"Could not extract resume text: {e}")
    if not text.strip(): raise HTTPException(400, "No readable text was found in this file")
    parsed = parse_resume(text); record = Resume(filename=file.filename or path.name, stored_path=str(path), raw_text=text, parsed_json=json.dumps(parsed)); db.add(record); db.commit(); db.refresh(record)
    return {"id": record.id, "filename": record.filename, "parsed": parsed}

@app.post("/api/resumes/{resume_id}/analyze", response_model=AnalysisResponse)
async def run_analysis(resume_id: int, payload: AnalyzeRequest, db: Session = Depends(get_db)):
    resume = db.get(Resume, resume_id)
    if not resume: raise HTTPException(404, "Resume not found")
    parsed = json.loads(resume.parsed_json); gh = await github(payload.integrations.github_username); links = validate_urls(payload.integrations.linkedin_url, payload.integrations.tableau_or_powerbi_url); bonus = gh.get("bonus", 0) + links["tableau_powerbi"].get("bonus", 0)
    scores, gap = score(parsed, payload.role, bonus); ai = analyze(parsed, gap, scores)
    existing = resume.score
    if existing: [setattr(existing, k, scores[k]) for k in ["overall","ats","skill","project","experience"]]; existing.breakdown_json=json.dumps(scores["breakdown"])
    else: db.add(Score(resume_id=resume.id, overall=scores["overall"], ats=scores["ats"], skill=scores["skill"], project=scores["project"], experience=scores["experience"], breakdown_json=json.dumps(scores["breakdown"])))
    db.commit(); return {"resume_id":resume.id, "parsed":parsed, "scores":scores, "gap":gap, "ai":ai, "integrations":{"github":gh, **links}}

@app.post("/api/resumes/{resume_id}/report")
async def generate_report(resume_id: int, payload: AnalyzeRequest, db: Session = Depends(get_db)):
    analysis = await run_analysis(resume_id, payload, db)
    path = REPORTS / f"cv-report-{resume_id}-{uuid.uuid4().hex[:8]}.pdf"; create_report(path, analysis["parsed"], analysis["scores"], analysis["gap"], analysis["ai"]); record = Report(resume_id=resume_id, path=str(path)); db.add(record); db.commit()
    return FileResponse(path, media_type="application/pdf", filename="cv-analysis-report.pdf")
