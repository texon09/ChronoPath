from tools.network_tool import network_quality_check


class DeliveryAgent:
    async def execute(self, state):
        narrative = state.get("story")
        request = state.get("request", {})
        delivery = await self.run(
            narrative,
            network_quality=request.get("network_quality", "good"),
        )
        state.set("delivery", delivery)
        return state

    async def run(self, narrative, network_quality="good"):
        network = await network_quality_check(network_quality)
        quality = network["quality"]

        if quality == "low":
            mode = "text"
            media = None
        elif quality == "medium":
            mode = "audio"
            media = "audio-placeholder.mp3"
        else:
            mode = "full"
            media = "visual-placeholder.png"

        return {
            "mode": mode,
            "media": media,
            "network": network,
            "story": narrative["story"],
        }

