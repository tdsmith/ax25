import logging

from .ax25 import Frame


class KissStream:
    def __init__(self, file_like):
        self.f = file_like
        self.buffer = b""
        self.i = 0

    def __iter__(self):
        partial = bytearray()
        byte = None
        while byte != b"\xc0" and byte != b"":
            byte = self.f.read(1)
        while True:
            byte = self.f.read(1)
            if len(byte) == 0:
                return
            byte = ord(byte)
            if byte == 0xc0 and partial:
                try:
                    frame = Frame.from_bytes(partial)
                    yield frame
                except ValueError:
                    logging.debug("Failed to parse %r" % partial)
                partial = bytearray()
            elif byte == 0xc0:
                # discard 0x00 command byte
                self.f.read(1)
            elif byte == 0xdb:
                nextbyte = self.f.read(1)
                if len(nextbyte) == 0:
                    return
                nextbyte = ord(nextbyte)
                if nextbyte == 0xdc:
                    partial.append(0xc0)
                elif nextbyte == 0xdd:
                    partial.append(0xdb)
            else:
                partial.append(byte)
