PROFILES = {
    "1": {
        "language": "English",
        "interests": ["architecture", "Maratha history", "local legends"],
        "tone": "immersive",
    }
}


def profile_lookup(user_id):
    return PROFILES.get(
        str(user_id),
        {
            "language": "English",
            "interests": ["history"],
            "tone": "clear",
        },
    )
