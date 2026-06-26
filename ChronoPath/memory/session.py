from datetime import datetime, timezone


class SessionMemory:
    def __init__(self):
        self._events = []

    def store_location_history(self, user_id, response):
        event = {
            "user_id": str(user_id),
            "place": response.get("place"),
            "context": response.get("context"),
            "created_at": datetime.now(timezone.utc).isoformat(),
        }
        self._events.append(event)
        return event

    def all_events(self):
        return list(self._events)
