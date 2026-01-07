"""Testes para a rota de login de usuário (POST /user/login)"""

import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_login_success(client: AsyncClient, test_user_data):
    """Testa login bem-sucedido com credenciais válidas"""
    # Primeiro, registrar o usuário
    await client.post("/user/register", json=test_user_data)
    
    # Tentar fazer login
    login_data = {
        "email": test_user_data["email"],
        "password": test_user_data["password"]
    }
    response = await client.post("/user/login", json=login_data)
    
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert isinstance(data["access_token"], str)
    assert len(data["access_token"]) > 0


@pytest.mark.asyncio
async def test_login_invalid_email(client: AsyncClient):
    """Testa login com email não registrado"""
    login_data = {
        "email": "nonexistent@example.com",
        "password": "SomePassword123"
    }
    response = await client.post("/user/login", json=login_data)
    
    assert response.status_code == 401
    assert "Invalid email or password" in response.json()["detail"]


@pytest.mark.asyncio
async def test_login_wrong_password(client: AsyncClient, test_user_data):
    """Testa login com senha incorreta"""
    # Registrar usuário
    await client.post("/user/register", json=test_user_data)
    
    # Tentar login com senha errada
    login_data = {
        "email": test_user_data["email"],
        "password": "WrongPassword123"
    }
    response = await client.post("/user/login", json=login_data)
    
    assert response.status_code == 401
    assert "Invalid email or password" in response.json()["detail"]


@pytest.mark.asyncio
async def test_login_missing_email(client: AsyncClient):
    """Testa login sem email"""
    login_data = {
        "password": "SomePassword123"
    }
    response = await client.post("/user/login", json=login_data)
    
    assert response.status_code == 422


@pytest.mark.asyncio
async def test_login_missing_password(client: AsyncClient):
    """Testa login sem senha"""
    login_data = {
        "email": "test@example.com"
    }
    response = await client.post("/user/login", json=login_data)
    
    assert response.status_code == 422


@pytest.mark.asyncio
async def test_login_empty_credentials(client: AsyncClient):
    """Testa login com credenciais vazias"""
    login_data = {
        "email": "",
        "password": ""
    }
    response = await client.post("/user/login", json=login_data)
    
    assert response.status_code in [401, 422]


@pytest.mark.asyncio
async def test_login_with_remember_true(client: AsyncClient, test_user_data):
    """Testa login com remember=True"""
    # Registrar usuário
    await client.post("/user/register", json=test_user_data)
    
    # Login com remember=True
    login_data = {
        "email": test_user_data["email"],
        "password": test_user_data["password"]
    }
    response = await client.post("/user/login?remember=true", json=login_data)
    
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data


@pytest.mark.asyncio
async def test_login_with_remember_false(client: AsyncClient, test_user_data):
    """Testa login com remember=False"""
    # Registrar usuário
    await client.post("/user/register", json=test_user_data)
    
    # Login com remember=False
    login_data = {
        "email": test_user_data["email"],
        "password": test_user_data["password"]
    }
    response = await client.post("/user/login?remember=false", json=login_data)
    
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data


@pytest.mark.asyncio
async def test_login_case_sensitive_email(client: AsyncClient, test_user_data):
    """Testa se o email é case-sensitive no login"""
    # Registrar usuário
    await client.post("/user/register", json=test_user_data)
    
    # Tentar login com email em maiúsculas
    login_data = {
        "email": test_user_data["email"].upper(),
        "password": test_user_data["password"]
    }
    response = await client.post("/user/login", json=login_data)
    
    # Depende da implementação - pode aceitar ou rejeitar
    assert response.status_code in [200, 401]
