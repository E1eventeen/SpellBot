import random
from datetime import datetime
import time
import math
random.seed(datetime.now().timestamp())

LENGTH_LIMIT = 10

class Dictionary:
    trace = []
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

    def arrayToStr(self, word):
        output = ""
        for letter in word:
            output += letter.char
        return output

    def outputTrace(self, board, file):
        f = open(file, "w")
        for letter in board.letters:
            f.write(letter.char)
        f.write("\n")
        for trial in self.trace:
            string = ""
            for letter in trial:
                string += letter.char
            isWord = self.isWord(string)
            for letter in trial:
                f.write("[" + str(letter.x) + ":" + str(letter.y) + ":" + letter.char + ":" + str(int(letter.custom)) + ":" + str(int(isWord)) + "],")
            f.write("\n")
        f.close()

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
    custom = False
    
    def __init__(self, char, x, y, board, mana = False, multiplier = 1, double = False, custom = False):
        self.char = char.lower()
        self.x = x
        self.y = y
        self.points = self.letterValues[self.char]
        self.board = board
        self.double = double
        self.multiplier = multiplier
        self.mana = mana
        self.custom = custom
        

    def __str__(self):
        return self.char

    def getSurrounding(self):

        surrounding = []
        
        for xDif in range(-1, 2):
            for yDif in range(-1, 2):
                surrounding.append(self.board.getLetter(self.x + xDif, self.y + yDif))

        surrounding.remove(surrounding[4])
        return surrounding

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

    def clear(self):
        self.letters.clear()

    def lettersInBoard(self, string):
        chars = []
        for letter in self.letters:
            chars.append(letter.char)
        for letter in string:
            if not letter in chars:
                return False
            chars.remove(letter)
        return True

    def wordInBoard(self, string, usedLetters = []):

        #print("Checking if " + string + " is in board without letters " + d.arrayToStr(usedLetters))
        
        if not self.lettersInBoard(string):
            return False

        if string == "":
            return True

        if usedLetters == []:
            for letter in self.letters:
                if string[0] == letter.char and not letter in usedLetters:
                    if self.wordInBoard(string[1:], usedLetters = usedLetters + [letter]):
                        return True
        else:
            for letter in usedLetters[-1].getSurrounding():
                if string[0] == letter.char and not letter in usedLetters:
                    if self.wordInBoard(string[1:], usedLetters = usedLetters + [letter]):
                        return True

    def letterInLocations(self, letter, usedLetters):
        for checkLetter in usedLetters:
            if checkLetter.x == letter.x and checkLetter.y == letter.y:
                return True
        return False

    def wordInBoardCust(self, string, customs, usedLetters = []):
        #print("Checking if " + string + " is in board with " + str(customs) + " customs without letters " + d.arrayToStr(usedLetters))
        
        if customs == 0 and not self.lettersInBoard(string):
            return False

        if string == "":
            return usedLetters

        if usedLetters == []: #First Iteration
            for letter in self.letters:
                #print("Checking starting letter " + letter.char)
                if string[0] == letter.char and not self.letterInLocations(letter, usedLetters):
                    n = self.wordInBoardCust(string[1:], customs, usedLetters + [letter])
                    if n == False:
                        return n
                    return n
        else: 
            for letter in usedLetters[-1].getSurrounding():
                if letter.x >= self.lenX or letter.x < 0:
                    continue
                if letter.y >= self.lenY or letter.y < 0:
                    continue
                
                if not self.letterInLocations(letter, usedLetters):
                    if string[0] == letter.char:
                        n = self.wordInBoardCust(string[1:], customs, usedLetters + [letter])
                        if n:
                            return n
                    elif customs > 0: #Try custom letter
                        n = self.wordInBoardCust(string[1:], customs - 1, usedLetters + [Letter(string[0], letter.x, letter.y, letter.board, mana = letter.mana, multiplier = letter.multiplier, double = letter.double, custom = True)])
                        if n:
                            return n
        return False

    def searchAll(self, customLetters):
        possibleWords = []
        i = 0
        for word in self.d.words:
            i += 1
            if i % 818 == 0:
                print(i / 81833 * 100.0)
            
            n = self.wordInBoardCust(word, customs = customLetters)
            if n:
                possibleWords.append(n)
        return possibleWords

    
def printLoadBar(x, y):
    print(str(math.floor(x / y * 100.0)) + "% \t- <|", end = "")
    for i in range(x):
        print("⬛", end = "")
    for i in range(y - x):
        print("⬜", end = "")
    print("|>")


"""
start_time = time.time()
d = Dictionary("2of12inf.txt")

b = Board(5,5, d)

b.buildFromString("abcdefghijklmnopqrstuvwxy")
b.getLetter(2,2).double = True
b.print()


print()
words = []
wordList = b.searchAll(0)
for word in wordList:
    words.append([d.arrayToStr(word), d.wordValue(word)])

words = sorted(words, key=lambda x: x[1])
print(words[-1])

end_time = time.time()
print(end_time - start_time)

    #h = b.search(b.getLetter(0,0), customs = 2)
    #words = sorted(h.getWords(b), key=lambda x: x[0])
    #print(words)
    #print(d.calculations)

    #b.setLetter('x', 0, 0)
    #b.setLetter('y', 1, 1)

    #start_time = time.time()
    #b.buildFromString(input("Input Board: "))
    #y = int(input("Enter Double X (-1 if null): ")) - 1
    #x = 5 - int(input("Enter Double Y (-1 if null): "))
    #b.getLetter(x, y).double = True
    #customs = int(input("Enter number of custom letters: "))
    #b.print()
    #h = b.searchAll(customs = customs)
    #words = sorted(h.getWords(b), key=lambda x: x[0])
    #print(words[-1])
    #end_time = time.time()
    #print(end_time - start_time)"""

