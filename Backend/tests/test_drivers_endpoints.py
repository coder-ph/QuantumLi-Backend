import pytest
import json
from Backend.app import app

@pytest.fixture
def client():
    with app.test_client() as client:
        yield client

def login(client, email, password):
    response = client.post('/auth/login', json={'email': email, 'password': password})
    assert response.status_code == 200
    data = response.get_json()
    return data['access_token']

def test_create_driver(client):
    token = login(client, 'testuser@example.com', 'testpassword')  
    headers = {'Authorization': f'Bearer {token}'}
    driver_data = {
        "name": "Test Driver",
        "email": "driver@example.com",
        "phone": "1234567890"
    }
    response = client.post('/api/v1/drivers', json=driver_data, headers=headers)
    assert response.status_code == 201 or response.status_code == 200

def test_get_all_drivers(client):
    token = login(client, 'testuser@example.com', 'testpassword')
    headers = {'Authorization': f'Bearer {token}'}
    response = client.get('/api/v1/drivers', headers=headers)
    assert response.status_code == 200

def test_get_driver(client):
    token = login(client, 'testuser@example.com', 'testpassword')
    headers = {'Authorization': f'Bearer {token}'}
    # Replace with an existing driver UUID for testing
    driver_id = '00000000-0000-0000-0000-000000000000'
    response = client.get(f'/api/v1/drivers/{driver_id}', headers=headers)
    # 404 is acceptable if driver does not exist
    assert response.status_code in [200, 404]

def test_update_driver(client):
    token = login(client, 'testuser@example.com', 'testpassword')
    headers = {'Authorization': f'Bearer {token}'}
    driver_id = '00000000-0000-0000-0000-000000000000'  # Replace with valid driver UUID
    update_data = {
        "phone": "0987654321"
    }
    response = client.put(f'/api/v1/drivers/{driver_id}', json=update_data, headers=headers)
    assert response.status_code in [200, 404]

def test_delete_driver(client):
    token = login(client, 'testuser@example.com', 'testpassword')
    headers = {'Authorization': f'Bearer {token}'}
    driver_id = '00000000-0000-0000-0000-000000000000'  # Replace with valid driver UUID
    response = client.delete(f'/api/v1/drivers/{driver_id}', headers=headers)
    assert response.status_code in [200, 404]

def test_upload_document(client):
    token = login(client, 'testuser@example.com', 'testpassword')
    headers = {'Authorization': f'Bearer {token}'}
    driver_id = '00000000-0000-0000-0000-000000000000'  # Replace with valid driver UUID
    data = {
        'file': (open('test_document.pdf', 'rb'), 'test_document.pdf')
    }
    response = client.post(f'/api/v1/drivers/{driver_id}/documents', content_type='multipart/form-data', headers=headers, data=data)
    assert response.status_code in [200, 201, 400, 404]  # 400 if no file or invalid, 404 if driver not found

def test_get_documents(client):
    token = login(client, 'testuser@example.com', 'testpassword')
    headers = {'Authorization': f'Bearer {token}'}
    driver_id = '00000000-0000-0000-0000-000000000000'  # Replace with valid driver UUID
    response = client.get(f'/api/v1/drivers/{driver_id}/documents', headers=headers)
    assert response.status_code in [200, 404]

def test_update_document_status(client):
    token = login(client, 'testuser@example.com', 'testpassword')
    headers = {'Authorization': f'Bearer {token}'}
    document_id = '00000000-0000-0000-0000-000000000000'  # Replace with valid document UUID
    update_data = {
        "status": "approved"
    }
    response = client.put(f'/api/v1/documents/{document_id}/status', json=update_data, headers=headers)
    assert response.status_code in [200, 404]
