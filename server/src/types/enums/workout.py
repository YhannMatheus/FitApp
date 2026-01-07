"""Enums relacionados a treinos"""

from enum import Enum


class TrainingTypeEnum(str, Enum):
    """Tipo de treino/workout"""
    CARDIO = "cardio"
    STRENGTH = "strength"
    FLEXIBILITY = "flexibility"
    BALANCE = "balance"
