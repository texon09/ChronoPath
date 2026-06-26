JOURNEYS = {
    "1": {
        "visited_places": ["Lal Mahal"],
        "recent_story_topics": ["Shivaji Maharaj's early Pune years"],
    }
}


def journey_lookup(user_id):
    return JOURNEYS.get(
        str(user_id),
        {
            "visited_places": [],
            "recent_story_topics": [],
        },
    )
