from fastapi import APIRouter, Depends, HTTPException, status
from src.services.user_services import UserService
from src.types.schemas.user import UserProfile
from src.types.schemas.auth import *
from src.core.auth.security import get_current_user

router = APIRouter(prefix="/user", tags=["User"])

@router.post("/login", response_model=Token)
async def login(data: LoginRequest, remember: bool = False) -> Token:
    try:
        access_token = await UserService.get_user(data, remember)
        return Token(access_token=access_token)
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while processing your request.",
        )

@router.post("/register", response_model=Token)
async def register(data: RegisterRequest, remember: bool = False) -> Token:
    try:
        access_token = await UserService.create_user(data)
        return Token(access_token=access_token)
    except HTTPException as e:
        raise e
    except Exception as e:
        import traceback
        error_detail = traceback.format_exc()
        print(f"\n{'='*80}\nREGISTRATION ERROR:\n{error_detail}\n{'='*80}\n")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error occurred while processing your request. Error: {str(e)}",
        )
    
@router.get("/profile", response_model=UserProfile)
async def get_profile(current_user = Depends(get_current_user)) -> UserProfile:
    try:
        user = current_user
        
        # Buscar workouts e body_assessments relacionados
        from src.types.models.workout import Workout
        from src.types.models.body_assessments import BodyAssessment
        from src.types.schemas.workout import WorkoutRead
        from src.types.schemas.body_assessment import BodyAssessmentBase
        
        workouts = await Workout.filter(user_id=user.id).all()
        body_assessments = await BodyAssessment.filter(user_id=user.id).all()
        
        workout_list = [WorkoutRead.from_orm(w) for w in workouts]
        body_history = [BodyAssessmentBase.from_orm(b) for b in body_assessments]
        
        # Gerar token para a resposta
        from src.core.auth.token import AccessToken
        token = AccessToken.generate(str(user.id), user.role, remember=False)
        
        return UserProfile(
            token=token,
            name=user.name,
            email=user.email,
            gender=user.gender,
            birth_date=user.birth_date,
            height_cm=user.height_cm,
            activity_level=user.activity_level,
            role=user.role,
            created_at=user.created_at,
            workouts=workout_list,
            body_history=body_history,
        )
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while processing your request.",
        )