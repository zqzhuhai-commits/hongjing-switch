from pathlib import Path
import struct,base64
from cryptography.hazmat.decrepit.ciphers.algorithms import Blowfish
from cryptography.hazmat.primitives.ciphers import Cipher,modes
N=int.from_bytes(base64.b64decode('AihRvNoIbTn85FZRYNZRcT+i6KpU+maCsEqr3Q5q+LDB5tH7Tz2qQ38V')[2:],'big')
def namehash(name):
 b=name.upper().encode('ascii');b+=b'\0'*(-len(b)%4);v=0
 for i in range(0,len(b),4):v=(((v<<1)|(v>>31))+int.from_bytes(b[i:i+4],'little'))&0xffffffff
 return v
class Mix:
 def __init__(self,b):
  self.b=b;start=0;head=b
  if b[:2]==b'\0\0':
   flags=struct.unpack_from('<I',b)[0];start=4
   if flags&0x20000:
    key=b''.join(pow(int.from_bytes(b[i:i+40],'little'),65537,N).to_bytes(40,'little')[:39] for i in (4,44))[:56]
    cipher=Cipher(Blowfish(key),modes.ECB())
    h=cipher.decryptor().update(b[84:92]);count,total=struct.unpack_from('<HI',h)
    length=(6+12*count+7)&~7;head=cipher.decryptor().update(b[84:84+length]);self.start=84+length
   else:head=b[4:];count,total=struct.unpack_from('<HI',head);self.start=10+12*count
  else:count,total=struct.unpack_from('<HI',head);self.start=6+12*count
  assert count<20000 and self.start+total<=len(b),(count,total,len(b),self.start)
  self.entries={}
  for i in range(count):
   id,o,n=struct.unpack_from('<III',head,6+12*i);assert o+n<=total;self.entries[id]=(o,n)
 def get(self,n):
  o,size=self.entries[namehash(n)];return self.b[self.start+o:self.start+o+size]
 def has(self,n):return namehash(n) in self.entries
names=['CONQUER.ENG','CONQUER.CHS','CONQUER.CHI','CONQUER.CHN','CONQUER.CSF','CONQUER.GER','12METFNT.FNT','HELP.FNT','6POINT.FNT','GRAD6FNT.FNT','EDITFNT.FNT','8POINT.FNT','3POINT.FNT','SCOREFNT.FNT','LED.FNT','VCR.FNT','LOCAL.MIX','HIRES.MIX','LORES.MIX','CHINESE.MIX','CHINESE.FNT','TUTORIAL.INI','MISSION.INI','RULES.INI']
