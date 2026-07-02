import pytest
from unittest.mock import AsyncMock, patch, MagicMock
from tools.profile_tool import profile_lookup
from agents.profile_agent import ProfileAgent
from core.session import SessionState

@pytest.fixture
def mock_db():
    mock_conn = AsyncMock()
    mock_conn.fetchrow = AsyncMock(return_value=None)
    
    mock_ctx = MagicMock()
    mock_ctx.__aenter__ = AsyncMock(return_value=mock_conn)
    mock_ctx.__aexit__ = AsyncMock()
    
    mock_pool = MagicMock()
    mock_pool.acquire = MagicMock(return_value=mock_ctx)
    return mock_pool, mock_conn

@pytest.mark.asyncio
async def test_profile_lookup_valid_db(mock_db):
    mock_pool, mock_conn = mock_db
    mock_conn.fetchrow.return_value = {
        "language": "French",
        "interests": '["art", "history"]',
        "tone": "enthusiastic"
    }

    with patch("tools.profile_tool.get_pool", return_value=mock_pool):
        res = await profile_lookup("user123")
        assert res["language"] == "French"
        assert res["interests"] == ["art", "history"]
        assert res["tone"] == "enthusiastic"

@pytest.mark.asyncio
async def test_profile_lookup_missing_record(mock_db):
    mock_pool, mock_conn = mock_db
    mock_conn.fetchrow.return_value = None

    with patch("tools.profile_tool.get_pool", return_value=mock_pool):
        res = await profile_lookup("user123")
        assert res["language"] == "English"
        assert res["interests"] == ["history"]
        assert res["tone"] == "clear"

@pytest.mark.asyncio
async def test_profile_lookup_invalid_id():
    # Invalid user_id should immediately trigger fallback without pool lookup
    res = await profile_lookup("")
    assert res["language"] == "English"

    res = await profile_lookup(None)
    assert res["language"] == "English"

@pytest.mark.asyncio
async def test_profile_lookup_db_error(mock_db):
    mock_pool, mock_conn = mock_db
    mock_conn.fetchrow.side_effect = Exception("DB Timeout")

    with patch("tools.profile_tool.get_pool", return_value=mock_pool):
        res = await profile_lookup("user123")
        assert res["language"] == "English" # Safe fallback on DB errors

@pytest.mark.asyncio
async def test_profile_agent_execution(mock_db):
    mock_pool, mock_conn = mock_db
    mock_conn.fetchrow.return_value = {
        "language": "German",
        "interests": '["castles"]',
        "tone": "formal"
    }

    with patch("tools.profile_tool.get_pool", return_value=mock_pool):
        agent = ProfileAgent()
        state = SessionState({"request": {"user_id": "user777"}})
        updated_state = await agent.execute(state)
        
        profile = updated_state.get("profile")
        assert profile["language"] == "German"
        assert profile["interests"] == ["castles"]
        assert profile["tone"] == "formal"
