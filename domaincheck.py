#!/usr/bin/env python3
"""Check whether domains are registered, using public RDAP data."""
import sys
import requests

def check(domain):
    r = requests.get(f"https://rdap.org/domain/{domain}", timeout=10)
    if r.status_code == 404:
        return "AVAILABLE"
    if r.status_code == 200:
        expires = next(
            (e["eventDate"][:10] for e in r.json().get("events", [])
             if e.get("eventAction") == "expiration"),
            "unknown",
        )
        return f"TAKEN (expires {expires})"
    return f"UNKNOWN (HTTP {r.status_code})"

if __name__ == "__main__":
    if len(sys.argv) < 2:
        sys.exit("Usage: python3 domaincheck.py example.com [more.com ...]")
    for d in sys.argv[1:]:
        print(f"{d}: {check(d)}")
