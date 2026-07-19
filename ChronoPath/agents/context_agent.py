from tools.journey_tool import semantic_search_journeys

class ContextAggregator:
    async def execute(self, state):
        location = state.get("location")
        profile = state.get("profile", {})
        journey = state.get("journey", {})
        request = state.get("request", {})
        user_id = request.get("user_id")
        
        # Try semantic search if we have a user and location
        semantic_memory = ""
        if user_id and location and location.get("place"):
            query = f"I am visiting {location['place']}, tell me something related to my past travels."
            past_story = await semantic_search_journeys(user_id, query)
            if past_story:
                semantic_memory = f"SEMANTIC MEMORY (Prioritize drawing an analogy to this past trip): {past_story}"
        
        context = self.run(location, profile, journey, semantic_memory)
        state.set("context", context)
        return state

    def run(self, location, profile, journey, semantic_memory):
        interests = ", ".join(profile.get("interests", [])) or "history"
        visited = ", ".join(journey.get("visited_places", [])) or "no prior stops"
        facts = location.get("facts", [])

        prompt = (
            f"{location['place']} in Pune belongs to the "
            f"{location['historical_context']}. The user likes {interests}. "
            f"They have already visited {visited}. Key facts: {' '.join(facts)}. "
        )
        if semantic_memory:
            prompt += f"\n\n{semantic_memory}\n"

        return {
            "context": location["historical_context"],
            "place": location["place"],
            "language": profile.get("language", "English"),
            "tone": profile.get("tone", "clear"),
            "interests": profile.get("interests", []),
            "age": profile.get("age"),
            "origin": profile.get("origin"),
            "background": profile.get("background"),
            "name": profile.get("name"),
            "visited_places": journey.get("visited_places", []),
            "facts": facts,
            "prompt_context": prompt,
        }
