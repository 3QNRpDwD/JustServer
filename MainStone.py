from StructureStone import *
from NetStone import StoneTransferProtocol



def Run():

    STP = StoneTransferProtocol( '127.0.0.1', 6974, 0 )

    req = STP.ReceiveStone() # 클라이언트로부터의 요청을 대기

    print( f"받은거 : { req.header } \n받은거 : { req.payload }" ) # 받은 요청을 출력

    SSP = ConstructStonePayload.from_( StructRawStonePayload( "sysinfo..", "command_input..", "command_output..", "stone_chain.." ) ) # 요청에 대한 응답에 대한 페이로드 생성
    SSH = ConstructStoneHeader.from_( SSP ) # 페이로드를 토대로 응답 헤더를 생성

    res = ConstructStone.from_( SSH, SSP ) # 헤더와 페이로드를 결합

    print( f"보낸거 : { res.header } \n보낸거 : { res.payload }" ) # 생성된 헤더와 페이로드 출력

    STP.SendStone( res.stone ) # 결홥된 페이로드와 헤더를 클라이언트로 전송

Run()