import random
from datetime import datetime
import time
random.seed(datetime.now().timestamp())

LENGTH_LIMIT = 10

class Dictionary:
    calculations = 0
    fileName = ""
    words = []

    def __init__(self, fileName):
        self.fileName = fileName
        self.loadWords()

    def loadWords(self):
        f = open(self.fileName, 'r')
        self.words = f.read().splitlines()
        f.close()

    def findWords(self, s):
        self.calculations += 1
        matching_words = [word for word in self.words if word.startswith(s)]
        return matching_words

    def isWord(self, s):
        return s in self.words

class Letter:
    letterValues = {'a':1, 'b':4, 'c':5, 'd':3, 'e':1, \
                    'f':5, 'g':3, 'h':4, 'i':1, 'j':7, \
                    'k':6, 'l':3, 'm':4, 'n':2, 'o':1, \
                    'p':4, 'q':8, 'r':2, 's':2, 't':2, \
                    'u':4, 'v':5, 'w':5, 'x':7, 'y':4, \
                    'z':8, '-':0}
    x = -1
    y = -1
    mana = False
    points = 0
    board = None
    
    
    def __init__(self, char, x, y, board, mana = False, multiplier = 1, double = False):
        self.char = char.lower()
        self.x = x
        self.y = y
        self.points = self.letterValues[self.char]
        self.board = board
        self.double = double
        self.multiplier = multiplier
        self.mana = mana
        

    def __str__(self):
        return self.char

    def getSurrounding(self):

        surrounding = []
        
        for xDif in range(-1, 2):
            for yDif in range(-1, 2):
                surrounding.append(self.board.getLetter(self.x + xDif, self.y + yDif))

        surrounding.remove(surrounding[4])
        return surrounding

class SearchHelper():
    words = []
    def __init__(self):
        pass
    
    def add(self, word):
        self.words.append(word)

    def getWords(self, board):
        output = []
        for word in self.words:
            output.append([board.wordValue(word), board.listToString(word)])
        return output

    def clear(self):
        self.words.clear()

class Board:
    letters = []
    lenX = 0
    lenY = 0
    d = None

    def __init__(self, lenX, lenY, d):
        self.lenX = lenX
        self.lenY = lenY
        self.d = d

    def getLetter(self, x, y):
        for letter in self.letters:
            if letter.x == x and letter.y == y:
                return letter
            
        return Letter('-', -1, -1, self)

    def wordValue(self, letters):
        value = 0;
        for letter in letters:
            value += letter.points
        for letter in letters:
            if letter.double:
                value *= 2
        if len(letters) > 5:
            value += 10
        return value

    def buildFromString(self, string):
        self.letters.clear()
        i = 0
        for letter in string:
            self.setLetter(letter, i // self.lenX, i % self.lenX)
            i += 1

    def setLetter(self, value, x, y):
        rmv = self.getLetter(x, y)
        if str(rmv) != '-': #If letter is on board, remove it
            self.letters.remove(rmv)
        self.letters.append(Letter(value, x, y, self))

    def print(self):
        for x in range(self.lenX):
            for y in range(self.lenY):
                if (self.getLetter(x, y).double):
                    print(self.getLetter(x, y).char + "*\t", end = "")
                else:
                    print(self.getLetter(x, y).char + "\t", end = "")
            print("")

    def fillRandom(self):
        for x in range(self.lenX):
            for y in range(self.lenY):
                if str(self.getLetter(x, y)) == '-': #If letter is empty, replace it
                    char = chr(random.randint(0,25) + 97)
                    self.setLetter(char, x, y)

    def listToString(self, letters):
        string = ""
        for letter in letters:
            string += letter.char
        return string

    def searchAll(self, customs = 0):
        s = SearchHelper()
        s.clear()
        for x in range(self.lenX):
            for y in range(self.lenY):
                print("Calculating letter (" + str(x) + ", " + str(y) + ").")
                self.search(self.getLetter(x, y), s, customs = customs)
        return s

    def search(self, origin, s = SearchHelper(), customs = 0):
        #s.clear()
        self.recursiveSearch([origin], s, customs = customs)
        return s

    def clear(self):
        self.letters.clear()

    def searchCustom(self, usedLetters, helper, customs = 1):

        for letter in usedLetters[-1].getSurrounding():
            valid = True
            if letter.x >= self.lenX or letter.x < 0: #If x out of bound
                valid = False
            if letter.y >= self.lenY or letter.y < 0: #If y out of bound
                valid = False
            if letter in usedLetters:
                valid = False

            if valid:
                for i in range(26):
                    customLetter = Letter(chr(i + 97), letter.x, letter.y, letter.board, mana = letter.mana, multiplier = letter.multiplier, double = letter.double)
                    string = self.listToString(usedLetters + [customLetter])
                    #print(string)

                    if len(d.findWords(string)) > 0:
                        if (d.isWord(string)):
                            #print("WORD FOUND:" + string)
                            helper.add(usedLetters + [customLetter])
                        self.recursiveSearch(usedLetters + [customLetter], helper, customs - 1)
        
    def recursiveSearch(self, usedLetters, helper, customs = 0):

        if(len(usedLetters) > LENGTH_LIMIT):
            return

        if(customs > 0):
            self.searchCustom(usedLetters, helper, customs = customs)

        for letter in usedLetters[-1].getSurrounding():
            valid = True
            if letter.x >= self.lenX or letter.x < 0: #If x out of bound
                valid = False
            if letter.y >= self.lenY or letter.y < 0: #If x out of bound
                valid = False

            if letter in usedLetters:
                valid = False

            if valid:
                string = self.listToString(usedLetters + [letter])
                #print(string)
                if len(self.d.findWords(string)) > 0: #If new word is possible, continue

                    if (self.d.isWord(string)): #If word is in wordlist output
                        #print("WORD FOUND:" + string)
                        helper.add(usedLetters + [letter])
                    
                    self.recursiveSearch(usedLetters + [letter], helper, customs)

def main():
    d = Dictionary("2of12inf.txt")

    b = Board(5,5, d)

    bests = []

    #b.buildFromString("abcdefghijklmnopqrstuvwxy")
    #b.getLetter(2,2).double = True
    #b.print()
    #print()
    #h = b.search(b.getLetter(0,0), customs = 2)
    #words = sorted(h.getWords(b), key=lambda x: x[0])
    #print(words)
    #print(d.calculations)

    #b.setLetter('x', 0, 0)
    #b.setLetter('y', 1, 1)

    start_time = time.time()
    b.buildFromString(input("Input Board: "))
    y = int(input("Enter Double X (-1 if null): ")) - 1
    x = 5 - int(input("Enter Double Y (-1 if null): "))
    b.getLetter(x, y).double = True
    customs = int(input("Enter number of custom letters: "))
    b.print()
    h = b.searchAll(customs = customs)
    words = sorted(h.getWords(b), key=lambda x: x[0])
    print(words[-1])
    end_time = time.time()
    print(end_time - start_time)
