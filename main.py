import pymem

class WindowsBackend:
    def __init__(self):
        self.pm = pymem.Pymem("cemu.exe")

    def read(self, address, size):
        return self.pm.read_bytes(address, size)

backend = WindowsBackend()

print(f"CEMU ProcessID: {backend.pm.process_id}")


