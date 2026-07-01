import unittest

from agents.supervisor import SupervisorAgent


class MvpFlowTest(unittest.TestCase):
    @unittest.mock.patch("agents.location_agent.reverse_geocode")
    @unittest.mock.patch("agents.location_agent.heritage_lookup")
    @unittest.mock.patch("agents.location_agent.fetch_history")
    def test_success_condition_for_shaniwar_wada(self, mock_history, mock_heritage, mock_geo):
        import asyncio
        async def mock_geo_resp(*args):
            return {"city": "Pune", "state": "MH", "country": "IN", "lat": 18.5196, "lng": 73.8553, "display_name": "Pune"}
        async def mock_heritage_resp(*args):
            return {"place": "Shaniwar Wada", "lat": 18.5196, "lng": 73.8553, "distance_km": 0.1, "period": "Peshwa Era", "themes": ["History"], "summary": "Seat of Peshwas"}
        async def mock_history_resp(*args):
            return {"context": "Peshwa Era", "facts": ["Built in 1732"]}
            
        mock_geo.side_effect = mock_geo_resp
        mock_heritage.side_effect = mock_heritage_resp
        mock_history.side_effect = mock_history_resp

        response = SupervisorAgent().run(
            {
                "user": "1",
                "lat": 18.5196,
                "lng": 73.8553,
            }
        )

        self.assertEqual(response["place"]["name"], "Shaniwar Wada")
        self.assertIn("Peshwa Era", response["text"]["title"])
        self.assertTrue(response["text"]["story"])
        self.assertTrue(response["safe"])


if __name__ == "__main__":
    unittest.main()
