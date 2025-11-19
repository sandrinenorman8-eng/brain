import pytest
from unittest.mock import Mock, patch
from utils.http_utils import post_json
import requests

def test_post_json_success():
    with patch('requests.post') as mock_post:
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"result": "success"}
        mock_post.return_value = mock_response
        
        response = post_json("http://test.com", {"data": "test"})
        
        assert response.status_code == 200
        assert response.json() == {"result": "success"}

def test_post_json_connection_error():
    with patch('requests.post') as mock_post:
        mock_post.side_effect = requests.exceptions.ConnectionError()
        
        with pytest.raises(ConnectionError, match="Failed to connect"):
            post_json("http://test.com", {"data": "test"}, max_retries=0)

def test_post_json_timeout():
    with patch('requests.post') as mock_post:
        mock_post.side_effect = requests.exceptions.Timeout()
        
        with pytest.raises(TimeoutError, match="timed out"):
            post_json("http://test.com", {"data": "test"}, max_retries=0)

def test_post_json_retry():
    with patch('requests.post') as mock_post:
        mock_response = Mock()
        mock_response.status_code = 200
        mock_post.side_effect = [
            requests.exceptions.ConnectionError(),
            mock_response
        ]
        
        response = post_json("http://test.com", {"data": "test"}, max_retries=2)
        
        assert response.status_code == 200
        assert mock_post.call_count == 2
