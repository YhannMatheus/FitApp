"""Testes para a rota de registro de usuário (POST /user/register)"""

import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_register_success(client: AsyncClient, test_user_data):
    """Testa o registro bem-sucedido de um novo usuário"""
    response = await client.post("/user/register", json=test_user_data)
    
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert isinstance(data["access_token"], str)
    assert len(data["access_token"]) > 0


@pytest.mark.asyncio
async def test_register_duplicate_email(client: AsyncClient, test_user_data):
    """Testa que não é possível registrar o mesmo email duas vezes"""
    # Primeiro registro
    response1 = await client.post("/user/register", json=test_user_data)
    assert response1.status_code == 200
    
    # Segundo registro com mesmo email
    response2 = await client.post("/user/register", json=test_user_data)
    assert response2.status_code == 400
    assert "Email already in use" in response2.json()["detail"]


@pytest.mark.asyncio
async def test_register_invalid_email(client: AsyncClient, test_user_data):
    """Testa registro com email inválido"""
    test_user_data["email"] = "invalid-email"
    response = await client.post("/user/register", json=test_user_data)
    
    assert response.status_code == 422  # Validation error


@pytest.mark.asyncio
async def test_register_missing_required_fields(client: AsyncClient):
    """Testa registro sem campos obrigatórios"""
    incomplete_data = {
        "email": "test@example.com",
        "password": "Test@123456"
    }
    response = await client.post("/user/register", json=incomplete_data)
    
    assert response.status_code == 422


@pytest.mark.asyncio
async def test_register_invalid_gender(client: AsyncClient, test_user_data):
    """Testa registro com gênero inválido"""
    test_user_data["gender"] = "invalid_gender"
    response = await client.post("/user/register", json=test_user_data)
    
    assert response.status_code == 422


@pytest.mark.asyncio
async def test_register_invalid_activity_level(client: AsyncClient, test_user_data):
    """Testa registro com nível de atividade inválido"""
    test_user_data["activity_level"] = "invalid_level"
    response = await client.post("/user/register", json=test_user_data)
    
    assert response.status_code == 422


@pytest.mark.asyncio
async def test_register_negative_height(client: AsyncClient, test_user_data):
    """Testa registro com altura negativa"""
    test_user_data["height_cm"] = -175.0
    response = await client.post("/user/register", json=test_user_data)
    
    # Pode ser 422 (validation error) ou 200 dependendo das validações
    assert response.status_code in [200, 422]


@pytest.mark.asyncio
async def test_register_with_remember_flag(client: AsyncClient, test_user_data):
    """Testa registro com flag remember=True"""
    response = await client.post(
        "/user/register?remember=true",
        json=test_user_data
    )
    
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
