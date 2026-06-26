HISTORICAL_CONTEXT = {
    "Shaniwar Wada": {
        "context": "Peshwa Era",
        "facts": [
            "Built in 1732 as the seat of the Peshwas.",
            "Served as a political center of the Maratha Empire.",
            "Known for fortified gates, palace courts, and later fire damage.",
        ],
    },
    "Aga Khan Palace": {
        "context": "Indian Freedom Movement",
        "facts": [
            "Built by Sultan Muhammed Shah Aga Khan III in 1892.",
            "Used to intern Mahatma Gandhi during the Quit India Movement.",
            "Now preserves memory connected to India's independence struggle.",
        ],
    },
}


def fetch_history(place):
    return HISTORICAL_CONTEXT.get(
        place,
        {
            "context": "Local History",
            "facts": ["This location has regional historical relevance."],
        },
    )
