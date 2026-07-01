class AgentAdapter:
    """Wraps an existing Milestone 2 agent so it can run inside the ADK graph."""
    def __init__(self, agent):
        self.agent = agent

    async def execute(self, state):
        return await self.agent.execute(state)
