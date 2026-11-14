from pathlib import Path
from html import escape
import subprocess
from profile_data import snapshot_date

p = Path(__file__).resolve().parents[1]
BG = '#030303'; WHITE = '#ffffff'; BLUE = '#243bff'; YELLOW = '#f5ff00'; MUTED = '#a1a1aa'
INTERESTS = ['self-hosting', 'local LLMs', 'compiler design']
CATEGORIES = [
 ('LANGUAGES', ['C++ / Python / PHP / Shell', 'TypeScript / JavaScript / HTML / CSS']),
 ('FRAMEWORKS / RUNTIMES', ['React / Electron / Elysia', 'Node.js / Bun']),
 ('DATA / PARSING', ['SQLite / Tree-sitter']),
 ('SYSTEMS / TOOLING', ['Linux / Docker / Git / Nix']),
]

def text(x, y, value, size=17, color=WHITE, extra=''):
 return f'<text x="{x}" y="{y}" font-family="monospace" font-size="{size}" fill="{color}" {extra}>{escape(value)}</text>'

def word(x, y, value, size):
 result = ''
 for dx, dy, color in [(1.4, 1.4, BLUE), (-.8, -.8, YELLOW), (0, 0, WHITE)]:
  result += f'<text x="{x+dx}" y="{y+dy}" font-family="Arial Black,Arial,sans-serif" font-style="italic" font-weight="900" font-size="{size}" letter-spacing="-1" fill="{color}">{escape(value)}</text>'
 return result

for mobile in [False, True]:
 w, h = (480, 490) if mobile else (960, 336)
 body = f'<rect width="{w}" height="{h}" fill="{BG}"/><path d="M18 10H{w-18}" stroke="#292933"/><path d="M18 10h65" stroke="{BLUE}"/><path d="M20 8h38" stroke="{YELLOW}"/>'
 body += text(20, 39, 'INTERESTS', 13, MUTED)
 if mobile:
  body += word(18, 75, 'self-hosting', 26) + word(254, 75, 'local LLMs', 26)
  body += word(18, 109, 'compiler design', 26)
  body += '<path d="M20 133H460" stroke="#292933"/>'
  positions = [(20, 162), (20, 247), (20, 332), (20, 401)]
 else:
  for x, value in zip([18, 340, 621], INTERESTS):body += word(x, 80, value, 29)
  body += '<path d="M20 106H940 M20 216H940 M475 126V287" stroke="#292933"/>'
  positions = [(20, 142), (501, 142), (20, 252), (501, 252)]
 for (label, lines), (x, y) in zip(CATEGORIES, positions):
  body += text(x, y, label, 13 if mobile else 14, YELLOW, 'letter-spacing=".7"')
  for i, line in enumerate(lines):body += text(x, y+29+i*25, line, 17)
 footer_y = h-17
 body += f'<path d="M20 {h-45}H{w-20}" stroke="#292933"/>'
 body += text(20, footer_y, 'USERSATOSHI', 10 if mobile else 12, MUTED)
 body += text(w-20, footer_y, 'SNAPSHOT / '+snapshot_date().strftime('%d %b %Y').upper(), 10 if mobile else 12, MUTED, 'text-anchor="end"')
 title = 'Interests: '+', '.join(INTERESTS)+'. '+'. '.join(label+': '+', '.join(lines) for label, lines in CATEGORIES)+'. Data snapshot: '+snapshot_date().strftime('%d %B %Y').lstrip('0')+'.'
 svg = f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img"><title>{escape(title)}</title>{body}</svg>'
 name = 'about'+('-mobile' if mobile else '')
 (p/'assets'/(name+'.svg')).write_text(svg)
 subprocess.run(['rsvg-convert', str(p/'assets'/(name+'.svg')), '-o', str(p/'assets'/(name+'.png'))], check=True)
print('Built categorized stack and interests for desktop and mobile.')
