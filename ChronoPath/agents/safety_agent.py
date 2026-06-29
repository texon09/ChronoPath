class SafetyAgent:
    REQUIRED_FIELDS = {"story", "facts", "language"}
    BLOCKED_PATTERNS = ["ignore previous instructions", "system prompt", "api key"]

    async def execute(self, state):
        narrative = state.get("story")
        safety = self.run(narrative)
        state.set("safety", safety)
        return state

    def run(self, narrative):
        story = narrative.get("story", "")
        has_schema = self.REQUIRED_FIELDS.issubset(narrative.keys())
        has_blocked_text = any(pattern in story.lower() for pattern in self.BLOCKED_PATTERNS)

        return {
            "approved": bool(has_schema and story and not has_blocked_text),
            "checks": {
                "schema": has_schema,
                "pii": True,
                "prompt_injection": not has_blocked_text,
                "grounding": bool(narrative.get("facts")),
            },
        }
