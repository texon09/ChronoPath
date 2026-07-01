from tools.journey_tool import journey_lookup


class JourneyAgent:
    async def execute(self, state):
        request = state.get("request")
        journey = await self.run(request)
        state.set("journey", journey)
        return state

    async def run(self, payload):
        return await journey_lookup(payload["user_id"])

