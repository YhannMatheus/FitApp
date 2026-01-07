"""Configurações e fixtures para os testes com pytest"""

import sys
import os
from pathlib import Path

# Adicionar o diretório raiz do projeto ao path
root_dir = Path(__file__).parent.parent
sys.path.insert(0, str(root_dir))

import pytest
import asyncio
from typing import AsyncGenerator
from httpx import AsyncClient, ASGITransport
from tortoise import Tortoise
from src.main import app


@pytest.fixture(scope="function", autouse=True)
async def initialize_tests():
    """Inicializa o banco de dados de teste antes de cada teste"""
    # Configurar Tortoise ORM com SQLite em memória
    await Tortoise.init(
        db_url="sqlite://:memory:",
        modules={"models": ["src.types.models.user", "src.types.models.workout", "src.types.models.exercise", "src.types.models.sets", "src.types.models.body_assessments", "src.types.models.caloric_intakes"]}
    )
    # Criar as tabelas
    await Tortoise.generate_schemas()
    
    yield
    
    # Cleanup - fechar conexões
    await Tortoise.close_connections()


@pytest.fixture
async def client() -> AsyncGenerator[AsyncClient, None]:
    """Cliente HTTP assíncrono para testes"""
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac


@pytest.fixture
async def test_user_data():
    """Dados de um usuário de teste"""
    return {
        "name": "Test User",
        "email": "test@example.com",
        "password": "Test@123456",
        "gender": "male",
        "birth_date": "1990-01-01",
        "height_cm": 175.0,
        "activity_level": "moderately_active"
    }


@pytest.fixture
async def authenticated_client(test_user_data) -> AsyncGenerator[tuple[AsyncClient, str], None]:
    """Cliente autenticado com token JWT"""
    # Criar novo cliente para garantir headers limpos
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        # Registrar usuário
        response = await client.post("/user/register", json=test_user_data)
        assert response.status_code == 200, f"Failed to register: {response.text}"
        token = response.json()["access_token"]
        
        # Configurar headers com token
        client.headers.update({"Authorization": f"Bearer {token}"})
        
        yield client, token
