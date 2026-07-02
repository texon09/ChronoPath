import logging
from memory.memory_manager import MemoryManager

logger = logging.getLogger("chronopath.agents.memory_agent")

class MemoryAgent:
    def __init__(self):
        self.manager = MemoryManager()

    async def execute(self, state):
        request_id = state.get("request_id")
        user_id = state.get("request", {}).get("user_id", "unknown")
        place = state.get("location", {}).get("place", "")
        story = state.get("story", {}).get("story", "")

        try:
            # Save session state to cache
            await self.manager.save_session(user_id, {"last_req": request_id})
            
            # Save generated story to cache
            await self.manager.save_story(user_id, {"story": story})
            
            # Log journey to both Redis list and Postgres tables
            await self.manager.save_journey(user_id, place, request_id, story)
            
            state.set("memory_saved", True)
        except Exception as e:
            logger.error("MemoryAgent execution failed for user %s: %s", user_id, e)
            state.set("memory_saved", False)

        return state

