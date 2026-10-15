from pathlib import Path
import ast, struct, hashlib, json, shutil, zipfile, bisect
from PIL import Image, ImageFont, ImageDraw
from mixlib import Mix, namehash

OUT = Path('RedAlert-CHS-v03')
(OUT/'patch').mkdir(parents=True, exist_ok=True)
sha = lambda b: hashlib.sha256(b).hexdigest()
def contents(m):
    return {k:m.b[m.start+o:m.start+o+n] for k,(o,n) in m.entries.items()}
def signed(k): return k if k < 0x80000000 else k-0x100000000
def pack(items):
    table, body = bytearray(), bytearray()
    for k in sorted(items,key=signed):
        table.extend(struct.pack('<III',k,len(body),len(items[k])))
        body.extend(items[k])
    return b'\0'*4+struct.pack('<HI',len(items),len(body))+table+body

base = Mix(Path('RedAlert-CHS-v02/patch/EXPAND2.MIX').read_bytes())
before = contents(base)
items = dict(before)
lang = Mix(Path('cn-inspect/germanuncensoredlanguagepack.MIX').read_bytes())
names = [s.decode('ascii') for s in Path('language-name-database.bin').read_bytes()[52:].split(b'\0') if s]
shapes = [s for s in names if s.lower().endswith('.shp')]
assert len(shapes)==90 and len({namehash(s) for s in names})==97
for n in shapes: items[namehash(n)] = lang.get(n)

# Use unused character slots for two complete caption glyphs; no UTF-8 bytes
# are passed to the original single-byte renderer. Both caption and button
# fonts receive matching glyphs. Existing glyph offsets and bytes stay intact.
captions = {192:'反击任务',193:'余波任务'}
assert not (set(captions) & set(base.get('CONQUER.ENG')[1112:]))
font_names=['GRAD6FNT.FNT']
def add_captions(font):
    b=bytearray(font)
    ib,ob,wb,db,hb=struct.unpack_from('<5H',b,4)
    assert b[ib+3]>=max(captions)
    height=b[ib+4]
    fontface=ImageFont.truetype('/tmp/RedAlert-NotoSansCJKsc-Regular.otf',min(height,16))
    for code,caption in captions.items():
        bbox=fontface.getbbox(caption)
        mask=Image.new('L',(bbox[2]-bbox[0]+2,height))
        ImageDraw.Draw(mask).text((1-bbox[0],-bbox[1]+max(0,(height-(bbox[3]-bbox[1]))//2)),caption,font=fontface,fill=255)
        assert mask.getbbox() and mask.width<256
        struct.pack_into('<H',b,ob+2*code,len(b))
        b[wb+code]=mask.width
        b[ib+5]=max(b[ib+5],mask.width)
        b[hb+2*code:hb+2*code+2]=bytes([0,height])
        for y in range(height):
            for x in range(0,mask.width,2):
                lo=int(mask.getpixel((x,y))>=96)
                hi=int(x+1<mask.width and mask.getpixel((x+1,y))>=96)
                b.append(lo|(hi<<4))
    assert len(b)<65536
    struct.pack_into('<H',b,0,len(b))
    return bytes(b)
for n in font_names:items[namehash(n)]=add_captions(base.get(n))
patched=pack(items)
(OUT/'patch/EXPAND2.MIX').write_bytes(patched)
check=Mix(patched)
changed={namehash(n) for n in shapes+font_names}
assert all(contents(check)[k]==v for k,v in before.items() if k not in changed)
assert check.get('CONQUER.ENG')==base.get('CONQUER.ENG')
for n in shapes:assert check.get(n)==lang.get(n)
keys=[signed(struct.unpack_from('<I',patched,10+12*i)[0]) for i in range(len(items))]
assert keys==sorted(keys)
for n in shapes+font_names+['CONQUER.ENG']:
    assert keys[bisect.bisect_left(keys,signed(namehash(n)))]==signed(namehash(n))

original_nro=Path('upload/RedAlert.nro').read_bytes()
nro=bytearray(original_nro)
patches=[]
for literal,code in [(b'Counterstrike Missions',192),(b'Aftermath Missions',193)]:
    assert original_nro.count(literal+b'\0')==1
    offset=original_nro.index(literal+b'\0')
    nro[offset:offset+len(literal)]=bytes([code])+b'\0'*(len(literal)-1)
    patches.append({'offset':offset,'original':literal.decode(),'translation':captions[code],'glyph_code':code,'span':len(literal)})
assert len(nro)==len(original_nro)
allowed={i for p in patches for i in range(p['offset'],p['offset']+p['span'])}
assert all(a==b or i in allowed for i,(a,b) in enumerate(zip(original_nro,nro)))
(OUT/'patch/RedAlert.nro').write_bytes(nro)

# Reuse the exact font decoder used in the previous patch for visual QA.
tree=ast.parse(Path('make_chs_patch.py').read_text())
render_node=next(n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name=='render')
env={'struct':struct,'Image':Image}
exec(compile(ast.Module(body=[render_node],type_ignores=[]),'<font-decoder>','exec'),env)
preview=Image.new('RGB',(600,240),'#161b22');draw=ImageDraw.Draw(preview)
draw.text((16,12),'FONT RESOURCE PREVIEW - NOT A SWITCH SCREENSHOT',fill='white')
for row,n in enumerate(font_names):
    draw.text((16,50+row*90),n,fill='white')
    for col,code in enumerate(captions):
        mask=env['render'](check.get(n),bytes([code])).resize((132,32),Image.Resampling.NEAREST)
        preview.paste('#f5d069',(210+col*175,50+row*90),mask)
preview.save(OUT/'menu-preview.png')
shutil.copyfile('cameo-comparison.png',OUT/'cameo-comparison.png')
shutil.copyfile('deliverables/红色警戒.nsp',OUT/'红色警戒.nsp')
manifest={'version':'0.3','files':{
    'EXPAND2.MIX':{'sha256':sha(patched),'size':len(patched),'accepted_before':[sha(Path('upload/EXPAND2.MIX').read_bytes()),sha(Path('RedAlert-CHS-v02/patch/EXPAND2.MIX').read_bytes())]},
    'RedAlert.nro':{'sha256':sha(nro),'size':len(nro),'accepted_before':[sha(original_nro)]}},
    'localized_shapes':shapes,'nro_string_patches':patches,'resource_entries':len(items),
    'preserved_v02_text':True,'nro_only_string_bytes_changed':True,'runtime_tested_on_switch':False}
(OUT/'manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2))
print(json.dumps({k:v for k,v in manifest.items() if k!='localized_shapes'},ensure_ascii=False,indent=2))
