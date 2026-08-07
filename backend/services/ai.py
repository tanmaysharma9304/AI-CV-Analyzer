import os
import google.generativeai as genai

def analyze(parsed: dict, gap: dict, scores: dict) -> dict:
    fallback = {"strengths": [f"Found {len(parsed['skills'])} technical skills", "Resume includes contact details" if parsed['email'] else "Skills were detected"], "weaknesses": ["Add more quantified impact statements"], "missing_skills": gap["missing_skills"], "career_advice": "Prioritize one role-aligned portfolio project and describe its measurable result.", "ats_suggestions": ["Use standard section headings", "Include role keywords naturally in experience bullets"], "resume_improvements": ["Start bullets with action verbs", "Add tools and outcomes to each project"]}
    key = os.getenv("GEMINI_API_KEY")
    if not key: return fallback
    try:
        genai.configure(api_key=key)
        prompt = f"Return concise JSON with strengths, weaknesses, missing_skills, career_advice, ats_suggestions, resume_improvements. Resume data: {parsed}. Gap: {gap}. Scores: {scores}"
        response = genai.GenerativeModel(os.getenv("GEMINI_MODEL", "gemini-1.5-flash")).generate_content(prompt, generation_config={"response_mime_type":"application/json"})
        import json
        return json.loads(response.text)
    except Exception:
        return fallback
