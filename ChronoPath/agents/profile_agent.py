from tools.profile_tool import profile_lookup


class ProfileAgent:
    async def execute(self, state):
        request = state.get("request")
        profile = await self.run(request)
        state.set("profile", profile)
        return state

    async def run(self, payload):
        return await profile_lookup(payload["user_id"])

