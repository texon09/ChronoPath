class FeedbackLoop:
    """Runs a generator agent and a reviewer agent in a loop until the reviewer passes or max attempts are reached."""
    def __init__(self, generator, reviewer, max_attempts=3):
        self.generator = generator
        self.reviewer = reviewer
        self.max_attempts = max_attempts

    async def execute(self, state):
        attempts = 0
        while attempts < self.max_attempts:
            attempts += 1
            # Run generator
            state = await self.generator.execute(state)
            
            # Run reviewer
            state = await self.reviewer.execute(state)
            
            review = state.get("review")
            if review and review.get("is_pass"):
                # Reviewer passed the draft
                break
                
            # If failed, add feedback to context so generator knows what to fix
            if review and review.get("feedback"):
                context = state.get("context", {})
                context["feedback"] = review["feedback"]
                state.set("context", context)
                
        return state
