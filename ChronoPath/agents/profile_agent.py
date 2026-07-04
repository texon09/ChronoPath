from tools.profile_tool import profile_lookup


class ProfileAgent:
    async def execute(self, state):
        request = state.get("request")
        profile = await self.run(request)
        state.set("profile", profile)
        return state

    async def run(self, payload):
        profile = await profile_lookup(payload["user_id"])
        # Override DB values with explicitly provided request values
        if payload.get("language"):
            profile["language"] = payload["language"]
        if payload.get("age"):
            profile["age"] = payload["age"]
        if payload.get("origin"):
            profile["origin"] = payload["origin"]
        if payload.get("background"):
            profile["background"] = payload["background"]
        return profile

