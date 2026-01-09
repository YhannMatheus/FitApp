import requests

BASE_URL = "http://localhost:8000/user"

def test_register_success():
    payload = {
        "email": "newuser@example.com",
        "name": "New User",
        "password": "password123",
        "birth_date": "1995-06-15",
        "height_cm": 170.0,
        "gender": "male",
        "activity_level": "moderately_active"
    }
    response = requests.post(f"{BASE_URL}/register", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["access_token"] is not None

def test_register_duplicate_email():
    payload = {
        "email": "john@example.com",  # Email já existe no seed
        "name": "John Duplicate",
        "password": "password123",
        "birth_date": "1990-01-01",
        "height_cm": 175.0,
        "gender": "male",
        "activity_level": "sedentary"
    }
    response = requests.post(f"{BASE_URL}/register", json=payload)
    assert response.status_code == 400 or response.status_code == 409
    data = response.json()
    assert "detail" in data

def test_register_missing_fields():
    payload = {
        "email": "incomplete@example.com",
        "name": "Incomplete User"
        # Missing required fields
    }
    response = requests.post(f"{BASE_URL}/register", json=payload)
    assert response.status_code == 422
    data = response.json()
    assert "detail" in data

def test_register_invalid_email():
    payload = {
        "email": "invalid-email",
        "name": "Invalid Email User",
        "password": "password123",
        "birth_date": "1990-01-01",
        "height_cm": 175.0,
        "gender": "male",
        "activity_level": "sedentary"
    }
    response = requests.post(f"{BASE_URL}/register", json=payload)
    assert response.status_code == 422
    data = response.json()
    assert "detail" in data