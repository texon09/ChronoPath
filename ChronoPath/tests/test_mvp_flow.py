import unittest

from agents.supervisor import SupervisorAgent


class MvpFlowTest(unittest.TestCase):
    def test_success_condition_for_shaniwar_wada(self):
        response = SupervisorAgent().run(
            {
                "user": "1",
                "lat": 18.5196,
                "lng": 73.8553,
            }
        )

        self.assertEqual(response["place"], "Shaniwar Wada")
        self.assertEqual(response["context"], "Peshwa Era")
        self.assertTrue(response["story"])


if __name__ == "__main__":
    unittest.main()
