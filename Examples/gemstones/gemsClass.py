
#--------------------------------
# imports
#--------------------------------
import os
import re
import random
import msvcrt
import time

class gems(object):

    #--------------------------------
    # constructor
    #--------------------------------
    def __init__(self):
        self.isAlive = False
        self.fileName = ""
        
        self.gemSequence = ""
        self.gemBook = {"A":"amethyst", "D":"diamond", "E":"emerald", "R":"ruby", "S":"sapphire", "T":"topaz"}
        self.patternLevel = re.compile(r'[A|D|E|R|S|T]+')
        self.gameCounter = 0
        
        self.missed = 0
        self.guessed = 0

        self.startTime = 0
        self.currentTime = 0
        self.tick = 0
        self.playingTime = 30
        return


    #--------------------------------
    # intro
    #--------------------------------
    def intro(self):
        self.setFile()
        self.loadFile()
        self.setTimer()
        return

    #--------------------------------
    # setTimer
    #--------------------------------
    def setTimer(self):
        self.startTime = time.clock()
        self.currentTime = time.clock()
        return
    
    #--------------------------------
    # loadFile
    #--------------------------------
    def loadFile(self):
        self.clearScreen()
        self.printTitle()
        f = open(self.fileName, 'r')
        seq = f.readline().upper()
        for letter in seq:
            if letter == "A" or letter == "D" or letter == "E" or letter == "R" or letter == "S" or letter == "T":
                self.gemSequence += letter
        f.close()
        print self.gemSequence
        self.isAlive = True
        print "game loaded..."
        raw_input("press enter to continue...")
        return

    #--------------------------------
    # setFile
    #--------------------------------
    def setFile(self):
        while True:
            self.clearScreen()
            self.printTitle()
            self.fileName = raw_input("Enter name of file to load: ")
            if os.path.isfile(self.fileName):
                print "file found!"
                print
                raw_input("press enter to continue...")
                break
            else:
                print "file NOT found!"
                print
                raw_input("press enter to continue...")


    #--------------------------------
    # timeOut
    #--------------------------------
    def timeOut(self):
        done = False

        self.currentTime = time.clock()
        if (self.currentTime - self.startTime) >= 1.0:
            self.tick += 1
            self.startTime = self.currentTime
        if self.tick >= self.playingTime:
            done = True
        
        return done

    #--------------------------------
    # run
    #--------------------------------
    def run(self):
        self.clearScreen()
        self.printTitle()
        
        if self.timeOut():
            self.isAlive = False
        else:
            print self.tick, "/", self.playingTime
            print
            print "amethyst -> purple"
            print "diamond  -> white"
            print "emerald  -> green"
            print "ruby     -> red"
            print "sapphire -> blue"
            print "topaz    -> yellow"
            print
            print self.gemBook[self.gemSequence[self.gameCounter]], "is color?"
            print
            if msvcrt.kbhit():
                i = msvcrt.getch()
                self.gemLogic(self.gemSequence[self.gameCounter],i)
                if self.gameCounter < len(self.gemSequence)-1:
                    self.gameCounter += 1
                else:
                    self.isAlive = False
                        
        return

    #--------------------------------
    # gemLogic
    #--------------------------------
    def gemLogic(self, gem, color):
        if (gem == "A" and color == "p") or (gem == "D" and color == "w") or (gem == "E" and color == "g") or (gem == "R" and color == "r") or (gem == "S" and color == "b") or (gem == "T" and color == "y"):
            self.guessed += 1
        else:
            self.missed += 1
        return

    #--------------------------------
    # print
    #--------------------------------
    def __str__(self):
        self.clearScreen()
        self.printTitle()
        print "total time:", self.tick
        print "guessed:", self.guessed
        print "missed:", self.missed
        print
        return raw_input("press enter to exit...")
    

    #--------------------------------
    # printTitle
    #--------------------------------
    def printTitle(self):
        print "                                /"
        print "   ___.   ___  , _ , _     ____ |"
        print " .'   ` .'   ` |' `|' `.  (     |"
        print " |    | |----' |   |   |  `--.  |"
        print "  `---| `.___, /   '   / \___.' `"
        print "  \___/                         '"
        print "\n"
        return

    #--------------------------------
    # clearScreen
    #--------------------------------
    def clearScreen(self):
        os.system('cls')
        return


#--------------------------------
# main
#--------------------------------
def main():
    print "this is just a class definition!"
    print "please run 'gems.py'..."
    print
    raw_input("press enter to continue...")
    return

if __name__ == "__main__":
    main()
