import os
import uuid
import asyncio
import urllib.parse
from gtts import gTTS

from config import get_settings

class MediaAgent:
    def __init__(self):
        self.settings = get_settings()
        os.makedirs("media", exist_ok=True)
        self.base_url = os.getenv("API_BASE_URL", "http://localhost:8000")
        
        self.bucket_name = os.getenv("GCS_BUCKET_NAME", "chronopath-media-bucket")
        self.project_id = os.getenv("GOOGLE_CLOUD_PROJECT", "")
        self.location = os.getenv("GOOGLE_CLOUD_LOCATION", "us-central1")

        try:
            if self.project_id:
                import vertexai
                vertexai.init(project=self.project_id, location=self.location)
        except Exception:
            pass

    async def execute(self, state):
        print("MEDIA_AGENT_SETTINGS - enable_audio:", self.settings.enable_audio, "enable_visual:", self.settings.enable_visual)
        narrative = state.get("story", {}).get("story", "")
        place = state.get("location", {}).get("place", "Historical Location")

        if not narrative:
            return state

        # Set default local fallback URLs
        audio_url = "/static/audio/fallback.mp3"
        visual_url = "/static/images/fallback.png"

        tasks = []
        task_names = []
        
        language = state.get("story", {}).get("language", "English")

        # Only invoke external APIs if explicitly enabled in configuration settings
        if self.settings.enable_audio:
            tasks.append(self._generate_audio(narrative, language))
            task_names.append("audio")

        if self.settings.enable_visual:
            tasks.append(self._generate_visual(place, narrative))
            task_names.append("visual")

        if tasks:
            results = await asyncio.gather(*tasks)
            for name, res in zip(task_names, results):
                if name == "audio":
                    audio_url = res.get("url", audio_url)
                elif name == "visual":
                    visual_url = res.get("url", visual_url)

        state.set("media", {
            "audio_url": audio_url,
            "visual_url": visual_url,
        })
        return state

    async def _generate_audio(self, text: str, language: str = "English") -> dict:
        lang_map = {
            "english": "en",
            "marathi": "mr",
            "hindi": "hi",
            "spanish": "es",
            "french": "fr"
        }
        lang_code = lang_map.get(language.strip().lower(), "en")

        # 1. Try Google Cloud Text-to-Speech if enabled and credentials exist
        if self.project_id and os.getenv("GOOGLE_APPLICATION_CREDENTIALS"):
            try:
                from google.cloud import texttospeech
                synthesis_input = texttospeech.SynthesisInput(text=text[:1500]) # Cap length
                
                gcp_lang_map = {
                    "en": ("en-IN", "en-IN-Standard-D"),
                    "mr": ("mr-IN", "mr-IN-Standard-A"),
                    "hi": ("hi-IN", "hi-IN-Standard-D"),
                    "es": ("es-ES", "es-ES-Standard-A"),
                    "fr": ("fr-FR", "fr-FR-Standard-A")
                }
                lang_tag, voice_name = gcp_lang_map.get(lang_code, ("en-IN", "en-IN-Standard-D"))
                
                voice = texttospeech.VoiceSelectionParams(
                    language_code=lang_tag,
                    name=voice_name
                )
                audio_config = texttospeech.AudioConfig(
                    audio_encoding=texttospeech.AudioEncoding.MP3
                )
                # Instantiate dynamically on the correct running event loop
                client = texttospeech.TextToSpeechAsyncClient()
                response = await client.synthesize_speech(
                    input=synthesis_input, voice=voice, audio_config=audio_config
                )
                filename = f"audio_{uuid.uuid4().hex}.mp3"
                url = await self._upload_to_gcs(filename, response.audio_content, "audio/mpeg")
                return {"url": url}
            except Exception as e:
                print(f"GCP TTS Error, falling back to gTTS: {e}")

        # 2. Fallback to gTTS (gratis local generation in target language)
        loop = asyncio.get_running_loop()
        def _generate():
            try:
                tts = gTTS(text=text[:1500], lang=lang_code, tld='co.in', slow=False)
                filename = f"audio_{uuid.uuid4().hex}.mp3"
                filepath = os.path.join("media", filename)
                tts.save(filepath)
                return f"{self.base_url}/media/{filename}"
            except Exception as e:
                print(f"gTTS Error: {e}")
                return ""

        try:
            url = await loop.run_in_executor(None, _generate)
            if url:
                return {"url": url}
        except Exception:
            pass

        return {"url": "/static/audio/fallback.mp3"}

    async def _generate_visual(self, place: str, narrative: str) -> dict:
        # 1. Try Vertex AI Image Generation if project_id is set
        if self.project_id:
            try:
                from vertexai.preview.vision_models import ImageGenerationModel
                prompt = f"A cinematic, historically accurate depiction of {place}. Highly detailed."
                loop = asyncio.get_running_loop()
                def _generate():
                    model = ImageGenerationModel.from_pretrained("imagegeneration@006")
                    images = model.generate_images(
                        prompt=prompt,
                        number_of_images=1,
                        aspect_ratio="16:9"
                    )
                    return images[0]._image_bytes

                image_bytes = await loop.run_in_executor(None, _generate)
                filename = f"visual_{uuid.uuid4().hex}.png"
                url = await self._upload_to_gcs(filename, image_bytes, "image/png")
                return {"url": url}
            except Exception as e:
                print(f"Vertex AI Image Generation Error, falling back to Pollinations: {e}")

        # 2. Fall back to Pollinations.ai (gratis instant visual generation)
        try:
            prompt = f"A cinematic, historically accurate depiction of {place}. Highly detailed, atmospheric."
            encoded_prompt = urllib.parse.quote(prompt)
            url = f"https://image.pollinations.ai/prompt/{encoded_prompt}?width=1024&height=576&nologo=true"
            return {"url": url}
        except Exception:
            pass

        return {"url": "/static/images/fallback.png"}

    async def _upload_to_gcs(self, filename: str, data: bytes, content_type: str) -> str:
        loop = asyncio.get_running_loop()
        def _upload():
            import datetime
            from google.cloud import storage
            client = storage.Client()
            bucket = client.bucket(self.bucket_name)
            blob = bucket.blob(filename)
            blob.upload_from_string(data, content_type=content_type)
            
            return blob.generate_signed_url(
                version="v4",
                expiration=datetime.timedelta(hours=1),
                method="GET"
            )

        try:
            return await loop.run_in_executor(None, _upload)
        except Exception as e:
            print(f"GCS Upload Error: {e}")
            return f"https://storage.googleapis.com/{self.bucket_name}/{filename}"
