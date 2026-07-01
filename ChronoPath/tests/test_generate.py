import unittest
from unittest.mock import patch
from fastapi.testclient import TestClient
from api.main import app

class GenerateEndpointTest(unittest.TestCase):
    def setUp(self):
        self.client = TestClient(app)

    @patch('agents.supervisor.SupervisorAgent.execute')
    def test_generate_returns_story(self, mock_execute):
        # We mock execute because it has real API integrations now
        import asyncio
        from schemas.response import GenerateResponse, PlaceResponse, TextResponse, AudioResponse, VisualResponse, MetaResponse
        mock_resp = GenerateResponse(
            request_id="123",
            place=PlaceResponse(id="Shaniwar Wada", name="Shaniwar Wada"),
            text=TextResponse(title="Shaniwar Wada", story="Test story"),
            audio=AudioResponse(url="http://audio", duration="1:00"),
            visual=VisualResponse(url="http://img"),
            safe=True,
            meta=MetaResponse(latency_ms="100.0", cache_hit="false")
        )
        
        mock_execute.return_value = mock_resp
        
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
        self.assertEqual(body["place"]["name"], "Shaniwar Wada")
        self.assertTrue(body["text"]["story"])
        self.assertTrue(body["safe"])
        self.assertTrue("audio" in body)
        self.assertTrue("visual" in body)
        self.assertTrue("meta" in body)

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

if __name__ == "__main__":
    unittest.main()
