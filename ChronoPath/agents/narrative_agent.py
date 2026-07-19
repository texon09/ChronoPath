import os
import asyncio
import google.generativeai as genai

class NarrativeAgent:
    async def execute(self, state):
        context = state.get("context")
        narrative = await self.run(context)
        state.set("story", narrative)
        return state

    async def run(self, context):
        place = context["place"]
        era = context["context"]
        language = context["language"]
        interests = context.get("interests", [])
        age = context.get("age")
        origin = context.get("origin")
        background = context.get("background")

        prompt = (
            f"Write a detailed, comprehensive, and highly engaging 8-10 sentence historical explanation for a user standing near {place}. "
            f"The historical context is {era}. "
            f"Ensure you discuss both the deep history of {place} and how it has evolved over the years to its present state. "
            f"The user is interested in: {', '.join(interests) if interests else 'general history'}. "
        )
        
        if age:
            prompt += f"The user is {age} years old; adapt the reading level, tone, and analogies appropriately for this age. "
        if origin:
            prompt += f"The user is originally from {origin}; draw deeply relatable historical parallels between {place} and the history of {origin}. "
        if background:
            prompt += f"The user's background/profession is '{background}'; emphasize historical aspects, architecture, or events that align with this background. "
            
        feedback = context.get("feedback")
        if feedback:
            prompt += f"\n\nCRITICAL FEEDBACK FROM REVIEWER: Your previous draft was rejected. You MUST fix these issues in this rewrite:\n{feedback}\n\n"

        prompt += f"Make the story vivid, educational, and immersive. Write it in {language}."
        
        try:
            api_key = os.getenv("GOOGLE_API_KEY")
            if api_key:
                genai.configure(api_key=api_key, transport='rest')
                
            model = genai.GenerativeModel("gemini-3.5-flash")
            
            # Temporary hack: google.generativeai automatically grabs GOOGLE_APPLICATION_CREDENTIALS 
            # and ignores the API key. We must temporarily hide it during generation.
            creds = os.environ.pop("GOOGLE_APPLICATION_CREDENTIALS", None)
            
            try:
                loop = asyncio.get_running_loop()
                response = await loop.run_in_executor(None, lambda: model.generate_content(prompt))
                story = response.text
            finally:
                if creds is not None:
                    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = creds
                    
        except Exception as e:
            print(f"Narrative generation failed: {e}")
            story = f"Welcome to {place}. This location holds deep historical significance from the {era}."

        return {
            "story": story.strip(),
            "facts": context.get("facts", []),
            "language": language,
        }
