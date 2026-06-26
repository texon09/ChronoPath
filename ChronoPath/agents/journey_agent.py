from tools.journey_tool import journey_lookup


class JourneyAgent:
    def run(self, payload):
        return journey_lookup(payload["user_id"])
