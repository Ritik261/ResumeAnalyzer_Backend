from app.model.resume import ResumeAnalysis
from app.services.langchain_analyzer import analyze_resume
from app.services.text_extractor import extract_text
from sqlalchemy.orm import Session
from app.model.usermodel import User

import uuid, os
UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)
async def process_resume(file, user_id, db):
    currUser = db.query(User).filter(User.id == user_id).first()
    filename = f"{uuid.uuid4()}_{file.filename}"
    path = os.path.join(UPLOAD_DIR, filename)

    with open(path, "wb") as f:
        f.write(await file.read())

    resume_text = extract_text(path)

    ai_result = analyze_resume(resume_text)

    print("ats score from result", ai_result["ats_score"])
    print("key skills from result", ai_result["key_skills"])
    print("recommendations from result", ai_result["improvement_recommendations"])

    #key_skills = ai_result.key_skills
    # ats_score = ai_result.ats_score
    # recommendations = ai_result.recommendationsr

    key_skills = ai_result["key_skills"]
    ats_score = ai_result["ats_score"]
    recommendations = ai_result["improvement_recommendations"]

    resume = ResumeAnalysis(
        user_id=user_id,
        filename=file.filename,
        extracted_text=resume_text,
        key_skills=key_skills,
        ats_score=ats_score,
        recommendations=recommendations,
    )

    # db.add(resume)
    # db.commit()
    # db.refresh(resume)

    # return {"output": ai_result}

    return resume

    # output = f"keySkills: {key_skills}, extractedSkills: {resume_text}, atsScore: {ats_score}, Recommendation: {recommendations}"

    # return {"output": output, "airesult": ai_result}
