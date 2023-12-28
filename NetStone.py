import socket
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
        try:
            Packet = bytearray()
            for iter in range(int(buffer_size  / 2048)):
                Packet.append(socket.recv( 2048 ))

            if buffer_size != 12:
                return StructStone( None, Packet ,None)
            
            Header = StructStoneHeader( Packet[0:4], Packet[4:8], Packet[8:12] )
            Payload = self.ParsingPacket( self.ReceiveStone(socket, struct.unpack('I', Header.StoneSize )[0] ) )

            if Header.StoneSize:
                return StructStone( Header, Payload ,None)
            
            return StructStone( Header, None ,None)
        except Exception as e:
            print("\n", e)

    def Disconnect( self, session ):
        try:
            session.Address.send( ConstructStone().Disconnect().stone )
            session.Address.close()
        except ConnectionResetError as e:
            print("\n",e)
        
    def Download( self, session, path):
        try:
            session.Address.send( ConstructStone().Download(path).stone )
            ConstructStone().Download(path).stone
        except ConnectionResetError as e:
            print("\n",e)
        
    def Upload( self, session, file_name):
        try:
            session.Address.send( ConstructStone().Upload().stone )
        except ConnectionResetError as e:
            print("\n",e)

            
        
        
            