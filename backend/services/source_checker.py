def check_source(url):
    if not url:
        return {"status": "Unknown", "score": 50}

    if "bbc" in url or "reuters" in url:
        return {"status": "Trusted", "score": 80}

    return {"status": "Unreliable", "score": 30}