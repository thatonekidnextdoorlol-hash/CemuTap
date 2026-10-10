import pymem
import re
import os

class WindowsBackend:
    def __init__(self):
        self.pm = pymem.Pymem("cemu.exe")

    def read(self, address, size):
        return self.pm.read_bytes(address, size)
        
    
def findbase():
        pattern = r"base: 0x([0-9a-fA-F]+)"
        logpath = os.path.join(os.environ["APPDATA"], "Cemu", "log.txt")
        with open(logpath, errors="ignore") as f:
             lpopt = f.read()
             matches = re.findall(pattern, lpopt)
             return int(matches[-1], 16)
        
def readunit(backend, base, guest, size):
    hostaddress = base + guest
    habo =  backend.read(hostaddress, size)
    return int.from_bytes(habo, "big")

backend = WindowsBackend()

print(f"CEMU ProcessID: {backend.pm.process_id}")
base = findbase()
print(hex(base))

try:
     print(readunit(backend, base, 0x10000000, 4))
     chunk = backend.read(base + 0x10000000, 0x100000)
     print(len(chunk))
     target = (0).to_bytes(2,"big")
     found=[]
     position=chunk.find(target,0)
     while position!=-1:
          found.append(position)
          position = chunk.find(target, position+1)
     print(len(found))

except Exception as e:
     print(f"!!! READ FAILURE. Is Cemu running? If it is, try running Cemu and this script at an administrator level: {e}")
     print(f"ps: this could also mean the script broke. create an issue in the main repository :P")

