# Esquema do Banco de Dados - KiloCal

## Diagrama de Relacionamentos (ERD)

```
┌─────────────────────────────────────────┐
│             USERS                       │
├─────────────────────────────────────────┤
│ PK  id                 INTEGER          │
│     email              VARCHAR(255) 🔑  │
│     hashed_password    VARCHAR          │
│     is_active          BOOLEAN          │
│     birth_date         DATE             │
│     height_cm          FLOAT            │
│     sex                ENUM             │
│     activity_level     ENUM             │
│     goal               VARCHAR          │
│     created_at         DATETIME         │
└─────────────────────────────────────────┘
           │
           │ 1:N
           ├──────────────────────────────────────┐
           │                                      │
           ▼                                      ▼
┌─────────────────────────────────────────┐ ┌─────────────────────────────────────────┐
│         WORKOUTS                        │ │       BODY_ASSESSMENTS                  │
├─────────────────────────────────────────┤ ├─────────────────────────────────────────┤
│ PK  id                    INTEGER       │ │ PK  id                   INTEGER        │
│ FK  user_id               INTEGER       │ │ FK  user_id              INTEGER        │
│     name                  VARCHAR(80)   │ │     date                 DATE            │
│     total_calories_burned FLOAT         │ │     weight_kg            FLOAT           │
│     created_at            DATETIME      │ │     waist_cm             FLOAT           │
└─────────────────────────────────────────┘ │     hip_cm               FLOAT           │
           │                                 │     chest_cm             FLOAT           │
           │ 1:N                             │     arm_cm               FLOAT           │
           │                                 │     thigh_cm             FLOAT           │
           ▼                                 │     calf_cm              FLOAT           │
┌─────────────────────────────────────────┐ │     body_fat_percent     FLOAT           │
│         EXERCISES                       │ │     lean_mass_kg         FLOAT           │
├─────────────────────────────────────────┤ │     bmi                  FLOAT           │
│ PK  id                  INTEGER         │ │     bmr                  FLOAT           │
│ FK  workout_id          INTEGER         │ │     tdee                 FLOAT           │
│     name                VARCHAR(80)     │ └─────────────────────────────────────────┘
│     description         VARCHAR(500)    │
│     exercise_type       ENUM            │
│     category            ENUM            │
│     intensity           ENUM            │ ┌─────────────────────────────────────────┐
│     calories_burned     FLOAT           │ │       CALORIC_INTAKES                   │
│     created_at          DATETIME        │ ├─────────────────────────────────────────┤
│     updated_at          DATETIME        │ │ PK  id                   INTEGER        │
└─────────────────────────────────────────┘ │ FK  user_id              INTEGER        │
           │                                 │     calories             FLOAT           │
           │ 1:N                             │     protein_g            FLOAT           │
           │                                 │     carbs_g              FLOAT           │
           ▼                                 │     fat_g                FLOAT           │
┌─────────────────────────────────────────┐ │     created_at           DATETIME        │
│             SETS                        │ └─────────────────────────────────────────┘
├─────────────────────────────────────────┤          ▲
│ PK  id                INTEGER           │          │
│ FK  exercise_id       INTEGER           │          │ 1:N
│     reps              INTEGER           │          │
│     weight            FLOAT             │          │
│     duration          INTEGER           │ ┌────────┘
│     calories_burned   FLOAT             │
│     created_at        DATETIME          │
└─────────────────────────────────────────┘
```

---

## Tabelas Detalhadas

### 🧑 **users** (Usuários)
Armazena informações dos usuários cadastrados na aplicação.

| Campo             | Tipo          | Descrição                                      | Constraints        |
|-------------------|---------------|------------------------------------------------|--------------------|
| `id`              | INTEGER       | Identificador único do usuário                 | PRIMARY KEY        |
| `email`           | VARCHAR(255)  | Email do usuário                               | UNIQUE, INDEX      |
| `hashed_password` | VARCHAR       | Senha criptografada                            | NOT NULL           |
| `is_active`       | BOOLEAN       | Status de ativação do usuário                  | DEFAULT TRUE       |
| `birth_date`      | DATE          | Data de nascimento                             | NOT NULL           |
| `height_cm`       | FLOAT         | Altura em centímetros                          | NOT NULL           |
| `sex`             | ENUM          | Sexo: `male`, `female`                         | NOT NULL           |
| `activity_level`  | ENUM          | Nível de atividade física                      | NOT NULL           |
| `goal`            | VARCHAR       | Objetivo do usuário                            | NOT NULL           |
| `created_at`      | DATETIME      | Data de criação do registro                    | DEFAULT NOW()      |

**Relacionamentos:**
- 1:N com `workouts` (um usuário tem vários treinos)
- 1:N com `body_assessments` (um usuário tem várias avaliações)
- 1:N com `caloric_intakes` (um usuário tem vários registros calóricos)

**Enums:**
- `SexEnum`: `male`, `female`
- `ActivityLevelEnum`: `sedentary`, `light`, `moderate`, `high`, `athlete`

---

### 🏋️ **workouts** (Treinos)
Armazena os treinos criados pelos usuários.

| Campo                     | Tipo         | Descrição                              | Constraints        |
|---------------------------|--------------|----------------------------------------|--------------------|
| `id`                      | INTEGER      | Identificador único do treino          | PRIMARY KEY        |
| `user_id`                 | INTEGER      | Referência ao usuário                  | FOREIGN KEY, CASCADE DELETE |
| `name`                    | VARCHAR(80)  | Nome do treino                         | NOT NULL           |
| `total_calories_burned`   | FLOAT        | Total de calorias queimadas            | NULLABLE           |
| `created_at`              | DATETIME     | Data de criação do treino              | DEFAULT NOW()      |

**Relacionamentos:**
- N:1 com `users` (vários treinos pertencem a um usuário)
- 1:N com `exercises` (um treino tem vários exercícios)

**Cascade:** Ao deletar um usuário, todos os seus treinos são deletados.

---

### 💪 **exercises** (Exercícios)
Armazena os exercícios dentro de cada treino.

| Campo               | Tipo          | Descrição                                    | Constraints        |
|---------------------|---------------|----------------------------------------------|--------------------|
| `id`                | INTEGER       | Identificador único do exercício             | PRIMARY KEY        |
| `workout_id`        | INTEGER       | Referência ao treino                         | FOREIGN KEY, CASCADE DELETE |
| `name`              | VARCHAR(80)   | Nome do exercício                            | NOT NULL           |
| `description`       | VARCHAR(500)  | Descrição detalhada do exercício             | NULLABLE           |
| `exercise_type`     | ENUM          | Tipo de exercício                            | NOT NULL           |
| `category`          | ENUM          | Categoria do exercício                       | NOT NULL           |
| `intensity`         | ENUM          | Intensidade do exercício                     | NOT NULL           |
| `calories_burned`   | FLOAT         | Calorias queimadas no exercício              | NULLABLE           |
| `created_at`        | DATETIME      | Data de criação                              | DEFAULT NOW()      |
| `updated_at`        | DATETIME      | Data da última atualização                   | ON UPDATE NOW()    |

**Relacionamentos:**
- N:1 com `workouts` (vários exercícios pertencem a um treino)
- 1:N com `sets` (um exercício tem várias séries)

**Enums:**
- `ExerciseTypeEnum`: `strength`, `cardio`, `flexibility`, `balance`
- `ExerciseCategoryEnum`: `chest`, `back`, `legs`, `shoulders`, `arms`, `abs`, `cardio`, `full_body`, `other`
- `IntensityLevelEnum`: `low`, `moderate`, `high`, `very_high`

**Cascade:** Ao deletar um treino, todos os seus exercícios são deletados.

---

### 🔢 **sets** (Séries)
Armazena as séries/repetições de cada exercício.

| Campo               | Tipo      | Descrição                                    | Constraints        |
|---------------------|-----------|----------------------------------------------|--------------------|
| `id`                | INTEGER   | Identificador único da série                 | PRIMARY KEY        |
| `exercise_id`       | INTEGER   | Referência ao exercício                      | FOREIGN KEY, CASCADE DELETE |
| `reps`              | INTEGER   | Número de repetições                         | NULLABLE           |
| `weight`            | FLOAT     | Peso utilizado (em kg)                       | NULLABLE           |
| `duration`          | INTEGER   | Duração (em segundos)                        | NULLABLE           |
| `calories_burned`   | FLOAT     | Calorias queimadas na série                  | NULLABLE           |
| `created_at`        | DATETIME  | Data de criação da série                     | DEFAULT NOW()      |

**Relacionamentos:**
- N:1 com `exercises` (várias séries pertencem a um exercício)

**Observações:**
- Para exercícios de força: use `reps` e `weight`
- Para exercícios de cardio: use `duration`
- Campos podem ser nulos para flexibilidade

**Cascade:** Ao deletar um exercício, todas as suas séries são deletadas.

---

### 📊 **body_assessments** (Avaliações Corporais)
Armazena avaliações físicas e medidas corporais do usuário ao longo do tempo.

| Campo                | Tipo      | Descrição                              | Constraints        |
|----------------------|-----------|----------------------------------------|--------------------|
| `id`                 | INTEGER   | Identificador único da avaliação       | PRIMARY KEY        |
| `user_id`            | INTEGER   | Referência ao usuário                  | FOREIGN KEY, CASCADE DELETE |
| `date`               | DATE      | Data da avaliação                      | NOT NULL           |
| `weight_kg`          | FLOAT     | Peso em quilogramas                    | NOT NULL           |
| `waist_cm`           | FLOAT     | Circunferência da cintura (cm)         | NULLABLE           |
| `hip_cm`             | FLOAT     | Circunferência do quadril (cm)         | NULLABLE           |
| `chest_cm`           | FLOAT     | Circunferência do peito (cm)           | NULLABLE           |
| `arm_cm`             | FLOAT     | Circunferência do braço (cm)           | NULLABLE           |
| `thigh_cm`           | FLOAT     | Circunferência da coxa (cm)            | NULLABLE           |
| `calf_cm`            | FLOAT     | Circunferência da panturrilha (cm)     | NULLABLE           |
| `body_fat_percent`   | FLOAT     | Percentual de gordura corporal (%)     | NULLABLE           |
| `lean_mass_kg`       | FLOAT     | Massa magra (kg)                       | NULLABLE           |
| `bmi`                | FLOAT     | Índice de Massa Corporal               | NULLABLE           |
| `bmr`                | FLOAT     | Taxa Metabólica Basal (kcal/dia)       | NULLABLE           |
| `tdee`               | FLOAT     | Gasto Energético Total Diário (kcal)   | NULLABLE           |

**Relacionamentos:**
- N:1 com `users` (várias avaliações pertencem a um usuário)

**Cascade:** Ao deletar um usuário, todas as suas avaliações são deletadas.

---

### 🍽️ **caloric_intakes** (Ingestão Calórica)
Registra a ingestão calórica e macronutrientes do usuário.

| Campo         | Tipo      | Descrição                              | Constraints        |
|---------------|-----------|----------------------------------------|--------------------|
| `id`          | INTEGER   | Identificador único do registro        | PRIMARY KEY        |
| `user_id`     | INTEGER   | Referência ao usuário                  | FOREIGN KEY, CASCADE DELETE |
| `calories`    | FLOAT     | Total de calorias ingeridas            | NOT NULL           |
| `protein_g`   | FLOAT     | Proteínas em gramas                    | NULLABLE           |
| `carbs_g`     | FLOAT     | Carboidratos em gramas                 | NULLABLE           |
| `fat_g`       | FLOAT     | Gorduras em gramas                     | NULLABLE           |
| `created_at`  | DATETIME  | Data e hora do registro                | DEFAULT NOW()      |

**Relacionamentos:**
- N:1 com `users` (vários registros pertencem a um usuário)

**Cascade:** Ao deletar um usuário, todos os seus registros calóricos são deletados.

---

## Fluxo de Dados

### 1. Criação de Treino Completo
```
1. Usuário cria um Workout
   ├─ Workout é salvo com user_id
   │
2. Sistema cria Exercises dentro do Workout
   ├─ Cada Exercise é salvo com workout_id
   │
3. Sistema cria Sets para cada Exercise
   ├─ Cada Set é salvo com exercise_id
   │
4. Sistema calcula calorias
   ├─ Calorias dos Sets → agregadas no Exercise
   ├─ Calorias dos Exercises → agregadas no Workout
   │
5. Workout finalizado com total_calories_burned calculado
```

### 2. Avaliação Corporal
```
1. Usuário registra medidas corporais
   ├─ body_assessment é criado com user_id
   │
2. Sistema calcula métricas
   ├─ BMI = peso / (altura²)
   ├─ BMR calculado pela fórmula de Harris-Benedict
   ├─ TDEE = BMR × fator de atividade
   │
3. Métricas são salvas no registro
```

### 3. Registro de Alimentação
```
1. Usuário registra refeição
   ├─ caloric_intake é criado com user_id
   │
2. Sistema armazena macros
   ├─ Calorias totais
   ├─ Proteínas, Carboidratos, Gorduras
   │
3. Registro salvo com timestamp
```

---

## Índices e Performance

### Índices Criados:
- `users.email` - INDEX UNIQUE (para login rápido)
- `workouts.user_id` - INDEX (foreign key)
- `exercises.workout_id` - INDEX (foreign key)
- `sets.exercise_id` - INDEX (foreign key)
- `body_assessments.user_id` - INDEX (foreign key)
- `caloric_intakes.user_id` - INDEX (foreign key)

### Otimizações:
- **Cascade Delete**: Ao deletar um usuário, todos os dados relacionados são deletados automaticamente
- **Soft Delete**: Campo `is_active` em users permite desativação sem perda de dados
- **Timestamps**: Todos os registros principais têm `created_at` para auditoria
- **Update Tracking**: Exercises têm `updated_at` para rastrear modificações

---

## Cálculos Automáticos

### Calorias Queimadas:
O sistema calcula automaticamente as calorias em cada nível:

1. **Set Level**: Com base em reps, weight, duration, tipo de exercício e peso do usuário
2. **Exercise Level**: Soma das calorias de todos os sets
3. **Workout Level**: Soma das calorias de todos os exercícios

### Fórmulas Implementadas:
- **BMI**: `peso_kg / (altura_m²)`
- **BMR**: Fórmula de Harris-Benedict (considera sexo, idade, peso, altura)
- **TDEE**: `BMR × fator_atividade`
- **Calorias de Treino**: MET (Metabolic Equivalent) × peso × tempo

---

## Regras de Negócio

### Validações:
- Email deve ser único
- Usuário deve ter pelo menos 18 anos (validado no backend)
- Altura e peso devem ser valores positivos
- Séries devem ter pelo menos um dos campos: reps, weight ou duration
- Datas futuras não são permitidas em body_assessments

### Constraints:
- `ON DELETE CASCADE`: Garante integridade referencial
- `UNIQUE`: Previne duplicação de emails
- `NOT NULL`: Campos obrigatórios garantidos
- `DEFAULT`: Valores padrão para campos opcionais

---

## Migrações (Alembic)

O projeto usa Alembic para gerenciar migrações do banco de dados.

**Arquivo de migração principal:**
- `alembic/versions/66e890e7ea00_criação_das_tabelas.py`

**Comandos úteis:**
```bash
# Criar nova migração
alembic revision --autogenerate -m "descrição"

# Aplicar migrações
alembic upgrade head

# Reverter migração
alembic downgrade -1

# Ver histórico
alembic history
```

---

## Observações Técnicas

- **ORM**: SQLAlchemy com suporte assíncrono (AsyncSession)
- **Driver**: asyncpg para PostgreSQL
- **Tipos**: Type hints completos com Mapped[]
- **Lazy Loading**: Relacionamentos carregados sob demanda
- **Eager Loading**: Use `selectinload()` para otimizar queries com relacionamentos
