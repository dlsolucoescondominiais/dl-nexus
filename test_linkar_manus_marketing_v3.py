import sys
import unittest
from unittest.mock import patch, MagicMock, mock_open
import json
import urllib.error

# Patch sys.exit and open to prevent early exit and FileNotFoundError
mock_exit = patch('sys.exit').start()
mock_file = patch('builtins.open', mock_open(read_data="N8N_API_KEY=mock_key\nN8N_HOST=http://mock-host")).start()

# Patch urlopen to prevent top-level API calls during import
mock_urlopen_import = patch('urllib.request.urlopen').start()
mock_response_import = MagicMock()
mock_response_import.read.return_value = b'{"nodes": [], "connections": {}}'
mock_urlopen_import.return_value.__enter__.return_value = mock_response_import

import linkar_manus_marketing_v3

class TestN8nRequest(unittest.TestCase):

    @patch('urllib.request.urlopen')
    def test_n8n_request_success(self, mock_urlopen):
        mock_response = MagicMock()
        mock_response.read.return_value = b'{"status": "success"}'
        mock_urlopen.return_value.__enter__.return_value = mock_response

        res, err = linkar_manus_marketing_v3.n8n_request("test", method="GET")
        self.assertEqual(res, {"status": "success"})
        self.assertIsNone(err)

    @patch('urllib.request.urlopen')
    def test_n8n_request_with_data(self, mock_urlopen):
        mock_response = MagicMock()
        mock_response.read.return_value = b'{"status": "success"}'
        mock_urlopen.return_value.__enter__.return_value = mock_response

        data = {"key": "value"}
        res, err = linkar_manus_marketing_v3.n8n_request("test", method="POST", data=data)
        self.assertEqual(res, {"status": "success"})
        self.assertIsNone(err)

        # Verify request parameters
        req = mock_urlopen.call_args[0][0]
        self.assertEqual(req.method, "POST")
        self.assertEqual(req.data, b'{"key": "value"}')
        self.assertEqual(req.get_header("Content-type").lower(), "application/json")

    @patch('urllib.request.urlopen')
    def test_n8n_request_http_error(self, mock_urlopen):
        fp = MagicMock()
        fp.read.return_value = b'Not found'
        err_mock = urllib.error.HTTPError("http://mock-host/test", 404, "Not Found", {}, fp)
        mock_urlopen.side_effect = err_mock

        res, err = linkar_manus_marketing_v3.n8n_request("test", method="GET")
        self.assertIsNone(res)
        self.assertEqual(err, "HTTP 404: Not found")

    @patch('urllib.request.urlopen')
    def test_n8n_request_exception(self, mock_urlopen):
        mock_urlopen.side_effect = Exception("Some general error")

        res, err = linkar_manus_marketing_v3.n8n_request("test", method="GET")
        self.assertIsNone(res)
        self.assertEqual(err, "Some general error")

if __name__ == '__main__':
    unittest.main()
