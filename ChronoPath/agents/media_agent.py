import os
import uuid
import asyncio
import urllib.parse
from gtts import gTTS

class MediaAgent:
    def __init__(self):
        # We ensure media directory exists to save gTTS files
        os.makedirs("media", exist_ok=True)
        # Using a default localhost URL for the static media files.
        # In a real deployed environment, this would be an environment variable.
        self.base_url = os.getenv("API_BASE_URL", "http://localhost:8000")

    async def execute(self, state):
        narrative = state.get("story", {}).get("story", "")
        place = state.get("location", {}).get("place", "Historical Location")
        language_name = state.get("profile", {}).get("language", "English")

        if not narrative:
            return state

        # Run TTS and Image Generation in parallel
        audio_task = self._generate_audio(narrative, language_name)
        visual_task = self._generate_visual(place, narrative)

        audio_res, visual_res = await asyncio.gather(audio_task, visual_task)

        state.set("media", {
            "audio_url": audio_res.get("url", ""),
            "visual_url": visual_res.get("url", ""),
        })
        return state

    async def _generate_audio(self, text: str, language_name: str) -> dict:
        loop = asyncio.get_running_loop()
        
        # Map English names to gTTS language codes
        lang_map = {
            "marathi": "mr",
            "hindi": "hi",
            "french": "fr",
            "spanish": "es",
            "english": "en"
        }
        lang_code = lang_map.get(language_name.lower(), "en")
        
        def _generate():
            try:
                # Use the mapped language code, default to 'en'
                tts = gTTS(text=text[:1500], lang=lang_code, slow=False)
                filename = f"audio_{uuid.uuid4().hex}.mp3"
                filepath = os.path.join("media", filename)
                tts.save(filepath)
                return f"{self.base_url}/media/{filename}"
            except Exception as e:
                print(f"gTTS Error: {e}")
                return ""

        try:
            url = await loop.run_in_executor(None, _generate)
            return {"url": url}
        except Exception:
            return {"url": ""}

    async def _generate_visual(self, place: str, narrative: str) -> dict:
        # We use Pollinations.ai for completely free, instant, and high-quality image generation.
        # It directly returns an image URL based on the URL-encoded prompt.
        prompt = f"A cinematic, historically accurate depiction of {place}. Highly detailed, atmospheric."
        encoded_prompt = urllib.parse.quote(prompt)
        url = f"https://image.pollinations.ai/prompt/{encoded_prompt}?width=1024&height=576&nologo=true"
        
        return {"url": url}
