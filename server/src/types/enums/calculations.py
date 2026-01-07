"""Enums relacionados a cálculos e métricas corporais"""

from enum import Enum


class ResistanceTypeEnum(str, Enum):
    """Tipo de resistência utilizada no exercício"""
    BODYWEIGHT = "bodyweight"
    FREE_WEIGHTS = "free_weights"
    MACHINES = "machines"
    BANDS = "bands"


class BodyFatFormulaEnum(str, Enum):
    """Fórmulas para cálculo de gordura corporal"""
    NAVY = "Navy"
    NORMAL = "Normal"


class BMRFormulaEnum(str, Enum):
    """Fórmulas para cálculo de Taxa Metabólica Basal"""
    HARRIS_BENEDICT = "harris_benedict"
    MIFFLIN_ST_JEOR = "mifflin_st_jeor"
    KATCH_MCARDLE = "katch_mcardle"
