import unittest

from schemas import GenerateRequest, GenerateResponse


class ContractTest(unittest.TestCase):
    def test_generate_request_accepts_valid_coordinates(self):
        request = GenerateRequest(user_id="1", lat=18.5196, lng=73.8553)

        self.assertEqual(request.user_id, "1")
        self.assertEqual(request.lat, 18.5196)
        self.assertEqual(request.lng, 73.8553)

    def test_generate_response_contract_matches_final_shape(self):
        payload = {
            "request_id": "req-1",
            "place": {"id": "place-1", "name": "Shaniwar Wada"},
            "text": {
                "title": "Shaniwar Wada",
                "story": "A historical narrative.",
                "facts": ["Built in 1732."],
            },
            "audio": {"url": "gs://bucket/audio/story.mp3", "duration": 42},
            "visual": {"url": "gs://bucket/images/story.png"},
            "metadata": {"latency_ms": 1200, "cached": False},
        }

        response = GenerateResponse(**payload)

        self.assertEqual(response.place.name, "Shaniwar Wada")
        self.assertEqual(response.text.facts, ["Built in 1732."])


if __name__ == "__main__":
    unittest.main()
