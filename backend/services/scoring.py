ROLE_SKILLS = {
 "QA Engineer": ["selenium", "pytest", "postman", "jira", "manual testing", "api testing", "sql", "git"],
 "Python Developer": ["python", "fastapi", "django", "flask", "sql", "git", "docker", "rest api"],
 "Data Analyst": ["python", "sql", "pandas", "numpy", "excel", "power bi", "tableau", "scikit-learn"],
 "Full Stack Developer": ["javascript", "typescript", "react", "node.js", "html", "css", "sql", "git", "rest api"]
}

def score(parsed: dict, role: str, bonus: float = 0) -> tuple[dict, dict]:
    required = ROLE_SKILLS.get(role, ROLE_SKILLS["Python Developer"])
    found = [s for s in required if s in parsed["skills"]]
    missing = [s for s in required if s not in found]
    skill = round(100 * len(found) / len(required), 1)
    project = min(100, len(parsed["projects"]) * 25 + (20 if "github" in parsed["skills"] else 0))
    experience = min(100, len(parsed["experience"]) * 15)
    checks = {"contact_details": bool(parsed["email"] and parsed["phone"]), "education": bool(parsed["education"]), "experience": bool(parsed["experience"]), "projects": bool(parsed["projects"]), "keywords": len(parsed["skills"]) >= 5, "sections": sum(bool(parsed[x]) for x in ["education", "experience", "projects"]) >= 2, "formatting": True}
    ats = round(100 * sum(checks.values()) / len(checks), 1)
    overall = round(min(100, .4 * ats + .35 * skill + .1 * project + .15 * experience + bonus), 1)
    scores = {"overall": overall, "ats": ats, "skill": skill, "project": project, "experience": experience, "breakdown": {"formula": "40% ATS + 35% role skills + 10% projects + 15% experience + integration bonus", "ats_checks": checks, "github_bonus": bonus}}
    gap = {"role": role, "required_skills": required, "found_skills": found, "missing_skills": missing, "recommendations": [f"Build a portfolio project using {s}." for s in missing[:4]] or ["Your role-specific skills are well aligned. Add measurable outcomes to projects."]}
    return scores, gap
