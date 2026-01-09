from src.core.calculations.body_metrics import BodyMetrics
from src.core.calculations.energy_expenditure import EnergyExpenditure
from datetime import datetime, timezone
from fastapi import HTTPException, status
from src.types.models.body_assessments import BodyAssessment
from src.types.schemas.body_assessment import BodyAssessmentCreate, BodyAssessmentReed
from typing import Optional
from tortoise.exceptions import DoesNotExist


class BodyAssessmentService:
    """Serviço para gerenciar avaliações corporais e cálculos de composição corporal"""
    
    @staticmethod
    def _calculate_body_fat_percentage(
        data: BodyAssessmentCreate,
    ) -> Optional[float]:
        """
        Calcula % de gordura corporal usando método Navy (circunferências).
        Requer: cintura, pescoço, altura. Para mulheres: + quadril.
        """
        # Verificar se temos as medidas mínimas necessárias
        if not data.neck_cm or not data.waist_cm:
            return None
        
        # Para mulheres, quadril é obrigatório no método Navy
        if data.user.gender.value == "female" and not data.hip_cm:
            return None
        
        try:
            bfp = BodyMetrics.calculate_body_fat_navy(
                sex=data.user.gender,
                waist_cm=data.waist_cm,
                neck_cm=data.neck_cm,
                height_cm=data.height_cm,
                hip_cm=data.hip_cm
            )
            return bfp
        except Exception as e:
            print(f"⚠️ Erro ao calcular BFP: {str(e)}")
            return None
    
    @staticmethod
    def _calculate_body_composition(
        weight_kg: float,
        bfp: Optional[float]
    ) -> tuple[Optional[float], Optional[float]]:
        """
        Calcula massa magra e massa gorda a partir do % de gordura.
        Retorna: (lean_mass_kg, fat_mass_kg)
        """
        if bfp is None:
            return None, None
        
        lean_mass = BodyMetrics.calculate_lean_mass(weight_kg, bfp)
        fat_mass = BodyMetrics.calculate_fat_mass(weight_kg, bfp)
        
        return lean_mass, fat_mass
    
    @staticmethod
    async def create_body_assessment(
        data: BodyAssessmentCreate
    ) -> BodyAssessmentReed:
        """
        Cria nova avaliação corporal com cálculos automáticos de:
        - IMC (Body Mass Index)
        - % Gordura (Body Fat Percentage) - se houver medidas
        - TMB (Taxa Metabólica Basal)
        - TDEE (Gasto Calórico Total Diário)
        - Massa Magra e Gorda
        """
        try:
            age = BodyMetrics.calculate_age(data.user.birth_date)
            bmi = BodyMetrics.calculate_bmi(data.weight_kg, data.height_cm)
            
            bfp = BodyAssessmentService._calculate_body_fat_percentage(data)
            lean_mass_kg, fat_mass_kg = BodyAssessmentService._calculate_body_composition(
                data.weight_kg, bfp
            )
            
            bmr = EnergyExpenditure.calculate_bmr(
                sex=data.user.gender,
                weight_kg=data.weight_kg,
                height_cm=data.height_cm,
                age=age
            )
            tdee = EnergyExpenditure.calculate_tdee(
                bmr=bmr,
                activity_level=data.user.activity_level
            )
            
            body_assessment = await BodyAssessment.create(
                user_id=data.user.id,
                # Medidas físicas
                weight_kg=data.weight_kg,
                height_cm=data.height_cm,
                waist_cm=data.waist_cm,
                hip_cm=data.hip_cm,
                chest_cm=data.chest_cm,
                neck_cm=data.neck_cm,
                arm_cm=data.arm_cm,
                thigh_cm=data.thigh_cm,
                # Dobras cutâneas
                fold_chest=data.fold_chest,
                fold_abdominal=data.fold_abdominal,
                fold_thigh=data.fold_thigh,
                fold_triceps=data.fold_triceps,
                fold_subscapular=data.fold_subscapular,
                fold_suprailiac=data.fold_suprailiac,
                fold_midaxillary=data.fold_midaxillary,
                # Resultados calculados
                bmi=bmi,
                bfp=bfp,
                bmr=bmr,
                tdee=tdee,
                lean_mass_kg=lean_mass_kg,
                fat_mass_kg=fat_mass_kg,
                created_at=datetime.now(timezone.utc),
            )
            
            return BodyAssessmentReed(
                id=body_assessment.id,
                bfp=body_assessment.bfp,
                bmi=body_assessment.bmi,
                bmr=body_assessment.bmr,
                tdee=body_assessment.tdee,
                lean_mass_kg=body_assessment.lean_mass_kg,
                fat_mass_kg=body_assessment.fat_mass_kg,
                created_at=body_assessment.created_at,
            )
            
        except ValueError as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Erro nos dados fornecidos: {str(e)}"
            )
        except Exception as e:
            print(f"❌ Erro ao criar avaliação corporal: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Erro ao criar avaliação corporal. Tente novamente."
            )

    @staticmethod
    async def get_body_assessment(
        assessment_id: str
    ) -> BodyAssessmentReed:
        """
        Recupera uma avaliação corporal pelo ID.
        """
        try:
            assessment = await BodyAssessment.get(id=assessment_id)
            return BodyAssessmentReed(
                id=assessment.id,
                bfp=assessment.bfp,
                bmi=assessment.bmi,
                bmr=assessment.bmr,
                tdee=assessment.tdee,
                lean_mass_kg=assessment.lean_mass_kg,
                fat_mass_kg=assessment.fat_mass_kg,
                created_at=assessment.created_at,
            )
        except DoesNotExist:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Avaliação corporal não encontrada."
            )
        except Exception as e:
            print(f"❌ Erro ao recuperar avaliação corporal: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Erro ao recuperar avaliação corporal. Tente novamente."
            )
        
    @staticmethod
    async def list_body_assessments_by_user(
        user_id: str
    ) -> list[BodyAssessmentReed]:
        """
        Lista todas as avaliações corporais de um usuário.
        """
        try:
            assessments = await BodyAssessment.filter(user_id=user_id).order_by('-created_at')
            return [
                BodyAssessmentReed(
                    id=assessment.id,
                    bfp=assessment.bfp,
                    bmi=assessment.bmi,
                    bmr=assessment.bmr,
                    tdee=assessment.tdee,
                    lean_mass_kg=assessment.lean_mass_kg,
                    fat_mass_kg=assessment.fat_mass_kg,
                    created_at=assessment.created_at,
                )
                for assessment in assessments
            ]
        except Exception as e:
            print(f"❌ Erro ao listar avaliações corporais: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Erro ao listar avaliações corporais. Tente novamente."
            )
        
    @staticmethod
    async def bmi_for_date(user_id: str) -> list[tuple[datetime, float]]:
        """
        Retorna lista de tuplas (data, IMC) para todas as avaliações de um usuário.
        """
        try:
            assessments = await BodyAssessment.filter(user_id=user_id).order_by('created_at')
            return [
                (assessment.created_at, assessment.bmi)
                for assessment in assessments
                if assessment.bmi is not None
            ]
        except Exception as e:
            print(f"❌ Erro ao recuperar dados de IMC: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Erro ao recuperar dados de IMC. Tente novamente."
            )
    
    @staticmethod
    async def bfp_for_date(user_id: str) -> list[tuple[datetime, float]]:
        """
        Retorna lista de tuplas (data, % Gordura) para todas as avaliações de um usuário.
        """
        try:
            assessments = await BodyAssessment.filter(user_id=user_id).order_by('created_at')
            return [
                (assessment.created_at, assessment.bfp)
                for assessment in assessments
                if assessment.bfp is not None
            ]
        except Exception as e:
            print(f"❌ Erro ao recuperar dados de % Gordura: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Erro ao recuperar dados de % Gordura. Tente novamente."
            )
    
    @staticmethod
    async def tdee_for_date(user_id: str) -> list[tuple[datetime, float]]:
        """
        Retorna lista de tuplas (data, TDEE) para todas as avaliações de um usuário.
        """
        try:
            assessments = await BodyAssessment.filter(user_id=user_id).order_by('created_at')
            return [
                (assessment.created_at, assessment.tdee)
                for assessment in assessments
                if assessment.tdee is not None
            ]
        except Exception as e:
            print(f"❌ Erro ao recuperar dados de TDEE: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Erro ao recuperar dados de TDEE. Tente novamente."
            )
    
    @staticmethod
    async def lean_mass_fat_mass_for_date(
        user_id: str
    ) -> list[tuple[datetime, float, float]]:
        """
        Retorna lista de tuplas (data, Massa Magra, Massa Gorda) para todas as avaliações de um usuário.
        """
        try:
            assessments = await BodyAssessment.filter(user_id=user_id).order_by('created_at')
            return [
                (assessment.created_at, assessment.lean_mass_kg, assessment.fat_mass_kg)
                for assessment in assessments
                if assessment.lean_mass_kg is not None and assessment.fat_mass_kg is not None
            ]
        except Exception as e:
            print(f"❌ Erro ao recuperar dados de Massa Magra/Gorda: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Erro ao recuperar dados de Massa Magra/Gorda. Tente novamente."
            )