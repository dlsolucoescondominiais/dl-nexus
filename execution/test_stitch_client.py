import unittest
from unittest.mock import MagicMock, patch
from execution.stitch_integration import StitchClient
import requests

class TestStitchClient(unittest.TestCase):

    def setUp(self):
        self.api_key = "test_api_key"
        self.base_url = "https://test.stitch.dev/v1"
        self.client = StitchClient(self.api_key, self.base_url)

    def test_init(self):
        self.assertEqual(self.client.api_key, self.api_key)
        self.assertEqual(self.client.base_url, self.base_url)
        self.assertEqual(self.client.session.headers.get("x-goog-api-key"), self.api_key)
        self.assertEqual(self.client.session.headers.get("Content-Type"), "application/json")

    @patch('execution.stitch_integration.requests.Session.post')
    def test_call_tool_success(self, mock_post):
        mock_response = MagicMock()
        mock_response.json.return_value = {"result": "success"}
        mock_post.return_value = mock_response

        result = self.client.call_tool("test_tool", {"arg1": "value1"})

        self.assertEqual(result, {"result": "success"})
        mock_post.assert_called_once_with(
            self.base_url,
            json={
                "jsonrpc": "2.0",
                "method": "tools/call",
                "params": {
                    "name": "test_tool",
                    "arguments": {"arg1": "value1"}
                },
                "id": 1
            },
            timeout=180
        )

    @patch('execution.stitch_integration.requests.Session.post')
    def test_call_tool_request_exception(self, mock_post):
        mock_post.side_effect = requests.exceptions.RequestException("Test error")

        result = self.client.call_tool("test_tool", {"arg1": "value1"})

        self.assertEqual(result, {"error": "Test error"})

    @patch('execution.stitch_integration.StitchClient.call_tool')
    def test_list_projects(self, mock_call_tool):
        mock_call_tool.return_value = {"result": {"content": [{"id": "1", "name": "Project 1"}]}}

        result = self.client.list_projects()

        self.assertEqual(result, [{"id": "1", "name": "Project 1"}])
        mock_call_tool.assert_called_once_with("list_projects")

    @patch('execution.stitch_integration.StitchClient.call_tool')
    def test_create_project(self, mock_call_tool):
        mock_call_tool.return_value = {"result": "project_created"}

        result = self.client.create_project("New Project")

        self.assertEqual(result, {"result": "project_created"})
        mock_call_tool.assert_called_once_with("create_project", {"title": "New Project"})

    @patch('execution.stitch_integration.StitchClient.call_tool')
    def test_generate_screen(self, mock_call_tool):
        mock_call_tool.return_value = {"result": "screen_generated"}

        result = self.client.generate_screen("proj_1", "Generate a login screen", "MOBILE")

        self.assertEqual(result, {"result": "screen_generated"})
        mock_call_tool.assert_called_once_with("generate_screen_from_text", {
            "projectId": "proj_1",
            "prompt": "Generate a login screen",
            "deviceType": "MOBILE"
        })

    @patch('execution.stitch_integration.StitchClient.call_tool')
    def test_get_screen(self, mock_call_tool):
        mock_call_tool.return_value = {"result": "screen_data"}

        result = self.client.get_screen("proj_1", "screen_1")

        self.assertEqual(result, {"result": "screen_data"})
        mock_call_tool.assert_called_once_with("get_screen", {
            "projectId": "proj_1",
            "screenId": "screen_1"
        })

    @patch('execution.stitch_integration.StitchClient.call_tool')
    def test_edit_screen(self, mock_call_tool):
        mock_call_tool.return_value = {"result": "screen_edited"}

        result = self.client.edit_screen("proj_1", "screen_1", "Make button red")

        self.assertEqual(result, {"result": "screen_edited"})
        mock_call_tool.assert_called_once_with("edit_screen", {
            "project_id": "proj_1",
            "screen_id": "screen_1",
            "text_prompt": "Make button red"
        })

    @patch('execution.stitch_integration.requests.Session.post')
    def test_list_tools_success(self, mock_post):
        mock_response = MagicMock()
        mock_response.json.return_value = {"result": {"tools": [{"name": "tool1"}]}}
        mock_post.return_value = mock_response

        result = self.client.list_tools()

        self.assertEqual(result, [{"name": "tool1"}])
        mock_post.assert_called_once_with(
            self.base_url,
            json={
                "jsonrpc": "2.0",
                "method": "tools/list",
                "params": {},
                "id": 1
            },
            timeout=30
        )

    @patch('execution.stitch_integration.requests.Session.post')
    def test_list_tools_exception(self, mock_post):
        mock_post.side_effect = Exception("Test error")

        result = self.client.list_tools()

        self.assertEqual(result, [])

if __name__ == '__main__':
    unittest.main()
