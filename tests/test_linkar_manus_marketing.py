import sys
import json
import urllib.error
from unittest.mock import patch, mock_open, MagicMock

# Mock out sys.exit, open, and urlopen before importing
with patch('sys.exit'), patch('builtins.open', mock_open(read_data='N8N_API_KEY=test_key\nN8N_HOST=http://test_host/')), patch('urllib.request.urlopen'):
    import linkar_manus_marketing

def test_n8n_request_success():
    with patch('urllib.request.urlopen') as mock_urlopen:
        mock_response = MagicMock()
        mock_response.read.return_value = b'{"success": true}'
        mock_response.__enter__.return_value = mock_response
        mock_urlopen.return_value = mock_response

        res, err = linkar_manus_marketing.n8n_request('test-endpoint')

        assert err is None
        assert res == {"success": True}

        # Verify the request URL and headers
        request_obj = mock_urlopen.call_args[0][0]
        assert request_obj.full_url == 'http://test_host/test-endpoint'
        assert request_obj.get_header('X-n8n-api-key') == 'test_key'
        assert request_obj.get_header('Accept') == 'application/json'

def test_n8n_request_with_data():
    with patch('urllib.request.urlopen') as mock_urlopen:
        mock_response = MagicMock()
        mock_response.read.return_value = b'{"updated": true}'
        mock_response.__enter__.return_value = mock_response
        mock_urlopen.return_value = mock_response

        data = {"key": "value"}
        res, err = linkar_manus_marketing.n8n_request('test-endpoint', method='PUT', data=data)

        assert err is None
        assert res == {"updated": True}

        request_obj = mock_urlopen.call_args[0][0]
        assert request_obj.method == 'PUT'
        assert request_obj.data == b'{"key": "value"}'
        assert request_obj.get_header('Content-type') == 'application/json'

def test_n8n_request_http_error():
    with patch('urllib.request.urlopen') as mock_urlopen:
        mock_error = urllib.error.HTTPError(
            url='http://test_host/test-endpoint',
            code=404,
            msg='Not Found',
            hdrs={},
            fp=MagicMock()
        )
        mock_error.read = MagicMock(return_value=b'Not found error message')
        mock_urlopen.side_effect = mock_error

        res, err = linkar_manus_marketing.n8n_request('test-endpoint')

        assert res is None
        assert err == "HTTP 404: Not found error message"

def test_n8n_request_general_error():
    with patch('urllib.request.urlopen') as mock_urlopen:
        mock_urlopen.side_effect = Exception("Connection refused")

        res, err = linkar_manus_marketing.n8n_request('test-endpoint')

        assert res is None
        assert err == "Connection refused"
