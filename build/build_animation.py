from pathlib import Path
import importlib.util,subprocess,concurrent.futures,shutil
p=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('profile_scene',p/'build_scene.py');m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
def render(job):
 mobile,frame=job;d=p/('mobile' if mobile else 'desktop');d.mkdir(exist_ok=True)
 path=d/f'frame-{frame:03d}.png'
 subprocess.run(['rsvg-convert','-o',str(path)],input=m.scene(mobile,frame).encode(),check=True)
with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:list(pool.map(render,[(mobile,f) for mobile in [False,True] for f in range(m.FRAME_COUNT)]))
for mobile in [False,True]:
 d=p/('mobile' if mobile else 'desktop');suffix='-mobile' if mobile else ''
 palette=d/'palette.png'
 subprocess.run(['ffmpeg','-v','error','-y','-framerate',str(m.FRAME_RATE),'-i',str(d/'frame-%03d.png'),'-vf','palettegen=stats_mode=full:max_colors=256','-frames:v','1','-update','1',str(palette)],check=True)
 subprocess.run(['ffmpeg','-v','error','-y','-framerate',str(m.FRAME_RATE),'-i',str(d/'frame-%03d.png'),'-i',str(palette),'-filter_complex','paletteuse=dither=none:diff_mode=rectangle','-loop','0',str(m.assets/f'profile{suffix}.gif')],check=True)
 shutil.copy2(d/'frame-000.png',m.assets/f'profile{suffix}.png')
 print(('mobile' if mobile else 'desktop')+': GIF and matching static fallback rendered',flush=True)
