import unittest
from unittest.mock import patch

from fastapi.testclient import TestClient

from api.main import app


class GenerateEndpointTest(unittest.TestCase):
    def setUp(self):
        self.client = TestClient(app)

    def test_generate_returns_story(self):
        response = self.client.post(
            "/generate",
            json={
                "user_id": "1",
                "latitude": 18.5196,
                "longitude": 73.8553,
            },
        )

        self.assertEqual(response.status_code, 200)
        body = response.json()
        self.assertEqual(body["place"], "Shaniwar Wada")
        self.assertTrue(body["text"]["story"])
        self.assertTrue(body["safe"])

    def test_generate_rejects_invalid_coordinates(self):
        response = self.client.post(
            "/generate",
            json={
                "user_id": "1",
                "latitude": 200,
                "longitude": 73.8553,
            },
        )

        self.assertEqual(response.status_code, 422)

    def test_generate_rejects_missing_user(self):
        response = self.client.post(
            "/generate",
            json={
                "latitude": 18.5196,
                "longitude": 73.8553,
            },
        )

        self.assertEqual(response.status_code, 422)

    def test_generate_rejects_empty_story(self):
        with patch(
            "agents.narrative_agent.NarrativeAgent.run",
            return_value={"story": "", "facts": [], "language": "English"},
        ):
            response = self.client.post(
                "/generate",
                json={
                    "user_id": "1",
                    "latitude": 18.5196,
                    "longitude": 73.8553,
                },
            )

        self.assertEqual(response.status_code, 502)


if __name__ == "__main__":
    unittest.main()
