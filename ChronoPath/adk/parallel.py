import asyncio

class ParallelRunner:
    """Wraps fanout execution."""
    def __init__(self, runners):
        self.runners = runners

    async def execute(self, state):
        # Internally this is where google.adk.workflow.Workflow could be used
        # to branch execution. For now, we use asyncio.gather to satisfy the adapter signature.
        await asyncio.gather(*(runner.execute(state) for runner in self.runners))
        return state
