from pathlib import Path
from html import escape
import subprocess
from profile_data import snapshot_date
p=Path(__file__).resolve().parents[1]
BG='#030303';WHITE='#ffffff';BLUE='#243bff';YELLOW='#f5ff00';MUTED='#a1a1aa'
def t(x,y,s,size=16,color=WHITE,extra=''):
 return f'<text x="{x}" y="{y}" font-family="monospace" font-size="{size}" fill="{color}" {extra}>{escape(s)}</text>'
def word(x,y,s,size):
 b=''
 for dx,dy,c in [(1.4,1.4,BLUE),(-.8,-.8,YELLOW),(0,0,WHITE)]:
  b+=f'<text x="{x+dx}" y="{y+dy}" font-family="Arial Black,Arial,sans-serif" font-style="italic" font-weight="900" font-size="{size}" letter-spacing="-1" fill="{c}">{escape(s)}</text>'
 return b
for mobile in [False,True]:
 w,h=(480,258) if mobile else (960,225)
 b=f'<rect width="{w}" height="{h}" fill="{BG}"/><path d="M18 10H{w-18}" stroke="#292933"/><path d="M18 10h65" stroke="{BLUE}"/><path d="M20 8h38" stroke="{YELLOW}"/>'
 if mobile:
  b+=t(17,35,'INTERESTS',13,MUTED)+word(15,73,'self-hosting',29)
  b+=f'<path d="M17 96H463" stroke="#292933"/>'
  b+=t(17,124,'TOOLS',15,YELLOW)
  b+=t(17,152,'TypeScript / JavaScript',20)+t(17,177,'Node.js / Bun / SQLite',20)+t(17,202,'Linux / Git',20)
  b+=t(17,241,'SNAPSHOT / '+snapshot_date().strftime('%d %b %Y').upper(),12,MUTED)
 else:
  b+=t(20,44,'INTERESTS',14,MUTED)+word(18,113,'self-hosting',38)
  b+=f'<path d="M452 34 426 163" stroke="#34343b"/>'
  b+=t(496,44,'TOOLS',16,YELLOW)+t(496,85,'TypeScript / JavaScript',24)+t(496,116,'Node.js / Bun / SQLite',24)+t(496,147,'Linux / Git',24)
  b+=f'<path d="M20 180H940" stroke="#292933"/>'
  b+=t(20,210,'USERSATOSHI',13,MUTED)+t(940,210,'SNAPSHOT / '+snapshot_date().strftime('%d %b %Y').upper(),13,MUTED,'text-anchor="end"')
 title='Interests: self-hosting. Tools: TypeScript, JavaScript, Node.js, Bun, SQLite, Linux, Git. Data snapshot: '+snapshot_date().strftime('%d %B %Y').lstrip('0')+'.'
 s=f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img"><title>{title}</title>{b}</svg>'
 name='about'+('-mobile' if mobile else '')
 (p/'assets'/(name+'.svg')).write_text(s)
 subprocess.run(['rsvg-convert',str(p/'assets'/(name+'.svg')),'-o',str(p/'assets'/(name+'.png'))],check=True)
print('Built a matching, static interests/tools footer.')
