import unittest
from unittest.mock import patch, mock_open, MagicMock
import os
import tempfile
import json
import n8n_utils

class TestN8nUtils(unittest.TestCase):

    @patch('builtins.open', new_callable=mock_open, read_data="N8N_API_KEY=test_key\nN8N_HOST=http://test.com\n")
    @patch('os.path.exists', return_value=True)
    def test_load_n8n_config(self, mock_exists, mock_file):
        host, key = n8n_utils.load_n8n_config(".env")
        self.assertEqual(host, "http://test.com/")
        self.assertEqual(key, "test_key")

    @patch('urllib.request.urlopen')
    def test_n8n_request_success(self, mock_urlopen):
        mock_response = MagicMock()
        mock_response.read.return_value = json.dumps({"status": "ok"}).encode('utf-8')
        mock_response.__enter__.return_value = mock_response
        mock_urlopen.return_value = mock_response

        res, err = n8n_utils.n8n_request("/test", "http://test.com/", "test_key")
        self.assertEqual(res, {"status": "ok"})
        self.assertIsNone(err)

    @patch('urllib.request.urlopen')
    def test_n8n_request_with_data(self, mock_urlopen):
        mock_response = MagicMock()
        mock_response.read.return_value = json.dumps({"status": "ok"}).encode('utf-8')
        mock_response.__enter__.return_value = mock_response
        mock_urlopen.return_value = mock_response

        res, err = n8n_utils.n8n_request("/test", "http://test.com/", "test_key", method="POST", data={"name": "test"})
        self.assertEqual(res, {"status": "ok"})
        self.assertIsNone(err)

if __name__ == '__main__':
    unittest.main()
