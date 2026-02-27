from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from sqlalchemy.orm import Session
from app.database.database import get_db
from app.model.usermodel import User
from app.services.resume_service import process_resume

router1 = APIRouter(prefix="/v1", tags=["upload"])

def get_current_user(request, db: Session = Depends(get_db)):
    from jose import jwt, JWTError
    from app.auth.auth import SECRET_KEY, ALGORITHM
    
    access_token = request.cookies.get("access_token")
    if not access_token:
        raise HTTPException(status_code=401, detail="Token not valid")
    
    if access_token.startswith("Bearer "):
        access_token = access_token[7:]
    
    try:
        payload = jwt.decode(access_token, SECRET_KEY, ALGORITHM)
        userEmail: str = payload.get("sub")
        if userEmail is None:
            raise HTTPException(status_code=401, detail="Invalid Token")
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid Token")

    user = db.query(User).filter(User.email == userEmail).first()
    if user is None:
        raise HTTPException(status_code=401, detail="User not found")
    return user.id

@router1.post("/upload")
async def upload_resume(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    currUser = Depends(get_current_user)
):
    if not file.filename.endswith((".pdf", ".docx")):
        raise HTTPException(status_code=400, detail="Invalid File Format")
    
    try:
        result = await process_resume(file, currUser, db)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")
