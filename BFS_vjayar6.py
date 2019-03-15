import Queue
import random
import time
import os
import itertools
import psutil

class Board:

    def __init__(self):
        self.board = [[], [], [], []] #[[1,2,3,4], [5,6,7,8], [9,10,11,12], [13,14,0,15]]
        self.goal = ((1,2,3,4), (5,6,7,8), (9,10,11,12), (13,14,15,0))       #Coding the goal-state
        self.empty = [3, 3]
        

    def initiate(self, inputString):  #Initializing the initial state of the 15-puzzle board from the given input
        if len(inputString) != 16:
            raise Exception("Solution cannot be found")
        listIndex = 0
        inputIndex = 0
        upperInputIndex = inputIndex + 4
        while inputIndex < upperInputIndex:
                self.board[listIndex].append(inputString[inputIndex])
#                self.printMessage("listIndex: "+str(listIndex)+"inputIndex: "+str(inputIndex))
                inputIndex += 1
                if inputIndex == upperInputIndex:
                    upperInputIndex = inputIndex + 4
                    listIndex += 1
                    if listIndex == 4:
                        break
        self.printMessage("Initial state of the game has been set according to your input: "+str(b.board))
        self.checkIfSolutionExists(inputString)   

    def checkIfSolutionExists(self, inputString):  #Checks if solution exists depending upon where the 0 is placed and the onversion count
        inversionCount = self.getInvCount(inputString)
        row = self.getRowOfZero(inputString)
        
        if (self.isEven(row) and self.isEven(inversionCount)) or (self.isOdd(row) and self.isOdd(inversionCount)):
            self.printMessage("\n The row where 0 is present from the end is "+str(row)+" and inversion count is "+str(inversionCount))
            raise Exception("Solution cannot be found")


    def iddfs(self, root_node):
        iterations = 0 # Only for stats.

  # Depth goes from 0 to infinity. We start at 0 to ensure optimality: we must check
  # that the initial state is not a goal state before generating its children.
        for depth in itertools.count(): 
            queue = [root_node]
    
    # Visited is a dictionary with node hash as key and node depth as value. We need
    # to track depth as in DFS we may encounter visited nodes later at shallower depth.
        visited = {} 

        while len(queue) > 0:
           iterations = iterations + 1
        #   animate_progress(iterations)
      
           node = queue.pop() # Get deepest node.
           visited[node.tilehash()] = node.moves # Mark current node as visited.

           if node.is_goal():
               return result(iterations, queue, node)
     
           if node.moves < depth:
               queue.extend(
               filter(
                 lambda child:
                    child.tilehash() not in visited or
                    visited[child.tilehash()] > child.moves,
                 node.children()))

  # Loop did not return result -> search space exhaustion, no goal found.
        return result(iterations, queue) 


        


    def isOdd(self, number):
        return number%2==1

    def isEven(self, number):
        return number%2==0

    def getRowOfZero(self, inputString):  #Returns ith row from the end where the 0 is placed
        i=0
        while i<16:
            if inputString[i] == 0:
                return 4-int(i/4)
            i += 1
            
    def convert_to_tuple(self, state):
        result = []
        for row in state:
            result.append(tuple(row))
        return tuple(result)


    def match(self, copy):
        a = Board()
        a.board = copy
        for row in range(0, 4):
            for col in range(0, 4):
                if a.board[row][col] == 0:
                    a.empty = [row, col]
        result = []
        for i in a.board:
            result.append(list(i))
        a.board = result
        return a

    def getInvCount(self, inputString):  #Checking the number of inverted tiles in the given state of the puzzle
        inversionCount = 0;
        i=0
        while i<16:
            j=i+1
            while j<16: 
                if (inputString[j] and inputString[i] and inputString[i] > inputString[j]): 
                    inversionCount += 1;
#                    self.printMessage("i and j"+str(inputString[i])+" "+str(inputString[j]))
                j += 1
            i+= 1
        return inversionCount; 
 
    def upwardMovement(self): #Move 0 one square up
        try:
            if self.empty[0] != 0:
                tmp = self.board[self.empty[0]-1][self.empty[1]]
                self.board[self.empty[0]-1][self.empty[1]] = 0
                self.board[self.empty[0]][self.empty[1]] = tmp
                self.empty = [self.empty[0]-1, self.empty[1]]
        except IndexError:
            pass

    def downwardMovement(self): #Move 0 one square down
        try:
            tmp = self.board[self.empty[0]+1][self.empty[1]]
            self.board[self.empty[0]+1][self.empty[1]] = 0
            self.board[self.empty[0]][self.empty[1]] = tmp
            self.empty = [self.empty[0]+1, self.empty[1]]
        except IndexError:
            pass

    def rightwardMovement(self): #Move 0 one square right
        try:
            tmp = self.board[self.empty[0]][self.empty[1]+1]
            self.board[self.empty[0]][self.empty[1]+1] = 0
            self.board[self.empty[0]][self.empty[1]] = tmp
            self.empty = [self.empty[0], self.empty[1]+1]
        except IndexError:
            pass

    def leftwardMovement(self): #Move 0 one square left
        try:
            if self.empty[1] != 0:
                tmp = self.board[self.empty[0]][self.empty[1]-1]
                self.board[self.empty[0]][self.empty[1]-1] = 0
                self.board[self.empty[0]][self.empty[1]] = tmp
                self.empty = [self.empty[0], self.empty[1]-1]
        except IndexError:
            pass

    def printMessage(self, inputString):  #Printing to the console
        print inputString
        
    def solve(self):   #Implementing Breadth First Search. Frontier is the name of the Queue.
        startTime = time.time()
        start = self.convert_to_tuple(self.board)
        pred = {}
        visited = []
        frontier = Queue.Queue()
        frontier.put(start)
        steps = 0
        
        while frontier.qsize() > 0:
            steps += 1
#            self.printMessage("Step: "+str(steps)+"Visited Node Length: "+str(len(visited)))
            tmp = frontier.get()
            ans = tmp
            if tmp == self.goal:
                path = []
                while tmp != start:
                    path.append(pred[tmp][1])
                    tmp = pred[tmp][0]
                finalPath =  path[::-1]  #Printing the final state reached, Time taken for the code to execute, path(directions) followed in BFS to reach the goal state from the initial state 
                self.printMessage("\n Final State reached: "+str(ans)+"\n Time Taken by the program: "+str(time.time()-startTime)+" seconds \n Path Followed: "+str(finalPath)+"\n Number of nodes expanded: "+str(len(visited)))
                self.memUsage() 
                return
            
            if tmp not in visited: #Checking for repetiion of states which are already visited
                visited.append(tmp)
                tmpboard = self.match(tmp)
                tmpboard.upwardMovement()
                if self.convert_to_tuple(tmpboard.board) != tmp:
                    frontier.put(self.convert_to_tuple(tmpboard.board))
                    if not pred.has_key(self.convert_to_tuple(tmpboard.board)):
                        pred[self.convert_to_tuple(tmpboard.board)]=[tmp, 'up']

                
                tmpboard = self.match(tmp)
                tmpboard.downwardMovement()
                if self.convert_to_tuple(tmpboard.board) != tmp:
                    frontier.put(self.convert_to_tuple(tmpboard.board))
                    if not pred.has_key(self.convert_to_tuple(tmpboard.board)):
                        pred[self.convert_to_tuple(tmpboard.board)]=[tmp, 'down']

                        
                tmpboard = self.match(tmp)
                tmpboard.rightwardMovement()
                if self.convert_to_tuple(tmpboard.board) != tmp:
                    frontier.put(self.convert_to_tuple(tmpboard.board))
                    if not pred.has_key(self.convert_to_tuple(tmpboard.board)):
                        pred[self.convert_to_tuple(tmpboard.board)]=[tmp, 'right']

                
                tmpboard = self.match(tmp)
                tmpboard.leftwardMovement()
                if self.convert_to_tuple(tmpboard.board) != tmp:
                    frontier.put(self.convert_to_tuple(tmpboard.board))
                    if not pred.has_key(self.convert_to_tuple(tmpboard.board)):
                        pred[self.convert_to_tuple(tmpboard.board)]=[tmp, 'left']

        raise Exception('Solution cannot be found')

    def memUsage(self):  #Tracking memory usage of the python process in terms of Kilo Bytes
        p = psutil.Process(os.getpid())
        print "\n Memory Used: "+str(p.memory_info()[0]/float(2 ** 20))+"KB"


b=Board()
b.initiate([0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15])
b.solve()
