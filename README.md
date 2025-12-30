# KiloCal

KiloCal é um aplicativo completo para rastreamento de fitness, focado em controle de treinos, avaliação corporal, cálculo de calorias e gerenciamento de usuários. O projeto é dividido em backend (FastAPI, PostgreSQL, SQLAlchemy, Alembic) e frontend (React, TypeScript, Vite).

## Funcionalidades
- Cadastro e autenticação de usuários
- CRUD de treinos, exercícios e séries
- Avaliação corporal e cálculo de calorias
- Integração entre frontend e backend via API RESTful
- Migrações de banco de dados com Alembic

## Tecnologias Utilizadas
- **Backend:** FastAPI, SQLAlchemy, Alembic, PostgreSQL, Pydantic, Uvicorn
- **Frontend:** React, TypeScript, Vite (em desenvolvimento)
- **Outros:** Docker, Docker Compose

## Estrutura do Projeto
```
KiloCal/
├── client/                # Frontend React (Vite)
├── server/                # Backend FastAPI
│   ├── src/               # Código principal do backend
│   ├── alembic/           # Migrações Alembic
│   └── requirements.txt   # Dependências Python
├── docker-compose.yml     # Orquestração de containers
└── README.md              # Este arquivo
```

## Como rodar o projeto

### Pré-requisitos
- Docker e Docker Compose instalados
- (Opcional) Python 3.11+ e Node.js 18+ para rodar localmente sem Docker

### Usando Docker Compose
1. Clone o repositório:
   ```bash
   git clone <repo-url>
   cd KiloCal
   ```
2. Suba os containers:
   ```bash
   docker-compose up --build
   ```
3. O backend estará disponível em `http://localhost:8000`.
4. O frontend estará disponível em `http://localhost:5173` (após implementação).

### Rodando localmente (sem Docker)
#### Backend
1. Crie e ative um ambiente virtual Python:
   ```bash
   cd server
   python -m venv venv
   venv\Scripts\activate  # Windows
   # ou
   source venv/bin/activate  # Linux/Mac
   ```
2. Instale as dependências:
   ```bash
   pip install -r requirements.txt
   ```
3. Configure o arquivo `.env` com as variáveis do banco de dados.
4. Execute as migrações:
   ```bash
   alembic upgrade head
   ```
5. Inicie o servidor:
   ```bash
   uvicorn src.main:app --reload
   ```

#### Frontend
1. Instale as dependências:
   ```bash
   cd client
   npm install
   ```
2. Inicie o servidor de desenvolvimento:
   ```bash
   npm run dev
   ```

## Estrutura das Pastas Principais
- `server/src/routes/`: Rotas da API
- `server/src/services/`: Lógica de negócio
- `server/src/types/`: Schemas, models e enums
- `client/`: Código do frontend React

## Contribuição
Pull requests são bem-vindos! Siga o padrão de código e descreva claramente suas alterações.

## Licença
Este projeto está sob a licença MIT.
