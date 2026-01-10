# 📚 **KiloCal API - Documentação Completa do Backend**

> **Versão:** 1.0.0  
> **Última Atualização:** 10 de Janeiro de 2026  
> **Base URL (Produção):** `https://kilocal-8fy9.onrender.com`  
> **Base URL (Desenvolvimento):** `http://localhost:8000`

---

## 📑 **Índice**

1. [Visão Geral](#visão-geral)
2. [Arquitetura do Sistema](#arquitetura-do-sistema)
3. [Stack Tecnológica](#stack-tecnológica)
4. [Configuração e Variáveis de Ambiente](#configuração-e-variáveis-de-ambiente)
5. [Banco de Dados](#banco-de-dados)
6. [Autenticação e Segurança](#autenticação-e-segurança)
7. [Middlewares](#middlewares)
8. [Endpoints da API](#endpoints-da-api)
9. [Modelos de Dados](#modelos-de-dados)
10. [Schemas e Validações](#schemas-e-validações)
11. [Services (Lógica de Negócio)](#services-lógica-de-negócio)
12. [Cálculos e Fórmulas](#cálculos-e-fórmulas)
13. [Tratamento de Erros](#tratamento-de-erros)
14. [Testes](#testes)
15. [Deploy e Produção](#deploy-e-produção)

---

## 🎯 **Visão Geral**

A **KiloCal API** é uma API RESTful desenvolvida para acompanhamento de treinos, cálculo de calorias e análise de composição corporal. O sistema permite que usuários:

- Registrem-se e façam login com autenticação JWT
- Criem avaliações corporais com cálculos automáticos (IMC, % gordura, TMB, TDEE)
- Acompanhem a evolução de métricas corporais ao longo do tempo
- Gerenciem treinos e exercícios (em desenvolvimento)

### **Principais Funcionalidades:**
- ✅ Sistema de autenticação JWT com refresh token
- ✅ Avaliações corporais com cálculos automáticos
- ✅ Middleware de autenticação global
- ✅ Suporte a múltiplas fórmulas de cálculo (Mifflin-St Jeor, Harris-Benedict, Navy Method)
- ✅ CORS configurado para web e mobile
- ✅ Banco de dados PostgreSQL em desenvolvimento e produção
- 🚧 Sistema de treinos e exercícios (em desenvolvimento)

---

## 🏗️ **Arquitetura do Sistema**

### **Estrutura de Pastas:**

```
server/
├── src/
│   ├── main.py                         # Ponto de entrada da aplicação
│   ├── core/                           # Núcleo do sistema
│   │   ├── auth/                       # Autenticação e segurança
│   │   │   ├── security.py             # Hash de senhas (bcrypt)
│   │   │   └── token.py                # Geração/validação JWT
│   │   ├── calculations/               # Fórmulas e cálculos
│   │   │   ├── body_metrics.py         # IMC, % gordura, massa magra/gorda
│   │   │   ├── energy_expenditure.py   # TMB, TDEE
│   │   │   ├── workout_calories.py     # Calorias de treino
│   │   │   └── biopedance.py           # Bioimpedância
│   │   ├── database/                   # Configuração do banco
│   │   │   ├── connection.py           # Conexão Tortoise ORM
│   │   │   ├── db_config.py            # Configuração do banco
│   │   │   └── seed_database.py        # Dados iniciais
│   │   ├── middlewares/                # Middlewares customizados
│   │   │   └── auth_middleware.py      # Middleware de autenticação
│   │   └── config.py                   # Configurações globais
│   ├── routes/                         # Endpoints da API
│   │   ├── user.py                     # Rotas de usuário (login/register)
│   │   └── body_assessment.py          # Rotas de avaliação corporal
│   ├── services/                       # Lógica de negócio
│   │   ├── user_services.py            # Serviços de usuário
│   │   ├── body_assessment_service.py  # Serviços de avaliação corporal
│   │   ├── session_services.py         # Gerenciamento de sessões
│   │   ├── workout_service.py          # Serviços de treino
│   │   ├── exercise_service.py         # Serviços de exercício
│   │   └── set_service.py              # Serviços de séries
│   └── types/                          # Tipos e modelos
│       ├── models/                     # Modelos Tortoise ORM
│       │   ├── user.py                 # Modelo User
│       │   ├── body_assessments.py     # Modelo BodyAssessment
│       │   ├── workout.py              # Modelo Workout
│       │   ├── exercise.py             # Modelo Exercise
│       │   ├── session.py              # Modelo Session
│       │   ├── sets.py                 # Modelo Set
│       │   └── caloric_intakes.py      # Modelo CaloricIntake
│       ├── schemas/                    # Schemas Pydantic
│       │   ├── auth.py                 # Schemas de autenticação
│       │   ├── user.py                 # Schemas de usuário
│       │   ├── body_assessment.py      # Schemas de avaliação corporal
│       │   ├── workout.py              # Schemas de treino
│       │   ├── exercise.py             # Schemas de exercício
│       │   ├── session.py              # Schemas de sessão
│       │   └── set.py                  # Schemas de série
│       └── enums/                      # Enumerações
│           ├── user.py                 # Enums de usuário
│           ├── workout.py              # Enums de treino
│           ├── exercise.py             # Enums de exercício
│           └── calculations.py         # Enums de cálculos
├── migrations/                         # Migrações do banco
│   └── models/
│       ├── 0_20260105000058_init.py
│       └── 1_20260109160251_update.py
├── tests/                              # Testes
│   └── user/
│       ├── login.py
│       └── register.py
├── docs/                               # Documentação
│   ├── API_DOCUMENTATION.md
│   ├── DATABASE_SCHEMA.md
│   └── CALCULATIONS_REFERENCE.md
├── .env                                # Variáveis de ambiente (gitignored)
├── .env.example                        # Template de variáveis
├── requirements.txt                    # Dependências Python
├── pyproject.toml                      # Configuração do projeto
└── pytest.ini                          # Configuração de testes
```

### **Padrão Arquitetural:**

O projeto segue uma arquitetura em **camadas**:

```
┌─────────────────────────────────────────────────────────┐
│  Cliente (Web/Mobile)                                   │
└─────────────────────────────────────────────────────────┘
                        ↓ HTTP Request
┌─────────────────────────────────────────────────────────┐
│  MIDDLEWARES (CORS, Auth)                               │
└─────────────────────────────────────────────────────────┘
                        ↓
┌─────────────────────────────────────────────────────────┐
│  ROUTES (Endpoints)                                     │
│  - Validação de entrada                                 │
│  - Extração de token                                    │
└─────────────────────────────────────────────────────────┘
                        ↓
┌─────────────────────────────────────────────────────────┐
│  SERVICES (Lógica de Negócio)                           │
│  - Validações complexas                                 │
│  - Cálculos automáticos                                 │
│  - Orquestração de operações                            │
└─────────────────────────────────────────────────────────┘
                        ↓
┌─────────────────────────────────────────────────────────┐
│  MODELS (ORM - Tortoise)                                │
│  - Interação com banco de dados                         │
│  - Queries e relacionamentos                            │
└─────────────────────────────────────────────────────────┘
                        ↓
┌─────────────────────────────────────────────────────────┐
│  DATABASE (PostgreSQL)                                  │
└─────────────────────────────────────────────────────────┘
```

---

## 🛠️ **Stack Tecnológica**

### **Framework e Linguagem:**
- **Python 3.11+**
- **FastAPI 0.128.0** - Framework web moderno e rápido
- **Uvicorn 0.40.0** - Servidor ASGI

### **Banco de Dados:**
- **PostgreSQL** (Desenvolvimento e Produção)
- **Tortoise ORM 0.25.3** - ORM assíncrono
- **Aerich 0.9.2** - Ferramenta de migração

### **Autenticação e Segurança:**
- **Python-Jose 3.5.0** - JWT (JSON Web Tokens)
- **Passlib 1.7.4** - Hash de senhas
- **Bcrypt 4.2.1** - Algoritmo de hash
- **Cryptography 46.0.3** - Criptografia

### **Validação e Serialização:**
- **Pydantic 2.12.5** - Validação de dados
- **Pydantic-Settings 2.12.0** - Configurações via .env
- **Email-Validator 2.3.0** - Validação de emails

### **Testes:**
- **Pytest 9.0.2** - Framework de testes
- **Pytest-Asyncio 1.3.0** - Testes assíncronos
- **HTTPx 0.28.1** - Cliente HTTP para testes

### **Utilitários:**
- **Python-Dotenv 1.2.1** - Gerenciamento de .env
- **PyYAML 6.0.3** - Configurações YAML

---

## ⚙️ **Configuração e Variáveis de Ambiente**

### **Arquivo `.env` (Desenvolvimento):**

```env
# ============================================================
# APLICAÇÃO
# ============================================================
APP_NAME=KiloCal
ENV=dev
DEBUG=True
STAGE=DEV

# ============================================================
# BANCO DE DADOS
# ============================================================
DEV_DATABASE_URL=postgresql://user:password@localhost:5432/kilocal_dev
PROD_DATABASE_URL=postgresql://user:password@host:5432/kilocal

# ============================================================
# SEGURANÇA - JWT
# ============================================================
JWT_SECRET_KEY=sua-chave-super-secreta-aqui-mude-em-producao
JWT_ALGORITHM=HS256
JWT_EXPIRE_DAYS=1
JWT_EXPIRE_DAYS_REMEMBER=7

# ============================================================
# CORS (Frontend)
# ============================================================
CORS_ORIGINS=http://localhost:3000,http://localhost:5173
```

### **Classe de Configuração (`src/core/config.py`):**

```python
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    APP_NAME: str = "KiloCal"
    ENV: str = "dev"
    DEBUG: bool = False
    STAGE: str = "DEV"
    
    # Database
    DEV_DATABASE_URL: str
    PROD_DATABASE_URL: str
    
    # JWT
    JWT_SECRET_KEY: str
    JWT_ALGORITHM: str = "HS256"
    JWT_EXPIRE_DAYS: int = 1
    JWT_EXPIRE_DAYS_REMEMBER: int = 7
    
    @property
    def DATABASE_URL(self) -> str:
        if self.STAGE.upper() == "PROD":
            return self.PROD_DATABASE_URL
        return self.DEV_DATABASE_URL

settings = Settings()
```

---

## 🗄️ **Banco de Dados**

### **ORM: Tortoise ORM**

O projeto utiliza **Tortoise ORM**, um ORM assíncrono inspirado no Django ORM.

**Configuração (`src/core/database/db_config.py`):**

```python
TORTOISE_ORM = {
    "connections": {
        "default": settings.DATABASE_URL
    },
    "apps": {
        "models": {
            "models": [
                "src.types.models.user",
                "src.types.models.body_assessments",
                "src.types.models.workout",
                "src.types.models.exercise",
                "src.types.models.session",
                "src.types.models.sets",
                "src.types.models.caloric_intakes",
                "aerich.models"
            ],
            "default_connection": "default",
        }
    },
}
```

### **Migrações:**

```bash
# Inicializar Aerich
aerich init -t src.core.database.db_config.TORTOISE_ORM

# Criar migração
aerich migrate --name "descrição_da_mudança"

# Aplicar migrações
aerich upgrade
```

### **Schema do Banco:**

#### **Tabela: `users`**
```sql
CREATE TABLE users (
    id UUID PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    name VARCHAR(255) NOT NULL,
    hashed_password VARCHAR(255) NOT NULL,
    birth_date DATE NOT NULL,
    role VARCHAR(10) DEFAULT 'user',
    height_cm FLOAT DEFAULT 0.0,
    goal FLOAT,
    gender VARCHAR(10) NOT NULL,
    activity_level VARCHAR(20) NOT NULL,
    activates_at TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

#### **Tabela: `body_assessments`**
```sql
CREATE TABLE body_assessments (
    id UUID PRIMARY KEY,
    user_id UUID REFERENCES users(id) ON DELETE CASCADE,
    weight_kg FLOAT NOT NULL,
    height_cm FLOAT NOT NULL,
    waist_cm FLOAT,
    hip_cm FLOAT,
    chest_cm FLOAT,
    neck_cm FLOAT,
    arm_cm FLOAT,
    thigh_cm FLOAT,
    fold_chest FLOAT,
    fold_abdominal FLOAT,
    fold_thigh FLOAT,
    fold_triceps FLOAT,
    fold_subscapular FLOAT,
    fold_suprailiac FLOAT,
    fold_midaxillary FLOAT,
    bfp FLOAT,           -- % de Gordura
    bmi FLOAT,           -- IMC
    bmr FLOAT,           -- Taxa Metabólica Basal
    tdee FLOAT,          -- Gasto Calórico Total
    lean_mass_kg FLOAT,  -- Massa Magra
    fat_mass_kg FLOAT,   -- Massa Gorda
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

---

## 🔐 **Autenticação e Segurança**

### **1. Sistema de Autenticação JWT**

#### **Geração de Token (`src/core/auth/token.py`):**

```python
class AccessToken:
    @staticmethod
    def generate(user_id: str, role: str, remember: bool = False) -> str:
        if remember:
            expire_time = timedelta(days=settings.JWT_EXPIRE_DAYS_REMEMBER)
        else:
            expire_time = timedelta(days=settings.JWT_EXPIRE_DAYS)
        
        expire = datetime.now(timezone.utc) + expire_time
        
        payload = {
            "sub": user_id,
            "role": role,
            "exp": expire,
            "iat": datetime.now(timezone.utc)
        }
        
        return jwt.encode(payload, settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM)
```

#### **Estrutura do Token JWT:**

```json
{
  "sub": "user-uuid-here",
  "role": "user",
  "exp": 1704672000,
  "iat": 1704585600
}
```

### **2. Hash de Senhas (`src/core/auth/security.py`):**

```python
class Authenticate:
    _context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    
    @classmethod
    def hash_password(cls, raw: str) -> str:
        password_bytes = raw.encode("utf-8")[:72]  # Bcrypt limit
        safe_password = password_bytes.decode("utf-8", errors="ignore")
        return cls._context.hash(safe_password)
    
    @classmethod
    def verify_password(cls, raw: str, hashed: str) -> bool:
        password_bytes = raw.encode("utf-8")[:72]
        safe_password = password_bytes.decode("utf-8", errors="ignore")
        return cls._context.verify(safe_password, hashed)
```

### **3. Fluxo de Autenticação:**

```
┌─────────────────────────────────────────────────────────┐
│  1. Cliente envia credenciais                           │
│     POST /user/login                                    │
│     Body: { email, password }                           │
└─────────────────────────────────────────────────────────┘
                        ↓
┌─────────────────────────────────────────────────────────┐
│  2. Backend valida credenciais                          │
│     - Busca usuário por email                           │
│     - Compara hash da senha                             │
└─────────────────────────────────────────────────────────┘
                        ↓
┌─────────────────────────────────────────────────────────┐
│  3. Gera JWT                                            │
│     access_token = AccessToken.generate(user_id, role)  │
└─────────────────────────────────────────────────────────┘
                        ↓
┌─────────────────────────────────────────────────────────┐
│  4. Cria sessão                                         │
│     SessionService.create_session(user_id, remember)    │
└─────────────────────────────────────────────────────────┘
                        ↓
┌─────────────────────────────────────────────────────────┐
│  5. Retorna token ao cliente                            │
│     Response: { access_token, token_type: "bearer" }    │
└─────────────────────────────────────────────────────────┘
                        ↓
┌─────────────────────────────────────────────────────────┐
│  6. Cliente salva token                                 │
│     - Web: Cookie HttpOnly                              │
│     - Mobile: AsyncStorage/Keychain                     │
└─────────────────────────────────────────────────────────┘
                        ↓
┌─────────────────────────────────────────────────────────┐
│  7. Requests futuras incluem token                      │
│     Headers: { Authorization: "Bearer <token>" }        │
└─────────────────────────────────────────────────────────┘
```

---

## 🛡️ **Middlewares**

### **1. AuthMiddleware (`src/core/middlewares/auth_middleware.py`)**

Middleware customizado que valida autenticação em **todas as rotas** (exceto públicas).

#### **Funcionalidades:**
- ✅ Intercepta todas as requisições
- ✅ Valida token JWT (via Cookie ou Header Authorization)
- ✅ Carrega usuário do banco e cacheia em `request.state.user`
- ✅ Permite rotas públicas sem autenticação
- ✅ Logging de acessos (auditoria)
- ✅ Tratamento centralizado de erros de autenticação

#### **Código:**

```python
class AuthMiddleware(BaseHTTPMiddleware):
    PUBLIC_PATHS = [
        "/docs", "/redoc", "/openapi.json",
        "/auth/login", "/auth/register", "/health", "/"
    ]
    
    async def dispatch(self, request: Request, call_next):
        # Pula autenticação para rotas públicas
        if any(request.url.path.startswith(path) for path in self.PUBLIC_PATHS):
            return await call_next(request)
        
        try:
            # Prioridade 1: Authorization Header (mobile/API)
            token = None
            auth_header = request.headers.get("Authorization")
            if auth_header:
                token = auth_header.replace("Bearer ", "")
            
            # Prioridade 2: Cookie (web - fallback)
            if not token:
                token = request.cookies.get("access_token")
            
            if not token:
                raise HTTPException(status_code=401, detail="Authentication required")
            
            # Decodifica JWT e busca usuário
            user_data = AccessToken.decode(token)
            user = await User.get(id=user_data.user_id)
            
            # Cacheia no request
            request.state.user = user
            request.state.user_id = user.id
            
            # Log
            logger.info(f"🔐 User {user.email} → {request.method} {request.url.path}")
            
            return await call_next(request)
            
        except HTTPException as e:
            return JSONResponse(status_code=e.status_code, content={"detail": e.detail})
        except Exception as e:
            logger.error(f"❌ Erro no AuthMiddleware: {str(e)}")
            return JSONResponse(status_code=500, content={"detail": "Internal error"})
```

#### **Uso nas Rotas:**

```python
@app.post("/body-assessment/")
async def create_body_assessment(request: Request, data: BodyAssessmentCreate):
    # Middleware já validou, só pegar do cache
    user = request.state.user
    # ... lógica da rota
```

### **2. CORSMiddleware (FastAPI)**

Configurado para aceitar requests de aplicações web e mobile.

```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "https://kilocal-8fy9.onrender.com"],
    allow_credentials=True,  # OBRIGATÓRIO para cookies
    allow_methods=["*"],
    allow_headers=["*"],
)
```

---

## 🌐 **Endpoints da API**

### **Base URL:** `/api/v1`

---

### **👤 Autenticação (`/user`)**

#### **POST `/user/register`**
Cria uma nova conta de usuário.

**Request Body:**
```json
{
  "email": "usuario@email.com",
  "name": "João Silva",
  "password": "senha123",
  "birth_date": "1990-01-15",
  "height_cm": 175.0,
  "gender": "male",
  "activity_level": "moderately_active"
}
```

**Response (201):**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

**Validações:**
- ✅ Email único (não pode duplicar)
- ✅ Senha mínima (definida no Pydantic)
- ✅ Data de nascimento válida
- ✅ Gender: `male` ou `female`
- ✅ Activity level: `sedentary`, `lightly_active`, `moderately_active`, `very_active`, `extra_active`, `athlete`

---

#### **POST `/user/login`**
Autentica um usuário existente.

**Request Body:**
```json
{
  "email": "usuario@email.com",
  "password": "senha123"
}
```

**Query Parameters:**
- `remember` (boolean, opcional): Se `true`, token expira em 7 dias. Default: `false` (1 dia).

**Response (200):**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

**Erros:**
- `401 Unauthorized`: Credenciais inválidas
- `500 Internal Server Error`: Erro no servidor

---

### **📊 Avaliação Corporal (`/body-assessment`)**

#### **POST `/body-assessment/`**
Cria uma nova avaliação corporal com cálculos automáticos.

**Headers:**
```
Authorization: Bearer <token>
```

**Request Body:**
```json
{
  "weight_kg": 75.5,
  "height_cm": 175.0,
  "waist_cm": 85.0,
  "hip_cm": 95.0,
  "neck_cm": 38.0,
  "chest_cm": 100.0,
  "arm_cm": 32.0,
  "thigh_cm": 55.0,
  "fold_chest": 12.0,
  "fold_abdominal": 20.0,
  "fold_thigh": 18.0,
  "fold_triceps": 15.0,
  "fold_subscapular": 14.0,
  "fold_suprailiac": 16.0,
  "fold_midaxillary": 13.0
}
```

**Campos obrigatórios:**
- `weight_kg` (float, > 0)
- `height_cm` (float, > 0)

**Campos opcionais:**
- Todas as circunferências (float, > 0)
- Todas as dobras cutâneas (float, >= 0)

**Response (201):**
```json
{
  "id": "uuid-da-avaliacao",
  "bfp": 18.5,           // % de Gordura
  "bmi": 24.7,           // IMC
  "bmr": 1750.0,         // Taxa Metabólica Basal (kcal/dia)
  "tdee": 2712.5,        // Gasto Calórico Total (kcal/dia)
  "lean_mass_kg": 61.5,  // Massa Magra
  "fat_mass_kg": 14.0,   // Massa Gorda
  "created_at": "2026-01-10T15:30:00Z"
}
```

**Cálculos Automáticos:**
1. **IMC (Body Mass Index):** `peso / (altura_m²)`
2. **% Gordura (Navy Method):** Fórmula baseada em circunferências
3. **TMB (Mifflin-St Jeor):** Gasto energético em repouso
4. **TDEE:** TMB × Multiplicador de atividade
5. **Massa Magra/Gorda:** Baseado no % de gordura

**Erros:**
- `401 Unauthorized`: Token inválido ou ausente
- `400 Bad Request`: Dados inválidos
- `500 Internal Server Error`: Erro no cálculo

---

#### **GET `/body-assessment/`**
Lista todas as avaliações corporais do usuário autenticado.

**Headers:**
```
Authorization: Bearer <token>
```

**Response (200):**
```json
[
  {
    "id": "uuid-1",
    "bfp": 18.5,
    "bmi": 24.7,
    "bmr": 1750.0,
    "tdee": 2712.5,
    "lean_mass_kg": 61.5,
    "fat_mass_kg": 14.0,
    "created_at": "2026-01-10T15:30:00Z"
  },
  {
    "id": "uuid-2",
    "bfp": 17.2,
    "bmi": 24.3,
    "bmr": 1765.0,
    "tdee": 2735.8,
    "lean_mass_kg": 62.8,
    "fat_mass_kg": 13.2,
    "created_at": "2026-01-05T10:15:00Z"
  }
]
```

**Ordenação:** Decrescente por data (mais recente primeiro)

---

#### **GET `/body-assessment/{assessment_id}`**
Retorna uma avaliação corporal específica com todos os dados.

**Headers:**
```
Authorization: Bearer <token>
```

**Path Parameters:**
- `assessment_id` (UUID): ID da avaliação

**Response (200):**
```json
{
  "id": "uuid-da-avaliacao",
  "user_id": "uuid-do-usuario",
  "weight_kg": 75.5,
  "height_cm": 175.0,
  "waist_cm": 85.0,
  "hip_cm": 95.0,
  "chest_cm": 100.0,
  "neck_cm": 38.0,
  "arm_cm": 32.0,
  "thigh_cm": 55.0,
  "fold_chest": 12.0,
  "fold_abdominal": 20.0,
  "fold_thigh": 18.0,
  "fold_triceps": 15.0,
  "fold_subscapular": 14.0,
  "fold_suprailiac": 16.0,
  "fold_midaxillary": 13.0,
  "bfp": 18.5,
  "bmi": 24.7,
  "bmr": 1750.0,
  "tdee": 2712.5,
  "lean_mass_kg": 61.5,
  "fat_mass_kg": 14.0,
  "created_at": "2026-01-10T15:30:00Z"
}
```

**Validações:**
- ✅ Avaliação deve existir
- ✅ Avaliação deve pertencer ao usuário autenticado

**Erros:**
- `401 Unauthorized`: Token inválido
- `403 Forbidden`: Avaliação não pertence ao usuário
- `404 Not Found`: Avaliação não encontrada

---

### **🏃 Treinos (Em Desenvolvimento)**

```
POST   /workout/             # Criar treino
GET    /workout/             # Listar treinos
GET    /workout/{id}         # Obter treino específico
PUT    /workout/{id}         # Atualizar treino
DELETE /workout/{id}         # Deletar treino
```

---

## 📦 **Modelos de Dados**

### **User (`src/types/models/user.py`)**

```python
class User(Model):
    id = fields.UUIDField(pk=True)
    email = fields.CharField(max_length=255, unique=True)
    name = fields.CharField(max_length=255)
    hashed_password = fields.CharField(max_length=255)
    birth_date = fields.DateField()
    role = fields.CharEnumField(RoleEnum, default=RoleEnum.USER)
    height_cm = fields.FloatField(default=0.0)
    goal = fields.FloatField(null=True)
    gender = fields.CharEnumField(GenderEnum)
    activity_level = fields.CharEnumField(ActivityLevelEnum)
    activates_at = fields.DatetimeField(null=True)
    created_at = fields.DatetimeField(auto_now_add=True)
    updated_at = fields.DatetimeField(auto_now=True)
    
    class Meta:
        table = "users"
```

### **BodyAssessment (`src/types/models/body_assessments.py`)**

```python
class BodyAssessment(Model):
    id = fields.UUIDField(pk=True)
    user = fields.ForeignKeyField("models.User", related_name="body_assessments", on_delete=fields.CASCADE)
    
    # Medidas físicas
    weight_kg = fields.FloatField()
    height_cm = fields.FloatField()
    waist_cm = fields.FloatField(null=True)
    hip_cm = fields.FloatField(null=True)
    chest_cm = fields.FloatField(null=True)
    neck_cm = fields.FloatField(null=True)
    arm_cm = fields.FloatField(null=True)
    thigh_cm = fields.FloatField(null=True)
    
    # Dobras cutâneas
    fold_chest = fields.FloatField(null=True)
    fold_abdominal = fields.FloatField(null=True)
    fold_thigh = fields.FloatField(null=True)
    fold_triceps = fields.FloatField(null=True)
    fold_subscapular = fields.FloatField(null=True)
    fold_suprailiac = fields.FloatField(null=True)
    fold_midaxillary = fields.FloatField(null=True)
    
    # Resultados calculados
    bfp = fields.FloatField(null=True)           # % de Gordura
    bmi = fields.FloatField(null=True)           # IMC
    bmr = fields.FloatField(null=True)           # Taxa Metabólica Basal
    tdee = fields.FloatField(null=True)          # Gasto Calórico Total
    lean_mass_kg = fields.FloatField(null=True)  # Massa Magra
    fat_mass_kg = fields.FloatField(null=True)   # Massa Gorda
    
    created_at = fields.DatetimeField(auto_now_add=True)
    
    class Meta:
        table = "body_assessments"
```

---

## 📝 **Schemas e Validações**

### **Schemas de Autenticação (`src/types/schemas/auth.py`)**

```python
class LoginRequest(BaseModel):
    email: EmailStr
    password: str

class RegisterRequest(BaseModel):
    email: EmailStr
    name: str
    password: str
    birth_date: date
    height_cm: float
    gender: GenderEnum
    activity_level: ActivityLevelEnum

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"

class TokenData(BaseModel):
    user_id: Optional[UUID] = None
    email: Optional[str] = None
    role: RoleEnum = RoleEnum.USER
```

### **Schemas de Body Assessment (`src/types/schemas/body_assessment.py`)**

```python
class BodyAssessmentCreate(BaseModel):
    weight_kg: float = Field(..., gt=0, description="Peso em kg")
    height_cm: float = Field(..., gt=0, description="Altura em cm")
    waist_cm: Optional[float] = Field(None, gt=0)
    hip_cm: Optional[float] = Field(None, gt=0)
    chest_cm: Optional[float] = Field(None, gt=0)
    neck_cm: Optional[float] = Field(None, gt=0)
    arm_cm: Optional[float] = Field(None, gt=0)
    thigh_cm: Optional[float] = Field(None, gt=0)
    fold_chest: Optional[float] = Field(None, ge=0)
    fold_abdominal: Optional[float] = Field(None, ge=0)
    fold_thigh: Optional[float] = Field(None, ge=0)
    fold_triceps: Optional[float] = Field(None, ge=0)
    fold_subscapular: Optional[float] = Field(None, ge=0)
    fold_suprailiac: Optional[float] = Field(None, ge=0)
    fold_midaxillary: Optional[float] = Field(None, ge=0)

class BodyAssessmentReed(BaseModel):
    id: UUID
    bfp: Optional[float] = Field(None, description="% de Gordura")
    bmi: Optional[float] = Field(None, description="IMC")
    bmr: Optional[float] = Field(None, description="Taxa Metabólica Basal")
    tdee: Optional[float] = Field(None, description="Gasto Calórico Total")
    lean_mass_kg: Optional[float] = Field(None, description="Massa Magra")
    fat_mass_kg: Optional[float] = Field(None, description="Massa Gorda")
    created_at: datetime

class BodyAssessmentBase(BaseModel):
    id: UUID
    user_id: UUID
    weight_kg: float
    height_cm: float
    # ... todos os campos completos
    bfp: Optional[float]
    bmi: Optional[float]
    bmr: Optional[float]
    tdee: Optional[float]
    lean_mass_kg: Optional[float]
    fat_mass_kg: Optional[float]
    created_at: datetime
```

---

## 🔧 **Services (Lógica de Negócio)**

### **UserService (`src/services/user_services.py`)**

Responsável por operações relacionadas a usuários.

**Principais métodos:**
- `create_user(data: RegisterRequest) -> str`: Cria usuário e retorna JWT
- `get_user(data: LoginRequest, remember: bool) -> str`: Autentica e retorna JWT

### **BodyAssessmentService (`src/services/body_assessment_service.py`)**

Responsável por avaliações corporais e cálculos automáticos.

**Principais métodos:**

```python
class BodyAssessmentService:
    @staticmethod
    async def create_body_assessment(
        user_id: UUID,
        user_gender: GenderEnum,
        user_birth_date: date,
        user_activity_level: ActivityLevelEnum,
        data: BodyAssessmentCreate
    ) -> BodyAssessmentReed:
        """
        Cria avaliação corporal com cálculos automáticos:
        - IMC
        - % Gordura (Navy Method)
        - TMB (Mifflin-St Jeor)
        - TDEE
        - Massa Magra/Gorda
        """
        age = BodyMetrics.calculate_age(user_birth_date)
        bmi = BodyMetrics.calculate_bmi(data.weight_kg, data.height_cm)
        
        bfp = BodyAssessmentService._calculate_body_fat_percentage(
            data, user_gender, user_birth_date, user_activity_level
        )
        
        lean_mass_kg, fat_mass_kg = BodyAssessmentService._calculate_body_composition(
            data.weight_kg, bfp
        )
        
        bmr = EnergyExpenditure.calculate_bmr(
            sex=user_gender,
            weight_kg=data.weight_kg,
            height_cm=data.height_cm,
            age=age
        )
        
        tdee = EnergyExpenditure.calculate_tdee(
            bmr=bmr,
            activity_level=user_activity_level
        )
        
        # Salva no banco...
    
    @staticmethod
    async def get_all_body_assessment_for_user_id(user_id: str) -> list[BodyAssessmentReed]:
        """Lista todas as avaliações do usuário"""
        
    @staticmethod
    async def get_body_assessment(assessment_id: str) -> BodyAssessmentBase:
        """Retorna avaliação específica"""
```

---

## 🧮 **Cálculos e Fórmulas**

### **BodyMetrics (`src/core/calculations/body_metrics.py`)**

#### **1. IMC (Body Mass Index)**

```python
def calculate_bmi(weight_kg: float, height_cm: float) -> float:
    height_m = height_cm / 100
    return round(weight_kg / (height_m**2), 2)
```

**Classificação:**
- < 18.5: Abaixo do peso
- 18.5-24.9: Peso normal
- 25-29.9: Sobrepeso
- 30-34.9: Obesidade Grau I
- 35-39.9: Obesidade Grau II
- ≥ 40: Obesidade Grau III

---

#### **2. % de Gordura (Navy Method)**

**Para Homens:**
```python
body_fat = (
    495 / (
        1.0324
        - 0.19077 * log10(waist_cm - neck_cm)
        + 0.15456 * log10(height_cm)
    )
    - 450
)
```

**Para Mulheres:**
```python
body_fat = (
    495 / (
        1.29579
        - 0.35004 * log10(waist_cm + hip_cm - neck_cm)
        + 0.22100 * log10(height_cm)
    )
    - 450
)
```

---

#### **3. Massa Magra e Gorda**

```python
def calculate_lean_mass(weight_kg: float, body_fat_percentage: float) -> float:
    fat_mass = weight_kg * (body_fat_percentage / 100)
    lean_mass = weight_kg - fat_mass
    return round(lean_mass, 2)

def calculate_fat_mass(weight_kg: float, body_fat_percentage: float) -> float:
    fat_mass = weight_kg * (body_fat_percentage / 100)
    return round(fat_mass, 2)
```

---

### **EnergyExpenditure (`src/core/calculations/energy_expenditure.py`)**

#### **1. TMB (Taxa Metabólica Basal) - Mifflin-St Jeor**

**Para Homens:**
```python
bmr = (10 * weight_kg) + (6.25 * height_cm) - (5 * age) + 5
```

**Para Mulheres:**
```python
bmr = (10 * weight_kg) + (6.25 * height_cm) - (5 * age) - 161
```

---

#### **2. TDEE (Total Daily Energy Expenditure)**

```python
def calculate_tdee(bmr: float, activity_level: ActivityLevelEnum) -> float:
    MULTIPLIERS = {
        ActivityLevelEnum.SEDENTARY: 1.2,
        ActivityLevelEnum.LIGHTLY_ACTIVE: 1.375,
        ActivityLevelEnum.MODERATELY_ACTIVE: 1.55,
        ActivityLevelEnum.VERY_ACTIVE: 1.725,
        ActivityLevelEnum.ATHLETE: 1.9,
    }
    multiplier = MULTIPLIERS[activity_level]
    return round(bmr * multiplier, 2)
```

**Exemplos:**
- Sedentário (sem exercício): TMB × 1.2
- Levemente ativo (1-3 dias/semana): TMB × 1.375
- Moderadamente ativo (3-5 dias/semana): TMB × 1.55
- Muito ativo (6-7 dias/semana): TMB × 1.725
- Atleta (2x/dia): TMB × 1.9

---

## ⚠️ **Tratamento de Erros**

### **Estrutura de Resposta de Erro:**

```json
{
  "detail": "Mensagem de erro legível",
  "timestamp": "2026-01-10T15:30:00Z"
}
```

### **Códigos HTTP:**

| Código | Significado | Quando Ocorre |
|--------|-------------|---------------|
| `200` | OK | Operação bem-sucedida (GET, PUT) |
| `201` | Created | Recurso criado (POST) |
| `400` | Bad Request | Dados inválidos ou faltando |
| `401` | Unauthorized | Token ausente ou inválido |
| `403` | Forbidden | Token válido mas sem permissão |
| `404` | Not Found | Recurso não encontrado |
| `409` | Conflict | Conflito (ex: email duplicado) |
| `422` | Unprocessable Entity | Validação Pydantic falhou |
| `500` | Internal Server Error | Erro inesperado no servidor |

### **Exemplos:**

**Email duplicado (409):**
```json
{
  "detail": "Email already registered"
}
```

**Token inválido (401):**
```json
{
  "detail": "Could not validate credentials"
}
```

**Dados inválidos (422):**
```json
{
  "detail": [
    {
      "loc": ["body", "weight_kg"],
      "msg": "ensure this value is greater than 0",
      "type": "value_error.number.not_gt"
    }
  ]
}
```

---

## 🧪 **Testes**

### **Estrutura de Testes:**

```
tests/
├── user/
│   ├── login.py
│   └── register.py
└── workouts/
```

### **Executar Testes:**

```bash
# Todos os testes
pytest

# Com cobertura
pytest --cov=src

# Testes específicos
pytest tests/user/login.py

# Modo verboso
pytest -v
```

### **Exemplo de Teste:**

```python
import pytest
from httpx import AsyncClient
from src.main import app

@pytest.mark.asyncio
async def test_register_user():
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.post("/user/register", json={
            "email": "test@example.com",
            "name": "Test User",
            "password": "password123",
            "birth_date": "1990-01-01",
            "height_cm": 175.0,
            "gender": "male",
            "activity_level": "moderately_active"
        })
        
        assert response.status_code == 201
        assert "access_token" in response.json()
```

---

## 🚀 **Deploy e Produção**

### **Plataforma: Render**

**URL de Produção:** `https://kilocal-8fy9.onrender.com`

### **Configuração:**

**1. Variáveis de Ambiente (Render):**
```env
STAGE=PROD
PROD_DATABASE_URL=postgresql://user:pass@host:5432/kilocal
JWT_SECRET_KEY=production-secret-key-super-secure
JWT_ALGORITHM=HS256
JWT_EXPIRE_DAYS=1
JWT_EXPIRE_DAYS_REMEMBER=7
```

**2. Start Command:**
```bash
uvicorn src.main:app --host 0.0.0.0 --port $PORT
```

**3. Build Command:**
```bash
pip install -r requirements.txt
aerich upgrade
```

### **Considerações de Produção:**

✅ **Segurança:**
- SSL/TLS habilitado (HTTPS)
- JWT_SECRET_KEY forte e único
- Senhas hasheadas com bcrypt
- CORS configurado apenas para domínios autorizados

✅ **Performance:**
- Conexões de banco em pool (Tortoise ORM)
- Queries otimizadas
- Cache de usuário no middleware

✅ **Monitoramento:**
- Logs estruturados
- Health check endpoint: `/health`

---

## 📈 **Roadmap**

### **Em Desenvolvimento:**
- 🚧 Sistema completo de treinos
- 🚧 Exercícios personalizados
- 🚧 Cálculo de calorias por treino
- 🚧 Histórico de evolução com gráficos

### **Planejado:**
- 📅 Sistema de metas
- 📅 Notificações push
- 📅 Integração com wearables
- 📅 Planos alimentares

---

## 👨‍💻 **Contribuindo**

### **Estrutura de Commits:**

```
feat: Adiciona endpoint de treinos
fix: Corrige cálculo de TMB
docs: Atualiza documentação da API
refactor: Refatora BodyAssessmentService
test: Adiciona testes para login
```

### **Fluxo de Trabalho:**

1. Clone o repositório
2. Crie uma branch: `git checkout -b feature/nova-funcionalidade`
3. Faça suas alterações
4. Execute os testes: `pytest`
5. Commit: `git commit -m "feat: descrição"`
6. Push: `git push origin feature/nova-funcionalidade`
7. Abra um Pull Request

---

## 📞 **Suporte**

**Issues:** [GitHub Issues](https://github.com/YhannMatheus/Kilocal/issues)  
**Email:** yhann.mendes@poraygua.com.br  
**Documentação:** [/docs](/docs)

---

**Última atualização:** 10 de Janeiro de 2026  
**Versão da API:** 1.0.0  
**Desenvolvido por:** Yhann Matheus
