import socket
import math
from StructureStone import *

class StoneTransferProtocol:
    def __init__(self) -> None:
        self.s = socket.socket()
        self.socket = None
        self.client = None
    
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

    def SendStone( self, session, Stone ):
        try:
            session.Address.send( Stone.stone )
                        
        except Exception as e:

            return f'failed... Reason: { e }'
        
        finally:
            return Stone
    
    def ReceiveStone( self, socket, buffer_size: int = 12 ) -> StructStone:
        if buffer_size > 12:
            Packets = [socket.recv(2048) for _ in range(math.ceil(buffer_size / 2048))]
            return StructStone(None, bytearray().join(Packets), None)
        else:
            Packet = socket.recv( buffer_size )
        
        if buffer_size == 12:
            Header = StructStoneHeader( Packet[0:4], Packet[4:8], Packet[8:12] )
            Payload = self.ParsingPacket( self.ReceiveStone(socket, struct.unpack('I', Header.StoneSize )[0] ) )
            return StructStone( Header, Payload ,None)
        
        return StructStone( None, Packet ,None)

    def Disconnect( self, session ):
        try:
            session.Address.send( ConstructStone().Disconnect().stone )
            session.Address.close()
        except ConnectionResetError as e:
            print("\n",e)
        
    def Download( self, session, path):
        try:
            session.Address.send( ConstructStone().Download(path).stone )
        except ConnectionResetError as e:
            print("\n",e)
        
    def Upload( self, session, file):
        try:
            session.Address.send( ConstructStone().Upload(file).stone )
        except ConnectionResetError as e:
            print("\n",e)

            
        
        
            