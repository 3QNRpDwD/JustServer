from dataclasses import dataclass, field
import struct

@dataclass
class StructRawStonePayload:
    sysinfo: str
    command_input: str
    response: str
    file: str

@dataclass
class StructStonePayload:

    sysinfo: bytes
    command_input: bytes
    response: bytes
    file: bytes

@dataclass
class StructStoneHeader:

    StoneStatus : bytes
    StoneType   : bytes
    StoneSize   : bytes

@dataclass
class StructStone:

    header: StructStoneHeader
    payload: StructStonePayload
    stone: bytes
    
@dataclass
class StoneChain: 

    previous_stone_hash: bytes
    stone_hash: bytes
    stonetree_hash: bytes
    timestamp: bytes
    transaction_list: bytes


class ConstructStonePayload:

    def from_(SRSP: StructRawStonePayload ) -> StructStonePayload:

        sysinfo     = SRSP.sysinfo        .encode()
        cmd_input   = SRSP.command_input  .encode()
        cmd_output  = SRSP.response       .encode()
        file = SRSP.file                  .encode()
        
        return StructStonePayload(sysinfo, cmd_input, cmd_output, file)

class ConstructStoneHeader:

    def from_(SSP: StructStonePayload) -> StructStoneHeader:
        sysinfo_len = len(SSP.sysinfo)
        cmd_input_len = len(SSP.command_input)
        cmd_output_len = len(SSP.response)

        StoneSize = sysinfo_len + cmd_input_len + cmd_output_len + 8
        StoneStatus = struct.pack("I", 0)

        if sysinfo_len and not cmd_input_len and not cmd_output_len: # Connection
            StoneType = struct.pack("I", 0)
        elif sysinfo_len and cmd_input_len and not cmd_output_len:   # ExecuteCmd
            StoneType = struct.pack("I", 2)
        elif sysinfo_len and not cmd_input_len and cmd_output_len:   # Response
            StoneType = struct.pack("I", 3)
        else:
            StoneType = struct.pack("I", 5)                          # Disconnect

        return StructStoneHeader(StoneStatus, StoneType, struct.pack("I", StoneSize))

    def __init__(self, packed_data):
        self.packed_data = packed_data

class ConstructStone:
    
    def from_(self, SSH: StructStoneHeader, SSP: StructStonePayload) -> StructStone:
        header = SSH.StoneStatus + SSH.StoneType + SSH.StoneSize
        payload = SSP.sysinfo+b'<>'+SSP.command_input+b'<>'+SSP.response+b'<>'+SSP.file+b'<>'
        stone = header + payload
        
        return  StructStone(header, payload, stone)

    def Upload(self, file: bytes) -> StructStoneHeader:
        SSP = StructStonePayload("sysinfo".encode(), bytearray(),bytearray(), file)
        return self.from_(StructStoneHeader(
                            struct.pack("I", 0),
                            struct.pack("I", 7),
                            struct.pack("I", len(SSP.sysinfo) + len(SSP.file) + 8)
                            ),
                          SSP
                        )
    
    def Download(self, file_path: str) -> StructStoneHeader:
        SSP = StructStonePayload("sysinfo".encode(), bytearray(), bytearray(), file_path.encode())
        return self.from_(StructStoneHeader(
                            struct.pack("I", 0),
                            struct.pack("I", 8),
                            struct.pack("I", len(SSP.sysinfo) + len(SSP.file) + 8)
                            ),
                          SSP
                        )

    def Command(self, cmd: str) -> StructStoneHeader:
        SSP = StructStonePayload("sysinfo".encode(), cmd.encode(), bytearray(), bytearray())
        return self.from_(StructStoneHeader(
                            struct.pack("I", 0),
                            struct.pack("I", 2),
                            struct.pack("I", len(SSP.sysinfo) + len(SSP.command_input) + 8)
                            ),
                          SSP
                        )
    
    def Disconnect(self) -> StructStoneHeader:
        return self.from_(StructStoneHeader(
                                struct.pack("I", 0),
                                struct.pack("I", 5),
                                struct.pack("I", 0)
                                ),
                          StructStonePayload(bytearray(), bytearray(), bytearray(), bytearray())
                        )

@dataclass
class StoneTransferProtocol:
    Connection :bytes = field(init=False, default=None)
    Handshake  :bytes = field(init=False, default=None)
    HealthCheck:bytes = field(init=False, default=None)
    Disconnect :bytes = field(init=False, default=None)

    ExecuteCmd :bytes = field(init=False, default=None)
    Upload     :bytes = field(init=False, default=None)
    Download   :bytes = field(init=False, default=None)
    Response   :bytes = field(init=False, default=None)
    Unknown    :None = field(init=False, default=None)
    
    def __post_init__(self):
        self.Connection  = struct.pack("I", 0)
        self.Handshake   = struct.pack("I", 1)
        self.HealthCheck = struct.pack("I", 4)
        self.Disconnect  = struct.pack("I", 5)

        self.ExecuteCmd  = struct.pack("I", 2)
        self.Upload      = struct.pack("I", 7)
        self.Download    = struct.pack("I", 8)
        self.Response    = struct.pack("I", 3)
        
        self.Unknown     = None
