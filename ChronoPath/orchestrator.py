from agents.supervisor import SupervisorAgent


async def execute(payload):
    return await SupervisorAgent().execute(payload)


def create_supervisor():
    return SupervisorAgent()
