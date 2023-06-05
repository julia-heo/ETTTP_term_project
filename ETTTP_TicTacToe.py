<<<<<<< HEAD:ETTTP_TicTacToe.py
'''
  ETTTP_TicTacToe_skeleton.py

  34743-02 Information Communications
  Term Project on Implementation of Ewah Tic-Tac-Toe Protocol

  Skeleton Code Prepared by JeiHee Cho
  May 24, 2023

 '''

import random         # random 모듈을 가져옴(누가 start할지 랜덤으로 정하기 위해)
import tkinter as tk  # 게임에 사용할 GUI를 구현하기 위해 tkinter 모듈을 가져옴
from socket import *  # socket programming을 하기 위해 socket 모듈을 가져옴
import _thread        # thread를 사용하기 위해 thread 모듈 import

SIZE=1024             #socket의 주고 받는 메세지의 크기를 사전에 정함

class TTT(tk.Tk):     #TTT라는 클래스 정의 (tic-tac-toe 게임에 필요한 기능들을 구현한 class)
    #클래스의 객체가 만들어질 때 초기화 될 값이 필요하므로 그런 값들을 __init__함수 안에 구현
    def __init__(self, target_socket,src_addr,dst_addr, client=True):   #인자로 target_socket, src_addr, dst_addr, client
        super().__init__()          # 자식 클래스의 부모클래스를 불러옴
        
        self.my_turn = -1           # my_turn을 -1로 초기화

        self.geometry('500x800')    # 500 * 800으로 창 사이즈를 설정

        self.active = 'GAME ACTIVE' #
        self.socket = target_socket #
        
        self.send_ip = dst_addr     # destination IP
        self.recv_ip = src_addr     # source IP
        
        self.total_cells = 9        # 0번 ~ 8번 : cell 9개
        self.line_size = 3          # 3 * 3 line size는 3
        
        
        # Set variables for Client and Server UI
        ############## updated ###########################
        if client:          # client일 경우
            self.myID = 1   # 내 ID를 1로 설정
            self.title('34743-02-Tic-Tac-Toe Client')   #창의 title을 34743-02-Tic-Tac-Toe Client로 설정
            self.user = {'value': self.line_size+1, 'bg': 'blue',
                     'win': 'Result: You Won!', 'text':'O','Name':"ME"}
            self.computer = {'value': 1, 'bg': 'orange',
                             'win': 'Result: You Lost!', 'text':'X','Name':"YOU"}
        else:
            self.myID = 0   # 내 ID를 0으로 설정
            self.title('34743-02-Tic-Tac-Toe Server')   #창의 title을 34743-02-Tic-Tac-Toe Server로 설정
            self.user = {'value': 1, 'bg': 'orange',
                         'win': 'Result: You Won!', 'text':'X','Name':"ME"}
            self.computer = {'value': self.line_size+1, 'bg': 'blue',
                     'win': 'Result: You Lost!', 'text':'O','Name':"YOU"}
        ##################################################


        self.board_bg = 'white'     #보드의 배경색은 white
        #어떤 라인들이 선택될 경우 이기는지에 관한 정보를 적어놓음
        self.all_lines = ((0, 1, 2), (3, 4, 5), (6, 7, 8),  # 가로줄
                          (0, 3, 6), (1, 4, 7), (2, 5, 8),  # 세로줄
                          (0, 4, 8), (2, 4, 6))             # 대각선

        self.create_control_frame() #create_control_frame이라는 함수 호출

    def create_control_frame(self): # 종료 버튼을 생성하는 함수
        '''
        Make Quit button to quit game
        Click this button to exit game

        '''
        #vvvvvvvvvvvvvvvvvvv  DO NOT CHANGE  vvvvvvvvvvvvvvvvvvv
        self.control_frame = tk.Frame()         # tk모듈을 사용한 프레임 생성
        self.control_frame.pack(side=tk.TOP)    # 제어 프레임을 GUI 창의 위쪽에 배치

        self.b_quit = tk.Button(self.control_frame, text='Quit',    # 버튼에 Quit이라고 적혀있으며, quit이라는 동작을 수행함
                                command=self.quit)
        self.b_quit.pack(side=tk.RIGHT)         # 종료 버튼을 오른쪽에 정렬합니다.
        #^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    def create_status_frame(self):              # Hold 인지 Ready인지 보여주는 함수
        '''
        Status UI that shows "Hold" or "Ready"
        '''
        #vvvvvvvvvvvvvvvvvvv  DO NOT CHANGE  vvvvvvvvvvvvvvvvvvv
        self.status_frame = tk.Frame()      # tk모듈을 사용한 프레임 생성
        self.status_frame.pack(expand=True,anchor='w',padx=20)  #status frame을 창에 배치하며, 프레임이 창의 크기에 맞게 생성되고, 왼쪽 정렬
                                                                #그리고, 왼쪽과 오른쪽의 간격을 20 픽셀로 설정
        #프레임에서 O라는 텍스트를 표시하는 레이블을 생성 이 때, 폰트는 Helevetica, 25, bold이며, 왼쪽 정렬함
        self.l_status_bullet = tk.Label(self.status_frame,text='O',font=('Helevetica',25,'bold'),justify='left')
        # O를 status frame의 왼쪽에 정렬함
        self.l_status_bullet.pack(side=tk.LEFT,anchor='w')
        # 다른 레이블을 생성하며 위에서와 같은 폰트를 사용함
        self.l_status = tk.Label(self.status_frame,font=('Helevetica',25,'bold'),justify='left')
        # status를 프레임의 오른쪽에 배치함
        self.l_status.pack(side=tk.RIGHT,anchor='w')
        #^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

    def create_result_frame(self):          # 결과 표시하는 UI를 생성하는 함수
        '''
        UI that shows Result
        '''
        #vvvvvvvvvvvvvvvvvvv  DO NOT CHANGE  vvvvvvvvvvvvvvvvvvv
        self.result_frame = tk.Frame()      # tk모듈을 사용한 프레임 생성
        self.result_frame.pack(expand=True,anchor='w',padx=20)  #result frame을 창에 배치하며, 프레임이 창의 크기에 맞게 생성되고, 왼쪽 정렬
                                                                #그리고, 왼쪽과 오른쪽의 간격을 20 픽셀로 설정
        # 결과 텍스트를 표시하는 레이블 (글씨와 관련된 설정은 Helvetica, 25, bold이며, 왼쪽 정렬)
        self.l_result = tk.Label(self.result_frame,font=('Helevetica',25,'bold'),justify='left')
        # 결과를 프레임의 아래에 배치
        self.l_result.pack(side=tk.BOTTOM,anchor='w')
        #^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

    def create_debug_frame(self):           # 사용자로부터 debug 텍스트를 입력받는 프레임 생성
        '''
        Debug UI that gets input from the user
        '''
        #vvvvvvvvvvvvvvvvvvv  DO NOT CHANGE  vvvvvvvvvvvvvvvvvvv
        self.debug_frame = tk.Frame()       # tk모듈을 사용한 프레임 생성
        self.debug_frame.pack(expand=True)  # debug frame을 창에 맞게 생성되게 만듦

        self.t_debug = tk.Text(self.debug_frame,height=2,width=50)  # debug frame에서 text 입력받을 창으로 heigh는 2, width는 50으로 설정
        self.t_debug.pack(side=tk.LEFT)                             # debug frame 내 왼쪽에 배치
        self.b_debug = tk.Button(self.debug_frame,text="Send",command=self.send_debug) #Send라는 버튼을 생성
        self.b_debug.pack(side=tk.RIGHT)    #send 버튼을 오른쪽에 배치
        #^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^


    def create_board_frame(self):           # Tic-Tac-Toe의 UI를 생성하는 함수
        '''
        Tic-Tac-Toe Board UI
        '''
        #vvvvvvvvvvvvvvvvvvv  DO NOT CHANGE  vvvvvvvvvvvvvvvvvvv
        self.board_frame = tk.Frame()       # tk모듈을 사용한 프레임 생성
        self.board_frame.pack(expand=True)  # board frame을 창에 맞게 생성되게 만듦

        self.cell = [None] * self.total_cells   # board의 cell을 정의 (개수는 위에서 정의)
        self.setText=[None]*self.total_cells    # board의 text를 정의 (개수는 위에서 정의)
        self.board = [0] * self.total_cells     # board의 상태를 정의 (개수는 위에서 정의)
        self.remaining_moves = list(range(self.total_cells)) # board의 remaining moves를 정의 (개수는 위에서 정의)
        for i in range(self.total_cells):       # total_cells 만큼 반복문 진행
            self.setText[i] = tk.StringVar()    # 각 cell에 text를 저장 위한 StringVar 생성
            self.setText[i].set("  ")           # 초기 text로 공백 설정
            # board의 한 칸을 의미하며, highlightthickness, borderwidth, relief, width, height, background, compound, textvariable, 폰트등 정의 
            self.cell[i] = tk.Label(self.board_frame, highlightthickness=1,borderwidth=5,relief='solid',
                                    width=5, height=3,
                                    bg=self.board_bg,compound="center",
                                    textvariable=self.setText[i],font=('Helevetica',30,'bold'))
            # 각 cell 이 클릭되었을 때의 반응을 bind함 클릭되면, self.my_move 호출
            self.cell[i].bind('<Button-1>',
                              lambda e, move=i: self.my_move(e, move))
            r, c = divmod(i, self.line_size)    # row 와 column을 divmod를 통해 저장
            self.cell[i].grid(row=r, column=c,sticky="nsew") # row와 column 이용해 cell 위치 지정

        #^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^



    def play(self, start_user=1):       # Tic-Tac-Toe프로그램 시작. start_user매개변수로 선 플레이어 정보 받아온다. 0:server 1:client
        '''
        Call this function to initiate the game

        start_user: if its 0, start by "server" and if its 1, start by "client"
        '''
        #vvvvvvvvvvvvvvvvvvv  DO NOT CHANGE  vvvvvvvvvvvvvvvvvvv
        self.last_click = 0             # 아직 클릭 정보 없음. 0으로 초기화
        self.create_board_frame()       # Tic-Tac-Toe의 UI를 생성하는 함수
        self.create_status_frame()      # Hold 인지 Ready인지 보여주는 함수
        self.create_result_frame()      # 결과 표시하는 UI를 생성하는 함수
        self.create_debug_frame()       # 사용자로부터 debug 텍스트를 입력받는 프레임을 생성하는 함수
        self.state = self.active        # self.active는'GAME ACTIVE'이다. state가 active라고 기록
        if start_user == self.myID:     # start_user(선 플레이어)가 자신의 ID와 같다면
            self.my_turn = 1                            # my_turn 변수를 1로 설정해 자신의 차례임을 표시
            self.user['text'] = 'X'                     # 선공 플레이어는 X로 선택한 칸 표시
            self.computer['text'] = 'O'                 # 상대(후공) 플레이어는 O로 선택한 칸 표시
            self.l_status_bullet.config(fg='green')     # Ready앞의 원을 초록색으로 칠한다
            self.l_status['text'] = ['Ready']           # "Ready" 텍스트를 UI에 띄운다
        else:
            self.my_turn = 0            # start_user(선 플레이어)가 자신의 ID와 같다면. 즉, 후공이라면
            self.user['text'] = 'O'                     # 후공 플레이어는 O로 선택한 칸 표시
            self.computer['text'] = 'X'                 # 상대(선공) 플레이어는 X로 선택한 칸 표시
            self.l_status_bullet.config(fg='red')       # Hold앞의 원을 빨강색으로 칠한다
            self.l_status['text'] = ['Hold']            # "Hold" 텍스트를 UI에 띄운다
            _thread.start_new_thread(self.get_move,())  # 상대의 움직임을 받을 준비. 프로그램 멈추는 것을 방지한다.
        #^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

    def quit(self):                                     # GUI를 닫는 함수
        '''
        Call this function to close GUI
        '''
        #vvvvvvvvvvvvvvvvvvv  DO NOT CHANGE  vvvvvvvvvvvvvvvvvvv
        self.destroy()                                  # Tkinter 창을 닫는 클래스 메소드
        #^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

    def my_move(self, e, user_move):                        # UI에서 클릭한 영역을 인식해
        '''
        Read button when the player clicks the button

        e: event
        user_move: button number, from 0 to 8
        '''
        #vvvvvvvvvvvvvvvvvvv  DO NOT CHANGE  vvvvvvvvvvvvvvvvvvv

        # When it is not my turn or the selected location is already taken, do nothing
        if self.board[user_move] != 0 or not self.my_turn:  # 이미 선택되어 누를수 없는 부분이거나 my_turn이 아닌 경우(my_turn==0)
            return                                          # 아무 동작 없이 return
        # Send move to peer
        valid = self.send_move(user_move)                   # 입력받은 좌표(user_move)를 send_move함수로 보낸다.
                                                            # send_move함수를 통해 상대에게 몇번 board를 눌렀는지 메시지를 보내고, ACK가 오는 것을 확인한다. 완료되면 True를 반환한다.
                                                            # 상대에게 알렸으니, 자신의 board에 반영할 차례이다.
        # If ACK is not returned from the peer or it is not valid, exit game
        if not valid:                                       # valid가 False라면 상대방에게 자신의 이동 정보를 제대로 전달하지 못한것이므로
            self.quit()                                     # 프로그램 종료

        # Update Tic-Tac-Toe board based on user's selection
        self.update_board(self.user, user_move)             # 자신의 보드를 업데이트

        # If the game is not over, change turn  
        if self.state == self.active:                       # active상태라면
            self.my_turn = 0                                # my_turn을 0으로 설정해 자신의 차례가 아님을 표시한다
            self.l_status_bullet.config(fg='red')           # Hold앞의 원을 빨강색으로 칠한다
            self.l_status ['text'] = ['Hold']               # "Hold" 텍스트를 UI에 띄운다
            _thread.start_new_thread(self.get_move,())      # 상대의 움직임을 받을 준비. 프로그램이 멈추는 것을 방지한다.
        #^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

    def get_move(self):                                        # 상대의 move 메세지를 받아 자신의 보드에 상대의 움직임을 반영하고, ACK를 전송하는 함수
        '''
        Function to get move from other peer
        Get message using socket, and check if it is valid
        If is valid, send ACK message
        If is not, close socket and quit
        '''
        ###################  Fill Out  #######################
        # get message using socket
        msg = self.socket.recv(SIZE).decode()                  # 상대가 자신의 move 좌표를 담아 보낸 메시지를 받아 decode한다
        msg_valid_check = check_msg(msg, self.recv_ip)         # 메시지가 유효한지(형식이 맞는지, 나에게 온 메시지가 맞는지) 검사

        if msg_valid_check:  # Message is not valid            # 메시지가 유효하지 않다면
            self.socket.close()                                # 소켓을 닫는다
            self.quit()                                        # UI를 종료한다
            return                                             # return. 더이상 함수 수행하지 않는다
        else:  # If message is valid - send ack, update board and change turn                                               # 메시지가 유효하다면
            msgR = msg.replace("\r\n", " ").replace(":", " ").replace("(", " ").replace(")", " ").replace(",", " ")         # 줄바꿈과 ":", "(", ")", ","를 띄어쓰기로 대체
            msgSplit = msgR.split(" ")                                                                                      # 띄어쓰기를 기준으로 문자열 분리

            # msgSplit[6]에 이동한 행, msgSplit[7]에 이동한 열 정보가 담겨있다.
            moveACK = "ACK ETTTP/1.0\r\nHost:"+self.send_ip+"\r\nNew-Move:(" + msgSplit[6] + "," + msgSplit[7] + ")\r\n\r\n" # 받은 정보를 담아 잘 받았음을 알리는 ACK 메세지를 만든다.
            self.socket.send(moveACK.encode())                  # ACK 메시지를 전송한다

            row = int(msgSplit[6])                              # 상대가 클릭한 행 (문자열로 저장되어있어 정수형으로 변환)
            col = int(msgSplit[7])                              # 상대가 클릭한 열 (문자열로 저장되어있어 정수형으로 변환)
            loc = 3 * row + col                                 # 누른 칸의 번호 next-move

            ######################################################

            # vvvvvvvvvvvvvvvvvvv  DO NOT CHANGE  vvvvvvvvvvvvvvvvvvv
            self.update_board(self.computer, loc, get=True)     # 받은 move를 이용해 board 업데이트
            if self.state == self.active:                       # active한 상태라면
                self.my_turn = 1                                # my_turn을 1로 변경해 자신의 차례임을 표시
                self.l_status_bullet.config(fg='green')         # Ready앞의 원을 초록색으로 칠한다
                self.l_status['text'] = ['Ready']               # "Ready" 텍스트를 띄운다
            # ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

    def send_debug(self):   # textbox에 입력된 debug 메세지를 통해서 결과가 도출되는 함수
        '''
        Function to send message to peer using input from the textbox
        Need to check if this turn is my turn or not
        '''
        if not self.my_turn:                    # 내 차례가 맞는지 확인하는 함수          
            self.t_debug.delete(1.0, "end")     # text box 내용을 삭제
            return                              # return
        # get message from the input box
        d_msg = self.t_debug.get(1.0, "end")    # text box의 메세지를 d_msg에 저장
        d_msg = d_msg.replace("\\r\\n", "\r\n") # msg is sanitized as \r\n is modified when it is given as input
        self.t_debug.delete(1.0, "end")         # text box 내용을 삭제

        ###################  Fill Out  #######################
        '''
        Check if the selected location is already taken or not
        '''
        # MSG="SEND ETTTP/1.0\r\nHost:127.0.0.1\r\nNew-Move:("+rowStr+", "+colStr+")\r\n\r\n"
        # d_msg처리 그리고 index 5에 (1, 2)이렇게 들어가 있음
        if check_msg(d_msg, self.recv_ip):  # Message is not valid
            self.socket.close()             # socket을 종료
            self.quit()                     # quit 해줌
            return                          # return 해줌

        d_msgR = d_msg.replace("\r\n", " ") # \r\n을 제거헤주고 공백으로 바꿔준다.
        d_msgR = d_msgR.replace(":", " ")   # :을 공백으로 바꿔준다.
        d_msgSplit = d_msgR.split(" ")      # 공백을 기준으로 split
        loc_chk = d_msgSplit[5]             # (1,2)이런 좌표를 loc_chk에 
                             
        loc_chk = loc_chk.replace("(", "").replace(")", "") # 괄호 제거 (eg. (1,2)이런 식인데 여기서 두 괄호를 제거하면 1,2가 됨)
        loc_chk = loc_chk.replace(",", " ")                 # 쉼표 제거 (eg. 1,2 --> [1, 2])
        loc_arr = loc_chk.split(" ")                        # 공백을 기준으로 잘라줌 (row와 col의 구별을 위해)
        
        d_row = int(loc_arr[0])                             # d_row가 [1,2]에서 앞의 숫자이므로 index 0을 가져오고 int로 바꿔줌
        d_col = int(loc_arr[1])                             # d_col가 [1,2]에서 앞의 숫자이므로 index 0을 가져오고 int로 바꿔줌
        loc = d_row * 3 + d_col                             # location 은 해당하는 row에 3을 곱하고 col을 더해줌 (eg. 8번일 경우 (2,2)--> 3 * 2 + 2)

    

        if not (0 <= d_row <= 2 and 0 <= d_col <= 2):       # 만약, 추출한 row와 col의 범위가 이상한 경우 해결하는 함수
            #print("클릭할 수 없는 부분입니다!")                   
            return                                          # 리턴해줌

        if (self.board[loc]):           #만약, 이미 loc이 선택되었을 경우 처리해주는 함수
            #print("이미 선택된 좌석입니다")
            return                      #리턴 해준다.

        # d_msg에 디버깅 메시지 저장되어있음 여기서
        # 디버깅은 들어오는 메세지가 틀린지 맞는지 확인 안해도 괜찮음
        '''
        Send message to peer
        '''
        self.socket.send(d_msg.encode())    # send msg
        '''
        Get ack
        '''
        d_msg_ack = self.socket.recv(SIZE).decode() # ack를 d_msg_ack에 저장

        # peer's move, from 0 to 8

        ######################################################

        #vvvvvvvvvvvvvvvvvvv  DO NOT CHANGE  vvvvvvvvvvvvvvvvvvv
        self.update_board(self.user, loc)           #board의 상태를 update함

        if self.state == self.active:               # always after my move
            self.my_turn = 0                        #  my_turn으로 0으로 바꿈
            self.l_status_bullet.config(fg='red')   # foreground 색을 red
            self.l_status ['text'] = ['Hold']       # status의 text를 Hold로
            _thread.start_new_thread(self.get_move,())  # 새로운 스레드에서 get_move 실행

        #^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
        
    def send_move(self,selection):      # move를 보내주는 함수
        '''
        Function to send message to peer using button click
        selection indicates the selected button
        '''
        row,col = divmod(selection,3)   # divmod를 통해 row와 col 추출
        ###################  Fill Out  #######################
        rowStr = str(row)               # 메세지를 보내기 위해 str형으로 바꿔줌
        colStr = str(col)               # 메세지를 보내기 위해 str형으로 바꿔줌
        
        # send message and check ACK

        # 주어진 msg 형식에 맞게 msg를 만들어줌
        msg = "SEND ETTTP/1.0\r\nHost:"+self.send_ip+"\r\nNew-Move:(" + rowStr + "," + colStr + ")\r\n\r\n "
        self.socket.send(msg.encode())  # socket을 이용하여 msg를 보냄

        # ACK
        rcvAck = self.socket.recv(SIZE).decode() # ACK 를 받고 rcvAck에 저장함
        # print("move 후 ACK: " + rcvAck)

        if check_msg(rcvAck, self.recv_ip):     # Message is not valid
            self.socket.close()                 # socket을 닫아줌
            self.quit()                         # quit 해줌

        return True                             # Message가 valid 하므로 True를 리턴해줌
        ######################################################

    def check_result(self, winner, get=False):  # peer와 result가 같은지 확인해주는 함수
        '''
        Function to check if the result between peers are same
        get: if it is false, it means this user is winner and need to report the result first
        '''
        # no skeleton
        ###################  Fill Out  #######################
        # msg를 형식에 맞게 만들어줌
        msg = "RESULT ETTTP/1.0\r\nHost:"+self.send_ip+"\r\nWinner:"+winner+"\r\n\r\n" # winner변수 넣어줌 
        
        self.socket.send(msg.encode())  # socket을 통해 message를 전송해줌

        result=self.socket.recv(SIZE).decode()  # 상대가 보내준 message 를 result에 저장

        msgWinner = result.replace("\r\n", " ").replace(":", " ").split(" ")    #winner를 확인하기 위해 \r\n, :을 공백으로 바꾸고 공백으로 나눠줌
        msg_Winner=msgWinner[5]         # index 5에 해당하는부분에 winner가 있음
        #print(msg_Winner+"는 졌어")
        if (msg_Winner==winner):        # 만약 두 결과가 같으면 (달라야 한 명은 이기고 한 명은 진게 돼서)
            return False                # False를 리턴해줌

        return True                     # 두 결과가 다르면 한 명은 winner 한 명은 loser 이므로 True를 리턴
        ######################################################

    # vvvvvvvvvvvvvvvvvvv  DO NOT CHANGE  vvvvvvvvvvvvvvvvvvv
    def update_board(self, player, move, get=False):    # board를 update를 해주는 함수
        '''
        This function updates Board if is clicked

        '''
        self.board[move] = player['value']                  # player가 선택한 cell의 index에 player의 vlaue를 넣어줌
        self.remaining_moves.remove(move)                   # 선택된 cell의 index를 remaining_moves 리스트에서 제거
        self.cell[self.last_click]['bg'] = self.board_bg    # 마지막으로 클릭한 셀의 배경을 기본 배경으로 변경
        self.last_click = move                              # 마지막으로 클릭한 cell index 를 업데이트
        self.setText[move].set(player['text'])              # 해당 cell의 플레이어의 text 설정
        self.cell[move]['bg'] = player['bg']                # cell의 background를 해당 플레이어의 background color로 설정        
        self.update_status(player, get=get)                 # update_status를 불러 update 완료

    def update_status(self, player, get=False):             # board의 status를 update 해주는 함수
        '''
        This function checks status - define if the game is over or not
        '''
        winner_sum = self.line_size * player['value']       # player가 이기기 위한 cell의 sum을 계산
        for line in self.all_lines:                         # 모든 line에 대해 확인
            if sum(self.board[i] for i in line) == winner_sum:      # 만약, 조건을 만족 시 
                self.l_status_bullet.config(fg='red')               # foreground를 red로 바꿔줌
                self.l_status['text'] = ['Hold']                    # text 도 Hold로 바꿔줌
                self.highlight_winning_line(player, line)           # winning line을 강조
                correct = self.check_result(player['Name'], get=get)    # 결과가 맞는지 check_result를 부름
                if correct:                                 # 만약 결과가 맞으면 (결과가 정상적)
                    self.state = player['win']              # state에 게임의 결과에 맞는 text 설정
                    self.l_result['text'] = player['win']   # l_result에 게임의 결과에 맞는 text 설정
                else:                                       # 결과가 유효하지 않으면
                    self.l_result['text'] = "Somethings wrong…" # l_result에 잘못됨 표기

    def highlight_winning_line(self, player, line):         # winning line을 하이라이트 해줌
        '''
        This function highlights the winning line
        '''
        for i in line:                                      # 해당 라인에 속한 것을 전부 바꿔야하기에 해당 개수 만큼 반복문
            self.cell[i]['bg'] = 'red'                      # 배경을 red로 바꿈

    # ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

# End of Root class

def check_msg(msg, recv_ip):                                    # 전송받은 메세지의 유효성을 확인하는 함수
    '''
    Function that checks if received message is ETTTP format
    '''
    ###################  Fill Out  #######################
    msgR = msg.replace("\r\n", " ").replace(":", " ")           # 줄바꿈과 ":"를 띄어쓰기로 대체한다
    msgSplit = msgR.split(" ")                                  # 띄어쓰기를 기준으로 문자열을 분리한다

    if not (msgSplit[1] == "ETTTP/1.0"):                        # 2번째 문자열에 프로토콜 정보가 담겨있다. ETTTP/1.0이 맞는지 확인
        print("잘못된 프로토콜")                                    # 에러 메시지 출력
        return True                                             
    
    if not (msgSplit[3] == str(recv_ip)):                       # 4번째 문자열에 메시지를 보낼 IP주소가 담겨있다. 즉, 메시지를 받은 입장에선 자신의 IP주소가 담겨있어야 한다.
        print("잘못된 ip주소!")                                    # 잘못된 ip 주소인 경우 에러 메시지 출력
        return True

    return False                                                # 유효한 경우 False 반환
=======
'''
  ETTTP_TicTacToe_skeleton.py

  34743-02 Information Communications
  Term Project on Implementation of Ewah Tic-Tac-Toe Protocol

  Skeleton Code Prepared by JeiHee Cho
  May 24, 2023

 '''

import random         # random 모듈을 가져옴(누가 start할지 랜덤으로 정하기 위해)
import tkinter as tk  # 게임에 사용할 GUI를 구현하기 위해 tkinter 모듈을 가져옴
from socket import *  # socket programming을 하기 위해 socket 모듈을 가져옴
import _thread        # thread를 사용하기 위해 thread 모듈 import

SIZE=1024             #socket의 주고 받는 메세지의 크기를 사전에 정함

class TTT(tk.Tk):     #TTT라는 클래스 정의 (tic-tac-toe 게임에 필요한 기능들을 구현한 class)
    #클래스의 객체가 만들어질 때 초기화 될 값이 필요하므로 그런 값들을 __init__함수 안에 구현
    def __init__(self, target_socket,src_addr,dst_addr, client=True):   #인자로 target_socket, src_addr, dst_addr, client
        super().__init__()          # 자식 클래스의 부모클래스를 불러옴
        
        self.my_turn = -1           # my_turn을 -1로 초기화

        self.geometry('500x800')    # 500 * 800으로 창 사이즈를 설정

        self.active = 'GAME ACTIVE' #
        self.socket = target_socket #
        
        self.send_ip = dst_addr     # destination IP
        self.recv_ip = src_addr     # source IP
        
        self.total_cells = 9        # 0번 ~ 8번 : cell 9개
        self.line_size = 3          # 3 * 3 line size는 3
        
        
        # Set variables for Client and Server UI
        ############## updated ###########################
        if client:          # client일 경우
            self.myID = 1   # 내 ID를 1로 설정
            self.title('34743-02-Tic-Tac-Toe Client')   #창의 title을 34743-02-Tic-Tac-Toe Client로 설정
            self.user = {'value': self.line_size+1, 'bg': 'blue',
                     'win': 'Result: You Won!', 'text':'O','Name':"ME"}
            self.computer = {'value': 1, 'bg': 'orange',
                             'win': 'Result: You Lost!', 'text':'X','Name':"YOU"}
        else:
            self.myID = 0   # 내 ID를 0으로 설정
            self.title('34743-02-Tic-Tac-Toe Server')   #창의 title을 34743-02-Tic-Tac-Toe Server로 설정
            self.user = {'value': 1, 'bg': 'orange',
                         'win': 'Result: You Won!', 'text':'X','Name':"ME"}
            self.computer = {'value': self.line_size+1, 'bg': 'blue',
                     'win': 'Result: You Lost!', 'text':'O','Name':"YOU"}
        ##################################################


        self.board_bg = 'white'     #보드의 배경색은 white
        #어떤 라인들이 선택될 경우 이기는지에 관한 정보를 적어놓음
        self.all_lines = ((0, 1, 2), (3, 4, 5), (6, 7, 8),  # 가로줄
                          (0, 3, 6), (1, 4, 7), (2, 5, 8),  # 세로줄
                          (0, 4, 8), (2, 4, 6))             # 대각선

        self.create_control_frame() #create_control_frame이라는 함수 호출

    def create_control_frame(self): # 종료 버튼을 생성하는 함수
        '''
        Make Quit button to quit game
        Click this button to exit game

        '''
        #vvvvvvvvvvvvvvvvvvv  DO NOT CHANGE  vvvvvvvvvvvvvvvvvvv
        self.control_frame = tk.Frame()         # tk모듈을 사용한 프레임 생성
        self.control_frame.pack(side=tk.TOP)    # 제어 프레임을 GUI 창의 위쪽에 배치

        self.b_quit = tk.Button(self.control_frame, text='Quit',    # 버튼에 Quit이라고 적혀있으며, quit이라는 동작을 수행함
                                command=self.quit)
        self.b_quit.pack(side=tk.RIGHT)         # 종료 버튼을 오른쪽에 정렬합니다.
        #^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    def create_status_frame(self):              # Hold 인지 Ready인지 보여주는 함수
        '''
        Status UI that shows "Hold" or "Ready"
        '''
        #vvvvvvvvvvvvvvvvvvv  DO NOT CHANGE  vvvvvvvvvvvvvvvvvvv
        self.status_frame = tk.Frame()      # tk모듈을 사용한 프레임 생성
        self.status_frame.pack(expand=True,anchor='w',padx=20)  #status frame을 창에 배치하며, 프레임이 창의 크기에 맞게 생성되고, 왼쪽 정렬
                                                                #그리고, 왼쪽과 오른쪽의 간격을 20 픽셀로 설정
        #프레임에서 O라는 텍스트를 표시하는 레이블을 생성 이 때, 폰트는 Helevetica, 25, bold이며, 왼쪽 정렬함
        self.l_status_bullet = tk.Label(self.status_frame,text='O',font=('Helevetica',25,'bold'),justify='left')
        # O를 status frame의 왼쪽에 정렬함
        self.l_status_bullet.pack(side=tk.LEFT,anchor='w')
        # 다른 레이블을 생성하며 위에서와 같은 폰트를 사용함
        self.l_status = tk.Label(self.status_frame,font=('Helevetica',25,'bold'),justify='left')
        # status를 프레임의 오른쪽에 배치함
        self.l_status.pack(side=tk.RIGHT,anchor='w')
        #^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

    def create_result_frame(self):          # 결과 표시하는 UI를 생성하는 함수
        '''
        UI that shows Result
        '''
        #vvvvvvvvvvvvvvvvvvv  DO NOT CHANGE  vvvvvvvvvvvvvvvvvvv
        self.result_frame = tk.Frame()      # tk모듈을 사용한 프레임 생성
        self.result_frame.pack(expand=True,anchor='w',padx=20)  #result frame을 창에 배치하며, 프레임이 창의 크기에 맞게 생성되고, 왼쪽 정렬
                                                                #그리고, 왼쪽과 오른쪽의 간격을 20 픽셀로 설정
        # 결과 텍스트를 표시하는 레이블 (글씨와 관련된 설정은 Helvetica, 25, bold이며, 왼쪽 정렬)
        self.l_result = tk.Label(self.result_frame,font=('Helevetica',25,'bold'),justify='left')
        # 결과를 프레임의 아래에 배치
        self.l_result.pack(side=tk.BOTTOM,anchor='w')
        #^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

    def create_debug_frame(self):           # 사용자로부터 debug 텍스트를 입력받는 프레임 생성
        '''
        Debug UI that gets input from the user
        '''
        #vvvvvvvvvvvvvvvvvvv  DO NOT CHANGE  vvvvvvvvvvvvvvvvvvv
        self.debug_frame = tk.Frame()       # tk모듈을 사용한 프레임 생성
        self.debug_frame.pack(expand=True)  # debug frame을 창에 맞게 생성되게 만듦

        self.t_debug = tk.Text(self.debug_frame,height=2,width=50)  # debug frame에서 text 입력받을 창으로 heigh는 2, width는 50으로 설정
        self.t_debug.pack(side=tk.LEFT)                             # debug frame 내 왼쪽에 배치
        self.b_debug = tk.Button(self.debug_frame,text="Send",command=self.send_debug) #Send라는 버튼을 생성
        self.b_debug.pack(side=tk.RIGHT)    #send 버튼을 오른쪽에 배치
        #^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^


    def create_board_frame(self):           # Tic-Tac-Toe의 UI를 생성하는 함수
        '''
        Tic-Tac-Toe Board UI
        '''
        #vvvvvvvvvvvvvvvvvvv  DO NOT CHANGE  vvvvvvvvvvvvvvvvvvv
        self.board_frame = tk.Frame()       # tk모듈을 사용한 프레임 생성
        self.board_frame.pack(expand=True)  # board frame을 창에 맞게 생성되게 만듦

        self.cell = [None] * self.total_cells   # board의 cell을 정의 (개수는 위에서 정의)
        self.setText=[None]*self.total_cells    # board의 text를 정의 (개수는 위에서 정의)
        self.board = [0] * self.total_cells     # board의 상태를 정의 (개수는 위에서 정의)
        self.remaining_moves = list(range(self.total_cells)) # board의 remaining moves를 정의 (개수는 위에서 정의)
        for i in range(self.total_cells):       # total_cells 만큼 반복문 진행
            self.setText[i] = tk.StringVar()    # 각 cell에 text를 저장 위한 StringVar 생성
            self.setText[i].set("  ")           # 초기 text로 공백 설정
            # board의 한 칸을 의미하며, highlightthickness, borderwidth, relief, width, height, background, compound, textvariable, 폰트등 정의 
            self.cell[i] = tk.Label(self.board_frame, highlightthickness=1,borderwidth=5,relief='solid',
                                    width=5, height=3,
                                    bg=self.board_bg,compound="center",
                                    textvariable=self.setText[i],font=('Helevetica',30,'bold'))
            # 각 cell 이 클릭되었을 때의 반응을 bind함 클릭되면, self.my_move 호출
            self.cell[i].bind('<Button-1>',
                              lambda e, move=i: self.my_move(e, move))
            r, c = divmod(i, self.line_size)    # row 와 column을 divmod를 통해 저장
            self.cell[i].grid(row=r, column=c,sticky="nsew") # row와 column 이용해 cell 위치 지정

        #^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^



    def play(self, start_user=1):       # Tic-Tac-Toe프로그램 시작. start_user매개변수로 선 플레이어 정보 받아온다. 0:server 1:client
        '''
        Call this function to initiate the game

        start_user: if its 0, start by "server" and if its 1, start by "client"
        '''
        #vvvvvvvvvvvvvvvvvvv  DO NOT CHANGE  vvvvvvvvvvvvvvvvvvv
        self.last_click = 0             # 아직 클릭 정보 없음. 0으로 초기화
        self.create_board_frame()       # Tic-Tac-Toe의 UI를 생성하는 함수
        self.create_status_frame()      # Hold 인지 Ready인지 보여주는 함수
        self.create_result_frame()      # 결과 표시하는 UI를 생성하는 함수
        self.create_debug_frame()       # 사용자로부터 debug 텍스트를 입력받는 프레임을 생성하는 함수
        self.state = self.active        # self.active는'GAME ACTIVE'이다. state가 active라고 기록
        if start_user == self.myID:     # start_user(선 플레이어)가 자신의 ID와 같다면
            self.my_turn = 1                            # my_turn 변수를 1로 설정해 자신의 차례임을 표시
            self.user['text'] = 'X'                     # 선공 플레이어는 X로 선택한 칸 표시
            self.computer['text'] = 'O'                 # 상대(후공) 플레이어는 O로 선택한 칸 표시
            self.l_status_bullet.config(fg='green')     # Ready앞의 원을 초록색으로 칠한다
            self.l_status['text'] = ['Ready']           # "Ready" 텍스트를 UI에 띄운다
        else:
            self.my_turn = 0            # start_user(선 플레이어)가 자신의 ID와 같다면. 즉, 후공이라면
            self.user['text'] = 'O'                     # 후공 플레이어는 O로 선택한 칸 표시
            self.computer['text'] = 'X'                 # 상대(선공) 플레이어는 X로 선택한 칸 표시
            self.l_status_bullet.config(fg='red')       # Hold앞의 원을 빨강색으로 칠한다
            self.l_status['text'] = ['Hold']            # "Hold" 텍스트를 UI에 띄운다
            _thread.start_new_thread(self.get_move,())  # 상대의 움직임을 받을 준비. 프로그램 멈추는 것을 방지한다.
        #^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

    def quit(self):                                     # GUI를 닫는 함수
        '''
        Call this function to close GUI
        '''
        #vvvvvvvvvvvvvvvvvvv  DO NOT CHANGE  vvvvvvvvvvvvvvvvvvv
        self.destroy()                                  # Tkinter 창을 닫는 클래스 메소드
        #^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

    def my_move(self, e, user_move):                        # UI에서 클릭한 영역을 인식해 send_move를 호출하고, 자신의 보드를 업데이트하는 함수
        '''
        Read button when the player clicks the button

        e: event
        user_move: button number, from 0 to 8
        '''
        #vvvvvvvvvvvvvvvvvvv  DO NOT CHANGE  vvvvvvvvvvvvvvvvvvv

        # When it is not my turn or the selected location is already taken, do nothing
        if self.board[user_move] != 0 or not self.my_turn:  # 이미 선택되어 누를수 없는 부분이거나 my_turn이 아닌 경우(my_turn==0)
            return                                          # 아무 동작 없이 return
        # Send move to peer
        valid = self.send_move(user_move)                   # 입력받은 좌표(user_move)를 send_move함수로 보낸다.
                                                            # send_move함수를 통해 상대에게 몇번 board를 눌렀는지 메시지를 보내고, ACK가 오는 것을 확인한다. 완료되면 True를 반환한다.
                                                            # 상대에게 알렸으니, 자신의 board에 반영할 차례이다.
        # If ACK is not returned from the peer or it is not valid, exit game
        if not valid:                                       # valid가 False라면 상대방에게 자신의 이동 정보를 제대로 전달하지 못한것이므로
            self.quit()                                     # 프로그램 종료

        # Update Tic-Tac-Toe board based on user's selection
        self.update_board(self.user, user_move)             # 자신의 보드를 업데이트

        # If the game is not over, change turn  
        if self.state == self.active:                       # active상태라면
            self.my_turn = 0                                # my_turn을 0으로 설정해 자신의 차례가 아님을 표시한다
            self.l_status_bullet.config(fg='red')           # Hold앞의 원을 빨강색으로 칠한다
            self.l_status ['text'] = ['Hold']               # "Hold" 텍스트를 UI에 띄운다
            _thread.start_new_thread(self.get_move,())      # 상대의 움직임을 받을 준비. 프로그램이 멈추는 것을 방지한다.
        #^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

    def get_move(self):                                        # 상대의 move 메세지를 받아 자신의 보드에 상대의 움직임을 반영하고, ACK를 전송하는 함수
        '''
        Function to get move from other peer
        Get message using socket, and check if it is valid
        If is valid, send ACK message
        If is not, close socket and quit
        '''
        ###################  Fill Out  #######################
        # get message using socket
        msg = self.socket.recv(SIZE).decode()                  # 상대가 자신의 move 좌표를 담아 보낸 메시지를 받아 decode한다
        msg_valid_check = check_msg(msg, self.recv_ip)         # 메시지가 유효한지(형식이 맞는지, 나에게 온 메시지가 맞는지) 검사
        
        if msg_valid_check:  # Message is not valid            # 메시지가 유효하지 않다면
            self.socket.close()                                # 소켓을 닫는다
            self.quit()                                        # UI를 종료한다
            return                                             # return. 더이상 함수 수행하지 않는다
        else:  # If message is valid - send ack, update board and change turn                                               # 메시지가 유효하다면
            msgR = msg.replace("\r\n", " ").replace(":", " ").replace("(", " ").replace(")", " ").replace(",", " ")         # 줄바꿈과 ":", "(", ")", ","를 띄어쓰기로 대체
            msgSplit = msgR.split(" ")                                                                                      # 띄어쓰기를 기준으로 문자열 분리

            # msgSplit[6]에 이동한 행, msgSplit[7]에 이동한 열 정보가 담겨있다.
            moveACK = "ACK ETTTP/1.0\r\nHost:"+self.send_ip+"\r\nNew-Move:(" + msgSplit[6] + "," + msgSplit[7] + ")\r\n\r\n" # 받은 정보를 담아 잘 받았음을 알리는 ACK 메세지를 만든다.
            self.socket.send(moveACK.encode())                  # ACK 메시지를 전송한다

            row = int(msgSplit[6])                              # 상대가 클릭한 행 (문자열로 저장되어있어 정수형으로 변환)
            col = int(msgSplit[7])                              # 상대가 클릭한 열 (문자열로 저장되어있어 정수형으로 변환)
            loc = 3 * row + col                                 # 누른 칸의 번호 next-move

            ######################################################

            # vvvvvvvvvvvvvvvvvvv  DO NOT CHANGE  vvvvvvvvvvvvvvvvvvv
            self.update_board(self.computer, loc, get=True)     # 받은 move를 이용해 board 업데이트
            if self.state == self.active:                       # active한 상태라면
                self.my_turn = 1                                # my_turn을 1로 변경해 자신의 차례임을 표시
                self.l_status_bullet.config(fg='green')         # Ready앞의 원을 초록색으로 칠한다
                self.l_status['text'] = ['Ready']               # "Ready" 텍스트를 띄운다
            # ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

    def send_debug(self):   # textbox에 입력된 debug 메세지를 통해서 결과가 도출되는 함수
        '''
        Function to send message to peer using input from the textbox
        Need to check if this turn is my turn or not
        '''
        if not self.my_turn:                    # 내 차례가 맞는지 확인하는 함수          
            self.t_debug.delete(1.0, "end")     # text box 내용을 삭제
            return                              # return
        # get message from the input box
        d_msg = self.t_debug.get(1.0, "end")    # text box의 메세지를 d_msg에 저장
        d_msg = d_msg.replace("\\r\\n", "\r\n") # msg is sanitized as \r\n is modified when it is given as input
        self.t_debug.delete(1.0, "end")         # text box 내용을 삭제

        ###################  Fill Out  #######################
        '''
        Check if the selected location is already taken or not
        '''
        # MSG="SEND ETTTP/1.0\r\nHost:127.0.0.1\r\nNew-Move:("+rowStr+", "+colStr+")\r\n\r\n"
        # d_msg처리 그리고 index 5에 (1, 2)이렇게 들어가 있음
        if check_msg(d_msg, self.recv_ip):  # Message is not valid
            self.socket.close()             # socket을 종료
            self.quit()                     # quit 해줌
            return                          # return 해줌

        d_msgR = d_msg.replace("\r\n", " ") # \r\n을 제거헤주고 공백으로 바꿔준다.
        d_msgR = d_msgR.replace(":", " ")   # :을 공백으로 바꿔준다.
        d_msgSplit = d_msgR.split(" ")      # 공백을 기준으로 split
        loc_chk = d_msgSplit[5]             # (1,2)이런 좌표를 loc_chk에 
                             
        loc_chk = loc_chk.replace("(", "").replace(")", "") # 괄호 제거 (eg. (1,2)이런 식인데 여기서 두 괄호를 제거하면 1,2가 됨)
        loc_chk = loc_chk.replace(",", " ")                 # 쉼표 제거 (eg. 1,2 --> [1, 2])
        loc_arr = loc_chk.split(" ")                        # 공백을 기준으로 잘라줌 (row와 col의 구별을 위해)
        
        d_row = int(loc_arr[0])                             # d_row가 [1,2]에서 앞의 숫자이므로 index 0을 가져오고 int로 바꿔줌
        d_col = int(loc_arr[1])                             # d_col가 [1,2]에서 앞의 숫자이므로 index 0을 가져오고 int로 바꿔줌
        loc = d_row * 3 + d_col                             # location 은 해당하는 row에 3을 곱하고 col을 더해줌 (eg. 8번일 경우 (2,2)--> 3 * 2 + 2)

    

        if not (0 <= d_row <= 2 and 0 <= d_col <= 2):       # 만약, 추출한 row와 col의 범위가 이상한 경우 해결하는 함수
            #print("클릭할 수 없는 부분입니다!")                   
            return                                          # 리턴해줌

        if (self.board[loc]):           #만약, 이미 loc이 선택되었을 경우 처리해주는 함수
            #print("이미 선택된 좌석입니다")
            return                      #리턴 해준다.

        # d_msg에 디버깅 메시지 저장되어있음 여기서
        # 디버깅은 들어오는 메세지가 틀린지 맞는지 확인 안해도 괜찮음
        '''
        Send message to peer
        '''
        self.socket.send(d_msg.encode())    # send msg
        '''
        Get ack
        '''
        d_msg_ack = self.socket.recv(SIZE).decode() # ack를 d_msg_ack에 저장

        # peer's move, from 0 to 8

        ######################################################

        #vvvvvvvvvvvvvvvvvvv  DO NOT CHANGE  vvvvvvvvvvvvvvvvvvv
        self.update_board(self.user, loc)           #board의 상태를 update함

        if self.state == self.active:               # always after my move
            self.my_turn = 0                        #  my_turn으로 0으로 바꿈
            self.l_status_bullet.config(fg='red')   # foreground 색을 red
            self.l_status ['text'] = ['Hold']       # status의 text를 Hold로
            _thread.start_new_thread(self.get_move,())  # 새로운 스레드에서 get_move 실행

        #^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
        
    def send_move(self,selection):      # move를 보내주는 함수
        '''
        Function to send message to peer using button click
        selection indicates the selected button
        '''
        row,col = divmod(selection,3)   # divmod를 통해 row와 col 추출
        ###################  Fill Out  #######################
        rowStr = str(row)               # 메세지를 보내기 위해 str형으로 바꿔줌
        colStr = str(col)               # 메세지를 보내기 위해 str형으로 바꿔줌
        
        # send message and check ACK

        # 주어진 msg 형식에 맞게 msg를 만들어줌
        msg = "SEND ETTTP/1.0\r\nHost:"+self.send_ip+"\r\nNew-Move:(" + rowStr + "," + colStr + ")\r\n\r\n "
        self.socket.send(msg.encode())  # socket을 이용하여 msg를 보냄

        # ACK
        rcvAck = self.socket.recv(SIZE).decode() # ACK 를 받고 rcvAck에 저장함
        # print("move 후 ACK: " + rcvAck)

        if check_msg(rcvAck, self.recv_ip):     # Message is not valid
            self.socket.close()                 # socket을 닫아줌
            self.quit()                         # quit 해줌

        return True                             # Message가 valid 하므로 True를 리턴해줌
        ######################################################

    def check_result(self, winner, get=False):  # peer와 result가 같은지 확인해주는 함수
        '''
        Function to check if the result between peers are same
        get: if it is false, it means this user is winner and need to report the result first
        '''
        # no skeleton
        ###################  Fill Out  #######################
        # msg를 형식에 맞게 만들어줌
        msg = "RESULT ETTTP/1.0\r\nHost:"+self.send_ip+"\r\nWinner:"+winner+"\r\n\r\n" # winner변수 넣어줌 
        
        self.socket.send(msg.encode())  # socket을 통해 message를 전송해줌

        result=self.socket.recv(SIZE).decode()  # 상대가 보내준 message 를 result에 저장

        msgWinner = result.replace("\r\n", " ").replace(":", " ").split(" ")    #winner를 확인하기 위해 \r\n, :을 공백으로 바꾸고 공백으로 나눠줌
        msg_Winner=msgWinner[5]         # index 5에 해당하는부분에 winner가 있음
        #print(msg_Winner+"는 졌어")
        if (msg_Winner==winner):        # 만약 두 결과가 같으면 (달라야 한 명은 이기고 한 명은 진게 돼서)
            return False                # False를 리턴해줌

        return True                     # 두 결과가 다르면 한 명은 winner 한 명은 loser 이므로 True를 리턴
        ######################################################

    # vvvvvvvvvvvvvvvvvvv  DO NOT CHANGE  vvvvvvvvvvvvvvvvvvv
    def update_board(self, player, move, get=False):    # board를 update를 해주는 함수
        '''
        This function updates Board if is clicked

        '''
        self.board[move] = player['value']                  # player가 선택한 cell의 index에 player의 vlaue를 넣어줌
        self.remaining_moves.remove(move)                   # 선택된 cell의 index를 remaining_moves 리스트에서 제거
        self.cell[self.last_click]['bg'] = self.board_bg    # 마지막으로 클릭한 셀의 배경을 기본 배경으로 변경
        self.last_click = move                              # 마지막으로 클릭한 cell index 를 업데이트
        self.setText[move].set(player['text'])              # 해당 cell의 플레이어의 text 설정
        self.cell[move]['bg'] = player['bg']                # cell의 background를 해당 플레이어의 background color로 설정        
        self.update_status(player, get=get)                 # update_status를 불러 update 완료

    def update_status(self, player, get=False):             # board의 status를 update 해주는 함수
        '''
        This function checks status - define if the game is over or not
        '''
        winner_sum = self.line_size * player['value']       # player가 이기기 위한 cell의 sum을 계산
        for line in self.all_lines:                         # 모든 line에 대해 확인
            if sum(self.board[i] for i in line) == winner_sum:      # 만약, 조건을 만족 시 
                self.l_status_bullet.config(fg='red')               # foreground를 red로 바꿔줌
                self.l_status['text'] = ['Hold']                    # text 도 Hold로 바꿔줌
                self.highlight_winning_line(player, line)           # winning line을 강조
                correct = self.check_result(player['Name'], get=get)    # 결과가 맞는지 check_result를 부름
                if correct:                                 # 만약 결과가 맞으면 (결과가 정상적)
                    self.state = player['win']              # state에 게임의 결과에 맞는 text 설정
                    self.l_result['text'] = player['win']   # l_result에 게임의 결과에 맞는 text 설정
                else:                                       # 결과가 유효하지 않으면
                    self.l_result['text'] = "Somethings wrong…" # l_result에 잘못됨 표기

    def highlight_winning_line(self, player, line):         # winning line을 하이라이트 해줌
        '''
        This function highlights the winning line
        '''
        for i in line:                                      # 해당 라인에 속한 것을 전부 바꿔야하기에 해당 개수 만큼 반복문
            self.cell[i]['bg'] = 'red'                      # 배경을 red로 바꿈

    # ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

# End of Root class

def check_msg(msg, recv_ip):                                    # 전송받은 메세지의 유효성을 확인하는 함수
    '''
    Function that checks if received message is ETTTP format
    '''
    ###################  Fill Out  #######################
    msgR = msg.replace("\r\n", " ").replace(":", " ")           # 줄바꿈과 ":"를 띄어쓰기로 대체한다
    msgSplit = msgR.split(" ")                                  # 띄어쓰기를 기준으로 문자열을 분리한다

    if not (msgSplit[1] == "ETTTP/1.0"):                        # 2번째 문자열에 프로토콜 정보가 담겨있다. ETTTP/1.0이 맞는지 확인
        print("잘못된 프로토콜")                                    # 에러 메시지 출력
        return True                                             
    
    if not (msgSplit[3] == str(recv_ip)):                       # 4번째 문자열에 메시지를 보낼 IP주소가 담겨있다. 즉, 메시지를 받은 입장에선 자신의 IP주소가 담겨있어야 한다.
        print("잘못된 ip주소!")                                    # 잘못된 ip 주소인 경우 에러 메시지 출력
        return True

    return False                                                # 유효한 경우 False 반환
>>>>>>> db9002253ed02bd2a27def731a60f783adb18ef1:ETTTP_TicTacToe_skeleton.py
    ######################################################