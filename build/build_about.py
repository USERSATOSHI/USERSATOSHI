from pathlib import Path
from html import escape
import subprocess
from profile_data import snapshot_date
p=Path(__file__).resolve().parents[1]
BG='#030303';WHITE='#ffffff';BLUE='#243bff';YELLOW='#f5ff00';MUTED='#a1a1aa'
# Curated from the owner's public repositories; not inferred from dependencies on refresh.
TOOLS = [
 'C++ / TypeScript / JavaScript',
 'Python / PHP / Shell / HTML / CSS',
 'React / Electron / Elysia',
 'Node.js / Bun / SQLite',
 'Linux / Docker / Git / Nix',
 'Tree-sitter',
]
def t(x,y,s,size=16,color=WHITE,extra=''):
 return f'<text x="{x}" y="{y}" font-family="monospace" font-size="{size}" fill="{color}" {extra}>{escape(s)}</text>'
def word(x,y,s,size):
 b=''
 for dx,dy,c in [(1.4,1.4,BLUE),(-.8,-.8,YELLOW),(0,0,WHITE)]:
  b+=f'<text x="{x+dx}" y="{y+dy}" font-family="Arial Black,Arial,sans-serif" font-style="italic" font-weight="900" font-size="{size}" letter-spacing="-1" fill="{c}">{escape(s)}</text>'
 return b
for mobile in [False,True]:
 w,h=(480,344) if mobile else (960,310)
 b=f'<rect width="{w}" height="{h}" fill="{BG}"/><path d="M18 10H{w-18}" stroke="#292933"/><path d="M18 10h65" stroke="{BLUE}"/><path d="M20 8h38" stroke="{YELLOW}"/>'
 if mobile:
  b+=t(17,35,'INTERESTS',13,MUTED)+word(15,73,'self-hosting',29)
  b+=f'<path d="M17 96H463" stroke="#292933"/>'
  b+=t(17,124,'LANGUAGES / TOOLS',13,YELLOW)
  for i,line in enumerate(TOOLS):b+=t(17,152+i*25,line,17)
  b+=t(17,h-17,'SNAPSHOT / '+snapshot_date().strftime('%d %b %Y').upper(),12,MUTED)
 else:
  b+=t(20,44,'INTERESTS',14,MUTED)+word(18,113,'self-hosting',38)
  b+=f'<path d="M395 34 369 250" stroke="#34343b"/>'
  b+=t(430,44,'LANGUAGES / TOOLS',14,YELLOW)
  for i,line in enumerate(TOOLS):b+=t(430,85+i*31,line,18)
  b+=f'<path d="M20 266H940" stroke="#292933"/>'
  b+=t(20,h-15,'USERSATOSHI',13,MUTED)+t(940,h-15,'SNAPSHOT / '+snapshot_date().strftime('%d %b %Y').upper(),13,MUTED,'text-anchor="end"')
 title='Interests: self-hosting. Languages and tools: '+', '.join(TOOLS)+'. Data snapshot: '+snapshot_date().strftime('%d %B %Y').lstrip('0')+'.'
 s=f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img"><title>{escape(title)}</title>{b}</svg>'
 name='about'+('-mobile' if mobile else '')
 (p/'assets'/(name+'.svg')).write_text(s)
 subprocess.run(['rsvg-convert',str(p/'assets'/(name+'.svg')),'-o',str(p/'assets'/(name+'.png'))],check=True)
print('Built matching interests and expanded languages/tools footer.')
