from src.types.schemas.body_assessment import BodyAssessmentBase
from src.types.schemas.auth import LoginRequest, RegisterRequest
from src.types.models.body_assessments import BodyAssessment
from src.types.schemas.workout import WorkoutRead
from src.types.schemas.user import UserProfile
from src.types.models.workout import Workout
from src.core.auth.security import Authenticate
from src.core.auth.token import AccessToken
from fastapi import HTTPException, status
from src.types.models.user import User

class UserService:
    @staticmethod
    async def create_user(data: RegisterRequest):
        if await User.exists(email=data.email):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="Email already in use"
            )

        hashed_password = Authenticate.hash_password(data.password)

        user = await User.create(
            name=data.name,
            email=data.email,
            hashed_password=hashed_password,
            gender=data.gender,
            birth_date=data.birth_date,
            height_cm=data.height_cm,
            activity_level=data.activity_level,
        )

        return AccessToken.generate(str(user.id), user.role.value, remember=True)

    @staticmethod
    async def get_user(data: LoginRequest, remember: bool) -> str:
        user = await User.get_or_none(email=data.email)
        
        invalid_auth_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

        if not user or not Authenticate.verify_password(data.password, user.hashed_password):
            raise invalid_auth_exception

        return AccessToken.generate(str(user.id), user.role.value, remember)

    @staticmethod
    async def get_by_id(user_id: str) -> User:
        user = await User.get_or_none(id=user_id)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
            )
        return user

    @staticmethod
    async def get_user_profile(token: str):
        token_data = AccessToken.decode(token)
        user_id = token_data.user_id

        user = await User.get_or_none(id=user_id)

        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
            )
        
        workouts = await Workout.filter(user_id=user.id).all()
        body_assessments = await BodyAssessment.filter(user_id=user.id).all()
        
        workout_list = [WorkoutRead.from_orm(w) for w in workouts]
        body_history = [BodyAssessmentBase.from_orm(b) for b in body_assessments]
        
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