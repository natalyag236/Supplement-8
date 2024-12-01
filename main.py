from unittest.mock import patch  
from main import get_request 

def test_returns_status_code_and_response_text():
    with patch('requests.get') as mock_request:
        url = 'https://echo.free.beeceptor.com'

        mock_request.return_value.status_code = 200
        mock_request.return_value.headers = {'Content-Type': 'text/plain'}
        mock_request.return_value.text = "Hello, world!"

        status_code, response = get_request(url)
        assert status_code == 200
        assert response == "Hello, world!"

def test_returns_status_code_and_json_when_json_content_type():
    with patch('requests.get') as mock_request:
        url = 'https://echo.free.beeceptor.com'

        mock_request.return_value.status_code = 200
        mock_request.return_value.headers = {'Content-Type': 'application/json'}
        mock_request.return_value.json.return_value = {'key': 'value'}

        status_code, response = get_request(url)
        assert status_code == 200
        assert response == {'key': 'value'}

def test_raises_exception_for_client_error():
    with patch('requests.get') as mock_request:
        url = 'https://echo.free.beeceptor.com'

        mock_request.return_value.status_code = 404
        mock_request.return_value.text = "Not Found"

        result = get_request(url)
        assert result == "Error: Client error: 404"

