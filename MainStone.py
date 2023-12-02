from StructureStone import *
from NetStone import StoneTransferProtocol


def run():
    STP = StoneTransferProtocol()
    STP.SetupConnection('127.0.0.1', 6974, 0)

    while True:
        req = STP.ReceiveStone()

        if req.header.StoneType == struct.pack("I", 1):
            print(req.payload.command_output.decode("cp949"))

        stone = input("Send command: ")

        if stone == "close":
            STP.SendStone(generator().stone)
            if STP.ReceiveStone().header.StoneType == struct.pack("I", 4):
                print("Client has disconnected.")
                break

        res = generator("sys_info",stone)

        STP.SendStone(res.stone)


    STP.Disconnect()
    
def generator(sys_info="", input= "", output= ""):
    SSP = ConstructStonePayload.from_(StructRawStonePayload(sys_info, input, output, ""))
    SSH = ConstructStoneHeader.from_(SSP)
    return ConstructStone.from_(SSH, SSP)

run()
