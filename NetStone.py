import socket
import asyncio
from StructureStone import *

class StoneTransferProtocol:
    def SetupConnection( self , addr : str, port :int, listen : int) :
        
        if self.socket == None:
        
            self.s.bind( ( addr, port ) )
            self.s.listen( listen )
            
        self.socket = self.s.accept()
        self.client = self.socket[0]

        return self.socket

    def ParsingPacket(self, Packet: StructStone) -> StructRawStonePayload:
        
        packet_data = Packet.payload.split(b"<>")
        
        while len(packet_data) < 4:
            packet_data.append(b"")
            
        return StructStonePayload( sysinfo= packet_data[0],
                                   command_input= packet_data[1], 
                                   response= packet_data[2],
                                   file= packet_data[3]
                                   )

    async def SendStone( self, session, Stone ):
        try:
            session.writer.write( Stone.stone )
            await session.writer.drain()
                        
        except Exception as e:

            return f'failed... Reason: { e }'
        
        finally:
            return Stone

    async def ReceiveStone( self, reader, buffer_size: int = 12 ) -> StructStone:
        Packet = await reader.read(buffer_size)

        if buffer_size != 12:
            return StructStone( None, Packet ,None)
        
        Header = StructStoneHeader( Packet[0:4], Packet[4:8], Packet[8:12] )
        Payload = self.ParsingPacket( await self.ReceiveStone(reader, struct.unpack('I', Header.StoneSize )[0] ) )

        if Header.StoneSize:
            return StructStone( Header, Payload ,None)
        
        return StructStone( Header, None ,None)

    async def Disconnect( self, session ):
        session.writer.write( ConstructStone().Disconnect().stone )
        await session.writer.drain()
        session.writer.close()
            
        
        
            