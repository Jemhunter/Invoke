import tkinter
import time
from tkinter import N, E, S, W, HORIZONTAL, END, LEFT, RIGHT, INSERT, BOTTOM, TOP, Y, X, BOTH, WORD
from tkinter import scrolledtext
import random
import ToolTips

class manaScroll (tkinter.Frame):
    '''Class to hold pots scroll window and manage numbers/sprites'''
    def __init__ (self, parent):
        '''Constructor'''
        #list of buttons - each one is a pot
        self.buttons = []

        #initialize the frame for this object
        tkinter.Frame.__init__(self, parent)
        #create canvas to hold scrolling frame
        self.canvas = tkinter.Canvas(parent, height=75, borderwidth=0)
        #create frame to hold buttons
        self.frame = tkinter.Frame(self.canvas)
        #create scroll bar
        self.scrollBar = tkinter.Scrollbar(parent, orient="horizontal", command=self.canvas.xview)
        #attach scroll bar to canvas
        self.canvas.configure(xscrollcommand=self.scrollBar.set)

        #place scroll bar and canvas
        self.scrollBar.grid(row=1, column=0, sticky=(N,E,S,W))
        self.canvas.grid(row=0, column=0, sticky=(N,E,S,W))
        #create a window to display the frame widget
        self.canvas.create_window((0,0), window = self.frame, anchor="nw", tags="self.frame")

        #bind reconfiguring size to call for configure
        self.frame.bind("<Configure>", self.onFrameConfigure)

        #get all pot images from files
        self.potImages = [tkinter.PhotoImage(file="resources/beakerEmpty.png"),
             tkinter.PhotoImage(file="resources/beakerLevel1.png"),
             tkinter.PhotoImage(file="resources/beakerLevel2.png"),
             tkinter.PhotoImage(file="resources/beakerLevel3.png"),
             tkinter.PhotoImage(file="resources/beakerLevel4.png"),
             tkinter.PhotoImage(file="resources/beakerLevel5.png")]

        #colour for active buttons
        self.buttonActive = "#f49fef"
        #add a starting pot
        self.addPot()
        #get default button colour
        self.buttonDefault =  self.buttons[0].cget("background")
        #activate first button
        self.buttons[0].configure(relief="sunken", bg=self.buttonActive)
        #set the first as selected
        self.selected = 0

    def addPot(self):
        '''Add a pot to the list'''
        #create a label string for the button
        label = str(len(self.buttons)) + " : 0"
        #create the button
        button  = tkinter.Button(self.frame,bd=5,disabledforeground="#000000",image=self.potImages[0],text=label,height=60,width=60,state="disabled",compound="bottom")
        #add to list of buttons
        self.buttons.append(button)
        #pack the button
        button.pack(side=LEFT)

    def onFrameConfigure(self, event):
        '''When the frame is resized - reconfigure the scroll area'''
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def changeSelected(self, toSelect):
        '''Change which pot is currently selected'''
        #if there is a selected pot and it is in range
        if self.selected > -1 and self.selected < len(self.buttons):
            #deselect that pot
            self.buttons[self.selected].config(relief="raised", bg=self.buttonDefault)

        #if to select exists
        if toSelect > -1 and toSelect < len(self.buttons):
            #set selected
            self.selected = toSelect
            #select that pot
            self.buttons[self.selected].configure(relief="sunken", bg=self.buttonActive)
            #get the position to move the scroll to
            pos = (toSelect - 3.5)/len(self.buttons)
            #if it is less than 0 set it to 0
            if pos < 0:
                pos = 0
            #scroll the canvas to focus on the selected pot
            self.canvas.xview_moveto(pos)
        else:
            #no selected pot
            self.selected = -1

    def changeValue(self, which, amount):
        '''Change the value of a specific pot. which - index of pot to change, amount - what to set it to'''
        #if the pot exists in the list of pots
        if which >= 0 and which < len(self.buttons):
            #create the label text
            labelText = str(which) + " : " + str(amount)
            #set the buttons text
            self.buttons[which].config(text=labelText)
            #set to correct sprite
            if amount == 0:
                self.buttons[which].config(image=self.potImages[0])
            elif amount <= 50:
                self.buttons[which].config(image=self.potImages[1])
            elif amount <= 100:
                self.buttons[which].config(image=self.potImages[2])
            elif amount <= 150:
                self.buttons[which].config(image=self.potImages[3])
            elif amount <= 200:
                self.buttons[which].config(image=self.potImages[4])
            else:
                self.buttons[which].config(image=self.potImages[5])

class codeGrid (tkinter.Frame):
    '''Grid object to hold all the code inside of'''
    def __init__ (self, parent, code):
        '''Constructor'''
        #create frame
        tkinter.Frame.__init__(self, parent)
        #create canvas to hold grid, that will scroll
        self.canvas = tkinter.Canvas(parent, borderwidth=0)
        #create frame to hold characters
        self.frame = tkinter.Frame(self.canvas, bg="#000000")
        #create scroll bars
        self.scrollBarH = tkinter.Scrollbar(parent, orient="horizontal", command=self.canvas.xview)
        self.scrollBarV = tkinter.Scrollbar(parent, orient="vertical", command=self.canvas.yview)
        self.canvas.configure(xscrollcommand=self.scrollBarH.set, yscrollcommand=self.scrollBarV.set)

        #locate items
        self.scrollBarH.grid(row=1, column=0, sticky=(N,E,S,W))
        self.scrollBarV.grid(row=0, column=1, sticky=(N,E,S,W))
        self.canvas.grid(row=0, column=0, sticky=(N,E,S,W))
        #create window to display frame
        self.canvas.create_window((0,0), window = self.frame, anchor="nw", tags="self.frame")

        #bind the window configure to recalculating the bounds
        self.frame.bind("<Configure>", self.onFrameConfigure)

        #nothing selected yet
        self.selectedX = -1
        self.selectedY = -1

        #2d array for each code element
        self.codeParts = []

        #iterate for rows
        for i in range(0, len(code)):
            #add row
            self.frame.grid_rowconfigure(i, weight=1)
        #iterate for columns
        for i in range(0, len(code[0])):
            #add column
            self.frame.grid_columnconfigure(i, weight=1)

        #current row variable
        r = 0
        #for each of the lines
        for line in code:
            #current column variable
            c = 0
            #list of code elements
            codes = []
            #iterate for each character
            for item in line:
                #create a label with that character
                l = tkinter.Label(self.frame, text = item, bg="#000000", fg="#ffffff", bd=3, font="TKFixedFont")
                #locate in grid
                l.grid(row=r, column=c, sticky=(N,E,S,W))
                #bind clicking on the label to code clicked function
                l.bind("<Button-1>", self.codeClicked)
                #add label to list
                codes.append(l)
                #increment column
                c = c + 1
            #add row to list
            self.codeParts.append(codes)
            #increment row
            r = r + 1

        #select first character
        self.changeSelection(0, 0)

    def codeClicked (self, event):
        '''When a code letter is clicked - set as breakpoint'''
        #get the character's colour
        colour = event.widget.cget("foreground")
        #if there is text in the label
        if event.widget.cget("text") != " ":
            #if it is white (no break)
            if colour == "#ffffff":
                #set to cyan - break point on
                event.widget.config(fg="#00ffff")
            else:
                #set to white - break point off
                event.widget.config(fg="#ffffff")

    def checkBreakPoint (self, x, y):
        '''Check if there is a break point on a certain character'''
        #if both x and y are valid list elements for the code
        if x > -1 and x < len(self.codeParts[0]) and y > -1 and y < len(self.codeParts):
            #if the colour of the text is cyan
            if self.codeParts[y][x].cget("foreground") == "#00ffff":
                #break point is present
                return True
        #no break point
        return False
    
    def onFrameConfigure(self, event):
        '''When the frame resizes, recalculate the scroll region'''
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))
    
    def changeSelection(self, x, y):
        '''Change which character is selected'''
        #if there is a selected character and it is in the code range
        if self.selectedX > -1 and self.selectedX < len(self.codeParts[0]) and self.selectedY > -1 and self.selectedY < len(self.codeParts):
            #change background colour back to black (unselected)
            self.codeParts[self.selectedY][self.selectedX].config(bg="#000000")
            #none currently selected (reset both to -1)
            self.selectedX = -1
            self.selectedY = -1

        #if the given values for selection are in the code range
        if x > -1 and x < len(self.codeParts[0]) and y > -1 and y < len(self.codeParts):
            #set selection values
            self.selectedX = x
            self.selectedY = y
            #highlight the character (magenta colour)
            self.codeParts[self.selectedY][self.selectedX].config(bg="#ff00ff")

class codeWindow (tkinter.Toplevel):
    '''Class to hold the code window'''
    def __init__(self, code, *args, **kwargs):
        '''Constructor'''
        tkinter.Toplevel.__init__(self, *args, **kwargs)
        #set the title and default geometry
        self.title("Invoke: Code")
        self.geometry("500x500")

        #set the icon
        self.iconbitmap(r"resources\icon.ico")

        #configure rows and columns for grid and scroll bars
        self.grid_rowconfigure(0,weight=10)
        self.grid_rowconfigure(1,minsize=20)
        self.grid_columnconfigure(0,weight=10)
        self.grid_columnconfigure(1,minsize=20)

        #create code grid
        self.gridCode = codeGrid(self, code)


class program ():
    '''Class to hold and process the instructions and related data'''
    def __init__(self, code, manaWindow, outputWindow, partsOutput, phialOutput, inputEntry, inputButton, codeWindow, partsFrame, runButton, pauseButton, textOutputDebug):
        '''Constructor - passes all tkinter UI parts needed and creates program data in default state'''
        self.code = code
        self.manaOutput = manaWindow
        self.textOutput = outputWindow
        self.partsOutput = partsOutput
        self.phialOutput = phialOutput
        self.inputEntry = inputEntry
        self.inputButton = inputButton
        self.codeWindow = codeWindow
        self.partsFrame = partsFrame
        self.textOutputDebug = textOutputDebug

        #move default output to top
        self.textOutput.tkraise()

        #assign buttons
        self.runButton = runButton
        self.pauseButton = pauseButton

        #debug output variables
        self.debug = False
        self.currentColour = 0
        self.currentColourDebug = 0

        #if the program is about to restart (after this pass)
        self.needToRestart = False

        #create mana pots
        self.manaPots = [0]
        #create empty phial
        self.manaPhial = 0
        #the currently selected pot
        self.currentPot = 0
        #the parts of a command currently in use
        self.parts = ["", "", ""]
        #where to replace the part next
        self.partToReplace = 0
        #if the program is running
        self.running = True
        #current instruction pointers
        self.pointerY = 0
        self.pointerX = 0
        #how to change the pointers after each instruction (x,y)
        self.pointerChange = [1, 0]
        #what the current direction of overflow is
        self.direction = random.randint(0,1)
        #if a new line is needed (has a character been printed most recently)
        self.needLine = False
        self.needLineDebug = False

        #default button colour
        self.defaultColour = self.inputButton.cget("background")

        #if the program is running
        self.running = False
        #if a single step should execute
        self.step = False
        #if input is needed
        self.inputNeeded = False
        #if the program is finished
        self.programComplete = False

        #initialize state of the run and pause buttons
        self.runButton.config(state = "normal")
        self.pauseButton.config(state = "disabled")

        #default tooltip for the command
        self.tip = ToolTips.ToolTips([self.partsFrame], ["No Command"])

    def runPressed (self):
        '''When run is pressed toggle into run mode'''
        self.running = True
        self.step = False

    def pausePressed (self):
        '''When pause is pressed toggle into paused mode'''
        self.running = False
        self.step = False

    def stepPressed (self):
        '''When step is pressed, set variable stating a single step is needed'''
        self.step = True

    def whichCommand (self, parts):
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

    def addMana (self, pots, amount, addPosition, startDir):
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
                #there is overflow
                #fill the current pot
                pots[addPosition] = 255
                #remove amount added from amount that needs to be added
                amount = amount - (255 - currentPotAmount)
                #split evenly into left and right overflow
                rightPart = amount // 2
                leftPart = amount // 2
                #if it was an odd number
                if amount % 2 != 0:
                    #if right first
                    if startDir == 0:
                        #add excess to right
                        rightPart = rightPart + 1
                    else:
                        #add excess to left
                        leftPart = leftPart + 1

                #for the pot on the left of the current to 0
                for i in range(addPosition - 1, -1, -1):
                    #if there is still mana to add on the left
                    if leftPart > 0:
                        #if the current pot is not full
                        if pots[i] < 255:
                            #get the amount in the pot
                            potAmount = pots[i]
                            #if there will not be further overflow
                            if potAmount + leftPart < 255:
                                #add left part remaining to the pot
                                pots[i] = pots[i] + leftPart
                                #no left part remaining
                                leftPart = 0
                            else:
                                #fill the pot
                                pots[i] = 255
                                #remove the amount added from the left part
                                leftPart = leftPart - (255 - potAmount)

                #if there is still a left part
                if leftPart > 0:
                    #add it to the right part (it bounced off the left wall)
                    rightPart = rightPart + leftPart

                #start position is one right of the add position
                currentPot = addPosition + 1
                #until the right part runs out
                while rightPart > 0:
                    #if there is not a current pot
                    if currentPot >= len(pots):
                        #add a new empty pot
                        pots.append(0)
                        self.manaOutput.addPot()
                    #if the pot is not full
                    if pots[currentPot] < 255:
                        #if there will not be overflow
                        if rightPart <= (255 - pots[currentPot]):
                            #add remaining amount to the pot
                            pots[currentPot] = pots[currentPot] + rightPart
                            #no right part remaining
                            rightPart = 0
                        else:
                            #get the pot amount
                            potAmount = pots[currentPot]
                            #fill the pot
                            pots[currentPot] = 255
                            #reduce the right part by the amount added
                            rightPart = rightPart - (255 - potAmount)
                    #move to the next pot
                    currentPot = currentPot + 1

        #return the updated pots      
        return pots


    def writeToText (self, data, colour):
        '''Write text to the default output'''
        #create the tag name
        tag = "colour" + str(self.currentColour)
        #configure tag
        self.textOutput.tag_configure(tag, foreground = colour)
        #increment colour counter
        self.currentColour = self.currentColour + 1
        #activate text output
        self.textOutput.config(state="normal")
        #write line in tagged colour
        self.textOutput.insert(END, data, tag)
        #deactivate text output - prevents user typing
        self.textOutput.config(state="disabled")
        #move to bottom of output
        self.textOutput.yview_moveto(1)

    def writeToTextDebug (self, data, colour):
        '''Write text to debug output window'''
        #create debug tag name
        tag = "colour" + str(self.currentColourDebug)
        #configure tag
        self.textOutputDebug.tag_configure(tag, foreground = colour)
        #increment debug colour counter
        self.currentColourDebug = self.currentColourDebug + 1
        #activate debug output
        self.textOutputDebug.config(state="normal")
        #write line in tagged colour
        self.textOutputDebug.insert(END, data, tag)
        #deactivate debug output - prevents user typing
        self.textOutputDebug.config(state="disabled")
        #move to bottom of debug output
        self.textOutputDebug.yview_moveto(1)
    
    def outputInt(self, value):
        '''Output an integer to the console'''
        #create message
        message = str(value) + "\n"
        #if a new line is needed (after char output)
        if self.needLine:
            #add new line to front of message
            message = "\n" + message
            #a new line is not needed next
            self.needLine = False
        #write the message
        self.writeToText(message, "#000000")

        #duplication of above but for debug output (prevents extra new lines where not necessary)
        message = str(value) + "\n"
        if self.needLineDebug:
            message = "\n" + message
            self.needLineDebug = False
        self.writeToTextDebug(message, "#000000")
            
    def outputChar(self, value):
        '''Output a single character to both outputs'''
        self.writeToText(str(chr(value)), "#000000")
        self.writeToTextDebug(str(chr(value)), "#000000")

    def outputDebug(self, message):
        '''Output a string to the debug output only (in debug colour too)'''
        #create message
        message = str(message) + "\n"
        #if a new line is needed
        if self.needLineDebug:
            #add new line
            message = "\n" + message
            #another line is not yet needed (for next time)
            self.needLineDebug = False
        #write the message to the debug output
        self.writeToTextDebug(message, "#0000ff")

    def outputInput(self, data, char):
        '''Output an input event to the outputs'''
        #create message
        message = "Input > " + str(data)
        #if it was a single character
        if char:
            #add integer representation to message
            message = message + " (" + str(ord(data)) + ")"
        #add new line to end of message
        message = message + "\n"
        #if another new line is needed (on the front)
        if self.needLine:
            #add new line
            message = "\n" + message
            #another new line is not needed next time
            self.needLine = False
        #write the message to the output
        self.writeToText(message, "#00ff00")

        #duplicate of above but for debug output (prevents excess or missing new lines)
        message = "Input > " + str(data)
        if char:
            message = message + " (" + str(ord(data)) + ")"
        message = message + "\n"
        if self.needLineDebug:
            message = "\n" + message
            self.needLineDebug
        self.writeToTextDebug(message, "#00ff00")

    def endMessage(self):
        '''Add the message to both outputs that the program has terminated'''
        #create message
        message = "Execution complete\n"
        #if a new line is needed
        if self.needLine:
            #add new line
            message = "\n" + message
            self.needLine = False
        #write message to the output
        self.writeToText(message, "#ff0000")

        #duplicate of above but for debug output
        message = "Execution complete\n"
        if self.needLineDebug:
            message = "\n" + message
            self.needLineDebug = False
        self.writeToTextDebug(message, "#ff0000")
    
    def movePointer(self):
        '''Move the pointer on the code grid'''
        try:
            #attempt (in case user closed the grid)
            #change selected characer
            self.codeWindow.changeSelection(self.pointerX, self.pointerY)
        except:
            #do nothing as code window was closed so no action needed
            pass
    
    def inputGiven (self, value):
        '''Check if an input is valid and process it'''
        number = -1
        try:
            #attempt convert to int
            value = int(value)
            #if it is a positive number
            if value >= 0:
                #use the value
                number = value
                #output that an integer was input
                self.outputInput(number, False)
        except:
            #if it isn't a number
            #if it has a length of 1
            if len(value) == 1:
                #use the unicode value for it (mod 256, so it is in ascii range)
                number = ord(value) % 256
                #output that a character was input
                self.outputInput(value, True)

        #if a valid input was given
        if number >= 0:
            #disable input button
            self.inputButton.config(state="disabled")
            #empty entry box
            self.inputEntry.delete(0, END)
            
            #call for it to be added to the pot
            self.manaPots = self.addMana(self.manaPots, number, self.currentPot, self.direction)
            #if the amount added was odd
            if number % 2 != 0:
                #invert the direction
                if self.direction == 0:
                    self.direction = 1
                else:
                    self.direction = 0

            #move pointer to next position
            self.pointerX = self.pointerX + self.pointerChange[0]
            self.pointerY = self.pointerY + self.pointerChange[1]

            #visually move the pointer
            self.movePointer()

            try:
                #if a break point was reached
                if self.codeWindow.checkBreakPoint(self.pointerX, self.pointerY):
                    #stop running
                    self.running = False
                    #switch buttons to paused
                    self.pauseButton.config(state = "disabled")
                    self.runButton.config(state = "normal")
                    #debug output
                    self.outputDebug("Breakpoint reached, pausing")
            except:
                pass

            #input is no longer needed
            self.inputNeeded = False

    def singleExecute (self):
        '''Run a single command'''
        returnValue = 0
        #if the program is running or stepping - not awaiting input and not complete
        if (self.running or self.step) and not self.inputNeeded and not self.programComplete:
            #if stepping
            if self.step:
                #wait for next button press
                self.step = False

            #valid code parts
            validParts = ["Q", "W", "E"]
            #other commands
            otherCommands = ["I", "R", ">", "<", "^", "V"]

            #wrap the pointer if it goes off the right side
            if self.pointerX >= len(self.code[0]):
                self.pointerX = 0
            #wrap the pointer if it goes off the left side
            if self.pointerX < 0:
                self.pointerX = len(self.code[0]) - 1
            #wrap the pointer if it goes off the bottom
            if self.pointerY >= len(self.code):
                self.pointerY = 0
            #wrap the pointer if it goes off the top
            if self.pointerY < 0:
                self.pointerY = len(self.code) - 1

            #the amount the pointer is being boosted by (jumps)
            pointerBoost = [0,0]
            #the currently selected character/instruction
            currentChar = self.code[self.pointerY][self.pointerX]

            #if it is a command or code character
            if currentChar in validParts or currentChar in otherCommands:
                #if the character is the invoke command
                if currentChar == "I":
                    #get which command the code makes up
                    command = self.whichCommand(self.parts)
                    if command == 0:
                        #right 1 pot
                        #increase selected pot
                        self.currentPot = self.currentPot + 1
                        #if this exceeds where there are currently pots
                        if self.currentPot >= len(self.manaPots):
                            #add a new empty pot
                            self.manaPots.append(0)
                            self.manaOutput.addPot()
                        #get a new random direction
                        self.direction = random.randint(0,1)
                        #select the correct pot
                        self.manaOutput.changeSelected(self.currentPot)
                        self.outputDebug("Moving right 1 pot")
                    elif command == 1:
                        #left 1 pot
                        #if not on the left wall
                        if self.currentPot != 0:
                            #get new random direction
                            self.direction = random.randint(0,1)
                        #move to the left
                        self.currentPot = self.currentPot - 1
                        #if at the left wall
                        if self.currentPot < 0:
                            #stay on first pot
                            self.currentPot = 0
                        #select the correct pot
                        self.manaOutput.changeSelected(self.currentPot)
                        self.outputDebug("Moving left 1 pot")
                    elif command == 2:
                        #add 1 to current pot
                        #call for 1 mana to be added to the current pot
                        self.manaPots = self.addMana(self.manaPots, 1, self.currentPot, self.direction)
                        #invert the direction
                        if self.direction == 0:
                            self.direction = 1
                        else:
                            self.direction = 0
                        self.outputDebug("Adding 1 to pot " + str(self.currentPot))
                    elif command == 3:
                        #remove 1 from current pot
                        #if there is mana in the pot
                        if self.manaPots[self.currentPot] > 0:
                            #take 1 mana from the pot
                            self.manaPots[self.currentPot] = self.manaPots[self.currentPot] - 1
                        self.outputDebug("Taking 1 from pot " + str(self.currentPot))
                    elif command == 4:
                        #output value of current pot
                        #output the number
                        self.outputDebug("Outputting pot " + str(self.currentPot) + " value")
                        self.outputInt(self.manaPots[self.currentPot])
                    elif command == 5:
                        #output character of current pot
                        #output character
                        self.outputDebug("Outputting pot " + str(self.currentPot) + " character")
                        self.outputChar(self.manaPots[self.currentPot])
                        #a new line is needed when a number is printed
                        self.needLine = True
                        self.needLineDebug = True
                    elif command == 6:
                        #Input and add to current pot
                        #get amount to add
                        self.inputNeeded = True
                        self.inputButton.config(state="normal")
                        #focus the input
                        self.inputEntry.focus_set()
                        self.outputDebug("Getting user input (store value or character value in pot " + str(self.currentPot)+ ")")
                    elif command == 7:
                        #draw as much as possible to fill phial
                        #get the maximum amount that can be taken
                        maximum = 511 - self.manaPhial
                        #if the maximum is greater than or equal to the amount in the current pot
                        if maximum >= self.manaPots[self.currentPot]:
                            #take all into phial
                            self.manaPhial = self.manaPhial + self.manaPots[self.currentPot]
                            #set pot to empty
                            self.manaPots[self.currentPot] = 0
                        else:
                            #fill phial
                            self.manaPhial = 511
                            #remove maximum from current pot
                            self.manaPots[self.currentPot] = self.manaPots[self.currentPot] - maximum
                        self.outputDebug("Drawing from " + str(self.currentPot) + " to fill phial")
                    elif command == 8:
                        #pour all from phial into pot
                        #add the amount in the phial to the current pot
                        self.manaPots = self.addMana(self.manaPots, self.manaPhial, self.currentPot, self.direction)
                        #if it was an odd amount
                        if self.manaPhial % 2 != 0:
                            #invert direction
                            if self.direction == 0:
                                self.direction = 1
                            else:
                                self.direction = 0
                        #empty phial
                        self.manaPhial = 0
                        self.outputDebug("Pouring phial into pot " + str(self.currentPot))
                    elif command == 9:
                        #stop
                        self.programComplete = True
                        self.outputDebug("Program Stop")
                elif currentChar == "R":
                    #revoke - jump if empty pot
                    #if the current pot is empty
                    if self.manaPots[self.currentPot] == 0:
                        #move the pointer 1 further in it's current direction
                        pointerBoost[0] = self.pointerChange[0]
                        pointerBoost[1] = self.pointerChange[1]
                        self.outputDebug("Pot " + str(self.currentPot) +" is empty, jumping over")
                    else:
                        self.outputDebug("Pot " + str(self.currentPot) +" is not empty ("+ str(self.manaPots[self.currentPot]) +"), no jump")
                elif currentChar == ">":
                    #switch to move right
                    self.pointerChange = [1, 0]
                    self.outputDebug("Moving right")
                elif currentChar == "<":
                    #switch to move left
                    self.pointerChange = [-1, 0]
                    self.outputDebug("Moving left")
                elif currentChar == "V":
                    #switch to move down
                    self.pointerChange = [0, 1]
                    self.outputDebug("Moving down")
                elif currentChar == "^":
                    #switch to move up
                    self.pointerChange = [0, -1]
                    self.outputDebug("Moving up")
                elif currentChar in validParts:
                    #it is Q,W or E
                    #replace the next part to replace whith this character
                    self.parts[self.partToReplace] = currentChar
                    #move to replace on one
                    self.partToReplace = self.partToReplace + 1
                    #if it is beyond the end
                    if self.partToReplace > 2:
                        #move back to start
                        self.partToReplace = 0

            else:
                returnValue = 1
            
            #adjust instruction pointer
            if not self.inputNeeded and not self.programComplete:
                self.pointerX = self.pointerX + self.pointerChange[0] + pointerBoost[0]
                self.pointerY = self.pointerY + self.pointerChange[1] + pointerBoost[1]
                self.movePointer()

            #button colours for parts
            quasColour = "#103be8"
            wexColour = "#e810ae"
            exortColour = "#dd8006"

            colours = []
            #fill list with colours based on parts
            for i in self.parts:
                if i == "Q":
                    colours.append(quasColour)
                elif i == "W":
                    colours.append(wexColour)
                elif i == "E":
                    colours.append(exortColour)
                else:
                    colours.append(self.defaultColour)

            #iterate for the parts
            for i in range(0, 3):
                #set the colours and text
                self.partsOutput[i].config(text=self.parts[i], bg=colours[i])

            #set the phical output
            self.phialOutput.config(text=self.manaPhial)

            #iterate for the pots
            for i in range(0, len(self.manaPots)):
                #set the pot values
                self.manaOutput.changeValue(i, self.manaPots[i])
                
            #get the command for the currently set parts
            comm = self.whichCommand(self.parts)
            #set the tooltip to be correct for the command
            if comm == -1:
                self.tip
                self.tip.tooltip_text = ["No Command"]
            elif comm == 0:
                self.tip.tooltip_text = ["Move right one pot"]
            elif comm == 1:
                self.tip.tooltip_text = ["Move left one pot"]
            elif comm == 2:
                self.tip.tooltip_text = ["Add 1 mana to current pot"]
            elif comm == 3:
                self.tip.tooltip_text = ["Take 1 mana from current pot"]
            elif comm == 4:
                self.tip.tooltip_text = ["Output number in current pot"]
            elif comm == 5:
                self.tip.tooltip_text = ["Output character of current pot"]
            elif comm == 6:
                self.tip.tooltip_text = ["Input value and add that mana to current pot"]
            elif comm == 7:
                self.tip.tooltip_text = ["Draw as much mana as possible from current pot to fill phial"]
            elif comm == 8:
                self.tip.tooltip_text = ["Pour all of phial into current pot"]
            elif comm == 9:
                self.tip.tooltip_text = ["Stop program"]

            try:
                #attempt to check if there is a break point
                if self.codeWindow.checkBreakPoint(self.pointerX, self.pointerY):
                    #pause if there is
                    self.running = False
                    self.pauseButton.config(state = "disabled")
                    self.runButton.config(state = "normal")
                    #debug output
                    self.outputDebug("Breakpoint reached, pausing")
                    
            except:
                #failed - code window is closed - don't do anything
                pass

        #if the program finished
        if self.programComplete:
            #output the end message
            self.endMessage()
            #-1 - means program ended
            return -1
        #return the default return value 0 - normal character, other - blank
        return returnValue
        
def openMenu (root):
    '''Create and run the default menu - to input the file path'''
    #set the title and geometry
    root.title("Invoke: File Open")
    root.geometry("300x30")

    #setup the grid
    root.grid_rowconfigure(0, minsize=300)
    root.grid_columnconfigure(0, minsize=30)

    #add a frame to hold the input
    mainFrame = tkinter.Frame(root)
    mainFrame.grid(row=0, column=0, sticky=(N,E,S,W))

    #create a stringvar to hold the path
    path = tkinter.StringVar()

    def convertToValid (fileInput):
        '''Convert file data to array of valid characters only'''
        validChars = ["Q", "W", "E", "R", "I", ">", "<", "V", "^"]
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
                    lineData.append(" ")

            #iterate for extra items that are needed
            for i in range(maxLength - len(lineData)):
                #add blanks to fill to square
                lineData.append(" ")

            #add line to data
            data.append(lineData)

        #return the array
        return data
    
    def load (pathString):
        #initialize data as none - if no file can be obtained it won't proceed
        fileData = None
        #check for correct extension
        if pathString.endswith(".inv"):
            try:
                #attempt to open and read the file
                invokeFile = open(pathString, "r")
                #store data in variable
                fileData = invokeFile.read()
                #close the file
                invokeFile.close()
            except:
                #if something went wrong the file wasn't found
                return None
        return fileData

    def attemptLoad ():
        '''Load has been pressed so attempt a load'''
        #get the path
        pathData = path.get()
        #load the files data
        data = load(pathData)
        #if there is some data
        if data != None:
            #convert to valid grid
            data = convertToValid(data)
            #if there is data to run
            if len(data) > 0:
                if len(data[0]) > 0:
                    #quit the path input menu
                    mainFrame.quit()
                    #open the main program
                    openProgram(root, data)
                    #once the program returns quit the main - prevents hanging
                    root.quit()

    #setup the frame grid - part for entry, part for button
    mainFrame.grid_rowconfigure(0, minsize=30)
    mainFrame.grid_columnconfigure(0, minsize=240)
    mainFrame.grid_columnconfigure(1, minsize=60)

    #create entry widget (assing path stringvar)
    fileInput = tkinter.Entry(mainFrame, bd=5, textvariable=path)
    #locate the entry in the grid
    fileInput.grid(row=0, column=0, sticky=(N,E,S,W))

    #create button which calls an attempt load when pressed
    invokeButton = tkinter.Button(mainFrame, bd=5, text="Load", command=attemptLoad)
    #locate the button in the grid
    invokeButton.grid(row=0, column=1, sticky=(N,E,S,W))

    #move the focus to the entry at the start
    fileInput.focus_set()

    #begin the update loop of the UI
    root.mainloop()

def openProgram(root, code):
    '''Create the interface for the main program'''
    def quitProgram():
        '''End the program completely'''
        root.destroy()

    #create window to store the UI in
    programWindow = tkinter.Frame(root)
    #locate the program window into the root
    programWindow.grid(row=0, column=0, sticky=(N,E,S,W))

    #set the title and geometry for the window    
    root.title("Invoke: Program")
    root.geometry("600x450")

    #set up the rows to hold all the UI
    programWindow.grid_rowconfigure(0,minsize=90)
    programWindow.grid_rowconfigure(1,minsize=5)
    programWindow.grid_rowconfigure(2,minsize=60)
    programWindow.grid_rowconfigure(3,minsize=5)
    programWindow.grid_rowconfigure(4,minsize=30)
    programWindow.grid_rowconfigure(5,minsize=5)
    programWindow.grid_rowconfigure(6,minsize=255)
    programWindow.grid_columnconfigure(0,minsize=600)

    #create frame to hold the memory scroll area
    memoryFrame = tkinter.Frame(programWindow)
    memoryFrame.grid(row=0, column=0, sticky=(N,E,S,W))

    #setup the grid in the memory frame to hold the scroll area and scroll bar
    memoryFrame.grid_rowconfigure(0,minsize=60)
    memoryFrame.grid_rowconfigure(1,minsize=15)
    memoryFrame.grid_columnconfigure(0,minsize=600)
    #ceate the scroll object
    memoryScroll = manaScroll(memoryFrame)

    #frame to hold the information about the phial and parts
    infoFrame = tkinter.Frame(programWindow)
    infoFrame.grid(row=2, column=0, sticky=(N,E,S,W))

    #setup columns in the info frame
    infoFrame.grid_rowconfigure(0, minsize=70)
    infoFrame.grid_columnconfigure(0,minsize=210)
    infoFrame.grid_columnconfigure(1,minsize=320)
    infoFrame.grid_columnconfigure(2,minsize=70)

    #create frame to hold the parts
    partsFrame = tkinter.Frame(infoFrame)
    partsFrame.grid(row=0, column=0, sticky=(N,E,S,W))

    #setup the columns for each of the parts in the part holder
    partsFrame.grid_rowconfigure(0, minsize=70)
    partsFrame.grid_columnconfigure(0, minsize=70)
    partsFrame.grid_columnconfigure(1, minsize=70)
    partsFrame.grid_columnconfigure(2, minsize=70)

    #get the image of the phial
    phialImage = tkinter.PhotoImage(file="resources/phial.png")

    #setup the parts and phial outputs
    part1 = tkinter.Button(partsFrame,bd=5,disabledforeground="#000000",text="",state="disabled")
    part2 = tkinter.Button(partsFrame,bd=5,disabledforeground="#000000",text="",state="disabled")
    part3 = tkinter.Button(partsFrame,bd=5,disabledforeground="#000000",text="",state="disabled")
    phial = tkinter.Button(infoFrame,bd=5,disabledforeground="#000000",image=phialImage,text="0",state="disabled",compound="bottom")

    #locate parts and phial into the grid
    part1.grid(row=0, column=0, sticky=(N,E,S,W))
    part2.grid(row=0, column=1, sticky=(N,E,S,W))
    part3.grid(row=0, column=2, sticky=(N,E,S,W))
    
    phial.grid(row=0, column=2, sticky=(N,E,S,W))

    #store the parts in a list
    partsOutput = [part1, part2, part3]

    #create frame to hold the inputs
    infoInput = tkinter.Frame(infoFrame)
    infoInput.grid(row=0, column=1, sticky=(N,E,S,W))

    #configure input grid
    infoInput.grid_rowconfigure(0,minsize=30)
    infoInput.grid_rowconfigure(1,minsize=30)
    infoInput.grid_columnconfigure(0,minsize=210)
    infoInput.grid_columnconfigure(1,minsize=110)

    #variables to hold input and debug
    inputText = tkinter.StringVar()
    debug = tkinter.IntVar()

    #create entry, input button and debug check box
    entryInput = tkinter.Entry(infoInput, bd=5, textvariable=inputText)
    entryInputButton = tkinter.Button(infoInput, bd=5, text="Input", state="disabled")
    debugCheck = tkinter.Checkbutton(infoInput, text="Debug Output", variable=debug, offvalue=0, onvalue=1)

    #locate input elements
    entryInput.grid(row=0,column=0,sticky=(N,E,S,W))
    entryInputButton.grid(row=0,column=1,sticky=(N,E,S,W))
    debugCheck.grid(row=1,column=0,sticky=(N,E,S,W))

    #create a frame to hold the controls
    controlsFrame = tkinter.Frame(programWindow)
    controlsFrame.grid(row=4, column=0, sticky=(N,E,S,W))

    #setup controls grid - for each of the buttons
    controlsFrame.grid_rowconfigure(0,minsize=30)
    controlsFrame.grid_columnconfigure(0,minsize=120)
    controlsFrame.grid_columnconfigure(1,minsize=120)
    controlsFrame.grid_columnconfigure(2,minsize=120)
    controlsFrame.grid_columnconfigure(3,minsize=120)
    controlsFrame.grid_columnconfigure(4,minsize=120)
    
    #create all the control buttons
    runButton = tkinter.Button(controlsFrame,text="Run")
    pauseButton = tkinter.Button(controlsFrame,text="Pause",state="disabled")
    stepButton = tkinter.Button(controlsFrame,text="Step")
    restartButton = tkinter.Button(controlsFrame,text="Restart")
    endButton = tkinter.Button(controlsFrame,text="Exit", command=quitProgram)

    #locate the control buttons
    runButton.grid(row=0,column=0,sticky=(N,E,S,W))
    pauseButton.grid(row=0,column=1,sticky=(N,E,S,W))
    stepButton.grid(row=0,column=2,sticky=(N,E,S,W))
    restartButton.grid(row=0,column=3,sticky=(N,E,S,W))
    endButton.grid(row=0,column=4,sticky=(N,E,S,W))

    #create and locate holder for the output
    outputFrame = tkinter.Frame(programWindow)
    outputFrame.grid(row=6, column=0, sticky=(N,E,S,W))

    #create grid for output holder
    outputFrame.grid_rowconfigure(0, minsize=240)
    outputFrame.grid_columnconfigure(0, minsize=600)

    #do not allow internal components to change the frames size
    outputFrame.grid_propagate(False)

    #create the normal output holder
    outputNormalHolder = tkinter.Frame(outputFrame)
    #locate holder
    outputNormalHolder.grid(row = 0, column = 0, sticky = (N,E,S,W))
    #configure grid of holder
    outputNormalHolder.grid_rowconfigure(0, minsize=240)
    outputNormalHolder.grid_columnconfigure(0, minsize=600)

    #create the debug output holder
    outputDebugHolder = tkinter.Frame(outputFrame)
    #locate holder
    outputDebugHolder.grid(row = 0, column = 0, sticky = (N,E,S,W))
    #configure grid of holder
    outputDebugHolder.grid_rowconfigure(0, minsize=240)
    outputDebugHolder.grid_columnconfigure(0, minsize=600)

    #create and locate normal scroll text output
    textOutput = scrolledtext.ScrolledText(outputNormalHolder, wrap=WORD, width=0, height=0, state="disabled")
    textOutput.grid(row=0, column=0, sticky=(N,E,S,W))

    #create and locate debug scroll text output
    textOutputDebug = scrolledtext.ScrolledText(outputDebugHolder, wrap=WORD, width=0, height=0, state="disabled")
    textOutputDebug.grid(row=0, column=0, sticky=(N,E,S,W))

    #move normal output to the top
    outputNormalHolder.tkraise()
    
    #create the program display window
    programWindowOutput = codeWindow(code)
    #create the program controller - passing all necessary components
    programControl = program(code, memoryScroll, textOutput, partsOutput, phial, entryInput, entryInputButton, programWindowOutput.gridCode, partsFrame, runButton, pauseButton, textOutputDebug)


    def runButtonPressed ():
        '''Run the program'''
        runButton.config(state="disabled")
        pauseButton.config(state="normal")
        programControl.runPressed()

    def pauseButtonPressed ():
        '''Pause the program'''
        runButton.config(state="normal")
        pauseButton.config(state="disabled")
        programControl.pausePressed()

    def inputButtonPressed ():
        '''Attempt input of data from entry widget'''
        programControl.inputGiven(inputText.get())

    def stepButtonPressed ():
        '''Perform a single step'''
        programControl.stepPressed()

    def debugChecked ():
        '''Invert the debug state'''
        #if debug is on
        if debug.get() == 1:
            #change the variable in the program controller
            programControl.debug = True
            #move the debug output to the top
            outputDebugHolder.tkraise()
            #scroll to same position in debug as in normal
            textOutputDebug.yview_moveto(textOutput.yview()[0])
        else:
            #change the variable in the program controller
            programControl.debug = False
            #move the normal output to the top
            outputNormalHolder.tkraise()
            #scroll to the same position in normal as in debug
            textOutput.yview_moveto(textOutputDebug.yview()[0])

    
    def restart(programControl, programWindowOutput):
        '''Reload the program'''
        #destroy the program controller
        del programControl
        #destroy the program windows
        programWindow.destroy()
        programWindowOutput.destroy()
        #recreate the programs
        openProgram(root, code)

    def restartPressed():
        '''When restart is pressed turn flag on in the program so at the end of next execution it restarts'''
        programControl.needToRestart = True
        #if the program is over - restart now
        if programControl.programComplete:
            restart(programControl, programWindowOutput)

    #bind control buttons to associated functions
    runButton.config(command=runButtonPressed)
    pauseButton.config(command=pauseButtonPressed)
    entryInputButton.config(command=inputButtonPressed)
    stepButton.config(command=stepButtonPressed)
    debugCheck.config(command=debugChecked)
    restartButton.config(command=restartPressed)

    def runningLoop ():
        '''Repeats while the program is running'''
        #run the next instruction (if possible)
        #will check if running or stepping or inputting first
        value = programControl.singleExecute()

        #if restart is required
        if programControl.needToRestart:
            #restart the program
            restart(programControl, programWindowOutput)

        #if the program hasn't ended and doesn't need to restart
        if value != -1 and not programControl.needToRestart:
            #normal case
            if value == 0:
                #repeat with normal delay
                root.after(150, runningLoop)
            #no code executed (blank)
            else:
                #repeat with short delay
                root.after(30, runningLoop)

    #start the running loop
    runningLoop()

    #start the UI update loop
    root.mainloop()

#create the program root
root = tkinter.Tk()
#set the icon for the window
root.iconbitmap(r"resources\icon.ico")
#cannot resize the window
root.resizable(False, False)

#start the program by opening the load menu
openMenu(root)
