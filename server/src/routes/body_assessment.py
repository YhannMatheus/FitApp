from fastapi import APIRouter, Depends, HTTPException, status, Header
from src.services.body_assessment_service import BodyAssessmentService
from src.types.schemas.body_assessment import *
from src.core.auth.token import AccessToken
from src.types.models.user import User

app = APIRouter(prefix="/body-assessment", tags=["Body Assessment"])

@app.post("/", response_model=BodyAssessmentReed)
async def create_body_assessment(data: BodyAssessmentCreate, authorization:str = Header(...)) -> BodyAssessmentReed:
    user_information = AccessToken.decode(authorization)
    
    try:
        # Busca o usuário do banco de dados usando o ID do token
        user = await User.get(id=user_information.user_id)
        
        body_assessment = await BodyAssessmentService.create_body_assessment(
            user_id=user.id,
            user_gender=user.gender,
            user_birth_date=user.birth_date,
            user_activity_level=user.activity_level,
            data=data
        )
        return body_assessment
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error occurred while creating body assessment: {str(e)}",
        )
    
@app.get("/", response_model=list[BodyAssessmentReed])
async def get_all(authorization:str = Header(...)) -> list[BodyAssessmentReed]:
    token = AccessToken.decode(authorization)   
    try:
        body_assessments = await BodyAssessmentService.get_all_body_assessment_for_user_id(str(token.user_id))
        return body_assessments
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error occurred while retrieving body assessments: {str(e)}",
        )
    
@app.get("/{assessment_id}", response_model=BodyAssessmentBase)
async def get_body_assessment(assessment_id:str, authorization:str = Header(...)) -> BodyAssessmentBase:
    user_information = AccessToken.decode(authorization) 
    try:
        body_assessment = await BodyAssessmentService.get_body_assessment(assessment_id)
        if str(user_information.user_id) != str(body_assessment.user_id):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You do not have permission to access this body assessment.",
            )
        return body_assessment
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error occurred while retrieving body assessment: {str(e)}",
        )
    
@app.get("/graph/{user_id}/weight", response_model=)