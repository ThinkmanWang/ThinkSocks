# -*- coding: utf-8 -*-

import sys
import os
import asyncio
import struct
import socket
import base64

import tornado.ioloop

from tornado.tcpserver import TCPServer
from tornado.tcpclient import TCPClient
from tornado.iostream import StreamClosedError
from tornado import gen

from pythinkutils.common.BinaryStream import BinaryStream

from pythinkutils.common.log import g_logger
from pythinkutils.aio.common.aiolog import g_aio_logger

class TCPConnection(object):

    SOCKS_VERSION = 0x05
    METHOD_NO_AUTH = 0x00
    METHOD_AUTH_BY_USERNAME_PASSWORD = 0x02
    NO_ACCEPTABLE_METHODS = 0xFF
    BUFFER_SIZE = 1024

    COMMAND_MAP = {
        0x01: 'CONNECT',
        0x02: 'BIND',
        0x03: 'UDP ASSOCIATION'
    }

    ACCEPTED_COMMANDS = [0x01, ]

    ADDRESS_TYPE_MAP = {
        0x01: 'IPv4 Address',
        0x03: 'Domain name',
        0x04: 'IPv6 Address'
    }
    ADDRESS_TYPE_LENGTH = {
        0x01: 4,
        0x04: 16
    }
    ACCEPTED_ADDRESS_TYPES = [0x01, 0x03, 0x04]
    REPLY_CODES = {
        0x00: 'succeeded',
        0x01: 'general SOCKS server failure',
        0x03: 'Network unreachable',
        0x04: 'Host unreachable',
        0x05: 'Connection refused',
        0x07: 'Command not supported',
        0x08: 'Address type not supported',
    }

    def __init__(self, stream, address):
        self.__stream = stream
        self.__upstream = None
        self.m_szClientAddress = address[0]
        self.m_nClientPort = address[1]

        self.m_byteVer = b"\x05"
        self.m_byteNMethod = b"\x01"
        self.m_byteMethods = b"\x00"

        self.m_byteCmd = b"\x00"
        self.m_byteRsv = b"\x00"
        self.m_byteATYP = b"\x01"
        self.m_byteAddressLen = b"\x00"
        self.m_byteAddress = b"\x00\x00\x00\x00"
        self.m_byteDstPort = b"\x00\x00"

        self.m_szUsername = ""
        self.m_szPassword = ""
        self.m_szAddress = None
        self.m_nPort = 0

        asyncio.gather(self.on_start())
        self.__stream.set_close_callback(self.on_close)

    def on_close(self):
        if self.__stream is not None \
                and self.__stream.closed() is False:
            self.__stream.close()
            self.__stream = None

        if self.__upstream is not None \
                and self.__upstream.closed() is False:
            self.__upstream.close()
            self.__upstream = None

        g_logger.info("TCP Closed")

    async def on_start(self):
        try:
            '''
            X'00' NO AUTHENTICATION REQUIRED
            X'01' GSSAPI
            X'02' USERNAME/PASSWORD
            X'03' to X'7F' IANA ASSIGNED
            X'80' to X'FE' RESERVED FOR PRIVATE METHODS
            X'FF' NO ACCEPTABLE METHODS

            +----+----------+----------+
            |VER | NMETHODS | METHODS  |
            +----+----------+----------+
            | 1  |    1     | 1 to 255 |
            +----+----------+----------+

            '''
            byteData = await self.__stream.read_bytes(2)
            nVer, nMethods = struct.unpack("!BB", byteData)

            if TCPConnection.SOCKS_VERSION != nVer:
                self.on_close()
                return

            if nMethods <= 0:
                self.on_close()
                return

            byteData = await self.__stream.read_bytes(nMethods)
            if b"\x02" not in byteData:
                await self.__stream.write(struct.pack("!BB", TCPConnection.SOCKS_VERSION, TCPConnection.NO_ACCEPTABLE_METHODS))
                self.on_close()
                return

            self.__stream.write(struct.pack("!BB", TCPConnection.SOCKS_VERSION, TCPConnection.METHOD_AUTH_BY_USERNAME_PASSWORD))

            byteData = await self.__stream.read_bytes(2)
            nVer = int(byteData[0])
            nUlen = int(byteData[1])
            self.m_szUsername = (await self.__stream.read_bytes(nUlen)).decode(ThinkSocks.ENCODING)

            byteData = await self.__stream.read_bytes(1)
            nPlen = int(byteData[0])
            self.m_szPassword = (await self.__stream.read_bytes(nPlen)).decode(ThinkSocks.ENCODING)

            bValid = await self.user_pwd_valid()

            if bValid is False:
                response = struct.pack("!BB", 1, 0xFF)
                self.__stream.write(response)
                self.on_close()
                return

            response = struct.pack("!BB", 1, 0)
            self.__stream.write(response)

            byteData = await self.__stream.read_bytes(4)
            await self.on_s5_command(byteData)

        except Exception as ex:
            await g_aio_logger.error(ex)
            self.on_close()

    '''
    +----+-----+-------+------+----------+----------+
    |VER | CMD |  RSV  | ATYP | DST.ADDR | DST.PORT |
    +----+-----+-------+------+----------+----------+
    | 1  |  1  | X'00' |  1   | Variable |    2     |
    +----+-----+-------+------+----------+----------+

    Where:

          o  VER    protocol version: X'05'
          o  CMD
             o  CONNECT X'01'
             o  BIND X'02'
             o  UDP ASSOCIATE X'03'
          o  RSV    RESERVED
          o  ATYP   address type of following address
             o  IP V4 address: X'01'
             o  DOMAINNAME: X'03'
             o  IP V6 address: X'04'
          o  DST.ADDR       desired destination address
          o  DST.PORT desired destination port in network octet
             order

    '''
    async def on_s5_command(self, data):
        version, cmd, _, address_type = struct.unpack("!BBBB", data)  # 5, 1, 0, 1
        self.m_byteCmd = data[1]
        self.m_byteRsv = data[2]
        self.m_byteATYP = data[3]
        # await g_aio_logger.info("%d|%d|%d|%d" % (int(data[0]), int(data[1]), int(data[2]), int(data[1])))

        if 1 != self.m_byteCmd:
            await g_aio_logger.info("Only support TCP")
            self.on_close()
            return

        self.m_nAddressType = address_type
        if 1 == address_type:  # IPv4
            byteData = await self.__stream.read_bytes(4)
            self.m_byteAddress = byteData
            self.m_szAddress = self._convert_readable_address(byteData)
            byteData = await self.__stream.read_bytes(2)
            await self.on_destination_port(byteData)

        elif 3 == address_type:  # DOMAINNAME
            byteData = await self.__stream.read_bytes(1)
            self.m_byteAddressLen = byteData
            nAddressLength = int(byteData)
            byteData = await self.__stream.read_bytes(nAddressLength)
            self.m_szAddress = byteData.decode(ThinkSocks.ENCODING)
            self.m_byteAddress = byteData
            byteData = await self.__stream.read_bytes(2)
            await self.on_destination_port(byteData)

        elif 4 == address_type:  # IP V6 address
            self.m_byteAddress = await self.__stream.read_bytes(16)
            byteData = await self.__stream.read_bytes(2)
            await self.on_destination_port(byteData)

        else:
            await g_aio_logger.info("Unknow address type!!!")
            self.on_close()
            return


    async def on_destination_port(self, data):
        # await g_aio_logger.info("%s" % (base64.encodestring(data).replace("\n", "").replace("\\n", "")))

        self.m_nPort, = struct.unpack("!H", data)
        self.m_byteDstPort = data

        # reply = struct.pack("!BBBBIH", TCPConnection.SOCKS_VERSION, 0, 0, address_type, addr, port)
        bs = BinaryStream()
        bs.writeBytes(self.m_byteVer)
        bs.writeBytes(b"\x00")
        bs.writeBytes(b"\x00")
        bs.writeBytes(bytes([self.m_byteATYP]))
        bs.writeBytes(self.m_byteAddress)
        bs.writeBytes(self.m_byteDstPort)
        byteReply = bs.base_stream.getvalue()
        self.m_nlenReply = len(byteReply)
        await self.__stream.write(byteReply)
        await self.do_command()

    async def request(self):
        try:
            while self.__stream is not None \
                    and self.__stream.closed() is False \
                    and self.__upstream is not None \
                    and self.__upstream.closed() is False:
                byteData = await self.__stream.read_bytes(TCPConnection.BUFFER_SIZE, True)
                szContent = base64.b64encode(byteData)
                await g_aio_logger.info(szContent)
                await self.__upstream.write(byteData)

        except Exception as ex:
            # await g_aio_logger.error(ex)
            self.on_close()

    async def response(self):
        try:
            while self.__stream is not None \
                    and self.__stream.closed() is False \
                    and self.__upstream is not None \
                    and self.__upstream.closed() is False:
                byteData = await self.__upstream.read_bytes(TCPConnection.BUFFER_SIZE, True)
                szContent = base64.b64encode(byteData)
                await g_aio_logger.info(szContent)
                await self.__stream.write(byteData)

        except Exception as ex:
            # await g_aio_logger.error(ex)
            self.on_close()

    async def do_command(self):
        self.__upstream = await TCPClient().connect(self.m_szAddress, self.m_nPort)

        asyncio.ensure_future(self.request())
        asyncio.ensure_future(self.response())

    def _convert_readable_address(self, addr):
        return socket.inet_ntop(socket.AF_INET if self.m_nAddressType == 0x01
                                else socket.AF_INET6, addr)

    async def user_pwd_valid(self):
        if "Ab123145" == self.m_szPassword:
            return True
        else:
            return False

class ThinkSocks(TCPServer):
    ENCODING = "utf-8"

    async def handle_stream(self, stream, address):
        # await g_aio_logger.info("TCP Connected...")
        TCPConnection(stream, address)
