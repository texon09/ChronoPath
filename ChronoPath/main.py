import argparse
import json

from agents.supervisor import SupervisorAgent


def run_demo(user_id="1", lat=18.5196, lng=73.8553, network_quality="good"):
    supervisor = SupervisorAgent()
    return supervisor.run(
        {
            "user_id": user_id,
            "lat": lat,
            "lng": lng,
            "network_quality": network_quality,
        }
    )


def main():
    parser = argparse.ArgumentParser(description="ChronoPath AI terminal MVP")
    parser.add_argument("--user", default="1")
    parser.add_argument("--lat", type=float, default=18.5196)
    parser.add_argument("--lng", type=float, default=73.8553)
    parser.add_argument("--network", default="good", choices=["good", "medium", "low"])
    args = parser.parse_args()

    response = run_demo(args.user, args.lat, args.lng, args.network)
    print(json.dumps(response, indent=2))


if __name__ == "__main__":
    main()
