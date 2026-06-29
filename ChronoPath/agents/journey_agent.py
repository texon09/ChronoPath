from tools.journey_tool import journey_lookup


class JourneyAgent:
    async def execute(self, state):
        request = state.get("request")
        journey = self.run(request)
        state.set("journey", journey)
        return state

    def run(self, payload):
        return journey_lookup(payload["user_id"])
