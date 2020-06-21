from tkinter import *
import tkinter.messagebox
import random
import copy


class State:  # a state of the game

    def __init__(self, o):  # constructor
        self.order = o  # the board itself
        self.score = 0  # the total score of the game
        self.scoreA = 0  # the score of player 1
        self.scoreB = 0  # the score of player 2
        self.nextStates = []  # a list of potential next moves
        self.whoseMove = True  # keeps track of whose turn it is, True = player 1, False = player 2

    def findScore(self):  # finds the scores of each player
        self.score = 0
        self.scoreA = 0
        self.scoreB = 0
        for i in range(0, len(self.order)):
            for j in range(0, len(self.order[i])):
                if "+" in self.order[i][j]:  # "+" indicates the box was made by player 1
                    self.score += int(self.order[i][j][1])
                    self.scoreA += int(self.order[i][j][1])
                elif "-" in self.order[i][j]:  # "-" indicates the box was made by player 2
                    self.score -= int(self.order[i][j][1])
                    self.scoreB += int(self.order[i][j][1])

    def move(self, i, j, x):  # changes the board
        self.order[i][j] = x
        self.wouldMakeBox(i, j, x)

    def findNextMoves(self): # finds potential next moves
        self.nextStates = []
        for i in range(0, len(self.order)):
            for j in range(0, len(self.order[i])):
                if self.order[i][j] == " ":
                    self.nextStates.append([i, j])

    def wouldMakeBox(self, i, j, x):  # checks to see if that move would make a box
        boxesToCheck = []
        if i > 0 and j % 2 != 0:
            boxesToCheck.append([i - 1, j])
        if i < len(self.order) - 1 and j % 2 != 0:
            boxesToCheck.append([i + 1, j])
        if j > 0 and i % 2 != 0:
            boxesToCheck.append([i, j - 1])
        if j < len(self.order) - 1 and i % 2 != 0:
            boxesToCheck.append([i, j + 1])
        for item in boxesToCheck:
            allSides = 0
            if self.order[item[0] - 1][item[1]] != " ":
                allSides += 1
            if self.order[item[0] + 1][item[1]] != " ":
                allSides += 1
            if self.order[item[0]][item[1] - 1] != " ":
                allSides += 1
            if self.order[item[0]][item[1] + 1] != " ":
                allSides += 1
            if allSides == 4:
                self.makeBox(item[0], item[1], x)

    def makeBox(self, i, j, x):  # marks the board and updates the score if the move made a box
        if x == "X":
            self.scoreA += int(self.order[i][j])
            self.order[i][j] = "+" + self.order[i][j]
        else:
            self.scoreB += int(self.order[i][j])
            self.order[i][j] = "-" + self.order[i][j]


class DotsAndBoxes(Frame): # the gui and the

    def __init__(self, parent=None):  # the constructor
        Frame.__init__(self, parent)
        self.pack()
        self.boardSize = IntVar(root)  # used to determine how big the board will be
        self.boardSize.set(2)
        self.plies = IntVar(root)  # used to set how far the algorithm will search
        self.plies.set(1)
        self.playerOneMode = BooleanVar(root)  # used to set players to human or computer mode
        self.playerTwoMode = BooleanVar(root)
        self.makeGui()

    def makeBoard(self):  # generates the 2d array that represents the board
        self.tl = Toplevel(self)  # create a new window to store the board
        self.dots = State([])  # make sure it is empty first
        self.movesInGame = (int(self.boardSize.get()) * 2 * (
                int(self.boardSize.get()) + 1))  # find out how many moves are in the game
        self.movesMade = 0  # make sure other variables are reset
        for i in range(0, (int(self.boardSize.get()) * 2) + 1):
            self.dots.order.append([])
            for j in range(0, (int(self.boardSize.get()) * 2) + 1):
                if i % 2 == 0:
                    if j % 2 == 0:
                        self.dots.order[i].append("*")
                    else:
                        self.dots.order[i].append(" ")
                else:
                    if j % 2 == 0:
                        self.dots.order[i].append(" ")
                    else:
                        self.dots.order[i].append(str(random.randint(1, 5)))
        self.display()
        if self.playerOneMode.get():
            self.doMiniMax()

    def move(self, i, j):
        if self.dots.order[i][j] == " ":
            if self.dots.whoseMove:
                self.dots.move(i, j, "X")
                self.dots.whoseMove = False
                self.display()
                if self.playerTwoMode.get():
                    self.doMiniMax()
                    self.movesMade += 1
            else:
                self.dots.move(i, j, "O")
                self.dots.whoseMove = True
                self.display()
                if self.playerOneMode.get():
                    self.doMiniMax()
                    self.movesMade += 1
            self.movesMade += 1
            if self.movesMade == self.movesInGame:
                self.declareWinner()

    def doMiniMax(self):  # calculates the best move
        print("Starting miniMax")
        print(self.movesInGame - self.movesMade)
        if int(self.plies.get()) > self.movesInGame - self.movesMade:
            self.plies.set(self.movesInGame - self.movesMade - 1)
        elif int(self.plies.get()) < 1:
            self.plies.set(1)
        print(self.plies.get())
        if self.dots.whoseMove:
            m = self.miniMax(self.dots, self.plies.get(), True, self.dots.score)[0]
            self.dots.move(m[0], m[1], "X")
            self.dots.whoseMove = False
        else:
            m = self.miniMax(self.dots, self.plies.get(), False, self.dots.score)[0]
            self.dots.move(m[0], m[1], "O")
            self.dots.whoseMove = True
        self.display()

    def miniMax(self, currentState, depth, whoseTurn, val):
        if depth == 0:
            currentState.findScore()
            return [None, currentState.score]
        if whoseTurn:
            currentState.findNextMoves()
            maxMove = currentState.nextStates[0]
            maxState = copy.deepcopy(currentState)
            maxState.move(maxMove[0], maxMove[1], "X")
            maxVal = self.miniMax(maxState, depth - 1, False, val)[1]
            for i in range(1, len(currentState.nextStates)):
                tempState = copy.deepcopy(currentState)
                tempState.move(currentState.nextStates[i][0], currentState.nextStates[i][1], "X")
                tempVal = self.miniMax(tempState, depth - 1, False, val)[1]
                if tempVal > maxVal:
                    maxVal = tempVal
                    maxMove = currentState.nextStates[i]
            return [maxMove, maxVal]
        else:
            currentState.findNextMoves()
            minMove = currentState.nextStates[0]
            minState = copy.deepcopy(currentState)
            minState.move(minMove[0], minMove[1], "O")
            minVal = self.miniMax(minState, depth - 1, True, val)[1]
            for i in range(1, len(currentState.nextStates)):
                tempState = copy.deepcopy(currentState)
                tempState.move(currentState.nextStates[i][0], currentState.nextStates[i][1], "O")
                tempVal = self.miniMax(tempState, depth - 1, True, val)[1]
                if tempVal < minVal:
                    minVal = tempVal
                    minMove = currentState.nextStates[i]
            return [minMove, minVal]

    def makeGui(self):  # creates the game options
        root.title("Nate's Dots and Boxes Game")  # title
        opFrame = LabelFrame(self, text="Options", padx=2, pady=2)
        opFrame.grid(row=0, column=0, sticky=NW)
        Label(opFrame, text="Player 1:", fg="red").grid(row=1, column=0)
        r1 = Radiobutton(opFrame, text="Human", variable=self.playerOneMode, value=False)
        r1.grid(row=2, column=0, columnspan=2, sticky=W)
        r2 = Radiobutton(opFrame, text="Computer", variable=self.playerOneMode, value=True)
        r2.grid(row=3, column=0, columnspan=2, sticky=W)
        Label(opFrame, text="Player 2:", fg="dodger blue").grid(row=4, column=0)
        r3 = Radiobutton(opFrame, text="Human", variable=self.playerTwoMode, value=False)
        r3.grid(row=5, column=0, columnspan=2, sticky=W)
        r4 = Radiobutton(opFrame, text="Computer", variable=self.playerTwoMode, value=True)
        r4.grid(row=6, column=0, columnspan=2, sticky=W)
        Label(opFrame, text="Plies:").grid(row=7, column=0, sticky=W)
        Label(opFrame, text="Size:").grid(row=8, column=0, sticky=W)
        Entry(opFrame, width=5, textvariable=self.plies).grid(row=7, column=1, padx=2, pady=2, sticky=W)
        Entry(opFrame, width=5, textvariable=self.boardSize).grid(row=8, column=1, padx=2, pady=2, sticky=W)
        b = Button(opFrame, width=10, text="Create board",
                   command=lambda: self.makeBoard())  # pressing will generate the board
        b.grid(row=9, column=0, columnspan=2, padx=2, pady=2, sticky=W)

    def display(self):  # creates the bvisual representation of the board as well as a way to play the game
        scoreFrame = LabelFrame(self.tl, text="Score", padx=2, pady=2)
        scoreFrame.grid(row=0, column=5, sticky=NW)
        Label(scoreFrame, text="Player one's score:", padx=2, pady=2).grid(row=1, column=5)
        Message(scoreFrame, text=str(self.dots.scoreA), padx=2, pady=2).grid(row=2, column=5)
        Label(scoreFrame, text="Player two's score:", padx=2, pady=2).grid(row=3, column=5)
        Message(scoreFrame, text=str(self.dots.scoreB), padx=2, pady=2).grid(row=4, column=5)
        b = LabelFrame(self.tl, text="Board", padx=2, pady=2)
        b.grid(row=0, rowspan=9, column=2, padx=2, pady=2, sticky=NW)
        for i in range(0, len(self.dots.order)):  #
            for j in range(0, len(self.dots.order)):
                if self.dots.order[i][j] == "*":
                    Button(b, text=self.dots.order[i][j], bg="black", width=2, height=1,
                           command=lambda i=i, j=j: self.move(i, j)).grid(row=i, column=j)
                elif self.dots.order[i][j] == "X":
                    Button(b, text=self.dots.order[i][j], fg="red", width=2,
                           command=lambda i=i, j=j: self.move(i, j)).grid(row=i, column=j)
                elif self.dots.order[i][j] == "O":
                    Button(b, text=self.dots.order[i][j], fg="dodger blue", width=2, height=1,
                           command=lambda i=i, j=j: self.move(i, j)).grid(row=i, column=j)
                elif self.dots.order[i][j][0] == "+":
                    Button(b, text=self.dots.order[i][j], bg="red", width=2, height=1,
                           command=lambda i=i, j=j: self.move(i, j)).grid(row=i, column=j)
                elif self.dots.order[i][j][0] == "-":
                    Button(b, text=self.dots.order[i][j], bg="dodger blue", width=2, height=1,
                           command=lambda i=i, j=j: self.move(i, j)).grid(row=i, column=j)
                else:
                    Button(b, text=self.dots.order[i][j], width=2,
                           command=lambda i=i, j=j: self.move(i, j)).grid(row=i, column=j)

    def declareWinner(self):  # creates a popup that states the winner and deletes the game board
        if self.dots.scoreA > self.dots.scoreB:
            winner = "Player One"
        else:
            winner = "Player Two"
        tkinter.messagebox.showinfo("Game Over", winner + " won the game!")  # the pop-up
        self.tl.destroy()  # destroys the game board


root = Tk()
DotsAndBoxes().mainloop()
