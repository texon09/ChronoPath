from tools.profile_tool import profile_lookup


class ProfileAgent:
    def run(self, payload):
        return profile_lookup(payload["user_id"])
