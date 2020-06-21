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
        self.score = 0  # reset scores
        self.scoreA = 0
        self.scoreB = 0
        for i in range(0, len(self.order)):
            for j in range(0, len(self.order[i])):
                if "+" in self.order[i][j]:  # "+" indicates the box was made by player 1
                    self.score += int(self.order[i][j][1])  # updates the scores
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
            if self.order[item[0] - 1][item[1]] != " ":  # is the position above filled?
                allSides += 1
            if self.order[item[0] + 1][item[1]] != " ":  # is the position below filled?
                allSides += 1
            if self.order[item[0]][item[1] - 1] != " ":  # is the position to the left filled?
                allSides += 1
            if self.order[item[0]][item[1] + 1] != " ":  # is the position to the right filled?
                allSides += 1
            if allSides == 4:  # all the sides are filled, we have a box
                self.makeBox(item[0], item[1], x)

    def makeBox(self, i, j, x):  # marks the board and updates the score if the move made a box
        if x == "X":  # player one made a box
            self.scoreA += int(self.order[i][j])
            self.order[i][j] = "+" + self.order[i][j]
        else:  # player two made a box
            self.scoreB += int(self.order[i][j])
            self.order[i][j] = "-" + self.order[i][j]


class DotsAndBoxes(Frame): # the gui and the

    def __init__(self, parent=None):  # the constructor
        Frame.__init__(self, parent)
        self.pack()
        self.boardSize = IntVar(root)  # used to determine how big the board will be
        self.boardSize.set(3)
        self.plies = IntVar(root)  # used to set how far the algorithm will search
        self.plies.set(3)
        self.playerOneMode = BooleanVar(root)  # used to set players to human or computer mode
        self.playerTwoMode = BooleanVar(root)
        self.playerTwoMode.set(True)  # player two is set to a robot by default
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
        if self.playerOneMode.get():  # if player one is a computer, move.
            self.doMiniMax()

    def move(self, i, j):  # makes a move
        if self.dots.order[i][j] == " ":
            if self.dots.whoseMove:  # it's player one's move
                self.dots.move(i, j, "X")  # make a move
                self.dots.whoseMove = False  # switch whose move it is
                self.display()  # update the board
                self.movesMade += 1  # update how many moves there are
                if self.movesMade == self.movesInGame:  # are we out of moves?
                    self.declareWinner()  # then end the game
                elif self.playerTwoMode.get():  # is the other player a robot?
                    self.doMiniMax()  # then they move automatically
            else:  # it's player two's move
                self.dots.move(i, j, "O")
                self.dots.whoseMove = True
                self.display()
                self.movesMade += 1
                if self.movesMade == self.movesInGame:
                    self.declareWinner()
                elif self.playerOneMode.get():
                    self.doMiniMax()

    def doMiniMax(self):  # makes a call to miniMax
        m = self.miniMax(self.dots, self.plies.get(), self.dots.whoseMove, -1000, 1000)[0]
        self.move(m[0], m[1])

    def miniMax(self, currentState, depth, whoseTurn, alpha, beta):  # algorithm to find the best move
        currentState.findNextMoves()  # where can we move in this state?
        if depth == 0 or len(currentState.nextStates) == 0:  # the bottom of the tree or the potential end of the game
            currentState.findScore()  # evaluate this position
            return [None, currentState.score]  # there is no where to move so we can return just the score
        if whoseTurn:  # finds best move for player 1
            maxMove = currentState.nextStates[0]  # the first state we evaluate
            maxState = copy.deepcopy(currentState)  # create a state based off the og state
            maxState.move(maxMove[0], maxMove[1], "X")  # make a potential move at this spot.
            maxVal = self.miniMax(maxState, depth - 1, False, alpha, beta)[1]
            for i in range(1, len(currentState.nextStates)):  # for all the potential states
                tempState = copy.deepcopy(currentState)  # create a state based off the og state
                tempState.move(currentState.nextStates[i][0], currentState.nextStates[i][1], "X")  # update a position
                tempVal = self.miniMax(tempState, depth - 1, False, alpha, beta)[1]
                if tempVal > maxVal:  # this state has a greater value
                    maxVal = tempVal  # set the maximum value
                    maxMove = currentState.nextStates[i]  # set the maximum state
                alpha = max(alpha, tempVal)  # update the alpha
                if beta <= alpha:  # prune
                    break
            return [maxMove, maxVal]
        else:  # finds best move for player 2
            minMove = currentState.nextStates[0]
            minState = copy.deepcopy(currentState)
            minState.move(minMove[0], minMove[1], "O")
            minVal = self.miniMax(minState, depth - 1, True, alpha, beta)[1]
            for i in range(1, len(currentState.nextStates)):
                tempState = copy.deepcopy(currentState)
                tempState.move(currentState.nextStates[i][0], currentState.nextStates[i][1], "O")
                tempVal = self.miniMax(tempState, depth - 1, True, alpha, beta)[1]
                if tempVal < minVal:  # same as above but looking at minimums
                    minVal = tempVal
                    minMove = currentState.nextStates[i]
                beta = min(beta, tempVal)
                if beta <= alpha:
                    break
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
        Message(scoreFrame, text=str(self.dots.scoreA), padx=2, pady=2).grid(row=2, column=5)  # displays p1 score
        Label(scoreFrame, text="Player two's score:", padx=2, pady=2).grid(row=3, column=5)
        Message(scoreFrame, text=str(self.dots.scoreB), padx=2, pady=2).grid(row=4, column=5)  # displays p2 score
        b = LabelFrame(self.tl, text="Board", padx=2, pady=2)
        b.grid(row=0, rowspan=9, column=2, padx=2, pady=2, sticky=NW)
        for i in range(0, len(self.dots.order)):  # creates the board, made of buttons, for the game
            for j in range(0, len(self.dots.order)):
                if i % 2 == 0:
                    if self.dots.order[i][j] == "*":  # this is a dot
                        Button(b, state = DISABLED, bg="black", width=2, height=1).grid(row=i, column=j)
                    elif self.dots.order[i][j] == "X":  # player one moved here
                        Button(b, bg="red", width=8, height=1, state = DISABLED).grid(row=i, column=j)
                    elif self.dots.order[i][j] == "O":  # player two moved here
                        Button(b, bg="dodger blue", width=8, height=1, state = DISABLED).grid(row=i, column=j)
                    else:  # this box is an available move
                        Button(b, text=self.dots.order[i][j], width=8, height = 1,
                               command=lambda i=i, j=j: self.move(i, j)).grid(row=i, column=j)
                else:
                    if self.dots.order[i][j] == "*":  # this is a dot
                        Button(b, bg="black", width=2, height=1, state = DISABLED).grid(row=i, column=j)
                    elif self.dots.order[i][j] == "X":  # player one moved here
                        Button(b, bg="red", width=2, height=4, state = DISABLED).grid(row=i, column=j)
                    elif self.dots.order[i][j] == "O":  # player two moved here
                        Button(b, bg="dodger blue", width=2, height=4, state = DISABLED).grid(row=i, column=j)
                    elif self.dots.order[i][j][0] == "+":  # player one made this box
                        Button(b, text=self.dots.order[i][j], bg="IndianRed1", width=4, height=2, font = '2',
                               state = DISABLED).grid(row=i, column=j)
                    elif self.dots.order[i][j][0] == "-":  # player two made this box
                        Button(b, text=self.dots.order[i][j], bg="light blue", width=4, height=2, font = '2',
                               state = DISABLED).grid(row=i, column=j)
                    elif self.dots.order[i][j] == " ":  # this box is an available move
                        Button(b, text=self.dots.order[i][j], width=2, height=4,
                               command=lambda i=i, j=j: self.move(i, j)).grid(row=i, column=j)
                    else:
                        Button(b, text=self.dots.order[i][j], width=4, height=2, font = '2',
                               state = DISABLED).grid(row=i, column=j)

    def declareWinner(self):  # creates a popup that states the winner and deletes the game board
        if self.dots.scoreA > self.dots.scoreB:
            winner = "Player One"
            tkinter.messagebox.showinfo("Game Over", winner + " won the game!")
        elif self.dots.scoreA < self.dots.scoreB:
            winner = "Player Two"
            tkinter.messagebox.showinfo("Game Over", winner + " won the game!")
        else:
            tkinter.messagebox.showinfo("Game Over", "Tie game!")
        self.tl.destroy()  # destroys the game board

root = Tk()
DotsAndBoxes().mainloop()
