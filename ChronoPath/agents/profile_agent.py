from tools.profile_tool import profile_lookup


class ProfileAgent:
    async def execute(self, state):
        request = state.get("request")
        profile = self.run(request)
        state.set("profile", profile)
        return state

    def run(self, payload):
        return profile_lookup(payload["user_id"])
