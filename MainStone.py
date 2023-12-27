from StructureStone import *
from dataclasses import dataclass, field
from NetStone import StoneTransferProtocol
import asyncio, threading, secrets, socket


class Server:
    def __init__(self, *address: list) -> None:
        self.__STP = StoneTransferProtocol()
        self.struct = ConstructStone()
        self.__Server_thread = threading.Thread(target=self.__run_service_handle, daemon=True)
        self.__Command_thread = threading.Thread(target=self.__run_command_handler, daemon=True)
        self.__address = address
        self.Sessions = set([])
        self.Session = None
        self.regular_sockets = {}
        self.packets = {}
        self.response = None
        self.command_list: dict = {
            "sessions" : self.__display_sessions, 
            "session"  : self.__display_session,
            "status"   : self.__display_server_status,
            }
        print(f"""
            \r\n
            =========================================
                C&C Server Successfully Started!
            =========================================

            Server Status: Active
            Version: [ 0.0.1 ]
            Address: [ {self.__address[0]} ]
            Port: [ {self.__address[1]} ]

            The server is up and running smoothly. What would you like to do?
            Type 'help' for assistance.
            Type 'exit' to shut down the server.

            =========================================
            \r\n\r\n""")
        
    def run(self):
        self.__Server_thread.start()
        self.__Command_thread.start()
        self.__Server_thread.join()
        self.__Command_thread.join()
        
    def __run_service_handle(self):
        # asyncio.run(self.__handle_Service())
        pass
        
    def __run_command_handler(self):
        # asyncio.run(self.__handle_command())
        pass
            
    async def __handle_Service(self):
        # self.server = await asyncio.start_server( self.__handle_client, *self.__address )   
        
        # async with self.server:
        #     await self.server.serve_forever()
        pass
        
    async def __handle_client(self,reader, writer):
        # packet = await self.__STP.AsyncReceiveStone(reader)

        if packet.header.StoneType == struct.pack('I', 0 ):
            session = Session( writer.get_extra_info('peername'), reader, writer )
            self.regular_sockets[session.SessionID] = self.__STP.regular_socket(writer.get_extra_info('socket'))
            self.packets[session.SessionID] = packet
            self.Sessions.add( session )
        
    async def __handle_command(self):
        while True:
            cmd = input("Server: ")
            
            for command, function in self.command_list.items():
                if cmd == command:
                    print( function() )
                
            if cmd.startswith("set"):
                print( self.__set_command(cmd) )
                
            elif self.Session:
                await self.__client_command(cmd)
                
            elif await self.__shutdown_command( cmd ):
                break
            # else:
            #     print(f"\nCommand {cmd} not found\n")
            
        exit()
        
        
    async def __client_command(self, cmd):
        if cmd == "close":
            await self.__STP.Disconnect(self.Session)
            self.Sessions.remove(self.Session)
            print(f"\nDisconnected from session: {self.Session.SessionID}\n")
            self.Session = None
            
        elif cmd == "exit":
            print("\nSession: {self.Session.SessionID} is Deselect.\n")
            self.Session = None
            
        elif cmd.startswith("/"):
            sessionid = self.Session.SessionID
            await self.__STP.SendStone(self.Session, self.struct.Command(cmd.replace("/", "")))
            self.packets[sessionid] = self.__STP.ReceiveStone(self.regular_sockets[sessionid])
            print(self.packets[sessionid].payload.decode("cp949"))
        
        
    def __display_sessions(self):
        display_session = "\n====== [ Index ] ====== [ Address ] ========== [ ID ] ========="
        count = 0
        for Session in self.Sessions:
            display_session += f"\n|      index : {count}       [ {Session.Address[0]} ]    [ {Session.SessionID} ]  |"
            count+=1
        display_session += "\n==========================[ end ]==============================\n"
        return display_session
        
        
    def __display_session(self):
        if self.Session == None:
            return f"\nNo session has been selected.\nUse the 'set' command to select a session\n"
            
        return f"\nThe currently selected session is {self.Session.SessionID}.\n"
    
    def __display_server_status(self):
        return f"\nServer activation status: {self.server.is_serving()}\n"
        
        
    def __set_command(self, cmd):
        session_id = cmd.replace("set", "").replace(" ", "")
        if not session_id:
            return "\nThe 'set' command must include the 'SessionID'\n"
            
        found_session = next((session for session in self.Sessions if session.SessionID == session_id), None)
        
        if not found_session:
            return "\nSession not found.\n"
            
        self.Session = found_session
        return f"\n{session_id} Session has been selected.\n"


    async def __shutdown_command(self, cmd):
        if (len(self.Sessions) == 0 and cmd == "shutdown"):
            
            print("\nThe server has shut down.\n")
            await self.server.wait_closed()
            
            return True
        
        elif cmd == "shutdown":
            
            for session in self.Sessions:
                await self.__STP.Disconnect(session)
            print("\nThe server has shut down.\n")
            
            return True
        
        return False
     
                
    
@dataclass
class Session:
    SessionID: str = field(init=False, default=None)
    Address: tuple
    reader: None
    writer: None

    def __post_init__(self):
        self.SessionID = SessionID(8).Token

    def __hash__(self):
        return hash(self.SessionID)
    
@dataclass
class SessionID:
    """
    Data class representing a session identifier.
    python
    Copy code
    Attributes:
    length (int): The length of the session identifier.
    Token (str): The session token (automatically generated).
    """
    length: int
    Token: str = field(init=False, default=None)

    def __post_init__(self):
        """
        Method executed after initialization.
        Generates the session token.
        """
        self.Token = secrets.token_hex(self.length)
    
Server("127.0.0.1", 6974).run()