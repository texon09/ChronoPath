
class NarrativeAgent:
    async def execute(self, state):
        context = state.get("context")
        narrative = self.run(context)
        state.set("story", narrative)
        return state

    def run(self, context):
        place = context["place"]
        era = context["context"]
        language = context["language"]
        interests = context.get("interests", [])

        architecture_line = ""
        if "architecture" in interests:
            architecture_line = (
                " Notice the idea of power expressed through gates, courtyards, "
                "and controlled entrances."
            )

        story = (
            f"You are standing near {place}, where Pune once moved to the rhythm "
            f"of the {era}. In the 18th century, this was not just a landmark; "
            f"it was a command center where political decisions, alliances, and "
            f"daily court life shaped the Maratha world.{architecture_line} "
            f"As you continue your route, imagine messengers, guards, nobles, "
            f"and citizens passing through this space, each carrying a small "
            f"piece of the city's memory."
        )

        return {
            "story": story,
            "facts": context.get("facts", []),
            "language": language,
        }

