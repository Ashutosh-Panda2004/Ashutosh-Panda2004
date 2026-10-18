from PIL import Image, ImageOps
import numpy as np, os
from rembg import new_session, remove
SRC='/home/hatch/workspace/user/media_library/image/11/11150682da5b373b25592fff1f4ace032df138bb69379fbce77b4789e8fdcb06.png'
OUT='/home/hatch/workspace/profile-readme-v2/work/source-prepped.png'
img=Image.open(SRC).convert('RGB')
session=new_session(os.environ.get('REMBG_MODEL','u2net_human_seg'))
cut=remove(img, session=session)
rgba=np.array(cut).astype(np.float32)/255.0
alpha=rgba[...,3]
gray=np.array(ImageOps.autocontrast(ImageOps.grayscale(img))).astype(np.float32)/255.0
out=(gray*alpha*255).astype(np.uint8)
ys,xs=np.where(alpha>0.2)
pad=30
y0,y1=max(int(ys.min())-pad,0),min(int(ys.max())+pad,out.shape[0])
x0,x1=max(int(xs.min())-pad,0),min(int(xs.max())+pad,out.shape[1])
out=out[y0:y1,x0:x1]
Image.fromarray(out).save(OUT)
print('wrote',OUT,out.shape,'bbox',x0,x1,y0,y1)
