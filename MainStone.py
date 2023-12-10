from StructureStone import *
from dataclasses import dataclass, field
from NetStone import StoneTransferProtocol
import asyncio, threading, secrets


class Server:
    def __init__(self, *address: list) -> None:
        self.__STP = StoneTransferProtocol()
        self.struct = ConstructStone()
        self.__Server_thread = threading.Thread(target=self.__run_service_handle, daemon=True)
        self.__Command_thread = threading.Thread(target=self.__run_command_handler, daemon=True)
        self.__address = address
        self.Sessions = set([])
        self.Session = None
        self.response = None
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
        exit()
        
    def __run_service_handle(self):
        asyncio.run(self.__handle_Service())
        
    def __run_command_handler(self):
        asyncio.run(self.__handle_command())
            
    async def __handle_Service(self):
        self.server = await asyncio.start_server( self.__handle_client, *self.__address )   
        
        async with self.server:
            await self.server.serve_forever()
        
    async def __handle_client(self,reader, writer):
        packet = await self.__STP.ReceiveStone(reader)
        self.Sessions.add( Session( writer.get_extra_info('peername'), reader, writer, packet ) )
            
        
    async def __handle_command(self):
        while True:
            cmd = input("Server: ")
            
            if cmd == "sessions":
                self.__display_sessions()
                
            elif cmd == "session":
                self.__display_session()
                    
            elif cmd == "status":
                print(f"\nServer activation status: {self.server.is_serving()}")
                
            elif cmd.startswith("set"):
                self.__set_command(cmd)
                    
            self.__client_command(cmd)
                
            if await self.__shutdown_command(self, cmd):
                break
        exit()
        
        
    async def __client_command(self, cmd):
        if cmd == "close":
            await self.__STP.Disconnect(self.Session)
            self.Sessions.remove(self.Session)
            print(f"\nDisconnected from session: {self.Session.SessionID}")
            self.Session = None
            
        elif cmd == "exit":
            
            print(f"\nSession: {self.Session.SessionID} is Deselect.")
            self.Session = None
            
        elif cmd.startswith("/"):
        
            await self.__STP.SendStone(self.Session, self.struct.Command(cmd.replace("/", "")))
        
        
    def __display_sessions(self):
        print("\n====== [ Index ] ====== [ Address ] ========== [ ID ] =========")
        count = 0
        for Session in self.Sessions:
            print(f"|      index : {count}       [ {Session.Address[0]} ]    [ {Session.SessionID} ]  |")
            count+=1
        print("==========================[ end ]==============================")
        
        
    def __display_session(self):
        if self.Session == None:
            print(f"\nNo session has been selected.\nUse the 'set' command to select a session")
            
        else:
            print(f"\nThe currently selected session is {self.Session.SessionID}.")
        
        
    def __set_command(self, cmd):
        cmd = cmd.replace("set", "").replace(" ", "")
        if cmd:
            
            session_id = cmd
            found_session = next((session for session in self.Sessions if session.SessionID == session_id), None)
            
            if found_session:
                
                self.Session = found_session
                print(f"\n{session_id } Session has been selected.")
                
            else:
                
                print("\nSession not found.")
        else:
            
            print("\nThe 'set' command must include the 'SessionID'")


    async def __shutdown_command(self, cmd):
        if (len(self.Sessions) == 0 and cmd == "shutdown"):
            
            print("\nThe server has shut down.")
            await self.server.wait_closed()
            
            return True
        
        elif cmd == "shutdown":
            
            for session in self.Sessions:
                await self.__STP.Disconnect(session)
            print("\nThe server has shut down.")
            
            return True
        
        return False
     
                
    
@dataclass
class Session:
    SessionID: str = field(init=False, default=None)
    Address: tuple
    reader: None
    writer: None
    pecket: bytes

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