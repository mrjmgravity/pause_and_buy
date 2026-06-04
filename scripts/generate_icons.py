import os
import zlib
import struct

ICON_DIR = os.path.join('web', 'icons')
os.makedirs(ICON_DIR, exist_ok=True)

COLOR = (30, 58, 138)

cdef = 'utf-8'

def write_png(path, width, height, color):
    data = bytearray()
    for _ in range(height):
        data.append(0)
        for _ in range(width):
            data.extend(color)
    compressed = zlib.compress(bytes(data), level=9)
    def chunk(chunk_type, chunk_data):
        crc = zlib.crc32(chunk_type + chunk_data) & 0xFFFFFFFF
        return struct.pack('>I', len(chunk_data)) + chunk_type + chunk_data + struct.pack('>I', crc)

    png = bytearray(b'\x89PNG\r\n\x1a\n')
    png.extend(chunk(b'IHDR', struct.pack('>IIBBBBB', width, height, 8, 2, 0, 0, 0)))
    png.extend(chunk(b'IDAT', compressed))
    png.extend(chunk(b'IEND', b''))
    with open(path, 'wb') as f:
        f.write(png)

write_png(os.path.join(ICON_DIR, 'icon-192.png'), 192, 192, COLOR)
write_png(os.path.join(ICON_DIR, 'icon-512.png'), 512, 512, COLOR)
print('Generated icons in', ICON_DIR)
