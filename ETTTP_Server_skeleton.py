'''
  ETTTP_Sever_skeleton.py

  34743-02 Information Communications
  Term Project on Implementation of Ewah Tic-Tac-Toe Protocol

  Skeleton Code Prepared by JeiHee Cho
  May 24, 2023

 '''

import random
import tkinter as tk
from socket import *
import _thread

from ETTTP_TicTacToe_skeleton import TTT, check_msg

# name이라는 변수 값이 main이면 아래 코드 실행
if __name__ == '__main__':

    global send_header, recv_header
    SERVER_PORT = 12000
    SIZE = 1024
    server_socket = socket(AF_INET, SOCK_STREAM)
    server_socket.bind(('', SERVER_PORT))
    server_socket.listen()
    MY_IP = '127.0.0.1'

    while True:
        client_socket, client_addr = server_socket.accept()  # 연결되도록 기다림

        ###################################################################
        # Send start move information to peer
        start = random.randrange(0, 2)  # select random to start
        startStr = str(start)
        client_socket.send(startStr.encode())  # start를 client에 보낸다.

        ######################### Fill Out ################################
        # Receive ack - if ack is correct, start game 
        startACK = client_socket.recv(1024).decode()
        startACKsplit = startACK.replace("\r\n", " ").replace(":", " ").split(" ")
        if not (startACKsplit[1] == "ETTTP/1.0"):
            print("잘못된 프로토콜")
            client_socket.close()
        if not (startACKsplit[3] == str(MY_IP)):
            print("잘못된 ip주소")
            client_socket.close()

        if (start == 0):  # 서버 
            if not (startACKsplit[5] == "YOU"):
                client_socket.close()
        elif (start == 1):
            if not (startACKsplit[5] == "ME"):
                client_socket.close()

        print("연결 성공")

        ###################################################################

        root = TTT(client=False, target_socket=client_socket, src_addr=MY_IP, dst_addr=client_addr[0])
        root.play(start_user=start)
        root.mainloop()

        client_socket.close()

        break
    server_socket.close()