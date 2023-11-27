from StructureStone import *
from NetStone import StoneTransferProtocol



def Run():

    STP = StoneTransferProtocol()
    
    while True:
        
        STP.SetupConnection( '127.0.0.1', 6974, 0 )
    
        req = STP.ReceiveStone() # 클라이언트로 부터의 요청을 대기
        stone = input("send command : ")
        SSP = ConstructStonePayload.from_( StructRawStonePayload( "sysinfo", stone, "", "" ) ) # 요청에 대한 응답에 대한 페이로드 생성
        SSH = ConstructStoneHeader.from_( SSP ) # 페이로드를 토대로 응답 헤더를 생성
        res = ConstructStone.from_( SSH, SSP ) # 헤더와 페이로드를 결합
        
        STP.SendStone( res.stone ) # 결홥된 페이로드와 헤더를 클라이언트로 전송

Run()