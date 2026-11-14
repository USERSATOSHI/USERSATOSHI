from pathlib import Path
from html import escape
from math import sin,cos,pi
import json,base64,subprocess
from profile_data import snapshot_date
root=Path(__file__).resolve().parents[1];assets=root/'assets';out=root/'build'
repos=json.loads((out/'selected.json').read_text())
FRAME_COUNT=48
FRAME_RATE=4
BLACK='#030303';WHITE='#ffffff';BLUE='#243bff';YELLOW='#f5ff00'
def data(path):return 'data:image/png;base64,'+base64.b64encode(path.read_bytes()).decode()
portrait=data(assets/'portrait-ai-enhanced.png');background=data(assets/'header-background.png')
def text(x,y,value,size=14,color=WHITE,font='monospace',extra=''):
 return f'<text x="{x}" y="{y}" font-family="{font}" font-size="{size}" fill="{color}" {extra}>{escape(str(value))}</text>'
def word(value,x,y,size,fg=WHITE):
 b=''
 for dx,dy,c in [(2,2,BLUE),(-1.3,-1.3,YELLOW),(0,0,fg)]:
  b+=text(x+dx,y+dy,value,size,c,'Arial Black,Arial,sans-serif','font-style="italic" font-weight="900" letter-spacing="-3"')
 return b
# Render the generated slash-field calendars without altering their data.
for name in ['activity','activity-mobile']:
 subprocess.run(['rsvg-convert',str(assets/(name+'.svg')),'-o',str(assets/(name+'.png'))],check=True)
calendar=data(assets/'activity.png');calendar_mobile=data(assets/'activity-mobile.png')

def stripe_families(mobile,t,color='white',outline=False):
 w,h=(480,320) if mobile else (960,400)
 scale=.70 if mobile else 1
 # Two interleaved diagonals: varied lengths, widths and staggered depth/motion.
 specs=[
  [(.015,.55,180,3),(.08,.09,105,8),(.13,.83,180,4),(.20,.32,145,12),(.26,.76,145,5),(.31,.10,100,3),(.38,.48,190,22),(.44,.90,130,3),(.49,.13,90,4),(.77,.10,90,5),(.88,.68,180,11),(.98,.38,110,4),(.045,.88,95,10),(.34,.02,95,18),(.46,.66,95,4),(.81,.95,125,16)],
  [(.015,.18,130,5),(.10,.66,165,4),(.19,.12,120,15),(.25,.48,180,3),(.35,.83,155,8),(.40,.18,155,17),(.49,.68,105,3),(.56,.95,100,5),(.70,.08,85,3),(.82,.86,155,6),(.94,.28,155,9),(.99,.84,140,4),(.04,.42,85,12),(.29,.89,110,18),(.44,.05,100,4),(.92,.92,90,14)]
 ]
 groups=[]
 for family,items in enumerate(specs):
  marks=''
  for i,(cx,cy,length,thickness) in enumerate(items):
   phase=t+i*.63+family*1.2
   x=cx*w+(18+4*(i%4))*scale*sin(phase)
   y=cy*h+12*scale*cos(phase+family)
   # Fixed opposing angles, rather than a field of parallel rain strokes.
   angle=(-61 if family==0 else 61)*pi/180
   ux,uy=cos(angle),sin(angle);nx,ny=-uy,ux
   L=length*scale;T=thickness*scale
   pts=[(x+u*L/2*ux+v*T/2*nx,y+u*L/2*uy+v*T/2*ny) for u,v in [(-1,-1),(1,-1),(1,1),(-1,1)]]
   points=' '.join(f'{xx},{yy}' for xx,yy in pts)
   if outline:
    if thickness>=6:marks+=f'<polygon points="{points}" fill="none" stroke="{color}" stroke-width="1"/>'
   else:marks+=f'<polygon points="{points}" fill="{color}"/>'
  groups.append(marks)
 return groups

def stripe_marks(mobile,t):
 # Parity stencil: intersections are inverted twice and return to the original.
 A,B=stripe_families(mobile,t)
 return f'<g mask="url(#not-b)">{A}</g><g mask="url(#not-a)">{B}</g>'

def inversion_layer(mobile,t):
 w,h=(480,320) if mobile else (960,400)
 A,B=stripe_families(mobile,t)
 na,nb=stripe_families(mobile,t,'black')
 # The face is the foreground of the composition; shards cross hair/hood around it.
 if mobile:
  face='<ellipse cx="216" cy="159" rx="89" ry="83" fill="black"/>'
 else:
  face='<path d="M142 116C168 101 190 116 211 126C232 136 258 121 280 125C312 130 333 160 328 190L319 231C300 264 278 288 248 301C215 312 181 288 155 263L132 223C119 187 122 145 142 116Z" fill="black"/>'
 protect=face+('' if mobile else '<rect x="515" y="75" width="420" height="270" fill="black"/>')
 edgeB=''.join(stripe_families(mobile,t,BLUE,True));edgeY=''.join(stripe_families(mobile,t,YELLOW,True))
 dxA=(5.5+1.4*sin(t))*(.75 if mobile else 1);dyA=-3
 dxB=-4.5*(.75 if mobile else 1);dyB=2+sin(t)
 return f'''<defs>
 <filter id="invert-art" x="-10" y="-10" width="{w+20}" height="{h+20}" filterUnits="userSpaceOnUse" color-interpolation-filters="sRGB"><feComponentTransfer><feFuncR type="table" tableValues="1 0"/><feFuncG type="table" tableValues="1 0"/><feFuncB type="table" tableValues="1 0"/><feFuncA type="identity"/></feComponentTransfer></filter>
 <mask id="not-a" maskUnits="userSpaceOnUse" x="0" y="0" width="{w}" height="{h}"><rect width="{w}" height="{h}" fill="white"/>{na}</mask>
 <mask id="not-b" maskUnits="userSpaceOnUse" x="0" y="0" width="{w}" height="{h}"><rect width="{w}" height="{h}" fill="white"/>{nb}</mask>
 <mask id="refract-a" maskUnits="userSpaceOnUse" x="0" y="0" width="{w}" height="{h}"><rect width="{w}" height="{h}" fill="black"/>{A}{protect}</mask>
 <mask id="refract-b" maskUnits="userSpaceOnUse" x="0" y="0" width="{w}" height="{h}"><rect width="{w}" height="{h}" fill="black"/>{B}{protect}</mask>
 <mask id="invert-a" maskUnits="userSpaceOnUse" x="0" y="0" width="{w}" height="{h}"><rect width="{w}" height="{h}" fill="black"/><g mask="url(#not-b)">{A}</g>{protect}</mask>
 <mask id="invert-b" maskUnits="userSpaceOnUse" x="0" y="0" width="{w}" height="{h}"><rect width="{w}" height="{h}" fill="black"/><g mask="url(#not-a)">{B}</g>{protect}</mask>
 <mask id="edge-safe" maskUnits="userSpaceOnUse" x="0" y="0" width="{w}" height="{h}"><rect width="{w}" height="{h}" fill="white"/>{protect}</mask>
 </defs>
 <g mask="url(#refract-a)"><use href="#header-art" transform="translate({dxA} {dyA})"/></g>
 <g mask="url(#refract-b)"><use href="#header-art" transform="translate({dxB} {dyB})"/></g>
 <g mask="url(#invert-a)"><use href="#header-art" transform="translate({dxA} {dyA})" filter="url(#invert-art)"/></g>
 <g mask="url(#invert-b)"><use href="#header-art" transform="translate({dxB} {dyB})" filter="url(#invert-art)"/></g>
 <g mask="url(#edge-safe)"><g transform="translate(1.2 1.2)">{edgeB}</g><g transform="translate(-1 -1)">{edgeY}</g></g>'''

def scene(mobile,frame=0,effects=True):
 w,h=(480,1370) if mobile else (960,1460);t=frame*2*pi/FRAME_COUNT
 b=f'<rect width="{w}" height="{h}" fill="{BLACK}"/>'
 if mobile:
  # A smaller portrait interleaved with shards on the shared background.
  b+='<defs><clipPath id="portrait-area"><rect width="480" height="320"/></clipPath><linearGradient id="fade-mobile" x2="0" y2="1"><stop offset="0" stop-color="white"/><stop offset=".78" stop-color="white"/><stop offset="1" stop-color="black"/></linearGradient><mask id="blend-mobile" maskUnits="userSpaceOnUse" x="0" y="0" width="480" height="320"><rect width="480" height="320" fill="url(#fade-mobile)"/></mask></defs>'
  b+='<g id="header-art">'
  b+=f'<image width="960" height="400" href="{background}"/>'
  b+=f'<image x="90" y="-12" width="280" height="365" href="{portrait}" clip-path="url(#portrait-area)" mask="url(#blend-mobile)"/>'
  b+='</g>'
  if effects:b+=inversion_layer(mobile,0)
  b+=f'<rect y="320" width="480" height="140" fill="{BLACK}"/>'
  b+=word('USERSATOSHI',17,377,48)+text(20,413,'as empty as vacuum',16)+text(20,442,'TUSHAR BHARTI',13,YELLOW)
  b+=f'<path d="m402 433 27-43 7 5-27 43Z" fill="{BLUE}"/><path d="m416 433 27-43 7 5-27 43Z" fill="{YELLOW}"/>'
  b+=f'<image x="0" y="471" width="480" height="472" href="{calendar_mobile}"/>'
  cy=960;cw=235;ch=170;gap=10
 else:
  b+='<defs><clipPath id="portrait-area"><rect width="510" height="400"/></clipPath><linearGradient id="fade" x2="0" y2="1"><stop offset="0" stop-color="white"/><stop offset=".72" stop-color="white"/><stop offset="1" stop-color="black"/></linearGradient><mask id="blend" maskUnits="userSpaceOnUse" x="0" y="0" width="510" height="400"><rect width="510" height="400" fill="url(#fade)"/></mask></defs>'
  b+='<g id="header-art">'
  b+=f'<image width="960" height="400" href="{background}"/>'
  b+=f'<image x="68" y="-8" width="350" height="456" href="{portrait}" clip-path="url(#portrait-area)" mask="url(#blend)"/>'
  b+='</g>'
  if effects:b+=inversion_layer(mobile,0)
  # A few shard edges from the reference, kept behind and around the portrait.
  b+=f'<path d="m12 48 35-48h16L28 48Z" fill="{BLUE}"/><path d="m18 48 35-48h9L27 48Z" fill="{YELLOW}"/><path d="m20 45 32-45h8L28 45Z" fill="{WHITE}"/>'
  b+=word('USER',541,159,86)+word('SATOSHI',541,242,86)
  b+=text(546,281,'as empty as vacuum',16)+f'<path d="M546 306H872" stroke="{YELLOW}"/>'+text(546,333,'TUSHAR BHARTI',13,WHITE,extra='letter-spacing="2"')
  b+=f'<image x="0" y="410" width="960" height="500" href="{calendar}"/>'
  cy=932;cw=470;ch=224;gap=20
 # Flat alternating panels, same proportions and typography as the selected reference.
 tags=['DISCORD FRAMEWORK','WORDPRESS EDITOR','AGENT WORKFLOWS','CODE REVIEW']
 for i,r in enumerate(repos):
  x=(i%2)*(cw+gap);basey=cy+(i//2)*(ch+gap)
  y=basey
  name=r['nameWithOwner'].split('/')[1];invert=i in [1,2];bg=WHITE if invert else BLACK;fg=BLACK if invert else WHITE
  b+=f'<rect x="{x}" y="{y}" width="{cw}" height="{ch}" fill="{bg}"/>'
  # Stationary cards; a low-amplitude corner accent breathes over 12 seconds.
  alpha=.94+.06*(1+sin(t-i*pi/2))/2
  size=23 if mobile else 34
  b+=f'<path d="M{x+cw-size} {y}h12l{size-12} {size-12}v12Z" fill="{BLUE}" opacity="{alpha}"/><path d="M{x} {y+ch-size}v12l{size-12} {size-12}h12Z" fill="{YELLOW}"/>'
  b+=text(x+(12 if mobile else 18),y+(27 if mobile else 31),tags[i],15 if mobile else 14,fg)
  b+=word(name,x+(10 if mobile else 16),y+(84 if mobile else 110),34 if mobile else 57,fg)
  xx=x+(12 if mobile else 18);by=y+(117 if mobile else 155);bw=cw-2*(12 if mobile else 18)
  b+=f'<rect x="{xx}" y="{by}" width="{bw}" height="5" fill="{fg}" opacity=".2"/><rect x="{xx}" y="{by}" width="{bw*r["authoredCommits"]/max(1,max(repo["authoredCommits"] for repo in repos))}" height="5" fill="{BLUE if invert else YELLOW}"/>'
  ty=y+(152 if mobile else 195)
  b+=text(xx,ty,f'{r["authoredCommits"]} commits',14 if mobile else 18,fg)
  val=f'{r["stargazerCount"]:,} ★' if i<2 else 'OWN PROJECT'
  b+=text(x+cw-(12 if mobile else 18),ty,val,13 if mobile else 18,fg,extra='text-anchor="end"')
 b+=text(12 if mobile else 18,h-22,'SNAPSHOT / '+snapshot_date().isoformat(),11 if mobile else 13,'#a1a1a1')
 return f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img"><title>USERSATOSHI. Approved portrait, blended banner, slash-field contributions, and diversified project cards.</title>{b}</svg>'
if __name__=='__main__':
 for mobile in [False,True]:
  suffix='-mobile' if mobile else ''
  subprocess.run(['rsvg-convert','-o',str(assets/f'profile{suffix}.png')],input=scene(mobile,0).encode(),check=True)
 print('Rendered the selected design with the approved portrait and diversified projects.')
