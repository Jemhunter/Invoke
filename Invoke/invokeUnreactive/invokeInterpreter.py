#all the characters that are considered valid
validChars = ["Q", "W", "E", "R", "I", ">", "<", "V", "^"]


def convertToValid (fileInput):
    '''Convert file data to array of valid characters only'''
    #convert to upper case
    fileInput = fileInput.upper()
    #create array to hold data in
    data = []
    #split into lines
    lines = fileInput.split("\n")
    #to store the max length
    maxLength = -1

    #iterate lines
    for line in lines:
        #if this line is longer than the current maximum
        if len(line) > maxLength:
            #update the maximum
            maxLength = len(line)

    #iterate lines
    for line in lines:
        #create list to hold the data for this line
        lineData = []
        #iteracte characters
        for char in line:
            #if it is a valid character
            if char in validChars:
                #add it to the list
                lineData.append(char)
            else:
                #add a blank
                lineData.append("")

        #iterate for extra items that are needed
        for i in range(maxLength - len(lineData)):
            #add blanks to fill to square
            lineData.append("")

        #add line to data
        data.append(lineData)

    #return the array
    return data


def getFile ():
    '''Get all the data from the file given'''
    #get the path from the user
    path = input("Enter path to Invoke file:")
    #initialize data as none - if no file can be obtained it won't proceed
    fileData = None
    #check for correct extension
    if path.endswith(".inv"):
        try:
            #attempt to open and read the file
            invokeFile = open(path, "r")
            #store data in variable
            fileData = invokeFile.read()
            #close the file
            invokeFile.close()
        except:
            #if something went wrong the file wasn't found
            print("File not found or invalid, please ensure you typed the path correctly")
    else:
        #if it wasn't a .inv file
        print("The file must be in the format filename.inv")

    #return the data
    return fileData


def whichCommand (parts):
    '''Determine which command is being executed from the 3 parts'''
    #list of valid parts
    validParts = ["Q", "W", "E"]

    #if there aren't 3
    if len(parts) < 3:
        #return no command
        return -1

    #if all are valid
    if parts[0] in validParts and parts[1] in validParts and parts[2] in validParts:
        #1st is Q
        if parts[0] == "Q":
            #2nd is Q
            if parts[1] == "Q":
                #3rd is Q
                if parts[2] == "Q":
                    #QQQ
                    return 6
                #3rd is W
                elif parts[2] == "W":
                    #QQW
                    return 3
                #3rd is E
                else:
                    #QQE
                    return 2
            #2nd is W
            elif parts[1] == "W":
                #3rd is Q
                if parts[2] == "Q":
                    #QQW
                    return 3
                #3rd is W
                elif parts[2] == "W":
                    #WWQ
                    return 1
                #3rd is E
                else:
                    #QWE
                    return 9
            #2nd is E
            else:
                #3rd is Q
                if parts[2] == "Q":
                    #QQE
                    return 2
                #3rd is W
                elif parts[2] == "W":
                    #QWE
                    return 9
                #3rd is E
                else:
                    #EEQ
                    return 5
        #1st is W
        elif parts[0] == "W":
            #2nd is Q
            if parts[1] == "Q":
                #3rd is Q
                if parts[2] == "Q":
                    #QQW
                    return 3
                #3rd is W
                elif parts[2] == "W":
                    #WWQ
                    return 1
                #3rd is E
                else:
                    #QWE
                    return 9
            #2nd is W
            elif parts[1] == "W":
                #3rd is Q
                if parts[2] == "Q":
                    #WWQ
                    return 1
                #3rd is W
                elif parts[2] == "W":
                    #WWW
                    return 7
                #3rd is E
                else:
                    #WWE
                    return 0
            #2nd is E
            else:
                #3rd is Q
                if parts[2] == "Q":
                    #QWE
                    return 9
                #3rd is W
                elif parts[2] == "W":
                    #WWE
                    return 0
                #3rd is E
                else:
                    #EEW
                    return 4
        #1st is E
        else:
            #2nd is Q
            if parts[1] == "Q":
                #3rd is Q
                if parts[2] == "Q":
                    #QQE
                    return 2
                #3rd is W
                elif parts[2] == "W":
                    #QWE
                    return 9
                #3rd is E
                else:
                    #EEQ
                    return 5
            #2nd is W
            elif parts[1] == "W":
                #3rd is Q
                if parts[2] == "Q":
                    #QWE
                    return 9
                #3rd is W
                elif parts[2] == "W":
                    #WWE
                    return 0
                #3rd is E
                else:
                    #EEW
                    return 4
            #2nd is E
            else:
                #3rd is Q
                if parts[2] == "Q":
                    #EEQ
                    return 5
                #3rd is W
                elif parts[2] == "W":
                    #EEW
                    return 4
                #3rd is E
                else:
                    #EEE
                    return 8

    #if no other command was found
    return -1


def addMana (pots, amount, addPosition):
    '''Add mana to a specific pot - with overflow'''
    #if addPosition is within pots
    if addPosition < len(pots) and addPosition > -1:
        #get the current pot amount
        currentPotAmount = pots[addPosition]

        #if there will not be overflow
        if currentPotAmount + amount <= 255:
            #add to the pot
            pots[addPosition] = pots[addPosition] + amount
        else:
            #fill pot - rest spills over
            pots[addPosition] = 255
    #return the updated pots      
    return pots


def outputChar(number):
    '''Print a single character with no return character'''
    print(chr(number), end="")


def outputNumber(number, needLine):
    '''Print a number with a leading new line if needed'''
    #if a new line is needed
    if needLine:
        #print the number with new line
        print("\n" + str(number))
    else:
        #print just the number
        print(number)


def getInput ():
    '''Get user input'''
    #get input
    inp = input(">")
    try:
        #attempt convert to int
        inp = int(inp)
        #return number (if positive)
        if inp >=0:
            return inp
    except:
        #if it isn't a number
        #if it has a length of 1
        if len(inp) == 1:
            #return the unicode value for it (mod 256, so it is in ascii range)
            return (ord(inp) % 256)
    #if a number or single character was not entered
    return 0


def runProgram (code, debug):
    '''Run a program, code is the program code and debug is if the debug prints are on'''
    #create mana pots
    manaPots = [0]
    #create empty phial
    manaPhial = 0
    #the currently selected pot
    currentPot = 0
    #the parts of a command currently in use
    parts = ["", "", ""]
    #where to replace the part next
    partToReplace = 0
    #if the program is running
    running = True
    #current instruction pointers
    pointerY = 0
    pointerX = 0
    #how to change the pointers after each instruction (x,y)
    pointerChange = [1, 0]
    #if a new line is needed (has a character been printed most recently)
    needLine = False

    #valid code parts
    validParts = ["Q", "W", "E"]
    #single command characters
    otherCommands = [">", "<", "V", "^", "I", "R"]

    #until the program stops
    while running:
        #wrap the pointer if it goes off the right side
        if pointerX >= len(code[0]):
            pointerX = 0
        #wrap the pointer if it goes off the left side
        if pointerX < 0:
            pointerX = len(code[0]) - 1
        #wrap the pointer if it goes off the bottom
        if pointerY >= len(code):
            pointerY = 0
        #wrap the pointer if it goes off the top
        if pointerY < 0:
            pointerY = len(code) - 1

        #the amount the pointer is being boosted by (jumps)
        pointerBoost = [0,0]
        #the currently selected character/instruction
        currentChar = code[pointerY][pointerX]

        #if in debug mode
        if debug:
            #output the character
            print(currentChar)

        #if it is a command or code character
        if currentChar in validParts or currentChar in otherCommands:
            #if the character is the invoke command
            if currentChar == "I":
                #get which command the code makes up
                command = whichCommand(parts)
                #if debug is on
                if debug:
                    #print the command id
                    print(command)
                if command == 0:
                    #right 1 pot
                    #increase selected pot
                    currentPot = currentPot + 1
                    #if this exceeds where there are currently pots
                    if currentPot >= len(manaPots):
                        #add a new empty pot
                        manaPots.append(0)
                elif command == 1:
                    #left 1 pot
                    #move to the left
                    currentPot = currentPot - 1
                    #if at the left wall
                    if currentPot < 0:
                        #stay on first pot
                        currentPot = 0
                elif command == 2:
                    #add 1 to current pot
                    #call for 1 mana to be added to the current pot
                    manaPots = addMana(manaPots, 1, currentPot)
                elif command == 3:
                    #remove 1 from current pot
                    #if there is mana in the pot
                    if manaPots[currentPot] > 0:
                        #take 1 mana from the pot
                        manaPots[currentPot] = manaPots[currentPot] - 1
                elif command == 4:
                    #output value of current pot
                    #output the number
                    outputNumber(manaPots[currentPot], needLine)
                    #a new line is no longer needed
                    needLine = False
                elif command == 5:
                    #output character of current pot
                    #output character
                    outputChar(manaPots[currentPot])
                    #a new line is needed when a number is printed
                    needLine = True
                elif command == 6:
                    #Input and add to current pot
                    #get amount to add
                    toAdd = getInput()
                    #call for it to be added to the pot
                    manaPots = addMana(manaPots, toAdd, currentPot)
                elif command == 7:
                    #draw as much as possible to fill phial
                    #get the maximum amount that can be taken
                    maximum = 511 - manaPhial
                    #if the maximum is greater than or equal to the amount in the current pot
                    if maximum >= manaPots[currentPot]:
                        #take all into phial
                        manaPhial = manaPhial + manaPots[currentPot]
                        #set pot to empty
                        manaPots[currentPot] = 0
                    else:
                        #fill phial
                        manaPhial = 511
                        #remove maximum from current pot
                        manaPots[currentPot] = manaPots[currentPot] - maximum
                elif command == 8:
                    #pour all from phial into pot
                    #add the amount in the phial to the current pot
                    manaPots = addMana(manaPots, manaPhial, currentPot)
                    #empty phial
                    manaPhial = 0
                elif command == 9:
                    #stop
                    running = False
            elif currentChar == "R":
                #revoke - jump if empty pot
                #if the current pot is empty
                if manaPots[currentPot] == 0:
                    #move the pointer 1 further in it's current direction
                    pointerBoost[0] = pointerChange[0]
                    pointerBoost[1] = pointerChange[1]
            elif currentChar == ">":
                #switch to move right
                pointerChange = [1, 0]
            elif currentChar == "<":
                #switch to move left
                pointerChange = [-1, 0]
            elif currentChar == "V":
                #switch to move down
                pointerChange = [0, 1]
            elif currentChar == "^":
                #switch to move up
                pointerChange = [0, -1]
            elif currentChar in validParts:
                #it is Q,W or E
                #replace the next part to replace whith this character
                parts[partToReplace] = currentChar
                #move to replace on one
                partToReplace = partToReplace + 1
                #if it is beyond the end
                if partToReplace > 2:
                    #move back to start
                    partToReplace = 0

        #adjust instruction pointer
        pointerX = pointerX + pointerChange[0] + pointerBoost[0]
        pointerY = pointerY + pointerChange[1] + pointerBoost[1]

        #if debug is on
        if debug:
            #prtint the mana pots, the current pot position, the phial and current parts
            print(manaPots)
            print("Current:" + str(currentPot))
            print("Phial:" + str(manaPhial))
            print(parts)

    #if a line is needed
    if needLine:
        #print complete message with leading new line
        print("\nExecution Complete")
    else:
        #print complete message
        print("Execution Complete")


def execute(debug):
    '''Get the code and run it'''
    #get file data
    fileData = getFile()
    #if there was some data
    if fileData != None:
        #convert to valid
        data = convertToValid(fileData)
        #if there is code in y axis (at least 1 row)
        if len(data) > 0:
            #if there is code in x axis (at least 1 column)
            if len (data[0]) > 0:
                #run the program
                runProgram(data, debug)
            else:
                #no columns
                print("No code found")
        else:
            #no rows
            print("No code found")
        

#Main Program
#run the program
execute(False)
#hold the terminal open until enter is pressed
input()
