# -*- coding: utf-8 -*-

from struct import *
from io import BytesIO

class BinaryStream:
    def __init__(self, base_stream = None):
        if base_stream is None:
            self.base_stream = BytesIO()
        else:
            self.base_stream = base_stream

    def readByte(self):
        return self.base_stream.read(1)

    def readBytes(self, length):
        return self.base_stream.read(length)

    def readChar(self, szByteOrder='!'):
        return self.unpack(szByteOrder + 'b')

    def readUChar(self, szByteOrder='!'):
        return self.unpack(szByteOrder + 'B')

    def readBool(self, szByteOrder='!'):
        return self.unpack(szByteOrder + '?')

    def readInt16(self, szByteOrder='!'):
        return self.unpack(szByteOrder + 'h', 2)

    def readUInt16(self, szByteOrder='!'):
        return self.unpack(szByteOrder + 'H', 2)

    def readInt32(self, szByteOrder='!'):
        return self.unpack(szByteOrder + 'i', 4)

    def readUInt32(self, szByteOrder='!'):
        return self.unpack(szByteOrder + 'I', 4)

    def readInt64(self, szByteOrder='!'):
        return self.unpack(szByteOrder + 'q', 8)

    def readUInt64(self, szByteOrder='!'):
        return self.unpack(szByteOrder + 'Q', 8)

    def readFloat(self, szByteOrder='!'):
        return self.unpack(szByteOrder + 'f', 4)

    def readDouble(self, szByteOrder='!'):
        return self.unpack(szByteOrder + 'd', 8)

    def readString(self):
        length = self.readUChar()
        return self.unpack(str(length) + 's', length)

    def writeBytes(self, value):
        self.base_stream.write(value)

    def writeChar(self, value, szByteOrder='!'):
        self.pack(szByteOrder + 'c', value)

    def writeUChar(self, value, szByteOrder='!'):
        self.pack(szByteOrder + 'C', value)

    def writeBool(self, value, szByteOrder='!'):
        self.pack(szByteOrder + '?', value)

    def writeInt16(self, value, szByteOrder='!'):
        self.pack(szByteOrder + 'h', value)

    def writeUInt16(self, value, szByteOrder='!'):
        self.pack(szByteOrder + 'H', value)

    def writeInt32(self, value, szByteOrder='!'):
        self.pack(szByteOrder + 'i', value)

    def writeUInt32(self, value, szByteOrder='!'):
        self.pack(szByteOrder + 'I', value)

    def writeInt64(self, value, szByteOrder='!'):
        self.pack(szByteOrder + 'q', value)

    def writeUInt64(self, value, szByteOrder='!'):
        self.pack(szByteOrder + 'Q', value)

    def writeFloat(self, value, szByteOrder='!'):
        self.pack(szByteOrder + 'f', value)

    def writeDouble(self, value, szByteOrder='!'):
        self.pack(szByteOrder + 'd', value)

    def writeString(self, value):
        length = len(value)
        self.writeUInt16(length)
        self.pack(str(length) + 's', value)

    def pack(self, fmt, data):
        return self.writeBytes(pack(fmt, data))

    def unpack(self, fmt, length = 1):
        return unpack(fmt, self.readBytes(length))[0]