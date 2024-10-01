import os
import unittest
from unittest.mock import MagicMock, patch
from crewai.cli.plus_api import PlusAPI


class TestPlusAPI(unittest.TestCase):
    def setUp(self):
        self.api_key = "test_api_key"
        self.api = PlusAPI(self.api_key)

    def test_init(self):
        self.assertEqual(self.api.api_key, self.api_key)
        self.assertEqual(
            self.api.headers,
            {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json",
                "User-Agent": "CrewAI-CLI/no-version-found",
                "X-Crewai-Version": "no-version-found",
            },
        )

    @patch("crewai.cli.plus_api.PlusAPI._make_request")
    def test_get_tool(self, mock_make_request):
        mock_response = MagicMock()
        mock_make_request.return_value = mock_response

        response = self.api.get_tool("test_tool_handle")

        mock_make_request.assert_called_once_with(
            "GET", "/crewai_plus/api/v1/tools/test_tool_handle"
        )
        self.assertEqual(response, mock_response)

    @patch("crewai.cli.plus_api.PlusAPI._make_request")
    def test_publish_tool(self, mock_make_request):
        mock_response = MagicMock()
        mock_make_request.return_value = mock_response
        handle = "test_tool_handle"
        public = True
        version = "1.0.0"
        description = "Test tool description"
        encoded_file = "encoded_test_file"

        response = self.api.publish_tool(
            handle, public, version, description, encoded_file
        )

        params = {
            "handle": handle,
            "public": public,
            "version": version,
            "file": encoded_file,
            "description": description,
        }
        mock_make_request.assert_called_once_with(
            "POST", "/crewai_plus/api/v1/tools", json=params
        )
        self.assertEqual(response, mock_response)

    @patch("crewai.cli.plus_api.PlusAPI._make_request")
    def test_publish_tool_without_description(self, mock_make_request):
        mock_response = MagicMock()
        mock_make_request.return_value = mock_response
        handle = "test_tool_handle"
        public = False
        version = "2.0.0"
        description = None
        encoded_file = "encoded_test_file"

        response = self.api.publish_tool(
            handle, public, version, description, encoded_file
        )

        params = {
            "handle": handle,
            "public": public,
            "version": version,
            "file": encoded_file,
            "description": description,
        }
        mock_make_request.assert_called_once_with(
            "POST", "/crewai_plus/api/v1/tools", json=params
        )
        self.assertEqual(response, mock_response)

    @patch("crewai.cli.plus_api.requests.request")
    def test_make_request(self, mock_request):
        mock_response = MagicMock()
        mock_request.return_value = mock_response

        response = self.api._make_request("GET", "test_endpoint")

        mock_request.assert_called_once_with(
            "GET", f"{self.api.base_url}/test_endpoint", headers=self.api.headers
        )
        self.assertEqual(response, mock_response)

    @patch("crewai.cli.plus_api.PlusAPI._make_request")
    def test_deploy_by_name(self, mock_make_request):
        self.api.deploy_by_name("test_project")
        mock_make_request.assert_called_once_with(
            "POST", "/crewai_plus/api/v1/crews/by-name/test_project/deploy"
        )

    @patch("crewai.cli.plus_api.PlusAPI._make_request")
    def test_deploy_by_uuid(self, mock_make_request):
        self.api.deploy_by_uuid("test_uuid")
        mock_make_request.assert_called_once_with(
            "POST", "/crewai_plus/api/v1/crews/test_uuid/deploy"
        )

    @patch("crewai.cli.plus_api.PlusAPI._make_request")
    def test_crew_status_by_name(self, mock_make_request):
        self.api.crew_status_by_name("test_project")
        mock_make_request.assert_called_once_with(
            "GET", "/crewai_plus/api/v1/crews/by-name/test_project/status"
        )

    @patch("crewai.cli.plus_api.PlusAPI._make_request")
    def test_crew_status_by_uuid(self, mock_make_request):
        self.api.crew_status_by_uuid("test_uuid")
        mock_make_request.assert_called_once_with(
            "GET", "/crewai_plus/api/v1/crews/test_uuid/status"
        )

    @patch("crewai.cli.plus_api.PlusAPI._make_request")
    def test_crew_by_name(self, mock_make_request):
        self.api.crew_by_name("test_project")
        mock_make_request.assert_called_once_with(
            "GET", "/crewai_plus/api/v1/crews/by-name/test_project/logs/deployment"
        )

        self.api.crew_by_name("test_project", "custom_log")
        mock_make_request.assert_called_with(
            "GET", "/crewai_plus/api/v1/crews/by-name/test_project/logs/custom_log"
        )

    @patch("crewai.cli.plus_api.PlusAPI._make_request")
    def test_crew_by_uuid(self, mock_make_request):
        self.api.crew_by_uuid("test_uuid")
        mock_make_request.assert_called_once_with(
            "GET", "/crewai_plus/api/v1/crews/test_uuid/logs/deployment"
        )

        self.api.crew_by_uuid("test_uuid", "custom_log")
        mock_make_request.assert_called_with(
            "GET", "/crewai_plus/api/v1/crews/test_uuid/logs/custom_log"
        )

    @patch("crewai.cli.plus_api.PlusAPI._make_request")
    def test_delete_crew_by_name(self, mock_make_request):
        self.api.delete_crew_by_name("test_project")
        mock_make_request.assert_called_once_with(
            "DELETE", "/crewai_plus/api/v1/crews/by-name/test_project"
        )

    @patch("crewai.cli.plus_api.PlusAPI._make_request")
    def test_delete_crew_by_uuid(self, mock_make_request):
        self.api.delete_crew_by_uuid("test_uuid")
        mock_make_request.assert_called_once_with(
            "DELETE", "/crewai_plus/api/v1/crews/test_uuid"
        )

    @patch("crewai.cli.plus_api.PlusAPI._make_request")
    def test_list_crews(self, mock_make_request):
        self.api.list_crews()
        mock_make_request.assert_called_once_with("GET", "/crewai_plus/api/v1/crews")

    @patch("crewai.cli.plus_api.PlusAPI._make_request")
    def test_create_crew(self, mock_make_request):
        payload = {"name": "test_crew"}
        self.api.create_crew(payload)
        mock_make_request.assert_called_once_with(
            "POST", "/crewai_plus/api/v1/crews", json=payload
        )

    @patch.dict(os.environ, {"CREWAI_BASE_URL": "https://custom-url.com/api"})
    def test_custom_base_url(self):
        custom_api = PlusAPI("test_key")
        self.assertEqual(
            custom_api.base_url,
            "https://custom-url.com/api",
        )