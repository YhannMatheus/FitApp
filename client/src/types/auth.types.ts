// Enums baseados na seção "Enumerações" da sua doc
export type SexEnum = 'male' | 'female';

export type ActivityLevelEnum = 
  | 'sedentary' 
  | 'lightly_active' 
  | 'moderately_active' 
  | 'very_active' 
  | 'extremely_active';

// Interface para o POST /auth/register
export interface RegisterRequest {
  name: string;             // min: 3, max: 120
  email: string;            // email válido
  password: string;         // min: 8 caracteres
  sex: SexEnum;
  birth_date: string;       // Formato YYYY-MM-DD
  height_cm: number;        // float > 0
  weight_kg: number;        // float > 0
  activity_level: ActivityLevelEnum;
}

// Interface para a resposta do usuário (GET /users/me)
export interface UserResponse {
  id: number;
  name: string;
  email: string;
  sex: SexEnum;
  birth_date: string;
  height: number;
  weight: number;
  activity_level: string;
}