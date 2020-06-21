# Nate Sanchez

from tkinter import *
import random


class state():
    emptyPos = 0  # position of the empty tile
    costToDo = 0  # the cost of moving here
    order = []  # a list containing the tiles
    nextMoves = []  # a list of potential next moves
    totManDist = 0  # the sum of manhattan costs
    numInGoal = 0  # the number of tiles in the goal position
    goalState = [1, 2, 3, 8, None, 4, 7, 6, 5] #the goal state

    def __init__(self, o, c, ps):
        self.order = o
        self.costToDo = c
        self.prevState = ps
        self.findPositions()

    def findPositions(self):  # finds the current position of each tile in the graph
        self.emptyPos = self.order.index(None)

    def findNextMoves(self):  # finds potential states
        self.nextMoves = []  # clears the list of any leftpver moves from the last runthrough
        if self.emptyPos != 0 and self.emptyPos != 3 and self.emptyPos != 6:  # checks if the blank tile can move left
            tempOrder = list.copy(self.order)
            tempCost = self.order[self.order.index(None) - 1]
            tempOrder[tempOrder.index(None)] = self.order[self.order.index(None) - 1]
            tempOrder[self.order.index(None) - 1] = None
            tempState = state(tempOrder, tempCost, self)
            self.nextMoves.append(tempState)
        if self.emptyPos != 2 and self.emptyPos != 5 and self.emptyPos != 8:  # checks if the blank tile can move right
            tempOrder = list.copy(self.order)
            tempCost = self.order[self.order.index(None) + 1]
            tempOrder[tempOrder.index(None)] = self.order[self.order.index(None) + 1]
            tempOrder[self.order.index(None) + 1] = None
            tempState = state(tempOrder, tempCost, self)
            self.nextMoves.append(tempState)
        if self.emptyPos > 2:  # checks if the blank tile can move up
            tempOrder = list.copy(self.order)
            tempCost = self.order[self.order.index(None) - 3]
            tempOrder[tempOrder.index(None)] = self.order[self.order.index(None) - 3]
            tempOrder[self.order.index(None) - 3] = None
            tempState = state(tempOrder, tempCost, self)
            self.nextMoves.append(tempState)
        if self.emptyPos < 6:  # checks if the blank tile can move down
            tempOrder = list.copy(self.order)
            tempCost = self.order[self.order.index(None) + 3]
            tempOrder[tempOrder.index(None)] = self.order[self.order.index(None) + 3]
            tempOrder[self.order.index(None) + 3] = None
            tempState = state(tempOrder, tempCost, self)
            self.nextMoves.append(tempState)

    def findTotManDist(self):  # finds the sum of the manhattan costs
        self.totManDist = 0
        for i in range(0, len(self.order)):
            if i == 0:
                diff = abs(self.order.index(None) - self.goalState.index(None))
            else:
                diff = abs(self.order.index(i) - self.goalState.index(i))
            if (diff == 1 or diff == 3):
                self.totManDist += 1
            elif (diff == 2 or diff == 4):
                self.totManDist += 2
            elif (diff == 5 or diff == 6 or diff == 7):
                self.totManDist += 3
            elif (diff == 8):
                self.totManDist += 4
            else:
                pass

    def findNumInGoal(self):  # fings how many tiles are in the correct position
        self.numInGoal = 0
        for i in range(0, len(self.order)):
            if self.order[i] == self.goalState[i]:
                self.numInGoal += 1

class board(Frame):  # this will be the gui and how the nodes are handled
    currentState = state([1, 2, 3, 8, None, 4, 7, 6, 5], 0, None)
    totCost = 0
    visitedStates = 0
    stepsToComplete = 0
    out = ""
    maxQueueSize = 0
    solutionCost = 0

    def __init__(self, parent=None):
        Frame.__init__(self, parent)
        self.pack()
        board.makeSquares(self, self.currentState)
        board.makeButtonsAndSuch(self)

    def reset(self):  # sets the state to the default state
        self.currentState = state([1, 2, 3, 8, None, 4, 7, 6, 5], 0, None)
        self.currentState.findPositions()
        self.visitedStates = 0
        self.totCost = 0
        self.stepsToComplete = 0
        self.out = ""
        self.maxQueueSize = 0
        self.solutionCost = 0
        self.makeSquares(self.currentState)

    def fastReset(self):  # resets some variables without setting the state to the default state
        self.visitedStates = 0
        self.totCost = 0
        self.stepsToComplete = 0
        self.out = ""
        self.maxQueueSize = 0
        self.solutionCost = 0

    def printState(self, state):
        for i in range(0, 9):
            if state.order[i] == None:
                self.out += "  "
            else:
                self.out += str(state.order[i])
                self.out += " "
            if i == 2 or i == 5 or i == 8:
                self.out += "\n"
        self.out += ("Cost: " + str(state.costToDo))
        del state
        self.out += "------\n"

    def scramble(self):  # creates a random initial state, potential for an unsolvable state
        self.fastReset()
        random.shuffle(self.currentState.order)
        self.makeSquares(self.currentState)

    def easy(self):  # creates the easy state
        self.fastReset()
        self.currentState.order = [1, 3, 4, 8, 6, 2, 7, None, 5]
        self.currentState.findPositions()
        self.makeSquares(self.currentState)

    def medium(self):  # creates the medium state
        self.fastReset()
        self.currentState.order = [2, 8, 1, None, 4, 3, 7, 6, 5]
        self.currentState.findPositions()
        self.makeSquares(self.currentState)

    def hard(self):  # creates the hard state
        self.fastReset()
        self.currentState.order = [5, 6, 7, 4, None, 8, 3, 2, 1]
        self.currentState.findPositions()
        self.makeSquares(self.currentState)

    def move(self, val):  # manually switches a tile with the blank tile
        temp1 = self.currentState.order.index(val)
        temp2 = self.currentState.order.index(None)
        temp3 = self.currentState.order[temp1]
        temp4 = self.currentState.order[temp2]
        self.currentState.order[temp1] = temp4
        self.currentState.order[temp2] = temp3
        self.currentState.findPositions()
        self.makeSquares(self.currentState)  # update the gui

    def bfs(self):  # breadth-first search
        myState = state(self.currentState.order.copy(), 0, None)
        steps = []  # keeps track of the best route
        queue = []  # keeps track of our next moves
        visited = set()  # keeps track of visited states
        while myState.order != myState.goalState:  # stop once we've reached the goal state
            visited.add(str(myState.order))  # add the current state to the visited set
            myState.findPositions()  # find the positions of every tile
            myState.findNextMoves()  # find what states we can go to
            for item in myState.nextMoves:
                if str(item.order) not in visited and item not in queue:  # can't revisit states
                    queue.append(item)
                    self.maxQueueSize += 1
            myState = queue.pop(0)  # fifo, go to the next item in the queue
            self.totCost += myState.costToDo  # increment the total cost
            self.visitedStates += 1  # increment how many states we visited
        goBackState = myState  # we've left the queue and need to return the optimal route via the state's parent
        self.currentState = state(myState.order.copy(), 0, None)  # keep track for the gui
        while (goBackState != None):  # go back until we get to the starting state
            steps.append(goBackState)
            goBackState = goBackState.prevState  # go back through parent nodes
        self.stepsToComplete = len(steps) - 1  # how many steps the optimal path takes
        while len(steps) > 0:
            solState = steps.pop()
            self.solutionCost += solState.costToDo
            self.printState(solState)  # print out the states in the optimal path
        self.makeSquares(self.currentState)  # should display the goal state if everything worked.

    def dfs(self):  # depth first search
        myState = state(self.currentState.order.copy(), 0, None)
        steps = []  # keeps track of the best route
        queue = []  # keeps track of our next moves
        visited = set()  # keeps track of visited states
        while myState.order != myState.goalState:  # stop once we've reached the goal state
            visited.add(str(myState.order))  # add the current state to the visited set
            myState.findPositions()  # find the positions of every tile
            myState.findNextMoves()  # find what states we can go to
            for item in myState.nextMoves:
                if str(item.order) not in visited and item not in queue:  # can't revisit states
                    queue.append(item)
                    self.maxQueueSize += 1
            myState = queue.pop(-1)  # lifo, go to the next item in the queue
            self.totCost += myState.costToDo  # increment the total cost
            self.visitedStates += 1  # increment how many states we visited
        goBackState = myState  # we've left the queue and need to return the optimal route via the state's parent
        self.currentState = state(myState.order.copy(), 0, None)  # keep track for the gui
        while (goBackState != None):  # go back until we get to the starting state
            steps.append(goBackState)
            goBackState = goBackState.prevState  # go back through parent nodes
        self.stepsToComplete = len(steps) - 1  # how many steps the optimal path takes
        while len(steps) > 0:
            solState = steps.pop()
            self.solutionCost += solState.costToDo
            self.printState(solState)  # print out the states in the optimal path
        self.makeSquares(self.currentState)  # should display the goal state if everything worked.

    def ucs(self):  # uniform-cost search
        myState = state(self.currentState.order.copy(), 0, None)
        steps = []  # keeps track of the best route
        queue = []  # keeps track of our next moves
        visited = set()  # keeps track of visited states
        while myState.order != myState.goalState:  # stop once we've reached the goal state
            visited.add(str(myState.order))  # add the current state to the visited set
            myState.findPositions()  # find the positions of every tile
            myState.findNextMoves()  # find what states we can go to
            for item in myState.nextMoves:
                if str(item.order) not in visited and item not in queue:
                    i = 0
                    while i < len(queue) and item.costToDo >= queue[i].costToDo:  # to put the state in the queue based on cost of a move
                        i += 1
                    if i == len(queue):
                        queue.append(item)  # this has the greatest cost and goes on the end.
                    else:
                        queue.insert(i, item)  # inserts at the index
                    self.maxQueueSize += 1
            myState = queue.pop(0)  # fifo, go to the next item in the queue
            self.totCost += myState.costToDo  # increment the total cost
            self.visitedStates += 1  # increment how many states we visited
        goBackState = myState  # we've left the queue and need to return the optimal route via the state's parent
        self.currentState = state(myState.order.copy(), 0, None)  # keep track for the gui
        while (goBackState != None):  # go back until we get to the starting state
            steps.append(goBackState)
            goBackState = goBackState.prevState  # go back through parent nodes
        self.stepsToComplete = len(steps) - 1  # how many steps the optimal path takes
        while len(steps) > 0:
            solState = steps.pop()
            self.solutionCost += solState.costToDo
            self.printState(solState)  # print out the states in the optimal path
        self.makeSquares(self.currentState)  # should display the goal state if everything worked.

    def best(self):  # best-first search, h = number of tiles not in correct position
        myState = state(self.currentState.order.copy(), 0, None)
        steps = []  # keeps track of the best route
        queue = []  # keeps track of our next moves
        visited = set()  # keeps track of visited states
        while myState.order != myState.goalState:  # stop once we've reached the goal state
            visited.add(str(myState.order))  # add the current state to the visited set
            myState.findPositions()  # find the positions of every tile
            myState.findNextMoves()  # find what states we can go to
            for item in myState.nextMoves:
                if str(item.order) not in visited and item not in queue:
                    item.findNumInGoal()  # find how many tiles are in the right spot
                    i = 0
                    while i < len(queue) and (9 - item.numInGoal) >= (
                            9 - queue[i].numInGoal):  # finds where to insert based on how many are out of place
                        i += 1
                    if i == len(queue):
                        queue.append(item)
                    else:
                        queue.insert(i, item)
                    self.maxQueueSize += 1
            myState = queue.pop(0)  # fifo, go to the next item in the queue
            self.totCost += myState.costToDo  # increment the total cost
            self.visitedStates += 1  # increment how many states we visited
        goBackState = myState  # we've left the queue and need to return the optimal route via the state's parent
        self.currentState = state(myState.order.copy(), 0, None)  # keep track for the gui
        while (goBackState != None):  # go back until we get to the starting state
            steps.append(goBackState)
            goBackState = goBackState.prevState  # go back through parent nodes
        self.stepsToComplete = len(steps) - 1  # how many steps the optimal path takes
        while len(steps) > 0:
            solState = steps.pop()
            self.solutionCost += solState.costToDo
            self.printState(solState)  # print out the states in the optimal path
        self.makeSquares(self.currentState)  # should display the goal state if everything worked.

    def a1(self):  # A* search, h = number of tiles that are not in correct position
        myState = state(self.currentState.order.copy(), 0, None)
        steps = []  # keeps track of the best route
        queue = []  # keeps track of our next moves
        visited = set()  # keeps track of visited states
        while myState.order != myState.goalState:  # stop once we've reached the goal state
            visited.add(str(myState.order))  # add the current state to the visited set
            myState.findPositions()  # find the positions of every tile
            myState.findNextMoves()  # find what states we can go to
            for item in myState.nextMoves:
                if str(item.order) not in visited and item not in queue:
                    item.findNumInGoal()
                    i = 0
                    while i < len(queue) and (item.costToDo + (9 - item.numInGoal)) >= (queue[i].costToDo + (9 - queue[
                        i].numInGoal)):  # finds where to insert based on cost of the move and the amount of tiles in the correct position
                        i += 1
                    if i == len(queue):
                        queue.append(item)
                    else:
                        queue.insert(i, item)
                    self.maxQueueSize += 1
            myState = queue.pop(0)  # fifo, go to the next item in the queue
            self.totCost += myState.costToDo  # increment the total cost
            self.visitedStates += 1  # increment how many states we visited
        goBackState = myState  # we've left the queue and need to return the optimal route via the state's parent
        self.currentState = state(myState.order.copy(), 0, None)  # keep track for the gui
        while (goBackState != None):  # go back until we get to the starting state
            steps.append(goBackState)
            goBackState = goBackState.prevState  # go back through parent nodes
        self.stepsToComplete = len(steps) - 1  # how many steps the optimal path takes
        while len(steps) > 0:
            solState = steps.pop()
            self.solutionCost += solState.costToDo
            self.printState(solState)  # print out the states in the optimal path
        self.makeSquares(self.currentState)  # should display the goal state if everything worked.

    def a2(self):  # A* search, h = sum of manhattan distances between all tiles and their correct positions
        myState = state(self.currentState.order.copy(), 0, None)
        steps = []  # keeps track of the best route
        queue = []  # keeps track of our next moves
        visited = set()  # keeps track of visited states
        while myState.order != myState.goalState:  # stop once we've reached the goal state
            visited.add(str(myState.order))  # add the current state to the visited set
            myState.findPositions()  # find the positions of every tile
            myState.findNextMoves()  # find what states we can go to
            for item in myState.nextMoves:
                if str(item.order) not in visited and item not in queue:
                    item.findTotManDist()
                    i = 0
                    while i < len(queue) and (item.costToDo + item.totManDist) >= (queue[i].costToDo + queue[
                        i].totManDist):  # finds where to insert based on total total manhattan distance and the cost to make a move
                        i += 1
                    if i == len(queue):
                        queue.append(item)
                    else:
                        queue.insert(i, item)
                    self.maxQueueSize += 1
            myState = queue.pop(0)  # fifo, go to the next item in the queue
            self.totCost += myState.costToDo  # increment the total cost
            self.visitedStates += 1  # increment how many states we visited
        goBackState = myState  # we've left the queue and need to return the optimal route via the state's parent
        self.currentState = state(myState.order.copy(), 0, None)  # keep track for the gui
        while (goBackState != None):  # go back until we get to the starting state
            steps.append(goBackState)
            goBackState = goBackState.prevState  # go back through parent nodes
        self.stepsToComplete = len(steps) - 1  # how many steps the optimal path takes
        while len(steps) > 0:
            solState = steps.pop()
            self.solutionCost += solState.costToDo
            self.printState(solState)  # print out the states in the optimal path
        self.makeSquares(self.currentState)  # should display the goal state if everything worked.

    def makeSquares(self, state):  # the part of the gui I want to be refreshed
        Button(self, text=state.order[0], command=lambda: self.move(state.order[0])).grid(row=0, column=2, ipadx=4, ipady=3)
        Button(self, text=state.order[1], command=lambda: self.move(state.order[1])).grid(row=0, column=3, ipadx=4, ipady=3)
        Button(self, text=state.order[2], command=lambda: self.move(state.order[2])).grid(row=0, column=4, ipadx=4, ipady=3)
        Button(self, text=state.order[3], command=lambda: self.move(state.order[3])).grid(row=1, column=2, ipadx=4, ipady=3)
        Button(self, text=state.order[4], command=lambda: self.move(state.order[4])).grid(row=1, column=3, ipadx=4, ipady=3)
        Button(self, text=state.order[5], command=lambda: self.move(state.order[5])).grid(row=1, column=4, ipadx=4, ipady=3)
        Button(self, text=state.order[6], command=lambda: self.move(state.order[6])).grid(row=2, column=2, ipadx=4, ipady=3)
        Button(self, text=state.order[7], command=lambda: self.move(state.order[7])).grid(row=2, column=3, ipadx=4, ipady=3)
        Button(self, text=state.order[8], command=lambda: self.move(state.order[8])).grid(row=2, column=4, ipadx=4, ipady=3)
        Label(self, text=self.totCost, width=10).grid(row=5, column=8)  # this is the actual cost and manhattan cost
        Label(self, text=self.stepsToComplete, width=10).grid(row=1, column=8)
        Label(self, text=self.visitedStates, width=10).grid(row=3, column=8)
        Label(self, text=self.solutionCost, width=10).grid(row=1, column=9)
        Label(self, text=self.maxQueueSize, width=10).grid(row=3, column=9)
        myScrollbar = Scrollbar(self, orient=VERTICAL)
        myScrollbar.grid(row=0, rowspan=10, column=7, sticky=(N, S))
        m = Text(self, yscrollcommand=myScrollbar.set, width=7, height=10)
        m.grid(row=0, rowspan=10, column=6)
        m.insert(END, self.out)
        myScrollbar.config(command=m.yview)

    def makeButtonsAndSuch(self):  # the part of the gui that shouldn't change
        Button(self, text='Easy', command=lambda: self.easy(), width=10).grid(row=0, column=0)  # set up for the easy problem
        Button(self, text='Medium', command=lambda: self.medium(), width=10).grid(row=1, column=0)  # set up for the medium problem
        Button(self, text='Hard', command=lambda: self.hard(), width=10).grid(row=2, column=0)  # set up for the hard problem
        Button(self, text='Scramble', command=lambda: self.scramble(), width=10).grid(row=3, column=0)  # scrambels the tiles
        Button(self, text='Breadth-first', command=lambda: self.bfs(), width=10).grid(row=0, column=1)  # all of these will start their respective searches
        Button(self, text='Depth-first', command=lambda: self.dfs(), width=10).grid(row=1, column=1)
        Button(self, text='Uniform-cost', command=lambda: self.ucs(), width=10).grid(row=2, column=1)
        Button(self, text='Best-first', command=lambda: self.best(), width=10).grid(row=3, column=1)
        Button(self, text='A*1', command=lambda: self.a1(), width=10).grid(row=4, column=1)
        Button(self, text='A*2', command=lambda: self.a2(), width=10).grid(row=5, column=1)
        Button(self, text='Reset', command=lambda: self.reset(), width=10).grid(row=4, column=0)
        Label(self, text='Total Cost:').grid(row=4, column=8)  # displays the total cost of all the moves we've made
        Label(self, text='Steps to Complete:').grid(row=0, column=8)  # displays the current total manhattan cost
        Label(self, text="States visited:").grid(row=2, column=8)
        Label(self, text='Solution Cost:').grid(row=0, column=9)  # displays the current total manhattan cost
        Label(self, text="Max Queue Size:").grid(row=2, column=9)
        Label(self, text="Please give the program time to load.").grid(row=7, column=0, columnspan=3)

board().mainloop()#Nate Sanchez