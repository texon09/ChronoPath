def network_quality_check(network_quality="good"):
    normalized = (network_quality or "good").lower()
    if normalized not in {"good", "medium", "low"}:
        normalized = "good"
    return {"quality": normalized}
