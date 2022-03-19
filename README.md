# Invoke
A simple esoteric programming language.

This was an idea that I just decided to go ahead and have a go at. I feel it worked pretty well all things considered.



# What is this?
The files here are interpreters and debuggers for a programming language idea (or a pair of ideas really).

The language was originally designed to be a combination of pure turing control languages (brainF) and 2d programming languages (befunge).



# Detailed Explaination
However I felt as I was working the idea through in the inital stages that I wanted something a little more unique - an interesting way of structuring commands. A language I was inspired by was Jolverine which is another esolang that uses an encoding wheel for it's commands but I wanted something unique. So I settled on making each command a compound of 3 parts which would then be executed (later renamed invoked)


Soon after I came up with the idea for doing it as 3 part commands it made me think of one thing: DOTA 2's Invoker. I am not an avid DOTA player by any means but I always really liked the idea of Invoker. The way he works is essentially as above: 3 parts of 3 options: Quas, Wex and Exort and as order doesn't matter this gives him 10 different spells.

Similarly this means that (appart from flow control) there are 10 commands in this language which are represented by 4 characters. (Q, W and E for the command and I to 'invoke' it)

So that gave me a thematic idea to work with but of course this exact same principle could be applied with no theme or with a different one if someone wanted to.


Similar to other 2d languages the pointer starts in the top left and is moving right by default. It will wrap around the boundaries and keep the same direction until it is changed.

All non valid characters are ignored and can be used for comments. The command characters are not case sensitive.


The file extension is .inv but it is essentially just a .txt file saved with another extension.


To keep with the theme the infinite memory tape used in other languages has been theoretically replaced by an infinite number of pots containing an amount of mana (0 initially) streching to the right.

The currently selected pot is always the leftmost one. More pots are automatically added to the right as needed.

Another interesting point about this language is that as with many turing machine type languages there is a limit to what each memory element can hold. The same is true here (it is 255, surprise surprise) but this is where the two sets of my files arise - reactive vs unreactive (so named because stable and unstable is too confusing with software versions) in unreactive (the simpler but more boring one) any mana that cannot fit in any pot simply spills out onto the floor and is lost. But in reactive the excess overflows into adjacent pots (half to each direction running until it finds a pot to fit into - it will bounce off the left wall at 0 and start going right - in the case of an odd number the extra will be sent in a random direction), this allows for very different programming techniques (I don't fully understand how it could be used but think it is interesting in concept at least) and allows for random generation by overflowing by 1.

Of course the overflow can easily lead to infinite loops due to the program never ending conditions so it needs to be managed carefully.


As well as the above there is a special memory location that I have refered to as the 'phial' which all of the mana from the current pot can be moved to (until the phial is full - excess is left behind) then the phial can be emptied into the current pot again later (excess overflows based on the version's rules as the phial is always emptied). The phial is larger than a pot as it can store 511. (one more than 2 pots - I have labored long over what size to make the phial - bigger than a pot or smaller? by how much? what is useful? - any suggestions are welcome on this matter as I'm sure someone out there has a better understanding of what this affects than I do)



# What are the commands?
\>, <, ^ and V - change the direction of the pointer to Right, Left, Up and Down in order.

I - invokes the current command - based on the most recent three command parts reached - if three have not been reached yet nothing happens.

R - 'revoke' - skips the over next character if the current pot is empty - only way of doing conditions.

Q - replaces the oldest command part with a Q

W - replaces the oldest command part with a W

E - replaces the oldest command part with a E


Commands made from QWE and executed by I:

WWE - Move current pot right 1

WWQ - Move current pot left 1 pot

QQE - Add 1 mana to current pot

QQW - Remove 1 mana from current pot

EEW - Output the amount of mana in the current pot as an integer

EEQ - Output the amount of mana in the current pot as a character (Extended ASCII)

QQQ - Input an integer or a single character (converted using extended ASCII (max 255)) and store that much mana in the current pot

WWW - Draw as much as mana as possible from current pot to the phial

EEE - Pout all mana in the phial into the current pot

QWE - Stop the program


Yes input can technically take a huge value that will overflow and fill lots of pots in the reactive version.



# The Debugger
I made an attempt to write a debugger for this interpreter - the interpreter for each version just runs in command line - to display the data (partially to prove to myself that my code actually works as intended).


I wrote it in python using tkinter and am very much aware it is probably not brilliantly structured but it works. (do let me know if I have made a glaring oversigt)


It asks first for the path of the .inv file (I recomment moving it to the same file as the debugger for ease of testing).


Then it loads the program and opens the debugger.


The bar at the top shows the memory pots (pink is currently selected), bellow it are the current command parts (which can be hovered over to find the command they currently represent) the input section and a debug check box (this toggles on and off the debug/verbose output) and the current phial indicator.

Then there are the controls - 'Run' starts the program running, 'Pause' pauses the execution, 'Step' runs a single character, 'Restart' reloads the program back to the start, 'Exit' closes the debugger.
Lastly is the output window which displays output and debug text.


The other window shows the program code in a grid. The magenta highlighted character is where the pointer currently is and which character will be interpreted by the next cycle (when paused). If you click on any of the characters you will find that the character changes colour to cyan, this indicates that there is now a break point on that character so when it is reached (before it's command is run) the execution will pause if it is running (stepping wil ignore it).


# Acknowledgements
I used a small script to add the tooltips for the command, it was very useful and worked perfectly for what i needed with a good example to help understanding. So a big thank you to Pedro Henriques (https://github.com/PedroHenriques) for creating Tkinter_ToolTips (https://github.com/PedroHenriques/Tkinter_ToolTips/blob/master/ToolTips.py) and for allowing it to be used so freely.


I had to do a lot of googling to learn all I needed to for the tkinter code, especially on the scrolling canvases so I want to thank Bryan Oakley for his brilliant answer to adding scrollbars to groups of widgets on stack overfow here: https://stackoverflow.com/questions/3085696/adding-a-scrollbar-to-a-group-of-widgets-in-tkinter
I'm not sure I would have managed to do this without this code example.



# End
Phew, that was long but I wanted to make sure i documented all this before I forget it.

This was intended as a small personal project but anyone is free to use it as they want.

I'm not sure that anyone would want to code in this language or have any interest but if there are any suggestions or questions please do let me know.
