def main() -> None:
    d: dict = {
        "realtime_endpoint": {
            "metadata1": {
                "source_app": ""
            },
            "metadata3": None,
            "metadata4": True,
        }
    }
    x1 = d.get("realtime_endpoint", {}).get("metadata1", {}).get("source_app") or "unknown"
    print(f"x1: {x1}")
    x2 = d.get("realtime_endpoint", {}).get("metadata2", {}).get("source_app") or "unknown"
    print(f"x2: {x2}")
    x3 = d.get("realtime_endpoint", {}).get("metadata3", {}).get("source_app") or "unknown"
    print(f"x3: {x3}")
    x4 = d.get("realtime_endpoint", {}).get("metadata4", {}).get("source_app") or "unknown"
    print(f"x4: {x4}")


if __name__ == "__main__":
    main()
