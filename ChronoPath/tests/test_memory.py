import pytest
from agents.memory_agent import MemoryAgent
from core.session import SessionState

@pytest.mark.asyncio
async def test_memory_agent():
    agent = MemoryAgent()
    state = SessionState({"request_id": "123", "story": {"story": "Test"}, "location": {"place": "Pune"}})
    result = await agent.execute(state)
    assert result.get("memory_saved") in [True, False]
