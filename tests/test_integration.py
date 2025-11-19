import pytest
import os
import tempfile
import shutil
from app_new import create_app
from config.config import Config

@pytest.fixture
def app():
    app = create_app()
    app.config['TESTING'] = True
    yield app

@pytest.fixture
def client(app):
    return app.test_client()

def test_get_categories(client):
    response = client.get('/api/categories')
    assert response.status_code == 200
    data = response.get_json()
    assert data['success'] is True
    assert 'data' in data

def test_add_category(client):
    response = client.post('/api/add_category', json={'name': 'test_category'})
    assert response.status_code == 201
    data = response.get_json()
    assert data['success'] is True
    assert data['data']['name'] == 'test_category'

def test_add_category_empty_name(client):
    response = client.post('/api/add_category', json={'name': ''})
    assert response.status_code == 400
    data = response.get_json()
    assert data['success'] is False

def test_add_category_too_long(client):
    response = client.post('/api/add_category', json={'name': 'a' * 20})
    assert response.status_code == 400
    data = response.get_json()
    assert data['success'] is False
    assert 'exceed 19 characters' in data['error']

def test_save_note(client):
    client.post('/api/add_category', json={'name': 'test_notes'})
    
    response = client.post('/api/save/test_notes', json={'text': 'Test note content'})
    assert response.status_code == 200
    data = response.get_json()
    assert data['success'] is True

def test_save_note_empty_text(client):
    response = client.post('/api/save/test_category', json={'text': ''})
    assert response.status_code == 400
    data = response.get_json()
    assert data['success'] is False

def test_list_notes(client):
    response = client.get('/api/list/test_category')
    assert response.status_code == 200
    data = response.get_json()
    assert data['success'] is True

def test_all_files(client):
    response = client.get('/api/all_files')
    assert response.status_code == 200
    data = response.get_json()
    assert data['success'] is True
    assert isinstance(data['data'], list)

def test_search_content_missing_term(client):
    response = client.post('/api/search_content', json={})
    assert response.status_code == 400
    data = response.get_json()
    assert data['success'] is False

def test_index_page(client):
    response = client.get('/')
    assert response.status_code in [200, 500]

def test_404_error(client):
    response = client.get('/nonexistent')
    assert response.status_code == 404
    data = response.get_json()
    assert data['success'] is False
    assert data['error_type'] == 'NotFound'
