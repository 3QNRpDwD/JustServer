import socket
from StructureStone import *

class StoneTransferProtocol:

    def __init__( self  ):
        self.s = socket.socket()
        self.socket = None
        self.client = None

    def SetupConnection( self , addr : str, port :int, listen : int) :
        
        if self.socket == None:
        
            self.s.bind( ( addr, port ) )
            self.s.listen( listen )
            
            print(f"""
            \r\n
            =========================================
                C&C Server Successfully Started!
            =========================================

            Server Status: Active
            Version: [ 0.0.1 ]
            Address: [ {addr} ]
            Port: [ {port} ]

            The server is up and running smoothly. What would you like to do?
            Type 'help' for assistance.
            Type 'exit' to shut down the server.

            =========================================\r\n\r\n""")
            
        self.socket = self.s.accept()
        self.client = self.socket[0]

        return self.socket
    
    def Disconnect( self ):
        self.client.close 

    def identifyPacketType( self, Packet: StructStoneHeader ) -> str:
        pass


    def ParsingPacket(self, Packet: StructStone) -> StructRawStonePayload:
        packet_data = Packet.payload.split(b"..")
        
        while len(packet_data) < 4:
            packet_data.append(b"")  # 빈 문자열이나 다른 기본값을 추가하거나 필요에 따라 수정하세요.

        return StructStonePayload(*packet_data)

    def SendStone( self, Stone ):

        try:
            self.client.send( Stone )
        
        except Exception as e:

            return f'failed... Reason: { e }'

    def ReceiveStone( self, buffer_size: int = 12 ) -> StructStone:

        Packet = self.client.recv( buffer_size )

        if buffer_size != 12:
            return StructStone( None, Packet ,None)
        
        Header = StructStoneHeader( Packet[0:4], Packet[4:8], Packet[8:12] )
        Payload = self.ParsingPacket( self.ReceiveStone( struct.unpack('I', Header.StoneSize )[0] ) )

        if Header.StoneSize:
            return StructStone( Header, Payload ,None)
        
        return StructStone( Header, None ,None)
        
        
            