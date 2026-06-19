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
    print(f"x1: {x1}")  # "unknown" — source_app is "" (falsy), so `or` kicks in
    x2 = d.get("realtime_endpoint", {}).get("metadata2", {}).get("source_app") or "unknown"
    print(f"x2: {x2}")  # "unknown" — metadata2 missing → {} default → .get(...) is None
    x3 = d.get("realtime_endpoint", {}).get("metadata3", {}).get("source_app") or "unknown"
    print(f"x3: {x3}")  # AttributeError — metadata3 exists as None, so {} default is NOT used; None.get(...) raises
    x4 = d.get("realtime_endpoint", {}).get("metadata4", {}).get("source_app") or "unknown"
    print(f"x4: {x4}")  # AttributeError — metadata4 is True; True.get(...) raises (never reached, x3 crashes first)


if __name__ == "__main__":
    main()
