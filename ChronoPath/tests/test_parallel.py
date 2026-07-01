import pytest
from adk.parallel import ParallelRunner
from adk.sequential import SequentialRunner
from core.session import SessionState

class MockAgent:
    def __init__(self, key, val):
        self.key = key
        self.val = val
        
    async def execute(self, state):
        state.set(self.key, self.val)
        return state

@pytest.mark.asyncio
async def test_parallel_runner():
    state = SessionState({})
    runner = ParallelRunner([MockAgent("a", 1), MockAgent("b", 2)])
    await runner.execute(state)
    assert state.get("a") == 1
    assert state.get("b") == 2

@pytest.mark.asyncio
async def test_sequential_runner():
    state = SessionState({})
    runner = SequentialRunner([MockAgent("c", 3), MockAgent("d", 4)])
    await runner.execute(state)
    assert state.get("c") == 3
    assert state.get("d") == 4
