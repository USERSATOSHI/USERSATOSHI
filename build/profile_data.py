"""Shared dates for all generated profile assets."""
from datetime import date
from pathlib import Path
import json

ROOT = Path(__file__).resolve().parents[1]

def snapshot_date():
    metadata = ROOT / 'data/snapshot.json'
    if metadata.exists():
        return date.fromisoformat(json.loads(metadata.read_text())['date'])
    calendar = json.loads((ROOT / 'data/calendar.json').read_text())
    weeks = calendar['data']['user']['contributionsCollection']['contributionCalendar']['weeks']
    return date.fromisoformat(max(d['date'] for w in weeks for d in w['contributionDays']))

def calendar_range(calendar):
    days = sorted(d['date'] for w in calendar['weeks'] for d in w['contributionDays'])
    return ' — '.join(date.fromisoformat(d).strftime('%b %Y').upper() for d in (days[0], days[-1]))
