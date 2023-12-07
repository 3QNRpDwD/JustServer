from dataclasses import dataclass, field
from datetime import datetime, timedelta
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
        cmd_output  = SRSP.response .encode()
        file = SRSP.file    .encode()
        
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
    
    def upload(SSP: StructStonePayload) -> StructStoneHeader:
        StoneSize = len(SSP.sysinfo) + len(SSP.file)
        return StructStoneHeader(struct.pack("I", 0), struct.pack("I", 7), struct.pack("I", StoneSize))
    
    def Download(SSP: StructStonePayload) -> StructStoneHeader:
        StoneSize = len(SSP.sysinfo) + len(SSP.file)
        return StructStoneHeader(struct.pack("I", 0), struct.pack("I", 8), struct.pack("I", StoneSize))


    def __init__(self, packed_data):
        self.packed_data = packed_data

class ConstructStone:
    
    def from_(SSH: StructStoneHeader, SSP: StructStonePayload) -> StructStone:
        header = SSH.StoneStatus + SSH.StoneType + SSH.StoneSize
        payload = f'{SSP.sysinfo}<>{SSP.command_input}<>{SSP.response}<>{SSP.file}<>'.encode()
        stone = header + payload
        
        return  StructStone(header, payload, stone)

class protocolRules:
    def __init__(self) -> None:
        self.Rules = [
                        { 0 : "sysinfo", 1 : "command_input", 2 : "response", 3 : "file" },
                        { 0 : "sysinfo", 1 : "command_input", 2 : "response", 3 : "file" }
                    ]

    def from_json():
        pass

    def to_json():
        pass