from tortoise import BaseDBAsyncClient

RUN_IN_TRANSACTION = True


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        CREATE TABLE IF NOT EXISTS "users" (
    "id" UUID NOT NULL PRIMARY KEY,
    "email" VARCHAR(255) NOT NULL UNIQUE,
    "name" VARCHAR(255) NOT NULL,
    "hashed_password" VARCHAR(255) NOT NULL,
    "birth_date" DATE NOT NULL,
    "role" VARCHAR(5) NOT NULL DEFAULT 'user',
    "height_cm" DOUBLE PRECISION NOT NULL DEFAULT 0,
    "goal" DOUBLE PRECISION,
    "gender" VARCHAR(6) NOT NULL,
    "activity_level" VARCHAR(17) NOT NULL,
    "activates_at" TIMESTAMPTZ,
    "created_at" TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "updated_at" TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP
);
COMMENT ON COLUMN "users"."role" IS 'USER: user\nADMIN: admin';
COMMENT ON COLUMN "users"."gender" IS 'MALE: male\nFEMALE: female';
COMMENT ON COLUMN "users"."activity_level" IS 'SEDENTARY: sedentary\nLIGHTLY_ACTIVE: lightly_active\nMODERATELY_ACTIVE: moderately_active\nVERY_ACTIVE: very_active\nEXTRA_ACTIVE: extra_active';
CREATE TABLE IF NOT EXISTS "workouts" (
    "id" UUID NOT NULL PRIMARY KEY,
    "name" VARCHAR(255) NOT NULL,
    "type" VARCHAR(11) NOT NULL,
    "total_calories_burned" DOUBLE PRECISION NOT NULL DEFAULT 0,
    "start_time" TIMESTAMPTZ NOT NULL,
    "end_time" TIMESTAMPTZ,
    "create_at" TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "user_id" UUID NOT NULL REFERENCES "users" ("id") ON DELETE CASCADE
);
COMMENT ON COLUMN "workouts"."type" IS 'CARDIO: cardio\nSTRENGTH: strength\nFLEXIBILITY: flexibility\nBALANCE: balance';
CREATE TABLE IF NOT EXISTS "exercises" (
    "id" UUID NOT NULL PRIMARY KEY,
    "name" VARCHAR(255) NOT NULL,
    "type" VARCHAR(9) NOT NULL,
    "intensity" VARCHAR(9) NOT NULL,
    "calories_burned" DOUBLE PRECISION NOT NULL DEFAULT 0,
    "created_at" TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "workout_id" UUID NOT NULL REFERENCES "workouts" ("id") ON DELETE CASCADE
);
COMMENT ON COLUMN "exercises"."type" IS 'BACK: back\nCHEST: chest\nLEGS: legs\nARMS: arms\nSHOULDERS: shoulders\nABDOMEN: abdomen';
COMMENT ON COLUMN "exercises"."intensity" IS 'LOW: low\nMEDIUM: medium\nHIGH: high\nVERY_HIGH: very_high';
CREATE TABLE IF NOT EXISTS "sets" (
    "id" UUID NOT NULL PRIMARY KEY,
    "reps" INT,
    "weight" DOUBLE PRECISION,
    "duration" INT,
    "calories_burned" DOUBLE PRECISION NOT NULL DEFAULT 0,
    "created_at" TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "exercise_id" UUID NOT NULL REFERENCES "exercises" ("id") ON DELETE CASCADE
);
CREATE TABLE IF NOT EXISTS "body_assessments" (
    "id" UUID NOT NULL PRIMARY KEY,
    "weight_kg" DOUBLE PRECISION NOT NULL,
    "height_cm" DOUBLE PRECISION NOT NULL,
    "waist_cm" DOUBLE PRECISION,
    "hip_cm" DOUBLE PRECISION,
    "chest_cm" DOUBLE PRECISION,
    "neck_cm" DOUBLE PRECISION,
    "arm_cm" DOUBLE PRECISION,
    "thigh_cm" DOUBLE PRECISION,
    "fold_chest" DOUBLE PRECISION,
    "fold_abdominal" DOUBLE PRECISION,
    "fold_thigh" DOUBLE PRECISION,
    "fold_triceps" DOUBLE PRECISION,
    "fold_subscapular" DOUBLE PRECISION,
    "fold_suprailiac" DOUBLE PRECISION,
    "fold_midaxillary" DOUBLE PRECISION,
    "bfp" DOUBLE PRECISION,
    "bmi" DOUBLE PRECISION,
    "bmr" DOUBLE PRECISION,
    "tdee" DOUBLE PRECISION,
    "lean_mass_kg" DOUBLE PRECISION,
    "fat_mass_kg" DOUBLE PRECISION,
    "created_at" TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "user_id" UUID NOT NULL REFERENCES "users" ("id") ON DELETE CASCADE
);
COMMENT ON COLUMN "body_assessments"."weight_kg" IS 'Peso total no dia da avaliação';
COMMENT ON COLUMN "body_assessments"."height_cm" IS 'Altura no momento (importante para crianças/jovens)';
CREATE TABLE IF NOT EXISTS "caloric_intakes" (
    "id" UUID NOT NULL PRIMARY KEY,
    "date" DATE NOT NULL,
    "calories_consumed" DOUBLE PRECISION NOT NULL DEFAULT 0,
    "protein_grams" DOUBLE PRECISION NOT NULL DEFAULT 0,
    "carbs_grams" DOUBLE PRECISION NOT NULL DEFAULT 0,
    "fats_grams" DOUBLE PRECISION NOT NULL DEFAULT 0,
    "created_at" TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "user_id" UUID NOT NULL REFERENCES "users" ("id") ON DELETE CASCADE
);
CREATE TABLE IF NOT EXISTS "aerich" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "version" VARCHAR(255) NOT NULL,
    "app" VARCHAR(100) NOT NULL,
    "content" JSONB NOT NULL
);"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        """


MODELS_STATE = (
    "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"
    "CyJiNVE="
)
