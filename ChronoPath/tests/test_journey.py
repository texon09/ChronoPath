import pytest
from unittest.mock import AsyncMock, patch, MagicMock
from tools.journey_tool import journey_lookup, save_journey, get_last_story
from agents.journey_agent import JourneyAgent
from core.session import SessionState

@pytest.fixture
def mock_db():
    mock_conn = AsyncMock()
    mock_conn.fetchrow = AsyncMock(return_value=None)
    mock_conn.execute = AsyncMock(return_value=None)
    
    mock_transaction = MagicMock()
    mock_transaction.__aenter__ = AsyncMock()
    mock_transaction.__aexit__ = AsyncMock()
    mock_conn.transaction = MagicMock(return_value=mock_transaction)
    
    mock_ctx = MagicMock()
    mock_ctx.__aenter__ = AsyncMock(return_value=mock_conn)
    mock_ctx.__aexit__ = AsyncMock()
    
    mock_pool = MagicMock()
    mock_pool.acquire = MagicMock(return_value=mock_ctx)
    return mock_pool, mock_conn

@pytest.mark.asyncio
async def test_journey_lookup_valid_db(mock_db):
    mock_pool, mock_conn = mock_db
    mock_conn.fetchrow.return_value = {
        "visited_places": '["Pune", "Mumbai"]',
        "recent_story_topics": '["Peshwas"]'
    }

    with patch("tools.journey_tool.get_pool", return_value=mock_pool):
        res = await journey_lookup("user123")
        assert res["visited_places"] == ["Pune", "Mumbai"]
        assert res["recent_story_topics"] == ["Peshwas"]

@pytest.mark.asyncio
async def test_journey_lookup_missing_record(mock_db):
    mock_pool, mock_conn = mock_db
    mock_conn.fetchrow.return_value = None

    with patch("tools.journey_tool.get_pool", return_value=mock_pool):
        res = await journey_lookup("user123")
        assert res["visited_places"] == []
        assert res["recent_story_topics"] == []

@pytest.mark.asyncio
async def test_save_journey(mock_db):
    mock_pool, mock_conn = mock_db
    
    # Simulate existing record
    mock_conn.fetchrow.return_value = {
        "visited_places": '["Pune"]',
        "recent_story_topics": '["History"]'
    }

    with patch("tools.journey_tool.get_pool", return_value=mock_pool):
        res = await save_journey("user123", "Mumbai", "Architecture")
        assert res is True
        mock_conn.execute.assert_called()

@pytest.mark.asyncio
async def test_get_last_story(mock_db):
    mock_pool, mock_conn = mock_db
    mock_conn.fetchrow.return_value = {"story_text": "This was the last story."}

    with patch("tools.journey_tool.get_pool", return_value=mock_pool):
        story = await get_last_story("user123")
        assert story == "This was the last story."

@pytest.mark.asyncio
async def test_journey_agent_execution(mock_db):
    mock_pool, mock_conn = mock_db
    mock_conn.fetchrow.return_value = {
        "visited_places": '["Pune"]',
        "recent_story_topics": '["History"]'
    }

    with patch("tools.journey_tool.get_pool", return_value=mock_pool):
        agent = JourneyAgent()
        state = SessionState({"request": {"user_id": "user777"}})
        updated_state = await agent.execute(state)
        
        journey = updated_state.get("journey")
        assert journey["visited_places"] == ["Pune"]
