'''
  ETTTP_Sever_skeleton.py

  34743-02 Information Communications
  Term Project on Implementation of Ewah Tic-Tac-Toe Protocol

  Skeleton Code Prepared by JeiHee Cho
  May 24, 2023

 '''

import random           # random 모듈을 가져옴(누가 start할지 랜덤으로 정하기 위해)
import tkinter as tk    # 게임에 사용할 GUI를 구현하기 위해 tkinter 모듈을 가져옴
from socket import *    # socket programming을 하기 위해 socket 모듈을 가져옴
import _thread          # thread를 사용하기 위해 thread 모듈 import

from ETTTP_TicTacToe import TTT, check_msg    # ETTTP_TicTacToe.py의 TTT클래스와 check_msg함수를 사용하기 위해 import

# name이라는 변수 값이 main이면 아래 코드 실행
if __name__ == '__main__':

    global send_header, recv_header
    SERVER_PORT = 12000                                 # 서버에서 Tic-Tac-Toe 프로그램의 포트 번호
    SIZE = 1024                                         # socket의 주고 받는 메세지의 크기를 사전에 정함
    server_socket = socket(AF_INET, SOCK_STREAM)        # 서버의 소켓 생성. AF_INET: IPv4인터넷 프로토콜 사용 , SOCK_STREAM: 연결 지향형 소켓. 
    server_socket.bind(('', SERVER_PORT))               # 소켓 주소 정보 할당 
    server_socket.listen()                              # 연결 수신 대기 상태
    MY_IP = '127.0.0.1'                                 # 서버의 ip

    while True:                                              # 서버는 client가 연결을 요청할떄까지 while문을 돌며 기다린다.
        client_socket, client_addr = server_socket.accept()  # 연결 수락. server와 client를 연결해주는 새로운 소켓 client_socket이 생성된다.
        # client_socket: 연결에서 데이터를 보내고 받을 수 있는 새로운 소켓 객체
        # client_addr: 연결의 다른 끝에 있는 소켓의 주소

        ###################################################################
        # Send start move information to peer
        start = random.randrange(0, 2)  # select random to start            # 랜덤으로 선 플레이어 선정. 0:server/1:client
        startStr = str(start)                                               # 뽑은 번호(0or1)을 문자열로 전환
        client_socket.send(startStr.encode())                               # start를 client에 보낸다.

        ######################### Fill Out ################################
        # Receive ack - if ack is correct, start game 
        startACK = client_socket.recv(SIZE).decode()                                    # client에서 보낸 ACK를 받고 바이트 형식의 데이터를 문자열로 decode
        startACKsplit = startACK.replace("\r\n", " ").replace(":", " ").split(" ")      # ACK 메세지에서 줄바꿈과 ":"를 띄어쓰기로 교체 후, 띄어쓰기를 기준으로 문자열 분리
        if not (startACKsplit[1] == "ETTTP/1.0"):               # 2번째 문자열에 프로토콜 정보가 담겨있다. ETTTP/1.0이 맞는지 확인
            print("잘못된 프로토콜")                                # 에러 메시지 출력
            client_socket.close()                               # 소켓 close
        if not (startACKsplit[3] == str(MY_IP)):                # 4번째 문자열에 메시지를 보낼 IP주소가 담겨있다. 즉, 받은 server 입장에선 자신의 IP주소가 담겨있어야 한다.
            print("잘못된 ip주소")                                 # 잘못된 ip 주소인 경우 에러 메시지 출력
            client_socket.close()                               # 소켓 close
        
        # 선 플레이어가 잘 전달됐는지 확인
        if (start == 0):                                        # 서버가 선인 경우                              
            if not (startACKsplit[5] == "YOU"):                 # 6번째 문자열에 YOU(client입장에서 server)가 있어야 한다.
                client_socket.close()                           # 아니라면 소켓 close
        elif (start == 1):                                      # 클라이언트가 선인 경우 
            if not (startACKsplit[5] == "ME"):                  # 6번째 문자열에 ME(client입장에서 자기 자신)가 있어야 한다.
                client_socket.close()                           # 아니라면 소켓 close

        print("연결 성공")                                        # 연결 성공 메세지 출력

        ###################################################################

        root = TTT(client=False, target_socket=client_socket, src_addr=MY_IP, dst_addr=client_addr[0])  
        # 자신이 서버라는 정보(client=false), 연결된 소켓, 자신의 IP주소, 상대의 IP주소를 매개변수로 넘겨 TTT클래스의 객체 생성
        root.play(start_user=start)     # TTT클래스의 play함수 수행. Tic-Tac-Toe 의 시작. 선 플레이어가 누군지에 대한 정보 start를 매개변수로 전달한다.
        root.mainloop()                 # 윈도우 내부에서 수행되는 마우스 클릭 같은 이벤트들이 발생하게끔 유지해주는 함수. 이벤트로부터 오는 메시지를 받고 전달하는 역할

        client_socket.close()           # 소켓 close

        break
    server_socket.close()               # while문 무한루프 종료. 서버의 소켓을 닫는다. 더이상 소켓 연결 요청을 받지 않는다.