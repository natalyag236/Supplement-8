from unittest.mock import patch  
from main import get_request 
import requests

def get_request(url):
    """
    Sends an HTTP GET request to the specified URL and returns the response details.

    Args:
        url (str): The URL to which the GET request is sent.

    Returns:
        tuple: A tuple containing the status code and the response content. 
              

    Raises:
        Exception: If the status code is in the range 400 to 499, a client error exception is raised.
    """
    try:
        response = requests.get(url)

        if 400 <= response.status_code <= 499:
            raise Exception(f"Client error: {response.status_code}")

        if 'application/json' in response.headers.get('Content-Type', ''):
            return response.status_code, response.json()

        return response.status_code, response.text

    except Exception as e:
        return f"Error: {e}"


def test_returns_status_code_and_response_text():
    from main import get_request  

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


def get__token_and_ip(url):
    """Sends a GET request to the given URL and extracts the Postman
    token and IP address from the response headers

    Args:
        url (str): The URL to which the GET request is sent

    Returns:
        tuple: a tuple containig the postman token and ip address from the respone headers
    """
    response = requests.get(url)
    
    postman_token = response.headers.get('Postman-Token', None)
    ip_address = response.headers.get('X-Forwarded-For', None)

    return postman_token, ip_address

def test_raises_exception_for_client_error():
    with patch('requests.get') as mock_request:
        url = 'https://echo.free.beeceptor.com'

        mock_request.return_value.status_code = 404
        mock_request.return_value.text = "Not Found"

        result = get_request(url)
        assert result == "Error: Client error: 404"

def test_get_token_and_ip():
    with patch('requests.get') as mock_request:
        url = 'https://echo.free.beeceptor.com'
        
        mock_request.return_value.headers = {
            'Postman-Token': '1234567890abcdef',
            'X-Forwarded-For': '192.168.1.1'
        }

        postman_token, ip_address = get__token_and_ip(url)
        
        assert postman_token == '1234567890abcdef'
        assert ip_address == '192.168.1.1'

def test_post_request():
    url = 'https://echo.free.beeceptor.com'
    payload = {'hello': 'world'}
    
    response = requests.post(url, json=payload)
    
    
    print(f"Status Code: {response.status_code}")
    print(f"Response JSON: {response.json()}")


