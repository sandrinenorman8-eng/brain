import pytest
from utils.response_utils import success_response, error_response

def test_success_response_basic():
    response, status_code = success_response()
    assert status_code == 200
    assert response.json['success'] is True
    assert response.json['message'] == "Success"
    assert 'timestamp' in response.json

def test_success_response_with_data():
    data = {"key": "value"}
    response, status_code = success_response(data, "Custom message", 201)
    assert status_code == 201
    assert response.json['success'] is True
    assert response.json['message'] == "Custom message"
    assert response.json['data'] == data

def test_error_response_basic():
    response, status_code = error_response()
    assert status_code == 400
    assert response.json['success'] is False
    assert response.json['error'] == "Error"
    assert response.json['error_type'] == "BadRequest"
    assert 'timestamp' in response.json

def test_error_response_custom():
    response, status_code = error_response("Not found", 404, "NotFound")
    assert status_code == 404
    assert response.json['error'] == "Not found"
    assert response.json['error_type'] == "NotFound"
