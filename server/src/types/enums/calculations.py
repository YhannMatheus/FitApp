from enum import Enum


class BMRFormulaEnum(str, Enum):
    HARRIS_BENEDICT = "harris_benedict"
    MIFFLIN_ST_JEOR = "mifflin_st_jeor"


class BodyFatFormulaEnum(str, Enum):
    NAVY = "navy"
    THREE_SKINFOLDS = "three_skinfolds"
    SEVEN_SKINFOLDS = "seven_skinfolds"
