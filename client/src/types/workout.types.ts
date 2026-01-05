export type ExerciseTypeEnum = 'strength' | 'cardio' | 'flexibility' | 'balance';

export type ExerciseCategoryEnum = 
  | 'chest' | 'back' | 'legs' | 'shoulders' | 'arms' 
  | 'abs' | 'cardio' | 'full_body' | 'other';

export type IntensityLevelEnum = 'low' | 'moderate' | 'high' | 'very_high';

export interface SetRequest {
  reps?: number;
  weight?: number;
  duration?: number; // em segundos
}

export interface ExerciseRequest {
  name: string;
  description?: string;
  exercise_type: ExerciseTypeEnum;
  category: ExerciseCategoryEnum;
  intensity: IntensityLevelEnum;
  sets: SetRequest[];
}

export interface WorkoutRequest {
  name: string;
  description?: string;
  exercises: ExerciseRequest[];
}