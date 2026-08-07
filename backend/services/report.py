from pathlib import Path
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch

def create_report(report_path: Path, parsed: dict, scores: dict, gap: dict, ai: dict) -> None:
    c = canvas.Canvas(str(report_path), pagesize=letter); width, height = letter; y = height - .7*inch
    def write(title, value):
        nonlocal y
        c.setFont("Helvetica-Bold", 12); c.drawString(.6*inch, y, title); y -= 16
        c.setFont("Helvetica", 9)
        for line in str(value).replace("[", "").replace("]", "").split("\n"):
            c.drawString(.75*inch, y, line[:120]); y -= 13
            if y < .7*inch: c.showPage(); y = height-.7*inch
        y -= 7
    c.setFont("Helvetica-Bold", 18); c.drawString(.6*inch, y, "AI CV Analyzer Report"); y -= 28
    write("Candidate", parsed.get("name"))
    # A compact score chart makes the report useful offline as well as in the dashboard.
    c.setFont("Helvetica-Bold", 12); c.drawString(.6*inch, y, "Score chart"); y -= 17
    labels = [("Overall", scores["overall"]), ("ATS", scores["ats"]), ("Skills", scores["skill"]), ("Projects", scores["project"]), ("Experience", scores["experience"])]
    for label, value in labels:
        c.setFont("Helvetica", 9); c.drawString(.75*inch, y, label)
        c.setFillColorRGB(.91, .92, .98); c.rect(1.55*inch, y-3, 3.7*inch, 9, stroke=0, fill=1)
        c.setFillColorRGB(.39, .40, .95); c.rect(1.55*inch, y-3, 3.7*inch * min(value, 100)/100, 9, stroke=0, fill=1)
        c.setFillColorRGB(0, 0, 0); c.drawRightString(5.6*inch, y, f"{value}%"); y -= 17
    y -= 5
    write("Missing skills", ", ".join(gap["missing_skills"]) or "None")
    write("Recommendations", ai.get("resume_improvements", []))
    write("Career advice", ai.get("career_advice", ""))
    c.save()
