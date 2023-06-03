'''
  ETTTP_Client_skeleton.py

  34743-02 Information Communications
  Term Project on Implementation of Ewah Tic-Tac-Toe Protocol

  Skeleton Code Prepared by JeiHee Cho
  May 24, 2023

 '''

import random           # random 모듈을 가져옴(누가 start할지 랜덤으로 정하기 위해)
import tkinter as tk    # 게임에 사용할 GUI를 구현하기 위해 tkinter 모듈을 가져옴
from socket import *    # socket programming을 하기 위해 socket 모듈을 가져옴
import _thread          # thread를 사용하기 위해 thread 모듈 import

from ETTTP_TicTacToe_skeleton import TTT, check_msg     # ETTTP_TicTacToe_skeleton.py의 TTT클래스와 check_msg함수를 사용하기 위해 import

# name이라는 변수 값이 main이면 아래 코드 실행
if __name__ == '__main__':

    SERVER_IP = '127.0.0.1'                 # 연결 요청할 서버의 ip주소
    MY_IP = '127.0.0.1'                     # 클라이언트의 ip주소
    SERVER_PORT = 12000                     # 서버와 연결해 사용할 프로그램의 Port번호
    SIZE = 1024                             # socket의 주고 받는 메세지의 크기를 사전에 정함
    SERVER_ADDR = (SERVER_IP, SERVER_PORT)  # 접속 정보 설정

    with socket(AF_INET, SOCK_STREAM) as client_socket:     # 클라이언트 소켓 설정.  AF_INET: IPv4인터넷 프로토콜 사용 , SOCK_STREAM: 연결 지향형 소켓. 
        client_socket.connect(SERVER_ADDR)                  # 서버에 접속

        ###################################################################
        # Receive who will start first from the server
        startStr = client_socket.recv(SIZE).decode()        # 서버에서 보낸 선 플레이어 번호를 받아 문자열로 decode
        start = int(startStr)                               # 문자로 된 선 플레이어 번호를 정수로 변환

        ######################### Fill Out ################################
        # Send ACK

        # start가 0또는 1이라면 유효하다
        if (start == 1):                           # client가 선 플레이어
            ACK = "ACK ETTTP/1.0\r\nHost:"+SERVER_IP+"\r\nFirst-Move:ME\r\n\r\n"    # 서버 ip로 first-move가 자신이라는 ACK를 보낸다
            print("당신이 먼저 시작합니다")             # client가 선이라는 메세지 띄우기
        elif (start == 0):                         # server가 선 플레이어
            ACK = "ACK ETTTP/1.0\r\nHost:"+SERVER_IP+"\r\nFirst-Move:YOU\r\n\r\n"   # 서버 ip로 first-move가 상대라는 ACK를 보낸다
            print("상대가 먼저 시작합니다")             # 상대가 선이라는 메세지 띄우기
        else:                                     # 0또는 1이 아니라면 잘못된 경우이다
            client_socket.close()                 # 소켓 close
        client_socket.send(ACK.encode())          # 만든 ACK 메세지를 소켓을 통해 전달한다.

        ###################################################################

        # Start game
        root = TTT(target_socket=client_socket, src_addr=MY_IP, dst_addr=SERVER_IP)
        # 연결된 소켓, 자신의 IP주소, 상대의 IP주소를 매개변수로 넘겨 TTT클래스의 객체 생성
        root.play(start_user=start)     # TTT클래스의 play함수 수행. Tic-Tac-Toe 의 시작. 선 플레이어가 누군지에 대한 정보 start를 매개변수로 전달한다.
        root.mainloop()                 # 윈도우 내부에서 수행되는 마우스 클릭 같은 이벤트들이 발생하게끔 유지해주는 함수. 이벤트로부터 오는 메시지를 받고 전달하는 역할
        client_socket.close()           # 소켓 close
        
        