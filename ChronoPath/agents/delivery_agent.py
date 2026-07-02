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

        # Determine inclusions based on network level
        if quality == "low":
            mode = "text"
            return_text = True
            return_audio = False
            return_visual = False
            media = None
        elif quality == "medium":
            mode = "audio"
            return_text = True
            return_audio = True
            return_visual = False
            media = "audio-placeholder.mp3"
        else: # High / good
            mode = "full"
            return_text = True
            return_audio = True
            return_visual = True
            media = "visual-placeholder.png"

        story_text = narrative.get("story", "") if isinstance(narrative, dict) else ""

        return {
            "mode": mode,
            "return_text": return_text,
            "return_audio": return_audio,
            "return_visual": return_visual,
            "media": media,
            "network": network,
            "story": story_text,
        }


