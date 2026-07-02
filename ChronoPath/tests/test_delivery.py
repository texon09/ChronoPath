import pytest
from agents.delivery_agent import DeliveryAgent
from core.session import SessionState

@pytest.mark.asyncio
async def test_delivery_agent_high_network():
    agent = DeliveryAgent()
    narrative = {"story": "High network story detail."}
    
    res = await agent.run(narrative, network_quality="good")
    assert res["mode"] == "full"
    assert res["return_text"] is True
    assert res["return_audio"] is True
    assert res["return_visual"] is True
    assert res["media"] == "visual-placeholder.png"

@pytest.mark.asyncio
async def test_delivery_agent_medium_network():
    agent = DeliveryAgent()
    narrative = {"story": "Medium network story detail."}
    
    res = await agent.run(narrative, network_quality="medium")
    assert res["mode"] == "audio"
    assert res["return_text"] is True
    assert res["return_audio"] is True
    assert res["return_visual"] is False
    assert res["media"] == "audio-placeholder.mp3"

@pytest.mark.asyncio
async def test_delivery_agent_low_network():
    agent = DeliveryAgent()
    narrative = {"story": "Low network story detail."}
    
    res = await agent.run(narrative, network_quality="low")
    assert res["mode"] == "text"
    assert res["return_text"] is True
    assert res["return_audio"] is False
    assert res["return_visual"] is False
    assert res["media"] is None

@pytest.mark.asyncio
async def test_delivery_agent_execute():
    agent = DeliveryAgent()
    state = SessionState({
        "story": {"story": "Test story output"},
        "request": {"network_quality": "low"}
    })
    
    updated_state = await agent.execute(state)
    delivery = updated_state.get("delivery")
    assert delivery["return_text"] is True
    assert delivery["return_audio"] is False
    assert delivery["return_visual"] is False
