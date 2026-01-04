# Documentação da API - KiloCal

## Índice
- [Autenticação](#autenticação)
- [Usuários](#usuários)
- [Treinos (Workouts)](#treinos-workouts)
- [Exercícios](#exercícios)
- [Séries (Sets)](#séries-sets)
- [Modelos de Dados](#modelos-de-dados)
- [Enumerações](#enumerações)

---

## Autenticação

### POST `/auth/register`
Registra um novo usuário no sistema.

**Headers:**
- Content-Type: `application/json`

**Body:**
```json
{
  "name": "string (min: 3, max: 120)",
  "email": "string (email válido)",
  "password": "string (min: 8 caracteres)",
  "sex": "male | female",
  "birth_date": "YYYY-MM-DD",
  "height_cm": "float (maior que 0)",
  "weight_kg": "float (maior que 0)",
  "activity_level": "sedentary | lightly_active | moderately_active | very_active | extremely_active"
}
```

**Resposta (200):**
```json
{
  "id": "integer",
  "name": "string",
  "email": "string",
  "sex": "male | female",
  "birth_date": "YYYY-MM-DD",
  "height": "float",
  "weight": "float",
  "activity_level": "string"
}
```

---

### POST `/auth/login`
Realiza login e retorna um token de acesso.

**Headers:**
- Content-Type: `application/json`

**Body:**
```json
{
  "email": "string (email válido)",
  "password": "string"
}
```

**Resposta (200):**
```json
{
  "access_token": "string (JWT token)",
  "token_type": "bearer"
}
```

---

## Usuários

### GET `/users/me`
Retorna os dados do usuário autenticado.

**Headers:**
- Authorization: `Bearer {access_token}`

**Resposta (200):**
```json
{
  "id": "integer",
  "name": "string",
  "email": "string",
  "sex": "male | female",
  "birth_date": "YYYY-MM-DD",
  "height": "float",
  "weight": "float",
  "activity_level": "string"
}
```

---

## Treinos (Workouts)

### POST `/workouts/`
Cria um novo treino com seus exercícios e séries.

**Headers:**
- Authorization: `Bearer {access_token}`
- Content-Type: `application/json`

**Body:**
```json
{
  "name": "string (min: 1, max: 100)",
  "description": "string (opcional, max: 500)",
  "exercises": [
    {
      "name": "string (min: 1, max: 100)",
      "description": "string (opcional, max: 500)",
      "exercise_type": "strength | cardio | flexibility | balance",
      "category": "chest | back | legs | shoulders | arms | abs | cardio | full_body | other",
      "intensity": "low | moderate | high | very_high",
      "sets": [
        {
          "reps": "integer (opcional, >= 1)",
          "weight": "float (opcional, >= 0)",
          "duration": "integer (opcional, >= 1, em segundos)"
        }
      ]
    }
  ]
}
```

**Resposta (200):**
```json
{
  "id": "UUID",
  "user_id": "UUID",
  "name": "string",
  "description": "string | null",
  "calories_burned": "float",
  "exercises": [
    {
      "id": "UUID",
      "workout_id": "UUID",
      "name": "string",
      "description": "string | null",
      "exercise_type": "string",
      "category": "string",
      "intensity": "string",
      "sets": [
        {
          "id": "UUID",
          "exercise_id": "UUID",
          "reps": "integer | null",
          "weight": "float | null",
          "duration": "integer | null",
          "created_at": "datetime"
        }
      ],
      "created_at": "datetime",
      "updated_at": "datetime | null"
    }
  ],
  "created_at": "datetime",
  "updated_at": "datetime | null"
}
```

---

## Exercícios

### POST `/exercises/workouts/{workout_id}/exercises`
Adiciona um novo exercício a um treino existente.

**Headers:**
- Authorization: `Bearer {access_token}`
- Content-Type: `application/json`

**Parâmetros de URL:**
- `workout_id`: UUID do treino

**Body:**
```json
{
  "name": "string (min: 1, max: 100)",
  "description": "string (opcional, max: 500)",
  "exercise_type": "strength | cardio | flexibility | balance",
  "category": "chest | back | legs | shoulders | arms | abs | cardio | full_body | other",
  "intensity": "low | moderate | high | very_high",
  "sets": [
    {
      "reps": "integer (opcional, >= 1)",
      "weight": "float (opcional, >= 0)",
      "duration": "integer (opcional, >= 1, em segundos)"
    }
  ]
}
```

**Resposta (200):**
```json
{
  "id": "UUID",
  "workout_id": "UUID",
  "name": "string",
  "description": "string | null",
  "exercise_type": "string",
  "category": "string",
  "intensity": "string",
  "sets": [
    {
      "id": "UUID",
      "exercise_id": "UUID",
      "reps": "integer | null",
      "weight": "float | null",
      "duration": "integer | null",
      "created_at": "datetime"
    }
  ],
  "created_at": "datetime",
  "updated_at": "datetime | null"
}
```

---

## Séries (Sets)

### POST `/sets/exercises/{exercise_id}/sets`
Adiciona uma nova série a um exercício existente.

**Headers:**
- Authorization: `Bearer {access_token}`
- Content-Type: `application/json`

**Parâmetros de URL:**
- `exercise_id`: UUID do exercício

**Body:**
```json
{
  "reps": "integer (opcional, >= 1)",
  "weight": "float (opcional, >= 0)",
  "duration": "integer (opcional, >= 1, em segundos)"
}
```

**Resposta (200):**
```json
{
  "id": "UUID",
  "exercise_id": "UUID",
  "reps": "integer | null",
  "weight": "float | null",
  "duration": "integer | null",
  "created_at": "datetime"
}
```

---

## Modelos de Dados

### Usuário (User)
```json
{
  "id": "integer",
  "name": "string",
  "email": "string",
  "sex": "male | female",
  "birth_date": "date",
  "height": "float (em cm)",
  "weight": "float (em kg)",
  "activity_level": "string"
}
```

### Treino (Workout)
```json
{
  "id": "UUID",
  "user_id": "UUID",
  "name": "string",
  "description": "string | null",
  "calories_burned": "float (calculado automaticamente)",
  "exercises": "array de exercícios",
  "created_at": "datetime",
  "updated_at": "datetime | null"
}
```

### Exercício (Exercise)
```json
{
  "id": "UUID",
  "workout_id": "UUID",
  "name": "string",
  "description": "string | null",
  "exercise_type": "ExerciseTypeEnum",
  "category": "ExerciseCategoryEnum",
  "intensity": "IntensityLevelEnum",
  "sets": "array de séries",
  "created_at": "datetime",
  "updated_at": "datetime | null"
}
```

### Série (Set)
```json
{
  "id": "UUID",
  "exercise_id": "UUID",
  "reps": "integer | null (repetições)",
  "weight": "float | null (peso em kg)",
  "duration": "integer | null (duração em segundos)",
  "created_at": "datetime"
}
```

---

## Enumerações

### SexEnum
- `male`: Masculino
- `female`: Feminino

### ActivityLevelEnum
- `sedentary`: Sedentário (pouco ou nenhum exercício)
- `lightly_active`: Levemente ativo (exercício leve 1-3 dias/semana)
- `moderately_active`: Moderadamente ativo (exercício moderado 3-5 dias/semana)
- `very_active`: Muito ativo (exercício intenso 6-7 dias/semana)
- `extremely_active`: Extremamente ativo (exercício muito intenso, atleta)

### ExerciseTypeEnum
- `strength`: Força/Musculação
- `cardio`: Cardio/Aeróbico
- `flexibility`: Flexibilidade
- `balance`: Equilíbrio

### ExerciseCategoryEnum
- `chest`: Peito
- `back`: Costas
- `legs`: Pernas
- `shoulders`: Ombros
- `arms`: Braços
- `abs`: Abdômen
- `cardio`: Cardio
- `full_body`: Corpo inteiro
- `other`: Outros

### IntensityLevelEnum
- `low`: Baixa intensidade
- `moderate`: Intensidade moderada
- `high`: Alta intensidade
- `very_high`: Intensidade muito alta

---

## Códigos de Resposta HTTP

- **200 OK**: Requisição bem-sucedida
- **201 Created**: Recurso criado com sucesso
- **400 Bad Request**: Dados inválidos na requisição
- **401 Unauthorized**: Token de autenticação inválido ou ausente
- **403 Forbidden**: Acesso negado ao recurso
- **404 Not Found**: Recurso não encontrado
- **422 Unprocessable Entity**: Erro de validação dos dados
- **500 Internal Server Error**: Erro interno do servidor

---

## Observações Importantes

1. **Autenticação**: Todas as rotas exceto `/auth/register` e `/auth/login` requerem um token de autenticação no header `Authorization: Bearer {token}`.

2. **Cálculo de Calorias**: As calorias queimadas são calculadas automaticamente pelo sistema baseando-se no tipo de exercício, intensidade, duração e peso do usuário.

3. **Séries**: Cada série pode ter:
   - `reps` (repetições): usado principalmente para exercícios de força
   - `weight` (peso): usado para exercícios com carga
   - `duration` (duração): usado principalmente para exercícios de cardio

4. **UUIDs**: Todos os IDs de workout, exercise e set são UUID v4.

5. **Datas**: As datas são retornadas no formato ISO 8601 (ex: `2026-01-03T10:30:00Z`).
