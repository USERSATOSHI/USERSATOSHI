"""Check generated outputs before the workflow commits them."""
from html.parser import HTMLParser
from pathlib import Path
from xml.etree import ElementTree as ET
import json
import subprocess

ROOT = Path(__file__).resolve().parents[1]
selected = json.loads((ROOT / 'build/selected.json').read_text())
expected = {r['url'] for r in selected}

class Assets(HTMLParser):
    def __init__(self):
        super().__init__()
        self.links = set()
        self.anchor = None

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag == 'a':
            self.anchor = attrs.get('href')
        if tag in ('img', 'source'):
            src = attrs.get('src') or attrs.get('srcset', '')
            if src.startswith('./') and not (ROOT / src).is_file():
                raise ValueError('Missing asset: ' + src)
        if tag == 'img':
            if not attrs.get('alt'):
                raise ValueError('Missing image description')
            if Path(attrs['src']).name.startswith('card-'):
                if self.anchor not in expected:
                    raise ValueError('Project card is missing its repository link')
                self.links.add(self.anchor)

    def handle_endtag(self, tag):
        if tag == 'a':
            self.anchor = None

parser = Assets()
parser.feed((ROOT / 'README.md').read_text())
assert parser.links == expected
calendar = json.loads((ROOT / 'data/calendar.json').read_text())['data']['user']['contributionsCollection']['contributionCalendar']
assert sum(d['contributionCount'] for w in calendar['weeks'] for d in w['contributionDays']) == calendar['totalContributions']
for suffix in ('', '-mobile'):
    weeks = calendar['weeks'][-26:] if suffix else calendar['weeks']
    svg = ET.parse(ROOT / 'assets' / f'activity{suffix}.svg').getroot()
    marks = svg.findall('.//{http://www.w3.org/2000/svg}polygon/{http://www.w3.org/2000/svg}title')
    assert len(marks) == sum(len(w['contributionDays']) for w in weeks)
    assert svg.find('{http://www.w3.org/2000/svg}title').text.startswith(str(calendar['totalContributions']))
    for name in ('aoi', 'gutenberg', 'kouro', 'kasanome'):
        asset = ROOT / 'assets' / f'card-{name}{suffix}.gif'
        stream = json.loads(subprocess.check_output([
            'ffprobe', '-v', 'error', '-count_frames', '-select_streams', 'v:0',
            '-show_entries', 'stream=nb_read_frames,duration', '-of', 'json', str(asset)
        ]))['streams'][0]
        assert int(stream['nb_read_frames']) == 48
        assert float(stream['duration']) == 12
        assert asset.stat().st_size < 10_000_000
print('Validated calendar days/totals, linked cards, image references, mobile fallbacks, and animation duration/size.')
