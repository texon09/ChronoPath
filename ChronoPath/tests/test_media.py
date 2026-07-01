import pytest
from agents.media_agent import MediaAgent
from core.session import SessionState

@pytest.mark.asyncio
async def test_media_agent():
    agent = MediaAgent()
    state = SessionState({"story": {"story": "Test story"}, "location": {"place": "Pune"}})
    result = await agent.execute(state)
    assert result.get("media") is not None
    assert "audio_url" in result.get("media")
    assert "visual_url" in result.get("media")
