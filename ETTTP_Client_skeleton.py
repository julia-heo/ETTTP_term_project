'''
  ETTTP_Client_skeleton.py

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

if __name__ == '__main__':

    SERVER_IP = '127.0.0.1'
    MY_IP = '127.0.0.1'
    SERVER_PORT = 12000
    SIZE = 1024
    SERVER_ADDR = (SERVER_IP, SERVER_PORT)

    with socket(AF_INET, SOCK_STREAM) as client_socket:
        client_socket.connect(SERVER_ADDR)  # connect 완료

        ###################################################################
        # Receive who will start first from the server
        startStr = client_socket.recv(1024).decode()
        start = int(startStr)

        ######################### Fill Out ################################
        # Send ACK

        # if start가 유효하면
        if (start == 1):  # client
            ACK = 'ACK ETTTP/1.0\r\nHost:127.0.0.1\r\nFirst-Move:ME\r\n\r\n'
            print("당신이 먼저 시작합니다")
        elif (start == 0):  # server
            ACK = 'ACK ETTTP/1.0\r\nHost:127.0.0.1\r\nFirst-Move:YOU\r\n\r\n'
            print("상대가 먼저 시작합니다")
        else:
            client_socket.close()
        client_socket.send(ACK.encode())

        ###################################################################

        # Start game
        root = TTT(target_socket=client_socket, src_addr=MY_IP, dst_addr=SERVER_IP)
        root.play(start_user=start)
        root.mainloop()
        client_socket.close()
        
        