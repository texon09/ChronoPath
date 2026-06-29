import unittest

from schemas import GenerateRequest, GenerateResponse


class ContractTest(unittest.TestCase):
    def test_generate_request_accepts_valid_coordinates(self):
        request = GenerateRequest(user_id="1", latitude=18.5196, longitude=73.8553)

        self.assertEqual(request.user_id, "1")
        self.assertEqual(request.latitude, 18.5196)
        self.assertEqual(request.longitude, 73.8553)

    def test_generate_request_accepts_legacy_lat_lng(self):
        request = GenerateRequest(user_id="1", lat=18.5196, lng=73.8553)

        self.assertEqual(request.latitude, 18.5196)
        self.assertEqual(request.longitude, 73.8553)

    def test_generate_response_contract_matches_final_shape(self):
        payload = {
            "request_id": "req-1",
            "place": "Shaniwar Wada",
            "text": {
                "title": "Shaniwar Wada",
                "story": "A historical narrative.",
            },
            "safe": True,
        }

        response = GenerateResponse(**payload)

        self.assertEqual(response.place, "Shaniwar Wada")
        self.assertTrue(response.safe)


if __name__ == "__main__":
    unittest.main()
