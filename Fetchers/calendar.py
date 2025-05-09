import requests
from ics import Calendar
from typing import List, Dict, Any

def fetch_calendar(urls: List[str]) -> List[Dict[str, Any]]:
    """
    Pour chaque URL ICS de la liste, télécharge et parse les événements d'aujourd'hui.
    Retourne la liste brute d'événements au format JSON minimal.
    """
    events: List[Dict[str, Any]] = []
    for url in urls:
        r = requests.get(url)
        r.raise_for_status()
        for cal in Calendar.parse_multiple([r.text]):
            for ev in cal.timeline.today():
                events.append({
                    "title":       ev.name,
                    "start":       ev.begin.isoformat(),
                    "end":         ev.end.isoformat() if ev.end else None,
                    "location":    ev.location or None,
                    "description": ev.description or None
                })
    return events
