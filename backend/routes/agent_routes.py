from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import get_db
from models import Test
from auth import get_current_user

router = APIRouter(prefix="/agents", tags=["Agent"])

@router.post("/submit-test")
def submit_test(
    patient_mask_id: str, gender: str, trial_id: str, center_code: str,
    test_id: str, agent_score: float, agent_review: str,
    db: Session = Depends(get_db), user = Depends(get_current_user)
):
    if user.role != "agent":
        raise HTTPException(status_code=403, detail="Not authorized")
    
    new_test = Test(
        patient_mask_id=patient_mask_id, gender=gender, trial_id=trial_id,
        center_code=center_code, agent_id=user.id, test_id=test_id,
        agent_score=agent_score, agent_review=agent_review
    )
    db.add(new_test)
    db.commit()
    return {"message": "Test submitted successfully"}
