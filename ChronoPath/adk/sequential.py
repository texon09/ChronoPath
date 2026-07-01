class SequentialRunner:
    """Wraps ADK workflow graph."""
    def __init__(self, runners):
        self.runners = runners

    async def execute(self, state):
        # Internally this is where google.adk.workflow.Workflow could be built
        # sequentially. For now, we iterate over the adapters.
        for runner in self.runners:
            await runner.execute(state)
        return state
