from tools.network_tool import network_quality_check


class DeliveryAgent:
    def run(self, narrative, network_quality="good"):
        network = network_quality_check(network_quality)
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
