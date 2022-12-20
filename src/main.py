import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLabel, QLCDNumber, QMessageBox
from PyQt5.QtGui import QIcon
from PyQt5 import uic
from PyQt5.QtCore import QSize, QTimer
from datetime import datetime


class Chess(QWidget):
    def __init__(self):
        super().__init__()
        self.turn = '0'
        self.whiteEattenIcons = []
        self.blackEattenIcons = []
        self.whiteNum = [[], []]
        self.blackNum = [[], []]
        for i in (10, 540):
            k = 0
            for j in (170, 230, 290, 350, 410):
                if i == 10:
                    self.whiteEattenIcons.append(QPushButton("", self))
                    self.whiteEattenIcons[k].setGeometry(i, j, 50, 50)
                    self.whiteEattenIcons[k].setIconSize(QSize(50, 50))

                    cur = QLabel('x0', self)
                    cur.setStyleSheet("color:white;""font-size:15pt;")
                    cur.setGeometry(i+60, j, 30, 50)
                    self.whiteNum[0].append(cur)
                    self.whiteNum[1].append(0)
                else:
                    self.blackEattenIcons.append(QPushButton("", self))
                    self.blackEattenIcons[k].setGeometry(i, j, 50, 50)
                    self.blackEattenIcons[k].setIconSize(QSize(50, 50))
                    cur = QLabel('0x', self)
                    cur.setStyleSheet("color:white;""font-size:15pt;")
                    cur.setGeometry(i-27, j, 30, 50)
                    self.blackNum[0].append(cur)
                    self.blackNum[1].append(0)
                k += 1
        self.board = list()
        self.whiteEattenIcons[0].setIcon(QIcon('../images/chessPieces/bQ.png'))
        self.whiteEattenIcons[1].setIcon(QIcon('../images/chessPieces/bR.png'))
        self.whiteEattenIcons[2].setIcon(QIcon('../images/chessPieces/bB.png'))
        self.whiteEattenIcons[3].setIcon(QIcon('../images/chessPieces/bH.png'))
        self.whiteEattenIcons[4].setIcon(QIcon('../images/chessPieces/bP.png'))

        self.blackEattenIcons[0].setIcon(QIcon('../images/chessPieces/wQ.png'))
        self.blackEattenIcons[1].setIcon(QIcon('../images/chessPieces/wR.png'))
        self.blackEattenIcons[2].setIcon(QIcon('../images/chessPieces/wB.png'))
        self.blackEattenIcons[3].setIcon(QIcon('../images/chessPieces/wH.png'))
        self.blackEattenIcons[4].setIcon(QIcon('../images/chessPieces/wP.png'))

        self.timeNowW = datetime.now()
        self.timeNowB = datetime.now()
        self.timeStopW = datetime(2000, 1, 1, 0, 0, 0)
        self.timeStopB = datetime(2000, 1, 1, 0, 0, 0)

        self.whiteLcd = QLCDNumber(self)
        self.blackLcd = QLCDNumber(self)

        self.whiteLcd.setGeometry(5, 40, 120, 30)
        self.blackLcd.setGeometry(470, 40, 120, 30)

        self.timerWhite = QTimer()
        self.timerBlack = QTimer()

        self.timerWhite.timeout.connect(self.whiteLcdFunc)
        self.timerBlack.timeout.connect(self.blackLcdFunc)

        self.timerWhite.start(1000)
        self.timerBlack.start(1000)

        self.nextMove = True
        self.setWindowTitle("Chess")
        self.setWindowIcon(QIcon('../images/chessIcon.png'))
        self.setFixedHeight(600)
        self.setFixedWidth(600)

        

        # '0' is white and '1' is black
        self.pieces = list()
        for i in range(0, 8):
            self.pieces.append(list())
            for j in range(0, 8):
                self.pieces[i].append(QPushButton("", self))
                self.pieces[i][j].setGeometry(50*(j+2), 50*(i+2), 50, 50)
                self.pieces[i][j].clicked.connect(self.whatPiece)
        self.createBoard()
        # first one for white king, second for black
        self.kingsPos = [(7, 4), (0, 4)]
        self.moveCol = 'background-color:#57cc99'
        self.eatCol = 'background-color:#d00000'
        self.whatChanged = list()

        self.cannotMoveWhite = [[], []]
        self.cannotMoveBlack = [[], []]
        self.castleKing = [False, False]  # for castlng
        self.kingCheck = list()
        self.checkCount = 0
        self.score = QLabel('0 : 0', self)
        self.score.setStyleSheet("color:white;""font-size:18pt;")
        self.score.setGeometry(270, 0, 250, 30)
        uic.loadUi('test.ui', self)
        self.scoreCount = [0, 0]  # first for white second for black

        self.help_btn = QPushButton("HELP",self)
        self.help_btn.setGeometry(510,570,75,23)
        self.help_btn.clicked.connect(self.help_)

    def help_(self):
        print("yes")
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Information)

        msg.setText("Some Documentation")
        msg.setInformativeText("""
This is a programm written on Python, which enables play by two players on the same computer. All possible rules of the game are being developed, including:

When choosing a piece, shows its possible moves positions, taking into account whether chess opens its own to the king, or whether it is possible to go to that position at a given moment in the game or not.
Have a section showing the current game results.
Counts the time spent by each player.
Showing the out-of-play stones.
  """)
        msg.setWindowTitle("Chess Game")
        
        msg.setStandardButtons(QMessageBox.Ok)
        retval = msg.exec_() 

    def whiteLcdFunc(self):
        if self.turn == '0':
            time = str(datetime.now() - self.timeNowW +
                       self.timeStopW).split('-')
            time = time[2][3:].split(':')
            time = [int(float(i)) for i in time]

            time = datetime(2000, 1, 1, int(
                time[0]), int(time[1]), int(time[2]))
        else:
            time = self.timeStopW
        f_time = time.strftime("%H:%M:%S")
        self.whiteLcd.display(f_time)
        self.whiteLcd.setDigitCount(12)

    def blackLcdFunc(self):
        if self.turn == '1':
            time = str(datetime.now() - self.timeNowB +
                       self.timeStopB).split('-')
            time = time[2][3:].split(':')
            time = [int(float(i)) for i in time]
            time = datetime(2000, 1, 1, int(
                time[0]), int(time[1]), int(time[2]))
        else:
            time = self.timeStopB
        f_time = time.strftime("%H:%M:%S")
        self.blackLcd.display(f_time)
        self.blackLcd.setDigitCount(12)

    def recolorBoard(self, do=True):
        all = self.whatChanged + self.kingCheck
        for i in all:
            if i in self.kingCheck and do:
                continue
            color = 'background-color: '
            if i[0] % 2:
                if i[1] % 2:
                    color += 'white'
                else:
                    color += '#bb9457'
            else:
                if i[1] % 2:
                    color += '#bb9457'
                else:
                    color += 'white'
            self.pieces[i[0]][i[1]].setStyleSheet(color)

    def colorCells(self):

        for i in self.kingCheck:
            self.pieces[i[0]][i[1]].setStyleSheet(
                'background-color:yellow')
        if len(self.whatChanged) == 0:
            return
        i = self.whatChanged[0]
        if len(self.kingCheck) == 0 or 'k' in self.board[i[0]][i[1]] or i not in self.kingCheck:

            self.pieces[i[0]][i[1]].setStyleSheet(self.moveCol)
        for i in self.whatChanged[1:]:
            if self.board[i[0]][i[1]] != "":
                self.pieces[i[0]][i[1]].setStyleSheet(self.eatCol)
            else:
                self.pieces[i[0]][i[1]].setStyleSheet(self.moveCol)

    def pawnMove(self, x, y):
        self.whatChanged = [(x, y)]
        t = False
        if len(self.kingCheck) != 0:
            t = True

        if self.turn == '0':
            k = (x, y) in self.cannotMoveWhite[0]
            if k:
                x1, y1 = self.cannotMoveWhite[1][self.cannotMoveWhite[0].index(
                    (x, y))]
            if self.board[x-1][y] == "" and (not k or y == y1) and (not t or (x-1, y) in self.kingCheck):
                self.whatChanged.append((x-1, y))
                if x == 6 and self.board[x-2][y] == "" and self.board[x-2][y] == "" and (not k or y == y1) and (not t or (x-2, y) in self.kingCheck):
                    self.whatChanged.append((x-2, y))
            if y-1 > -1 and self.board[x-1][y-1] != "" and self.board[x-1][y-1][0] == '1' and (not k or (x-1, y-1) == (x1, y1)) and (not t or (x-1, y-1) in self.kingCheck):
                self.whatChanged.append((x-1, y-1))
            if y+1 < 8 and self.board[x-1][y+1] != "" and self.board[x-1][y+1][0] == '1' and (not k or (x-1, y+1) == (x1, y1)) and (not t or (x-1, y+1) in self.kingCheck):
                self.whatChanged.append((x-1, y+1))
        elif self.turn == '1':
            k = (x, y) in self.cannotMoveBlack[0]
            if k:
                x1, y1 = self.cannotMoveBlack[1][self.cannotMoveBlack[0].index(
                    (x, y))]
            if self.board[x+1][y] == "" and (not k or y == y1) and (not t or (x+1, y) in self.kingCheck):
                self.whatChanged.append((x+1, y))
                if x == 1 and self.board[x+2][y] == "" and (not k or y == y1) and (not t or (x+2, y) in self.kingCheck):
                    self.whatChanged.append((x+2, y))
            if y-1 > -1 and self.board[x+1][y-1] != "" and self.board[x+1][y-1][0] == '0' and (not k or (k and (x+1, y-1) == (x1, y1))) and (not t or (x+1, y-1) in self.kingCheck):
                self.whatChanged.append((x+1, y-1))
            if y+1 < 8 and self.board[x+1][y+1] != "" and self.board[x+1][y+1][0] == '0' and (not k or (k and (x+1, y+1) == (x1, y1))) and (not t or (x+1, y+1) in self.kingCheck):
                self.whatChanged.append((x+1, y+1))

    def bishopMove(self, x, y, ):
        f = False
        if len(self.kingCheck) != 0:
            f = True

        self.whatChanged = [(x, y)]
        if self.turn == '1':
            t = (x, y) in self.cannotMoveBlack[0]
            if t:
                x1, y1 = self.cannotMoveBlack[1][self.cannotMoveBlack[0].index(
                    (x, y))]
        else:
            t = (x, y) in self.cannotMoveWhite[0]
            if t:
                x1, y1 = self.cannotMoveWhite[1][self.cannotMoveWhite[0].index(
                    (x, y))]
        i, j = x+1, y+1

        while i < 8 and j < 8:
            if self.turn in self.board[i][j]:
                break
            if (not t or x1-i == y1-j) and (not f or (i, j) in self.kingCheck):
                self.whatChanged.append((i, j))
            if self.board[i][j] != "":
                break
            i += 1
            j += 1
        i, j = x+1, y-1
        while i < 8 and j > -1:
            if self.turn in self.board[i][j]:
                break
            if (not t or x1-i == y1-j) and (not f or (i, j) in self.kingCheck):
                self.whatChanged.append((i, j))
            if self.board[i][j] != "":
                break
            i += 1
            j -= 1
        i, j = x-1, y+1
        while i > -1 and j < 8:
            if self.turn in self.board[i][j]:
                break
            if (not t or x1-i == y1-j) and (not f or (i, j) in self.kingCheck):
                self.whatChanged.append((i, j))
            if self.board[i][j] != "":
                break
            i -= 1
            j += 1
        i, j = x-1, y-1
        while i > -1 and j > -1:
            if self.turn in self.board[i][j]:
                break
            if (not t or x1-i == y1-j) and (not f or (i, j) in self.kingCheck):
                self.whatChanged.append((i, j))
            if self.board[i][j] != "":
                break
            i -= 1
            j -= 1

    def rookMove(self, x, y, ):
        f = False
        if len(self.kingCheck) != 0:
            f = True

        self.whatChanged = [(x, y)]
        if self.turn == '1':
            t = (x, y) in self.cannotMoveBlack[0]
            if t:
                x1, y1 = self.cannotMoveBlack[1][self.cannotMoveBlack[0].index(
                    (x, y))]
        else:
            t = (x, y) in self.cannotMoveWhite[0]
            if t:
                x1, y1 = self.cannotMoveWhite[1][self.cannotMoveWhite[0].index(
                    (x, y))]

        i = x+1
        while i < 8:
            if self.turn in self.board[i][y]:
                break
            if (not t or y == y1) and (not f or (i, y) in self.kingCheck):
                self.whatChanged.append((i, y))
            if self.board[i][y] != "":
                break
            i += 1
        i = x-1
        while i > -1:
            if self.turn in self.board[i][y]:
                break
            if (not t or y == y1) and (not f or (i, y) in self.kingCheck):
                self.whatChanged.append((i, y))
            if self.board[i][y] != "":
                break
            i -= 1
        i = y+1
        while i < 8:
            if self.turn in self.board[x][i]:
                break
            if (not t or x == x1) and (not f or (x, i) in self.kingCheck):
                self.whatChanged.append((x, i))
            if self.board[x][i] != "":
                break
            i += 1
        i = y-1
        while i > -1:
            if self.turn in self.board[x][i]:
                break
            if (not t or x == x1) and (not f or (x, i) in self.kingCheck):
                self.whatChanged.append((x, i))
            if self.board[x][i] != "":
                break
            i -= 1

    def knightMove(self, x, y, ):
        f = False
        if len(self.kingCheck) != 0:
            f = True

        self.whatChanged = [(x, y)]
        if self.turn == '1':
            t = (x, y) in self.cannotMoveBlack[0]
            if t:
                x1, y1 = self.cannotMoveBlack[1][self.cannotMoveBlack[0].index(
                    (x, y))]
        else:
            t = (x, y) in self.cannotMoveWhite[0]
            if t:
                x1, y1 = self.cannotMoveWhite[1][self.cannotMoveWhite[0].index(
                    (x, y))]

        self.whatChanged = [(x, y)]
        if x+2 < 8:
            if y+1 < 8 and self.turn not in self.board[x+2][y+1] and (not t or (x1, y1) == (x+2, y+1)) and (not f or (x+2, y+1) in self.kingCheck):
                self.whatChanged.append((x+2, y+1))
            if y-1 > -1 and self.turn not in self.board[x+2][y-1] and (not t or (x1, y1) == (x+2, y-1)) and (not f or (x+2, y-1) in self.kingCheck):
                self.whatChanged.append((x+2, y-1))
        if x+1 < 8:
            if y+2 < 8 and self.turn not in self.board[x+1][y+2] and (not t or (x1, y1) == (x+1, y+2)) and (not f or (x+1, y+2) in self.kingCheck):
                self.whatChanged.append((x+1, y+2))
            if y-2 > -1 and self.turn not in self.board[x+1][y-2] and (not t or (x1, y1) == (x+1, y-2)) and (not f or (x+1, y-2) in self.kingCheck):
                self.whatChanged.append((x+1, y-2))
        if x-2 > -1:
            if y+1 < 8 and self.turn not in self.board[x-2][y+1] and (not t or (x1, y1) == (x-2, y+1)) and (not f or (x-2, y+1) in self.kingCheck):
                self.whatChanged.append((x-2, y+1))
            if y-1 > -1 and self.turn not in self.board[x-2][y-1] and (not t or (x1, y1) == (x-2, y-1)) and (not f or (x-2, y-1) in self.kingCheck):
                self.whatChanged.append((x-2, y-1))
        if x-1 > -1:
            if y+2 < 8 and self.turn not in self.board[x-1][y+2] and (not t or (x1, y1) == (x-1, y+2)) and (not f or (x-1, y+2) in self.kingCheck):
                self.whatChanged.append((x-1, y+2))
            if y-2 > -1 and self.turn not in self.board[x-1][y-2] and (not t or (x1, y1) == (x-1, y-2)) and (not f or (x-1, y-2) in self.kingCheck):
                self.whatChanged.append((x-1, y-2))

    def queenMove(self, x, y):
        self.rookMove(x, y)
        cur = self.whatChanged
        self.bishopMove(x, y)
        if len(self.whatChanged) != 0:
            del self.whatChanged[0]
        self.whatChanged = cur + self.whatChanged

    def kingMove(self, x, y):
        if self.turn == '1':
            cstl = self.castleKing[1]
            pos = 0
        else:
            cstl = self.castleKing[0]
            pos = 7
        i = x-1
        t = False

        self.whatChanged = [(x, y)]
        for i in range(i, i+3):
            if i < 8 and i > -1:
                j = y-1
                for j in range(j, j+3):
                    if j < 8 and j > -1:
                        if self.turn in self.board[i][j]:
                            continue
                        self.board[x][y] = ""
                        self.checkOfKing((i, j))
                        self.board[x][y] = "1k" if pos == 0 else '0k'
                        if len(self.kingCheck) == 0:
                            t = False
                        else:
                            t = True
                        if (not t or (i, j) not in self.kingCheck):
                            self.whatChanged.append((i, j))
        if not cstl and 'k' in self.board[pos][4] and len(self.whatChanged) >=2:
            k = True
            for i in range(4):
                if (i == 0):
                    if self.board[pos][i][1] == "" or (self.board[pos][i][1] != "" and self.board[pos][i][1] != 'r'):
                        k = False
                        break
                else:
                    if self.board[pos][i] != "":
                        k = False
                        break
                    self.board[pos][y] = ""
                    self.checkOfKing((pos, i))
                    self.board[pos][y] = "1k" if pos == 0 else '0k'
                    if len(self.kingCheck) == 0:
                        t = False
                    else:
                        t = True
                    if t:
                        k = False
                        break
            if k:
                self.whatChanged.append((pos, 2))
            k = True
            for i in range(5, 8):
                if (i == 7):
                    if self.board[pos][i][1] != "" or (self.board[pos][i][1] != "" and self.board[pos][i][1] != 'r'):
                        k = False
                        break
                else:
                    if self.board[pos][i] != "":
                        k = False
                        break
                    self.board[pos][y] = ""
                    self.checkOfKing((pos, i))
                    self.board[pos][y] = "1k" if pos == 0 else '0k'
                    if len(self.kingCheck) == 0:
                        t = False
                    else:
                        t = True
                    if t:
                        k = False
                        break
            if k:
                self.whatChanged.append((pos, 6))
        self.checkOfKing((x, y))

    def checkKingCheck(self):
        cur1 = list()
        cur2 = list()
        x, y = self.kingsPos[1] if self.turn == '1' else self.kingsPos[0]

        i, j = x+1, y+1
        i1, j1 = -1, -1
        count = 0
        while i < 8 and j < 8:
            cur_el = self.board[i][j]
            if self.turn in cur_el:
                if not count:
                    count += 1
                    i1, j1 = i, j
                else:
                    break
            elif cur_el != "":
                if (cur_el[1] == 'b' or cur_el[1] == 'q') and count == 1:
                    cur1.append((i1, j1))
                    cur2.append((i, j))
                break
            i += 1
            j += 1
        i, j = x+1, y-1
        count = 0
        while i < 8 and j > -1:
            cur_el = self.board[i][j]
            if self.turn in cur_el:
                if not count:
                    count += 1
                    i1, j1 = i, j
                else:
                    break
            elif cur_el != "":
                if (cur_el[1] == 'b' or cur_el[1] == 'q') and count == 1:
                    cur1.append((i1, j1))
                    cur2.append((i, j))
                break
            i += 1
            j -= 1
        i, j = x-1, y+1
        count = 0
        while i > -1 and j < 8:
            cur_el = self.board[i][j]
            if self.turn in cur_el:
                if not count:
                    count += 1
                    i1, j1 = i, j
                else:
                    break
            elif cur_el != "":
                if (cur_el[1] == 'b' or cur_el[1] == 'q') and count == 1:
                    cur1.append((i1, j1))
                    cur2.append((i, j))
                break
            i -= 1
            j += 1
        i, j = x-1, y-1
        count = 0
        while i > -1 and j > -1:
            cur_el = self.board[i][j]
            if self.turn in cur_el:
                if not count:
                    count += 1
                    i1, j1 = i, j
                else:
                    break
            elif cur_el != "":
                if (cur_el[1] == 'b' or cur_el[1] == 'q') and count == 1:
                    cur1.append((i1, j1))
                    cur2.append((i, j))
                break
            i -= 1
            j -= 1

        i = x+1
        count = 0
        while i < 8:
            cur_el = self.board[i][y]
            if self.turn in cur_el:
                if not count:
                    count += 1
                    i1, j1 = i, y
                else:
                    break
            elif cur_el != "":
                if (cur_el[1] == 'r' or cur_el[1] == 'q') and count == 1:
                    cur1.append((i1, j1))
                    cur2.append((i, y))
                break
            i += 1
        i = x-1
        count = 0
        while i > -1:
            cur_el = self.board[i][y]
            if self.turn in cur_el:
                if not count:
                    count += 1
                    i1, j1 = i, y
                else:
                    break
            elif cur_el != "":
                if (cur_el[1] == 'r' or cur_el[1] == 'q') and count == 1:
                    cur1.append((i1, j1))
                    cur2.append((i, y))
                break
            i -= 1
        i = y+1
        count = 0
        while i < 8:
            cur_el = self.board[x][i]
            if self.turn in cur_el:
                if not count:
                    count += 1
                    i1, j1 = x, i
                else:
                    break
            elif cur_el != "":
                if (cur_el[1] == 'r' or cur_el[1] == 'q') and count == 1:
                    cur1.append((i1, j1))
                    cur2.append((x, i))
                break
            i += 1
        i = y-1
        count = 0
        while i > -1:
            cur_el = self.board[x][i]
            if self.turn in cur_el:
                if not count:
                    count += 1
                    i1, j1 = x, i
                else:
                    break
            elif cur_el != "":
                if (cur_el[1] == 'r' or cur_el[1] == 'q') and count == 1:
                    cur1.append((i1, j1))
                    cur2.append((x, i))
                break
            i -= 1

        if self.turn == '1':
            self.cannotMoveBlack = [cur1, cur2]
            self.cannotMoveWhite = []
        else:
            self.cannotMoveBlack = []
            self.cannotMoveWhite = [cur1, cur2]

    def getPos(self, piece):
        for i in range(8):
            for j in range(8):
                if self.pieces[i][j] == piece:
                    return(i, j)

    def whatIcon(self, x, y):
        if self.board[x][y][0] == '1':
            if self.board[x][y][1] == 'r':
                return '../images/chessPieces/bR.png'
            if self.board[x][y][1] == 'h':
                return '../images/chessPieces/bH.png'
            if self.board[x][y][1] == 'b':
                return '../images/chessPieces/bB.png'
            if self.board[x][y][1] == 'q':
                return '../images/chessPieces/bQ.png'
            if self.board[x][y][1] == 'k':
                return '../images/chessPieces/bK.png'
            if self.board[x][y][1] == 'p':
                return '../images/chessPieces/bP.png'
        elif self.board[x][y][0] == '0':
            if self.board[x][y][1] == 'r':
                return '../images/chessPieces/wR.png'
            if self.board[x][y][1] == 'h':
                return '../images/chessPieces/wH.png'
            if self.board[x][y][1] == 'b':
                return '../images/chessPieces/wB.png'
            if self.board[x][y][1] == 'q':
                return '../images/chessPieces/wQ.png'
            if self.board[x][y][1] == 'k':
                return '../images/chessPieces/wK.png'
            if self.board[x][y][1] == 'p':
                return '../images/chessPieces/wP.png'

    def movePiece(self, cord):
        x1, y1 = self.whatChanged[0]
        x2, y2 = cord
        t = False

        if self.board[x1][y1][1] == 'k' and (x1 != x2 or y1 != y2):
            if self.turn == '0' and not self.castleKing[0]:
                self.kingsPos[0] = (x2, y2)
                if x1 == 7 and (y2 == 2 or y2 == 6):
                    t = True

                else:
                    t = False
                self.castleKing[0] = True
            elif self.turn == '1' and not self.castleKing[1]:
                self.kingsPos[1] = (x2, y2)
                if x1 == 0 and (y2 == 2 or y2 == 6):
                    t = True

                else:
                    t = False
                self.castleKing[1] = True
        if self.board[x1][y1][1] == 'p':
            if self.turn == '0' and x2 == 0:
                self.board[x1][y1] = '0q'
            elif x2 == 7:
                self.board[x1][y1] = '1q'
        # 170,230,290,350,410
        # +60 -27
        if self.board[x2][y2] != "" and (x1 != x2 and y1 != y2):
            tmp = self.board[x2][y2][1]
            if self.turn == '0':
                if tmp == 'q':
                    self.whiteNum[1][0] += 1
                    self.whiteNum[0][0].setText('x'+str(self.whiteNum[1][0]))
                elif tmp == 'r':
                    self.whiteNum[1][1] += 1
                    self.whiteNum[0][1].setText('x'+str(self.whiteNum[1][1]))
                elif tmp == 'b':
                    self.whiteNum[1][2] += 1
                    self.whiteNum[0][2].setText('x'+str(self.whiteNum[1][2]))
                elif tmp == 'h':
                    self.whiteNum[1][3] += 1
                    self.whiteNum[0][3].setText('x'+str(self.whiteNum[1][3]))
                elif tmp == 'p':
                    self.whiteNum[1][4] += 1
                    self.whiteNum[0][4].setText('x' + str(self.whiteNum[1][4]))
            else:
                if tmp == 'q':
                    self.blackNum[1][0] += 1
                    self.blackNum[0][0].setText(str(self.blackNum[1][0]) + 'x')
                elif tmp == 'r':
                    self.blackNum[1][1] += 1
                    self.blackNum[0][1].setText(str(self.blackNum[1][1]) + 'x')
                elif tmp == 'b':
                    self.blackNum[1][2] += 1
                    self.blackNum[0][2].setText(str(self.blackNum[1][2]) + 'x')
                elif tmp == 'h':
                    self.blackNum[1][3] += 1
                    self.blackNum[0][3].setText(str(self.blackNum[1][3]) + 'x')
                elif tmp == 'p':
                    self.blackNum[1][4] += 1
                    self.blackNum[0][4].setText(str(self.blackNum[1][4]) + 'x')
        if t:
            i = 2
        else:
            i = 1

        for i in range(i):
            self.pieces[x1][y1].setIcon(QIcon())

            self.pieces[x2][y2].setIcon(QIcon(self.whatIcon(x1, y1)))
            self.board[x2][y2] = self.board[x1][y1]

            if t:
                self.board[x1][y1] = ""
                if y2 == 2:
                    y1 = 0
                    y2 = 3
                else:
                    y1 = 7
                    y2 = 5

        self.recolorBoard(False)
        if not (x1 == x2 and y1 == y2):
            self.board[x1][y1] = ""
            if self.turn == '0':
                time = str(datetime.now() - self.timeNowW +
                           self.timeStopW).split('-')
                time = time[2][3:].split(':')
                time = [int(float(i)) for i in time]
                time = datetime(2000, 1, 1, int(
                    time[0]), int(time[1]), int(time[2]))
                self.timeStopW = time
                self.timeNowB = datetime.now()
                self.turnLabel.setText('Turn: Black')
                self.turnLabel.setStyleSheet("color:black;""font-size:18pt;")
                self.turnLabel.setGeometry(235, 530, 130, 30)
                self.turn = '1'
            else:
                time = str(datetime.now() - self.timeNowB +
                           self.timeStopB).split('-')
                time = time[2][3:].split(':')
                time = [int(float(i)) for i in time]
                time = datetime(2000, 1, 1, int(
                    time[0]), int(time[1]), int(time[2]))
                self.timeStopB = time
                self.timeNowW = datetime.now()

                self.turnLabel.setText('Turn: White')
                self.turnLabel.setStyleSheet("color:white;""font-size:18pt;")
                self.turnLabel.setGeometry(235, 530, 130, 30)
                self.turn = '0'

    def whatPiece(self, cord=None):

        if not cord:
            self.checkKingCheck()
            x, y = self.getPos(self.sender())
        else:
            x, y = cord
        if (x, y) in self.whatChanged:
            self.movePiece((x, y))

            self.recolorBoard()
            self.checkOfKing()
            self.checkKingCheck()
            self.whatChanged = list()
            self.colorCells()
            if not self.canMove():
                self.kingCheck = list()
                if self.turn == '0':
                    self.scoreCount[1] += 1
                else:
                    self.scoreCount[0] += 1
                self.timeStopB = datetime(2000,1,1,0,0,0)
                self.timeStopW = datetime(2000,1,1,0,0,0)

                text = str(self.scoreCount[0]) + \
                    " : " + str(self.scoreCount[1])
                self.score.setText(text)
                self.score.setStyleSheet("color:white;""font-size:18pt;")
                self.score.setGeometry(270, 0, 250, 30)
                self.createBoard()
                return True
            return
        elif len(self.kingCheck) == 0:
            self.recolorBoard()
            self.whatChanged = list()

        if self.board[x][y] == "" and not cord:
            if len(self.whatChanged) != 0:
                self.recolorBoard()
            self.whatChanged = list()
            self.checkOfKing()
            return

        if self.turn in self.board[x][y] and not cord:
            self.recolorBoard()
            self.whatChanged = list()

        if self.board[x][y][1] == 'p' and self.board[x][y][0] == self.turn and self.checkCount < 2:
            self.pawnMove(x, y)
        elif self.board[x][y][1] == 'b' and self.board[x][y][0] == self.turn and self.checkCount < 2:
            self.bishopMove(x, y)
        elif self.board[x][y][1] == 'r' and self.board[x][y][0] == self.turn and self.checkCount < 2:
            self.rookMove(x, y)
        elif self.board[x][y][1] == 'q' and self.board[x][y][0] == self.turn and self.checkCount < 2:
            self.queenMove(x, y)
        elif self.board[x][y][1] == 'h' and self.board[x][y][0] == self.turn and self.checkCount < 2:
            self.knightMove(x, y)
        elif self.board[x][y][1] == 'k' and self.board[x][y][0] == self.turn:
            self.kingMove(x, y)
        if not cord:
            self.colorCells()

    def createBoard(self):
        self.turn = '0'  # '0' is white and '1' is black
        self.board = [['1r', '1h', '1b', '1q', '1k', '1b', '1h', '1r'],
                      ['1p', '1p', '1p', '1p', '1p', '1p', '1p', '1p'],
                      ['', '', '', '', '', '', '', ''],
                      ['', '', '', '', '', '', '', ''],
                      ['', '', '', '', '', '', '', ''],
                      ['', '', '', '', '', '', '', ''],
                      ['0p', '0p', '0p', '0p', '0p', '0p', '0p', '0p'],
                      ['0r', '0h', '0b', '0q', '0k', '0b', '0h', '0r']]

        self.turnLabel = QLabel('Turn: White', self)
        self.turnLabel.setStyleSheet("color:white;""font-size:18pt;")
        self.turnLabel.setGeometry(235, 530, 130, 30)
        self.turnLabel.setText('Turn: White')
        self.turnLabel.setStyleSheet("color:white;""font-size:18pt;")
        self.turnLabel.setGeometry(235, 530, 130, 30)

        for j in range(5):
            self.whiteNum[1][j] = 0
            self.whiteNum[0][j].setText('x'+str(self.whiteNum[1][j]))
            self.blackNum[1][j] = 0
            self.blackNum[0][j].setText(str(self.blackNum[1][j]) + 'x')
        print(self.blackNum)
        print(self.whiteNum)

        for i in range(0, 8):
            self.pieces.append(list())
            for j in range(0, 8):
                color = 'background-color: '
                if i % 2:
                    if j % 2:
                        color += 'white'
                    else:
                        color += '#bb9457'
                else:
                    if j % 2:
                        color += '#bb9457'
                    else:
                        color += 'white'
                self.pieces[i][j].setStyleSheet(color)
                if i == 0:
                    if j == 0 or j == 7:
                        self.pieces[i][j].setIcon(QIcon('../images/chessPieces/bR.png'))
                    elif j == 1 or j == 6:
                        self.pieces[i][j].setIcon(QIcon('../images/chessPieces/bH.png'))
                    elif j == 2 or j == 5:
                        self.pieces[i][j].setIcon(QIcon('../images/chessPieces/bB.png'))
                    elif j == 3:
                        self.pieces[i][j].setIcon(QIcon('../images/chessPieces/bQ.png'))
                    elif j == 4:
                        self.pieces[i][j].setIcon(QIcon('../images/chessPieces/bK.png'))
                elif i == 1:
                    self.pieces[i][j].setIcon(QIcon('../images/chessPieces/bP.png'))
                elif i == 7:
                    if j == 0 or j == 7:
                        self.pieces[i][j].setIcon(QIcon('../images/chessPieces/wR.png'))
                    elif j == 1 or j == 6:
                        self.pieces[i][j].setIcon(QIcon('../images/chessPieces/wH.png'))
                    elif j == 2 or j == 5:
                        self.pieces[i][j].setIcon(QIcon('../images/chessPieces/wB.png'))
                    elif j == 3:
                        self.pieces[i][j].setIcon(QIcon('../images/chessPieces/wQ.png'))
                    elif j == 4:
                        self.pieces[i][j].setIcon(QIcon('../images/chessPieces/wK.png'))
                elif i == 6:
                    self.pieces[i][j].setIcon(QIcon('../images/chessPieces/wP.png'))
                else:
                    self.pieces[i][j].setIcon(QIcon())
                self.pieces[i][j].setIconSize(QSize(50, 50))

    def checkOfKing(self, cord=None):
        self.checkCount = 0
        self.kingCheck = []
        if self.turn == '0':
            turn_ = '1'
            if cord == None:
                kPos = self.kingsPos[0]
            else:
                kPos = cord
        else:
            turn_ = '0'
            if cord == None:
                kPos = self.kingsPos[1]
            else:
                kPos = cord
        self.kingCheck = []
        i = 0
        x, y = kPos[0] + 1, kPos[1] + 1
        while True:
            if not (x < 8 and y < 8):
                self.kingCheck = self.kingCheck[:i]
                break
            self.kingCheck.append((x, y))
            if self.board[x][y] == turn_ + 'b' or self.board[x][y] == turn_ + 'q':
                self.checkCount += 1
                break
            elif self.board[x][y] != "":
                self.kingCheck = self.kingCheck[:i]
                break
            x += 1
            y += 1
        i = len(self.kingCheck)
        x, y = kPos[0] + 1, kPos[1] - 1
        while True:
            if not (x < 8 and y > -1):
                self.kingCheck = self.kingCheck[:i]
                break
            self.kingCheck.append((x, y))
            if self.board[x][y] == turn_ + 'b' or self.board[x][y] == turn_ + 'q':
                self.checkCount += 1
                break
            elif self.board[x][y] != "":
                self.kingCheck = self.kingCheck[:i]
                break
            x += 1
            y -= 1
        i = len(self.kingCheck)
        x, y = kPos[0] - 1, kPos[1] - 1
        while True:
            if not (x > -1 and y > -1):
                self.kingCheck = self.kingCheck[:i]
                break
            self.kingCheck.append((x, y))
            if self.board[x][y] == turn_ + 'b' or self.board[x][y] == turn_ + 'q':
                self.checkCount += 1
                break
            elif self.board[x][y] != "":
                self.kingCheck = self.kingCheck[:i]
                break
            x -= 1
            y -= 1
        i = len(self.kingCheck)
        x, y = kPos[0] - 1, kPos[1] + 1
        while True:
            if not (x > -1 and y < 8):
                self.kingCheck = self.kingCheck[:i]
                break
            self.kingCheck.append((x, y))
            if self.board[x][y] == turn_ + 'b' or self.board[x][y] == turn_ + 'q':
                self.checkCount += 1
                break
            elif self.board[x][y] != "":
                self.kingCheck = self.kingCheck[:i]
                break
            y += 1
            x -= 1

        i = len(self.kingCheck)
        x, y = kPos[0] + 1, kPos[1]
        while True:
            if not (x < 8):
                self.kingCheck = self.kingCheck[:i]
                break
            self.kingCheck.append((x, y))
            if self.board[x][y] == turn_ + 'r' or self.board[x][y] == turn_ + 'q':
                self.checkCount += 1
                break
            elif self.board[x][y] != "":
                self.kingCheck = self.kingCheck[:i]
                break
            x += 1
        i = len(self.kingCheck)
        x = kPos[0] - 1
        while True:
            if not (x > -1):
                self.kingCheck = self.kingCheck[:i]
                break
            self.kingCheck.append((x, y))
            if self.board[x][y] == turn_ + 'r' or self.board[x][y] == turn_ + 'q':
                self.checkCount += 1
                break
            elif self.board[x][y] != "":
                self.kingCheck = self.kingCheck[:i]
                break
            x -= 1

        i = len(self.kingCheck)
        x, y = kPos[0], kPos[1] + 1
        while True:
            if not (y < 8):
                self.kingCheck = self.kingCheck[:i]
                break
            self.kingCheck.append((x, y))
            if self.board[x][y] == turn_ + 'r' or self.board[x][y] == turn_ + 'q':
                self.checkCount += 1
                break
            elif self.board[x][y] != "":
                self.kingCheck = self.kingCheck[:i]
                break
            y += 1

        i = len(self.kingCheck)
        y = kPos[1] - 1
        while True:
            if not (y > -1):
                self.kingCheck = self.kingCheck[:i]
                break
            self.kingCheck.append((x, y))
            if self.board[x][y] == turn_ + 'r' or self.board[x][y] == turn_ + 'q':
                self.checkCount += 1
                break
            elif self.board[x][y] != "":
                self.kingCheck = self.kingCheck[:i]
                break
            y -= 1

        x, y = kPos[0], kPos[1]
        if x+2 < 8:
            if y+1 < 8 and self.board[x+2][y+1] == turn_ + 'h':
                self.checkCount += 1
                self.kingCheck.append((x+2, y+1))
            if y-1 > -1 and self.board[x+2][y-1] == turn_ + 'h':
                self.checkCount += 1
                self.kingCheck.append((x+2, y-1))
        if x+1 < 8:
            if y+2 < 8 and self.board[x+1][y+2] == turn_ + 'h':
                self.checkCount += 1
                self.kingCheck.append((x+1, y+2))
            if y-2 > -1 and self.board[x+1][y-2] == turn_ + 'h':
                self.checkCount += 1
                self.kingCheck.append((x+1, y-2))
        if x-2 > -1:
            if y+1 < 8 and self.board[x-2][y+1] == turn_ + 'h':
                self.checkCount += 1
                self.kingCheck.append((x-2, y+1))
            if y-1 > -1 and self.board[x-2][y-1] == turn_ + 'h':
                self.checkCount += 1
                self.kingCheck.append((x-2, y-1))
        if x-1 > -1:
            if y+2 < 8 and self.board[x-1][y+2] == turn_ + 'h':
                self.checkCount += 1
                self.kingCheck.append((x-1, y+2))
            if y-2 > -1 and self.board[x-1][y-2] == turn_ + 'h':
                self.checkCount += 1
                self.kingCheck.append((x-1, y-2))

        if turn_ == '1':
            if x-1 > -1:
                if y-1 > -1 and self.board[x-1][y-1] != "" and self.board[x-1][y] == '1p':
                    self.checkCount += 1
                    self.kingCheck.append((x-1, y-1))
                if y+1 < 8 and self.board[x-1][y+1] != "" and self.board[x-1][y+1] == '1p':
                    self.checkCount += 1
                    self.kingCheck.append((x-1, y+1))
        else:
            if x+1 < 8:

                if y-1 > -1 and self.board[x+1][y-1] != "" and self.board[x+1][y-1] == '0p':
                    self.checkCount += 1
                    self.kingCheck.append((x+1, y-1))
                if y+1 < 8 and self.board[x+1][y+1] != "" and self.board[x+1][y+1] == '0p':
                    self.checkCount += 1
                    self.kingCheck.append((x+1, y+1))

        if len(self.kingCheck) == 0:
            return
        self.kingCheck = [(kPos[0], kPos[1])] + self.kingCheck

    def canMove(self):
        if self.turn == '0':
            turn_ = '0'
        else:
            turn_ = '1'
        for x in range(8):
            for y in range(8):
                self.whatChanged = []
                if self.board[x][y] == "" or self.board[x][y][0] != turn_:
                    continue
                self.whatPiece((x, y))
                if len(self.whatChanged) > 1:
                    self.whatChanged = []
                    return True
        return False


app = QApplication(sys.argv)
window = Chess()
window.show()
sys.exit(app.exec())

'''
if __name__ == "__main__":
    app = QApplication(sys.argv)
    # ...
    sys.exit(app.exec())
'''
