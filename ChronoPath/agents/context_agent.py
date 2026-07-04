
class ContextAggregator:
    async def execute(self, state):
        location = state.get("location")
        profile = state.get("profile", {})
        journey = state.get("journey", {})
        context = self.run(location, profile, journey)
        state.set("context", context)
        return state

    def run(self, location, profile, journey):
        interests = ", ".join(profile.get("interests", [])) or "history"
        visited = ", ".join(journey.get("visited_places", [])) or "no prior stops"
        facts = location.get("facts", [])

        return {
            "context": location["historical_context"],
            "place": location["place"],
            "language": profile.get("language", "English"),
            "tone": profile.get("tone", "clear"),
            "interests": profile.get("interests", []),
            "age": profile.get("age"),
            "origin": profile.get("origin"),
            "background": profile.get("background"),
            "visited_places": journey.get("visited_places", []),
            "facts": facts,
            "prompt_context": (
                f"{location['place']} in Pune belongs to the "
                f"{location['historical_context']}. The user likes {interests}. "
                f"They have already visited {visited}. Key facts: {' '.join(facts)}"
            ),
        }

