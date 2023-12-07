from StructureStone import *
from NetStone import StoneTransferProtocol


def run():
    STP = StoneTransferProtocol()
    STP.SetupConnection('127.0.0.1', 6974, 0)

    while True:
        req = STP.ReceiveStone()

        if req.header.StoneType == struct.pack("I", 3):
            print(req.payload.response.decode("cp949"))

        stone = input("Send command: ")

        if stone == "exit":
            STP.SendStone(disconnect().stone)
            if STP.ReceiveStone().header.StoneType == struct.pack("I", 5):
                print("Client has disconnected.")
                break
            
        elif stone in "download":
            STP.SendStone(handle_download(stone.split(" ")[0]).stone)
            
        else:
            STP.SendStone(handle_command(stone).stone)

    STP.Disconnect()
    
def handle_command(input= ""):
    SSP = ConstructStonePayload.from_(StructRawStonePayload("sys_info", input, "", ""))
    SSH = ConstructStoneHeader.from_(SSP)
    return ConstructStone.from_(SSH, SSP)

def disconnect():
    SSP = ConstructStonePayload.from_(StructRawStonePayload("", "", "", ""))
    SSH = ConstructStoneHeader.from_(SSP)
    return ConstructStone.from_(SSH, SSP)

def handle_download(path):
    SSP = ConstructStonePayload.from_(StructRawStonePayload("sys_info", "", "", path))
    SSH = ConstructStoneHeader.upload(SSP)
    return ConstructStone.from_(SSH, SSP)

run()
