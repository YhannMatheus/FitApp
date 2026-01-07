"""Testes para a rota de perfil de usuário (GET /user/profile)"""

import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_get_profile_success(authenticated_client):
    """Testa obtenção do perfil com autenticação válida"""
    client, token = authenticated_client
    
    response = await client.get("/user/profile")
    
    assert response.status_code == 200
    data = response.json()
    
    # Verificar campos obrigatórios
    assert "token" in data
    assert "name" in data
    assert "email" in data
    assert "gender" in data
    assert "birth_date" in data
    assert "height_cm" in data
    assert "activity_level" in data
    assert "role" in data
    assert "created_at" in data
    assert "workouts" in data
    assert "body_history" in data
    
    # Verificar tipos
    assert isinstance(data["workouts"], list)
    assert isinstance(data["body_history"], list)


@pytest.mark.asyncio
async def test_get_profile_without_auth(client: AsyncClient):
    """Testa obtenção do perfil sem autenticação"""
    response = await client.get("/user/profile")
    
    assert response.status_code == 401


@pytest.mark.asyncio
async def test_get_profile_invalid_token(client: AsyncClient):
    """Testa obtenção do perfil com token inválido"""
    client.headers.update({"Authorization": "Bearer invalid_token_here"})
    response = await client.get("/user/profile")
    
    assert response.status_code == 401


@pytest.mark.asyncio
async def test_get_profile_expired_token(client: AsyncClient):
    """Testa obtenção do perfil com token expirado"""
    # Token JWT expirado (exemplo - você pode gerar um token expirado real)
    expired_token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiaWF0IjoxNTE2MjM5MDIyLCJleHAiOjE1MTYyMzkwMjJ9.4Adcj0vbzb8fB_s83t5VKkVCVSr-3LlPn0IGK8H5Qk4"
    client.headers.update({"Authorization": f"Bearer {expired_token}"})
    response = await client.get("/user/profile")
    
    assert response.status_code == 401


@pytest.mark.asyncio
async def test_get_profile_malformed_token(client: AsyncClient):
    """Testa obtenção do perfil com token malformado"""
    client.headers.update({"Authorization": "Bearer not.a.valid.jwt"})
    response = await client.get("/user/profile")
    
    assert response.status_code == 401


@pytest.mark.asyncio
async def test_get_profile_missing_bearer(client: AsyncClient):
    """Testa obtenção do perfil sem o prefixo Bearer"""
    # Registrar e fazer login
    test_user = {
        "name": "Test User",
        "email": "test@example.com",
        "password": "Test@123456",
        "gender": "male",
        "birth_date": "1990-01-01",
        "height_cm": 175.0,
        "activity_level": "moderately_active"
    }
    reg_response = await client.post("/user/register", json=test_user)
    token = reg_response.json()["access_token"]
    
    # Enviar token sem "Bearer "
    client.headers.update({"Authorization": token})
    response = await client.get("/user/profile")
    
    assert response.status_code == 401


@pytest.mark.asyncio
async def test_get_profile_empty_workouts(authenticated_client):
    """Testa que um usuário recém-criado tem lista de workouts vazia"""
    client, token = authenticated_client
    
    response = await client.get("/user/profile")
    
    assert response.status_code == 200
    data = response.json()
    assert data["workouts"] == []


@pytest.mark.asyncio
async def test_get_profile_empty_body_history(authenticated_client):
    """Testa que um usuário recém-criado tem histórico corporal vazio"""
    client, token = authenticated_client
    
    response = await client.get("/user/profile")
    
    assert response.status_code == 200
    data = response.json()
    assert data["body_history"] == []


@pytest.mark.asyncio
async def test_get_profile_returns_correct_user_data(authenticated_client, test_user_data):
    """Testa que o perfil retorna os dados corretos do usuário"""
    client, token = authenticated_client
    
    response = await client.get("/user/profile")
    
    assert response.status_code == 200
    data = response.json()
    
    # Verificar que os dados correspondem ao usuário registrado
    assert data["name"] == test_user_data["name"]
    assert data["email"] == test_user_data["email"]
    assert data["gender"] == test_user_data["gender"]
    assert data["height_cm"] == test_user_data["height_cm"]
    assert data["activity_level"] == test_user_data["activity_level"]
