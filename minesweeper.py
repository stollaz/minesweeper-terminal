# ╔ ╗ ╚ ╝ ╠ ╣ ╬ ═ ║ ╦ ╩
# ⬤

import re
import time
import random
import sys
sys.setrecursionlimit(1500) # Increase recursion limit so that clearing an area of the board is less likely to cause a stack overflow

import os
def cls(): # Function to clear the board regardless of the OS
    os.system('cls' if os.name=='nt' else 'clear')

WIDTH = 10 # Global variables for board stats
HEIGHT = 10
MINECOUNT = 2*max(WIDTH,HEIGHT)

LETTERS = [] # Stores the set of valid letters used when selecting a cell
NUMBERS = [] # * for numbers

# Class to store possible colours and text styles
class colours:
    ResetAll = "\033[0m"

    Bold       = "\033[1m"
    Dim        = "\033[2m"
    Underlined = "\033[4m"
    Blink      = "\033[5m"
    Reverse    = "\033[7m"
    Hidden     = "\033[8m"

    ResetBold       = "\033[21m"
    ResetDim        = "\033[22m"
    ResetUnderlined = "\033[24m"
    ResetBlink      = "\033[25m"
    ResetReverse    = "\033[27m"
    ResetHidden     = "\033[28m"

    Default      = "\033[39m"
    Black        = "\033[30m"
    Red          = "\033[31m"
    Green        = "\033[32m"
    Yellow       = "\033[33m"
    Blue         = "\033[34m"
    Magenta      = "\033[35m"
    Cyan         = "\033[36m"
    LightGray    = "\033[37m"
    DarkGray     = "\033[90m"
    LightRed     = "\033[91m"
    LightGreen   = "\033[92m"
    LightYellow  = "\033[93m"
    LightBlue    = "\033[94m"
    LightMagenta = "\033[95m"
    LightCyan    = "\033[96m"
    White        = "\033[97m"

    BackgroundDefault      = "\033[49m"
    BackgroundBlack        = "\033[40m"
    BackgroundRed          = "\033[41m"
    BackgroundGreen        = "\033[42m"
    BackgroundYellow       = "\033[43m"
    BackgroundBlue         = "\033[44m"
    BackgroundMagenta      = "\033[45m"
    BackgroundCyan         = "\033[46m"
    BackgroundLightGray    = "\033[47m"
    BackgroundDarkGray     = "\033[100m"
    BackgroundLightRed     = "\033[101m"
    BackgroundLightGreen   = "\033[102m"
    BackgroundLightYellow  = "\033[103m"
    BackgroundLightBlue    = "\033[104m"
    BackgroundLightMagenta = "\033[105m"
    BackgroundLightCyan    = "\033[106m"
    BackgroundWhite        = "\033[107m"

class Cell: # Stores the state of a cell
    types = ["mine","safe"]
    isFlagged = False # Stores if the cell is marked with a flag
    isVisible = False # Stores if the cell has been revealed or is still hidden
    isExploded = False # Stores whether the cell has exploded
    adjacentCount = -1 # Stores how many bombs are adjacent to the current cell
    type = "" # Stores the type of the cell

    def __init__(self): # Initialisation function
        # x = random.randint(1,mineCOUNT) # Old code to randomise mines - this is now done differently
        # if x < 3: self.type = "mine"
        # else: self.type = "safe"
        self.type = "safe" # Simply defaults the cell to a safe cell

    # def pickCellType():
    #     x = random.randint(1,10)
    #     if x < 2: return "mine"
    #     else: return "safe"

    def display(self): # Function to choose what symbol to use to display the current cell
        if self.isVisible: # If cell is marked as visible
            if self.type == "mine": return MINE 
            elif self.type == "safe": # If the cell is safe...
                if self.adjacentCount == 0: return SAFE # IF cell has no adjacent mines, display the default safe cell icon
                else: return colours.LightBlue + str(self.adjacentCount) + colours.White # Otherwise print the number of adjacent bombs
        elif self.isFlagged: # If the cell is flagged
            return FLAG
        else: # Otherwise return the default unknown cell icon
            return UNKNOWN

    def flag(self): # Procedure to toggle the state of the flagged variable
        self.isFlagged = not self.isFlagged
        # if self.type == "mine" and self.isFlagged: self.isExploded = True

    def reveal(self): # Procedure to reveal the current cell
        self.isVisible = True
        if self.type == "mine" and self.isVisible: self.isExploded = True # If the cell is a bomb and has been revealed, mark it as exploded


def calculateAdjacentCount(i,j): # Function to calculate the number of mines adjacent to a given cell
    count = 0
    for a in range (-1,2):
        for b in range (-1,2):
            if (i+a < HEIGHT and b+j < WIDTH and i+a >= 0 and b+j >= 0):
                if board[i+a][j+b].type == "mine": count += 1
    return count

board = [] # Initialise board as array

def rerollBoard(): # Procedure to reroll the board, mainly used at the start when the player makes the first move, as the first cell must reveal surrounding cells to be useful
    global board
    for i in range(HEIGHT):
        for j in range(WIDTH):
            board[i][j] = "" # Reset board but keep dimensions (remove cell data)
    initBoard()

# Unused backup function
# def initBoardBACKUP():
#     global board
#     mines = 0
#     #board = []
#     for i in range(HEIGHT):
#         row = []
#         for j in range (WIDTH):
#             c = "" #Cell()
#             row.append(c)
#         board.append(row)

#     for i in range(HEIGHT):
#         row = []
#         for j in range (WIDTH):
#             c = Cell()
#             if c.type == "mine": mines += 1
#             board[i][j] = c

#     for i in range(HEIGHT):
#         for j in range (WIDTH):
#             board[i][j].adjacentCount = calculateAdjacentCount(i,j)

def initBoard(): # Procedure to initialise the board with bombs
    global board # Make changes to the gloabl board variable in this procedure
    mines = 0
    #board = []
    for i in range(HEIGHT): # Loops to create board structure
        row = []
        for j in range (WIDTH):
            c = "" #Cell()
            row.append(c)
        board.append(row)

    for i in range(HEIGHT): # Loops to initialise basic Cell objects in each cell
        row = []
        for j in range (WIDTH):
            c = Cell()
            # if c.type == "mine": mines += 1
            board[i][j] = c

    while mines != MINECOUNT: # Randomly create mines at random cell locations
        i = random.randint(0,HEIGHT-1)
        j = random.randint(0,HEIGHT-1)
        if board[i][j].type != "mine": # Ensure that cells are not selected mutliple times 
            board[i][j].type = "mine"
            #print("mine at ({0},{1})".format(i,j))
            mines += 1

    #print("{0} mines generated - countmines() = {1}".format(mines, countmines()))
    assert mines == countmines() # Assert that the number of mines created matches the number of mines found by the countmines() function

    for i in range(HEIGHT): # Loops to calculate adjacent mine count in each cell and store it
        for j in range (WIDTH):
            board[i][j].adjacentCount = calculateAdjacentCount(i,j)

    global NUMBERS, LETTERS # Modify global NUMBERS and LETTERS arrays
    NUMBERS = []
    LETTERS = []
    for i in range(WIDTH): NUMBERS.append(str(i)) # Store set of valid numbers
    for i in range (HEIGHT): LETTERS.append(str(chr(i+65))) # Store set of valid letters
    #print("NUMBERS = {0}\nLETTERS = {1}".format(NUMBERS, LETTERS))

# Define symbols for different cell types
FLAG = colours.Green + "■" + colours.White
MINE = colours.Red + "■" + colours.White
SAFE = colours.LightBlue + "□" + colours.White
UNKNOWN = colours.LightGray + "■" + colours.White
DEBUG = colours.Yellow + "□" + colours.White

def printBoard(): # Procedure to print the board out
    print("\n   ", end = '')
    for i in range(WIDTH): # Write numbers at the top corresponding to the column
        print("{0}".format(str(i)).ljust(6), end = '') # Ensure spacing remains consistent with double digit numbers by using .ljust() to do padding
    #print("   0     1     2     3     4     5     6     7     8     9")
    print("\n╔", end = '')
    for i in range(WIDTH): # Draw top edge of board
        if i != WIDTH-1: print("═════╦", end = '')
        else: print("═════╗", end = '')
    print()

    #print("\n╔═════╦═════╦═════╦═════╦═════╦═════╦═════╦═════╦═════╦═════╗")
    for y in range(HEIGHT): # Draw middle lines of board and draw symbols within
        for c in range(WIDTH): print("║ ", board[y][c].display() , " ", end = '')
        print("║ {0}".format(chr(y+65))) # Write letters to the side of the board corresponding the row
        if y != HEIGHT-1: # If not last row
            #print("╠═════╬═════╬═════╬═════╬═════╬═════╬═════╬═════╬═════╬═════╣")
            print("╠", end = '') # Draw between row dividers
            for i in range(WIDTH):
                if i != WIDTH-1: print("═════╬", end = '')
                else: print("═════╣", end = '')
            print("\n", end = '')
        else: # Otherwise if last row
            print("╚", end = '')
            for i in range(WIDTH): # Draw bottom edge of board
                if i != WIDTH-1: print("═════╩", end = '')
                else: print("═════╝", end = '')
            #print("╚═════╩═════╩═════╩═════╩═════╩═════╩═════╩═════╩═════╩═════╝\n")
    print("\n\n", end = '')
    return

def checkEnd(mineCount, start_time): # Function to check if the game has ended - takes in the number of mines as a parameter
    end_time = time.time()
    total_time = round(end_time - start_time)
    revealedmineCount = 0 # Keep track of how many mines are revealed
    flaggedmineCount = 0 # Keep track of how many mines are correctly flagged
    flaggedSafeCount = 0 # Keep track of how many safe cells are incorrectly flagged
    for i in range(HEIGHT): # Loop and increment relevant variables
        for j in range(WIDTH):
            if board[i][j].type == "mine" and board[i][j].isVisible: revealedmineCount += 1
            elif board[i][j].type == "mine" and board[i][j].isFlagged: flaggedmineCount += 1
            elif board[i][j].type == "safe" and board[i][j].isFlagged: flaggedSafeCount += 1

    if flaggedSafeCount > 0: # If some safe cells are incorrectly flagged, the game is not over, as you cannot have any safe cells marked to win
        return False
    elif revealedmineCount > 0: # If any mines have been revealed, the game is over and you lose
        print("{0}Mine Detonated. Game Over. {1}".format(colours.Bold + colours.Red, colours.White + colours.ResetBold))
        return True
    elif flaggedmineCount == mineCount: # Otherwise if the number of flagged mines equals the number of mines on the board, all mines are defused and you win
        print("{0}All Mines Defused! You Win! Game Time: {2} seconds.{1}".format(colours.Bold + colours.Green, colours.White + colours.ResetBold, total_time))
        return True
    else: return False

# Function to validate the action being performed
def validateAction(t):
    actions = ["flag","clear","reveal_all","hide_all","help"] # Array of possible actions
    if t.lower() in actions: return True # If the attempted action exists in the array, return True
    else: return False

# Function to take in the cell data (e.g. F5, 0A, 15J) and split it into a letter part and a number part
def getParts(c):
    letter_part = ""
    number_part = -1

    match = re.match(r"([A-Z]+)([0-9]+)|([0-9]+)([A-Z]+)", c, re.I) # Regex to match to the input
    items = ""
    if match: # If it matches, split string based on what it matches
        items = match.groups()
    #print(items)
    for i in items:
        if i != None:
            if re.match(r"([A-Z]+)",i,re.I): letter_part = i.upper() # Find the part where it is just the letters and store it in upper case
            if re.match(r"([0-9]+)",i,re.I): number_part = int(i) # Find the purely numerical part and store it as an integer

    return letter_part,number_part # Return both - note that this function will correctly treat 5F and F5 as the same cell

# Function to validate that the entered cell is real
def validateCell(c):
    letters = LETTERS
    numbers = NUMBERS

    letter_part = ""
    number_part = -1

    letter_part, number_part = getParts(c) # Get parts of the cell input

    ret = ""

    if letter_part in letters and str(number_part) in numbers: # If the cell is fully valid and is in the correct ranges defined by LETTERS and NUMBERS
        ret = letter_part + str(number_part) # Prepare to return the cell data info as a string
    else: return c, False # Otherwise it is invalid and return as such
    y = int(ord(letter_part.upper()) - 65)
    col = int(number_part)
    if board[y][col].isVisible: return ret, False # If the cell entered is already revealed, nothing can be done to it, so it is an invalid cell
    else: return ret, True 

# Secondary recursive procedure to reveal an area around a cell, and keep doing so until an area is revealed bounded by either cells with adjacent mines, or the edges of the board
def revealArea2(a,b):
    y = a
    col = b
    try: # Catch any random errors
        current = board[y][col]

        if (y < 0 or col < 0): raise Exception('Out of Bounds') # If the cell is out of bounds, raise an exception and skip this cell

        if current.type == "mine": 0 # Do nothing if the current cell is a mine
        elif current.type == "safe" and current.isVisible: 0 # Do nothing if the current cell is both safe and visible (to avoid infinitely looping as it tries the same cell repeatedly)
        elif current.type == "safe" and not current.isVisible: # Otherwise if the cell is safe and not revealed yet
            current.reveal() # Reveal it
            if current.adjacentCount == 0: # If it has no adjacent bombs, recursively check the surrounding cells in the same way
                for i in range (-1,2):
                    for j in range(-1,2):
                        if(0<=y+i<WIDTH and 0<=col+j<HEIGHT): revealArea2(y+i,col+j) # And only do this if it is in the valid range
            # note that if the cell does have adjacent mines we stop checking adjacent cells, so that these cells with adjacent mines act as the border

    except: 0

# Primary procedure to reveal an area around a cell, which starts the recursive part above
def revealArea(y, col, area=2):
    if y == str(y) or y == chr(y): y = int(ord(y) - 65)
    current = board[y][col]

    if current.type == "mine": current.reveal() # If the current cell is a mine, reveal it
    elif current.type == "safe" and current.isVisible: 0 # Do nothing if the current cell is already revealed (though this should not be necessary as it should be caught by other functions)
    elif current.type == "safe" and not current.isVisible: # Otherwise if the cell is safe and not visible yet
        if current.adjacentCount != 0: current.reveal() # Reveal the cell if it does not have adjacent mines 
        else: # Otherwise it has no adjacent mines, so start recursively checking the cells adjacent to it
            current.reveal()
            for i in range (-1,2):
                for j in range(-1,2):
                    revealArea2(y+i,col+j) # Call secondary recursive function defined above

# Procedure to perform an action specified by t on the cell [y,col]
def doAction(y, col, t):
    y = int(ord(y) - 65)
    # col = int(c[1])
    if t == "flag": board[y][col].flag() # If action is flag, mark the cell as flagged
    elif t == "reveal_all": # Debug option to reveal the whole board, for visualisation (side effect: this ends the game, so cannot really be used to cheat)
        for i in range(HEIGHT):
            for j in range(WIDTH): board[i][j].isVisible = True # Marks all cells as visible
    elif t == "hide_all":  # Debug option to reverse the above, and hide all cells on the board (side effect: this can never be used)
        for i in range(HEIGHT):
            for j in range(WIDTH): board[i][j].isVisible = False # Marks all cells as no longer visible
    elif t == "clear": # Otherwise we are clearing a cell
        #board[y][col].reveal()
        revealArea(y, col) # Start the potentially recursive procedure on that cell

# Function to parse a complex action, which is an actiona and a cell on one line
def parseComplexAction(s):
    separators = [':',',','.',' ','|'] # Define valid separators
    actions = ["flag","clear","reveal_all","hide_all","f","c","help"] # Define valid actions, with some shorthands such as "f" for "flag" and "c" for "clear"

    if s == "help" or s == "reveal_all" or s == "hide_all": return True,0,0,s # If the action is help or a debug option, let it be valid

    separator = ''
    action = ""
    cell = ""

    for sep in separators: # Loop through separators to find the valid one
        if s.find(sep) != -1: separator = sep
    if separator == '': # If no valid separator is found, display error
        print("Invalid separator. - use a valid separator to separate an action from a cell.\nValid separators are as follows: {0}".format(separators))
        return False,0,0,0

    splittext = s.split(str(separator)) # Split text around separator
    if splittext[0].lower() in actions: action = splittext[0].lower() # If the first part is the action store it as such, otherwise check 2nd part
    elif splittext[1].lower() in actions: action = splittext[1].lower()
    else: # If no Valid action found, display error
        print("Invalid action. Try again")
        return False,0,0,0
    if action == "f": action = "flag" # Convert shorthand actions to full versions
    if action == "c": action = "clear"

    if validateCell(splittext[1])[1]: cell = validateCell(splittext[1])[0] # If the 2nd part is the cell, store it as such, otherwise check 1st part
    elif validateCell(splittext[0])[1]: cell = validateCell(splittext[0])[0]
    else:
        print("Invalid cell. Try again")
        return False,0,0,0

    y, col = getParts(cell) # Get parts from cell data

    #doAction(y, col, action)
    return True, y, col, action

# Function to count the mines on the board (largely unecessary, as it should always equal the global MINECOUNT)
def countmines():
    count = 0
    for i in range(HEIGHT):
        for j in range(WIDTH):
            if board[i][j].type == "mine": count += 1
    return count

# Function to count the number of flags on the board
def countFlags():
    count = 0
    for i in range(HEIGHT):
        for j in range(WIDTH):
            if board[i][j].isFlagged: count += 1
    return count

# Procedure to allow setting up a game with custom size and number of mines
def setupCustomGame():
    cls()
    print("Custom Game Setup\n")
    w = -1
    h = -1
    b = -1
    
    while not 2 < w <= 26:
        try:
            w = int(input("Enter WIDTH of board: "))
            if w > 26: print("Invalid Input - Number Too Large (Maximum size is 26). Try Again.")
            elif w < 3: print("Invalid Input - Number Too Small (Minimum size is 3). Try Again.")
        except:
            print("Invalid Input. Try Again.")
            w = -1
    
    print("Width set to {0}\n".format(w))

    while not 2 < h <= 26:
        try:
            h = int(input("Enter HEIGHT of board: "))
            if h > 26: print("Invalid Input - Number Too Large (Maximum size is 26). Try Again.")
            elif h < 3: print("Invalid Input - Number Too Small (Minimum size is 3). Try Again.")
        except:
            print("Invalid Input. Try Again.")
            h = -1
    
    print("Height set to {0}\n".format(h))

    while not 0 < b < w*h: # Number of bombs cannot equal or exceed number of cells available on the board, otherwise it is unplayable
        try:
            b = int(input("Enter NUMBER OF MINES on board: "))
            if b >= w*h: print("Invalid Input - Number Too Large. Try Again.")
            elif b < 0: print("Invalid Input - Number Too Small. Try Again.")
        except:
            print("Invalid Input. Try Again.")
            b = -1
    
    print("Mines set to {0}\n".format(b))

    return w,h,b

# Start menu to allow board configuration
def menu():
    global WIDTH, HEIGHT, MINECOUNT
    cls()
    choices = ["1","2","3","4","5","9","0"]
    print("==WELCOME TO MINESWEEPER==")
    print("\nNOTE: It is recommended you make your console window as large as possible before playing, to avoid graphical errors\nIf the above line got cut off mid-way, you may need to make your text size smaller\n")
    choice = ""
    while choice not in choices:
        print("\nSelect Game Type:\n1. Default Easy (8x8 grid, 10 mines)\n2. Default Medium (10x10 grid, 20 mines)\n3. Default Hard (12x12 grid, 24 mines)\n4. Default Insane (20x20 grid, 50 mines)\n5. Custom Game\n9. Exit\n0. Help")
        choice = input("\n> ")
        if choice == "1":
            WIDTH = 8
            HEIGHT = 8
            MINECOUNT = 10
        elif choice == "2":
            WIDTH = 10
            HEIGHT = 10
            MINECOUNT = 20
        elif choice == "3":
            WIDTH = 12
            HEIGHT = 12
            MINECOUNT = 24
        elif choice == "4":
            WIDTH = 20
            HEIGHT = 20
            MINECOUNT = 50
        elif choice == "5":
            WIDTH, HEIGHT, MINECOUNT = setupCustomGame()
        elif choice == "9":
            exit()
        elif choice == "0":
            choice = -1
            cls()
            print("\nThe goal of minesweeper is to clear the board of all mines.\nThe numbers on revealed (blue) cells indicates the number of adjacent mines.\nUnrevealed cells are indicated in gray.\nThe game is won by marking all mines with a flag, as well having no non-mines flagged.\nClearing a safe cell reveals information, while clearing a mine is game over!\n")
            print("When the game begins, actions are controlled by typing in the terminal.\nYou must type either a valid action followed by a cell reference, or a cell reference followed by an action.\nValid actions are currently: flag, clear, help\nValid cells are either the letter for the row followed by the number for the column, or vice versa.\nYou can separate the action and the cell with either a space, or one of the following characters: ',', '.', ':', '|'\n\nGood Luck!\n")
            input("Press enter to continue")
            cls()
        else: print("Invalid choice. Try again.")

# Main function to play game 
def play():
    menu()
    cls()
    initBoard()
    printBoard()
    start_time = time.time()
    end = False
    first = True
    while not end: # Loop until game over
        print("MINESWEEPER :: {0} mines -- {1} flags planted".format(countmines(), countFlags())) # Display how many mines there are, and how many flags are planted - note the two being equal does not mean game over
        
        # valid = False
        # while not valid: # Keep asking for a cell until a valid one is entered
        #     c = input("Enter cell coordinates (e.g. F4) to play\n> ")
        #     c, valid = validateCell(c)
        #     if not valid: print("Invalid - try again")
            
        # valid = False
        # while not valid: # Keep asking for an action until a valid one is entered
        #     t = input("Enter action to perform on cell {0}:\nActions: Flag, Clear, Help\n> ".format(c))
        #     valid = validateAction(t)
        #     if not valid: print("Invalid action - try again")
        #     if t.lower() == "help": # Help text
        #         print("\nFlag:  Add or remove a flag on a given cell, to mark it as being a mine\nClear: Clear a cell - if the cell is safe, information will be revealed.\n       If the cell is a mine, the game is over!\nIf you made a mistake, choose Flag, as this can be easily removed without penalty\n")
        #         valid = False

        # y, col = getParts(c)

        valid = False
        while not valid:
            p = input("Enter command (type 'help' for more info)\n> ")
            valid,y,col,t = parseComplexAction(p)
            if t == "help":
                print("\nOn one line, type an action and a cell to perform the action upon.\nValid actions are: clear, flag, help\nA valid cell is a letter for the row and a number for the column, with no spaces between\nSome examples of valid commands include: 'clear D5', 'H7 flag','clear:a0', etc.\n\n")
                valid = False

        if first: # If this is the first go, ensure that the entered cell is safe and has no adjacent mines, to allow for the effect of clearing a large area as seen in normal minesweeper games
            y_ = int(ord(y) - 65)
            #col = int(c[1])
            done = False
            while not done:
                if board[y_][col].type == "mine" or board[y_][col].adjacentCount > 0: # If the entered cell is a mine or has adjacent bombs, reroll the board
                    rerollBoard() 
                else: done = True
            first = False
        
        print("y={0},col={1}".format(y,col))
        doAction(y, col,t) # Perform the action
        
        cls() # Clear the board and print it again, to avoid cluttering the terminal
        printBoard()
        end = checkEnd(countmines(), start_time) # Check for the end

play()