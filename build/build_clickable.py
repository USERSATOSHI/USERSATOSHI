from pathlib import Path
import subprocess,shutil,concurrent.futures
root=Path(__file__).resolve().parents[1];build=root/'build';assets=root/'assets'
image_command=shutil.which('magick') or shutil.which('convert')
if not image_command:raise RuntimeError('ImageMagick is required')
jobs=[]
for mobile in [False,True]:
 suffix='-mobile' if mobile else '';d=build/('mobile' if mobile else 'desktop')
 jobs.append((d,'header'+suffix,(480,957,0,0) if mobile else (960,929,0,0)))
 cw,ch,gap,y0=(235,176,10,957) if mobile else (470,230,20,929)
 for i,name in enumerate(['aoi','gutenberg','kouro','kasanome']):
  jobs.append((d,'card-'+name+suffix,(cw,ch,(i%2)*(cw+gap),y0+(i//2)*((170+10) if mobile else (224+20)))))
def export(job):
 d,name,(w,h,x,y)=job
 crop=f'crop={w}:{h}:{x}:{y}';palette=build/(name+'-palette.png')
 if name.startswith('header'):
  subprocess.run([image_command,str(d/'frame-000.png'),'-crop',f'{w}x{h}+{x}+{y}','+repage',str(assets/(name+'.png'))],check=True)
  return name+' (static)'
 subprocess.run(['ffmpeg','-v','error','-y','-framerate','4','-i',str(d/'frame-%03d.png'),'-vf',crop+',palettegen=stats_mode=full:max_colors=256','-frames:v','1','-update','1',str(palette)],check=True)
 subprocess.run(['ffmpeg','-v','error','-y','-framerate','4','-i',str(d/'frame-%03d.png'),'-i',str(palette),'-filter_complex',f'[0:v]{crop}[c];[c][1:v]paletteuse=dither=none:diff_mode=rectangle','-loop','0',str(assets/(name+'.gif'))],check=True)
 subprocess.run([image_command,str(d/'frame-000.png'),'-crop',f'{w}x{h}+{x}+{y}','+repage',str(assets/(name+'.png'))],check=True)
 return name
with concurrent.futures.ThreadPoolExecutor(max_workers=3) as pool:
 for name in pool.map(export,jobs):print('Exported '+name,flush=True)
