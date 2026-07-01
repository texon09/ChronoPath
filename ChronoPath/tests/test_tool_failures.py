import pytest
from tools.geo_tool import reverse_geocode, heritage_lookup
from tools.history_tool import fetch_history
from tools.network_tool import network_quality_check

@pytest.mark.asyncio
async def test_geo_tool_fallback():
    # When api key is missing or invalid, should fallback to Unknown
    res = await reverse_geocode(0, 0)
    assert res["city"] == "Unknown"
    
    h_res = await heritage_lookup(0, 0)
    assert h_res["place"] == "Unknown Heritage Site"

@pytest.mark.asyncio
async def test_history_tool_fallback():
    res = await fetch_history("SomeFakePlaceThatDoesNotExist12345")
    assert "facts" in res
    assert len(res["facts"]) > 0

@pytest.mark.asyncio
async def test_network_tool_fallback():
    res = await network_quality_check("invalid_input")
    assert res["quality"] in ["good", "medium", "low"]
