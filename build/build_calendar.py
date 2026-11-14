from pathlib import Path
from html import escape
from math import sqrt,log1p
import json,subprocess
from profile_data import calendar_range
root=Path(__file__).resolve().parents[1];a=root/'assets'
cal=json.loads((root/'data/calendar.json').read_text())['data']['user']['contributionsCollection']['contributionCalendar']
peak=max(d['contributionCount'] for week in cal['weeks'] for d in week['contributionDays'])
def text(x,y,s,size=14,color='#eeeeff',extra=''):
 family='Arial Black,Arial,sans-serif' if size>=60 else 'monospace'
 return f'<text x="{x}" y="{y}" font-family="{family}" font-size="{size}" fill="{color}" {extra}>{escape(str(s))}</text>'
for mobile in [False,True]:
 w,h=(480,472) if mobile else (960,500)
 weeks=cal['weeks'][-26:] if mobile else cal['weeks']
 b=f'<rect width="{w}" height="{h}" fill="#030303"/>'
 for dx,dy,c in [(3,3,'#243bff'),(-1.5,-1.5,'#f5ff00'),(0,0,'#ffffff')]:
  b+=text(25+dx,85+dy,f'{cal["totalContributions"]:,}',72 if mobile else 86,c,'font-style="italic" font-weight="900" letter-spacing="-4"')
 b+=text(29,119,'CONTRIBUTIONS',13 if mobile else 14,extra='letter-spacing="3"')
 b+=text(w-25,38,'LATEST 26 WEEKS' if mobile else calendar_range(cal),12 if mobile else 13,extra='text-anchor="end" letter-spacing="1.5"')
 x0=22 if mobile else 44;step=(w-2*x0-15)/max(1,len(weeks)-1)
 for wi,week in enumerate(weeks):
  for d in week['contributionDays']:
   n=d['contributionCount'];ratio=log1p(n)/log1p(peak) if n else 0
   hh=10+27*ratio if n else 10;ww=2+6.2*ratio if n else 1.7
   x=x0+wi*step;y=(169 if mobile else 185)+d['weekday']*37
   skew=hh*.32
   points=f'{x+skew},{y-hh/2} {x+skew+ww},{y-hh/2} {x+ww},{y+hh/2} {x},{y+hh/2}'
   color='#252525' if not n else '#4e62ff' if n<3 else '#e0e2ff' if n<8 else '#f5ff00'
   if n>=8:
    b+=f'<polygon points="{points}" fill="#243bff" transform="translate(3 3)"/>'
   b+=f'<polygon points="{points}" fill="{color}"><title>{d["date"]}: {n} contributions</title></polygon>'
 b+=text(26,h-25,'ONE SLASH / ONE DAY',10 if mobile else 12,extra='letter-spacing="1.5"')
 if not mobile:b+=text(w-25,h-25,'SIZE / DAILY CONTRIBUTIONS',12,extra='text-anchor="end" letter-spacing="1.5"')
 else:b+=text(26,h-7,'FULL-YEAR TOTAL / 26 WEEKS SHOWN',9,'#999999')
 s=f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img"><title>{cal["totalContributions"]} GitHub contributions. Slash-field calendar: one slash per day, size uses logarithmic scaling of actual daily count.</title>{b}</svg>'
 suffix='-mobile' if mobile else ''
 path=a/f'activity{suffix}.svg';path.write_text(s)
 subprocess.run(['rsvg-convert',str(path),'-o',str(a/f'activity{suffix}.png')],check=True)
print('Slash calendars rendered from the verified daily contribution data.')
