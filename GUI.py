import SpellBot
import time
from tkinter import *

ws = Tk()
ws.title("SpellBot")

def focus_next_window(event):
    event.widget.tk_focusNext().focus()
    return("break")

def clear(letters, outputLabel):
    for textBox in letters:
        textBox.delete(0, "end")
    outputLabel.config(text = "")

def calculate(letters, v, outputLabel):
    print(v.get())
    
    string = ""
    for textBox in letters:
        letter = textBox.get()
        letter = letter.lower()
        if letter == "":
            letter = "-"
        if letter in "abcdefghijklmnopqrstuvwxyz-":
            string += letter
        else:
            string += "-"

    d = SpellBot.Dictionary("2of12inf.txt")
    b = SpellBot.Board(5, 5, d)
    start_time = time.time()
    b.buildFromString(string)

    b.getLetter(v.get() // 5, v.get() % 5).double=True
    
    h = b.searchAll()
    words = sorted(h.getWords(b), key = lambda x: x[0])
    outputLabel.config(text = words[-1][1] + " - " + str(words[-1][0]))
    print(words[-1])
    end_time = time.time()
    print(end_time - start_time)

def validate_input(new_value):
    return len(new_value) <= 1

superFrame = Frame(ws)
superFrame.grid(row = 0, column = 0)

titleFrame = Frame(ws)
titleFrame.grid(row = 0, column = 0)


letterFrameSuper = Frame(superFrame)
letterFrameSuper.grid(row = 1, column = 0, sticky = N)
letterFrame = Frame(letterFrameSuper)
letterFrame.grid(row = 1, column = 0, sticky = N)

radioFrame = Frame(superFrame)
radioFrame.grid(row = 1, column = 1)

buttonFrame = Frame(superFrame)
buttonFrame.grid(row = 2, column = 0)

letterLabel = Label(superFrame, text = "Letter Grid")
letterLabel.grid(row = 0, column = 0)

doubleLabel = Label(superFrame, text = "2x Word Location")
doubleLabel.grid(row = 0, column = 1)
noneLabel = Label(superFrame, text = "(Bottom if none)")
noneLabel.grid(row = 2, column = 1)
outputLabel = Label(letterFrameSuper, text = '')
outputLabel.grid(row = 5, column = 0)


letterInputs = [] #Create Entry Boxes
for i in range(25): 
    stringValue = StringVar()
    validation = ws.register(validate_input)
    letterInputs.append(Entry(letterFrame, width = 2, textvariable=stringValue, validate = "key", validatecommand = (validation, "%P")))
    letterInputs[i].grid(row = i // 5, column= i % 5, sticky="nsew")
    letterInputs[i].bind("<Tab>", focus_next_window)

radioButtons = [] #Create Radio Buttons
v = IntVar()
for i in range(25):
    radioButtons.append(Radiobutton(radioFrame, variable = v, value = i))
    radioButtons[i].grid(row = i // 5, column= i % 5, sticky="nsew")

radioButtons.append(Radiobutton(radioFrame, variable = v, value = -1))
radioButtons[25].grid(row = 5, column = 2, sticky="nsew")

b_Calculate = Button(buttonFrame, text = "Calculate", command= lambda: calculate(letterInputs, v, outputLabel))
b_Calculate.grid(row = 0, column = 0)

b_Calculate = Button(buttonFrame, text = "Clear", command= lambda: clear(letterInputs, outputLabel))
b_Calculate.grid(row = 0, column = 1)

ws.mainloop()
