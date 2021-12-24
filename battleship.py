"""
Battleship Project
Name:
Roll No:
"""

import battleship_tests as test

project = "Battleship" # don't edit this

### SIMULATION FUNCTIONS ###

from tkinter import *
import random

EMPTY_UNCLICKED = 1
SHIP_UNCLICKED = 2
EMPTY_CLICKED = 3
SHIP_CLICKED = 4


'''
makeModel(data)
Parameters: dict mapping strs to values
Returns: None
'''
def makeModel(data):
    data["rows"]=10
    data["cols"]=10
    data["board_size"]=500
    data["cell_size"]=data["board_size"]/(data["rows"])
    data["user_board"]=emptyGrid(data["rows"],data["cols"])
    data["computer_board"]=emptyGrid(data["rows"],data["cols"])
    data["number_ships"]=5
    addShips(data["computer_board"],data["number_ships"])
    data["temp_ship"]=[]
    data["user_ships"]=0
    data["winner"]=None
    return data
'''
makeView(data, userCanvas, compCanvas)
Parameters: dict mapping strs to values ; Tkinter canvas ; Tkinter canvas
Returns: None
'''
def makeView(data, userCanvas, compCanvas):
    drawGrid(data,userCanvas,data["user_board"],True)
    drawGrid(data, compCanvas,data["computer_board"],False)
    drawShip(data,userCanvas,data["temp_ship"])
    drawGameOver(data,userCanvas)
    return


'''
keyPressed(data, events)
Parameters: dict mapping strs to values ; key event object
Returns: None
'''
def keyPressed(data, event):
    pass


'''
mousePressed(data, event, board)
Parameters: dict mapping strs to values ; mouse event object ; 2D list of ints
Returns: None
'''
def mousePressed(data, event, board):
    if data["winner"]!=None:
        return None
    r,c=getClickedCell(data, event)
    if board=="user":
        clickUserBoard(data, r, c)
    if board=="comp":
        runGameTurn(data, r, c)



#### WEEK 1 ####

'''
emptyGrid(rows, cols)
Parameters: int ; int
Returns: 2D list of ints
'''
def emptyGrid(rows, cols):
    all=[]
    for i in range(rows):
        a=[]
        for j in range(cols):
            a.append(EMPTY_UNCLICKED)
        all.append(a)
    return all


'''
createShip()
Parameters: no parameters
Returns: 2D list of ints
'''
def createShip():
    r=random.randint(1,8)#2
    c=random.randint(1,8)#3
    z=random.randint(0,1)#0
    if z==0:
        ship=[[r-1,c],[r,c],[r+1,c]]#[1,3][2,3][3,3]
    else:
        ship=[[r,c-1],[r,c],[r,c+1]]#[2,2][2,3][2,4]
    return ship


'''
checkShip(grid, ship)
Parameters: 2D list of ints ; 2D list of ints
Returns: bool
'''
def checkShip(grid, ship):
    for i in range(len(ship)):
        if grid[ship[i][0]][ship[i][1]]!=EMPTY_UNCLICKED: 
            return False
    return True


'''
addShips(grid, numShips)
Parameters: 2D list of ints ; int
Returns: 2D list of ints
'''
def addShips(grid, numShips):
    S=0
    while S<numShips:
        create1=createShip()
        check1=checkShip(grid, create1)
        if  check1==True:
            for j in create1:
                grid[j[0]][j[1]]=SHIP_UNCLICKED    
            S+=1    
    return grid


'''
drawGrid(data, canvas, grid, showShips)
Parameters: dict mapping strs to values ; Tkinter canvas ; 2D list of ints ; bool
Returns: None
'''
def drawGrid(data, canvas, grid, showShips):
    for r in range(data["rows"]):
        for c in range(data["cols"]):
            if grid[r][c]==SHIP_UNCLICKED:
                if showShips==True:
                    canvas.create_rectangle(c*data["cell_size"],r*data["cell_size"],data["cell_size"]+c*data["cell_size"],r*data["cell_size"]+data["cell_size"],fill="yellow")
                else:
                    canvas.create_rectangle(c*data["cell_size"],r*data["cell_size"],data["cell_size"]+c*data["cell_size"],r*data["cell_size"]+data["cell_size"],fill="blue")
            elif grid[r][c]==SHIP_CLICKED:
                canvas.create_rectangle(c*data["cell_size"],r*data["cell_size"],data["cell_size"]+c*data["cell_size"],r*data["cell_size"]+data["cell_size"],fill="red")
            elif grid[r][c]==EMPTY_CLICKED:
                canvas.create_rectangle(c*data["cell_size"],r*data["cell_size"],data["cell_size"]+c*data["cell_size"],r*data["cell_size"]+data["cell_size"],fill="white")
            else:
                canvas.create_rectangle(c*data["cell_size"],r*data["cell_size"],data["cell_size"]+c*data["cell_size"],r*data["cell_size"]+data["cell_size"],fill="blue")
    return

### WEEK 2 ###

'''
isVertical(ship)
Parameters: 2D list of ints
Returns: bool
'''
def isVertical(ship):
    r=0
    if ship[r][1]==ship[r+1][1]==ship[r+2][1]:
        ship.sort()
        if ship[r+1][0]-ship[r][0]==1 and ship[r+2][0]-ship[r+1][0]==1:
            return True
    return False
    


'''
isHorizontal(ship)
Parameters: 2D list of ints
Returns: bool
'''
def isHorizontal(ship):
    r=0
    if ship[r][0]==ship[r+1][0]==ship[r+2][0]:
        ship.sort()
        if ship[r+1][1]-ship[r][1]==1 and ship[r+2][1]-ship[r+1][1]==1:
            return True
    return False
    return


'''
getClickedCell(data, event)
Parameters: dict mapping strs to values ; mouse event object
Returns: list of ints
'''
def getClickedCell(data, event):
    cell=data["cell_size"]
    data1=[int(event.y/cell),int(event.x/cell)]
    return data1
'''
drawShip(data, canvas, ship)
Parameters: dict mapping strs to values ; Tkinter canvas; 2D list of ints
Returns: None
'''
def drawShip(data, canvas, ship):
    for i in ship:
        r=i[0]
        c=i[1]
        canvas.create_rectangle(c*data["cell_size"],r*data["cell_size"],data["cell_size"]+c*data["cell_size"],r*data["cell_size"]+data["cell_size"],fill="white")
    return


'''
shipIsValid(grid, ship)
Parameters: 2D list of ints ; 2D list of ints
Returns: bool
'''
def shipIsValid(grid, ship):
    if len(ship)==3 and checkShip(grid,ship)==True and (isVertical(ship)==True or isHorizontal(ship)==True):
        return True
    return False


'''
placeShip(data)
Parameters: dict mapping strs to values
Returns: None
'''
def placeShip(data):
    g=data["user_board"]
    if shipIsValid(g, data["temp_ship"]):
        for i in data["temp_ship"]:
            g[i[0]][i[1]]=SHIP_UNCLICKED
        data["user_ships"]=data["user_ships"]+1
    else:
        print("Ship is not Valid")
    data["temp_ship"]=[]
    return


'''
clickUserBoard(data, row, col)
Parameters: dict mapping strs to values ; int ; int
Returns: None
'''
def clickUserBoard(data, row, col):
    g=data["user_board"]
    if [row,col] in g or data["user_ships"]==5:
        return
    data["temp_ship"].append([row,col])
    if len(data["temp_ship"])==3:
        placeShip(data)
    if data["user_ships"]==5:
        print("You can start the game")
    return


### WEEK 3 ###

'''
updateBoard(data, board, row, col, player)
Parameters: dict mapping strs to values ; 2D list of ints ; int ; int ; str
Returns: None
'''
def updateBoard(data, board, row, col, player):
    if board[row][col]==SHIP_UNCLICKED:
        board[row][col]=SHIP_CLICKED
    else:
        board[row][col]==EMPTY_UNCLICKED
        board[row][col]=EMPTY_CLICKED
    if isGameOver(board)==True:
        data["winner"]=player
    return


'''
runGameTurn(data, row, col)
Parameters: dict mapping strs to values ; int ; int
Returns: None
'''
def runGameTurn(data, row, col):
    computer=data["computer_board"]
    user=data["user_board"]
    if computer[row][col]== SHIP_CLICKED or computer[row][col]== EMPTY_CLICKED:
        return
    else:
        updateBoard(data,computer,row,col,"user")
    row,col=getComputerGuess(user)
    updateBoard(data,user,row,col,"comp")    
    return


'''
getComputerGuess(board)
Parameters: 2D list of ints
Returns: list of ints
'''
def getComputerGuess(board):
    computer=0
    while computer!=1:
        r=random.randint(0,9)
        c=random.randint(0,9)
        if board[r][c]==SHIP_UNCLICKED or board[r][c]==EMPTY_UNCLICKED:
            return[r,c]
    return


'''
isGameOver(board)
Parameters: 2D list of ints
Returns: bool
'''
def isGameOver(board):
    for i in range (len(board)):
        for j in range (len(board)):
            if board[i][j]==SHIP_UNCLICKED:
                return False
    return True


'''
drawGameOver(data, canvas)
Parameters: dict mapping strs to values ; Tkinter canvas
Returns: None
'''
def drawGameOver(data, canvas):
    if data["winner"]=="user":
        canvas.create_text(300, 50, text="you won the game", fill="black", font=('Helvetica 15 bold'))
    elif data["winner"]=="comp":
        canvas.create_text(300, 50, text="you lose the game", fill="black", font=('Helvetica 15 bold'))
    return


### SIMULATION FRAMEWORK ###

from tkinter import *

def updateView(data, userCanvas, compCanvas):
    userCanvas.delete(ALL)
    compCanvas.delete(ALL)
    makeView(data, userCanvas, compCanvas)
    userCanvas.update()
    compCanvas.update()

def keyEventHandler(data, userCanvas, compCanvas, event):
    keyPressed(data, event)
    updateView(data, userCanvas, compCanvas)

def mouseEventHandler(data, userCanvas, compCanvas, event, board):
    mousePressed(data, event, board)
    updateView(data, userCanvas, compCanvas)

def runSimulation(w, h):
    data = { }
    makeModel(data)

    root = Tk()
    root.resizable(width=False, height=False) # prevents resizing window

    # We need two canvases - one for the user, one for the computer
    Label(root, text = "USER BOARD - click cells to place ships on your board.").pack()
    userCanvas = Canvas(root, width=w, height=h)
    userCanvas.configure(bd=0, highlightthickness=0)
    userCanvas.pack()

    compWindow = Toplevel(root)
    compWindow.resizable(width=False, height=False) # prevents resizing window
    Label(compWindow, text = "COMPUTER BOARD - click to make guesses. The computer will guess on your board.").pack()
    compCanvas = Canvas(compWindow, width=w, height=h)
    compCanvas.configure(bd=0, highlightthickness=0)
    compCanvas.pack()

    makeView(data, userCanvas, compCanvas)

    root.bind("<Key>", lambda event : keyEventHandler(data, userCanvas, compCanvas, event))
    compWindow.bind("<Key>", lambda event : keyEventHandler(data, userCanvas, compCanvas, event))
    userCanvas.bind("<Button-1>", lambda event : mouseEventHandler(data, userCanvas, compCanvas, event, "user"))
    compCanvas.bind("<Button-1>", lambda event : mouseEventHandler(data, userCanvas, compCanvas, event, "comp"))

    updateView(data, userCanvas, compCanvas)

    root.mainloop()


### RUN CODE ###

# This code runs the test cases to check your work
if __name__ == "__main__":

    ## Finally, run the simulation to test it manually ##
    runSimulation(500, 500)
    test.testDrawGameOver()