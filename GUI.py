import SpellBot
import time
from tkinter import *

ws = Tk()
ws.title("SpellBot")

def focus_next_window(event):
    event.widget.tk_focusNext().focus()
    return("break")

def clear(letters):
    for textBox in letters:
        textBox.delete(0, "end")

def calculate(letters):
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
    h = b.searchAll()
    words = sorted(h.getWords(b), key = lambda x: x[0])
    print(words[-1])
    end_time = time.time()
    print(end_time - start_time)

def validate_input(new_value):
    
    return len(new_value) <= 1

letterFrame = Frame(ws)
letterFrame.grid(row = 0, column = 0)
buttonFrame = Frame(ws)
buttonFrame.grid(row = 1, column = 0)

letterInputs = []

for i in range(25): #Create Entry Boxes
    stringValue = StringVar() #Assign StringVar
    validation = ws.register(validate_input)
    letterInputs.append(Entry(letterFrame, width = 2, textvariable=stringValue, validate = "key", validatecommand = (validation, "%P")))
    letterInputs[i].grid(row = i // 5, column= i % 5, sticky="nsew")
    letterInputs[i].bind("<Tab>", focus_next_window)

b_Calculate = Button(buttonFrame, text = "Calculate", command= lambda: calculate(letterInputs))
b_Calculate.grid(row = 0, column = 0)

b_Calculate = Button(buttonFrame, text = "Clear", command= lambda: clear(letterInputs))
b_Calculate.grid(row = 0, column = 1)

ws.mainloop()
