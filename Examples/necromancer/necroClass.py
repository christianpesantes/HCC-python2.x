
import os
import random

class necro(object):

    #------------------------------------------------------
    # contructor
    #------------------------------------------------------
    def __init__ (self):

        # system variables
        self.isAlive = True
        self.command = ""

        # character variables
        self.name     = ""
        self.tupNames = ("Alpha", "Beta", "Gamma", "Delta", "Epsilon", "Zeta")

        # minions & resources variables
        # "corpses":0, "mana":1, "health":2, "successRate":3, "manaBonus":4, "healthBonus":5
        self.resources   = [ 10,  50,  50]
        self.castMage    = [  1,  10,   5,   25]
        self.castGolem   = [  1,   0,  15,   75]
        self.castGoblin  = [  1,   5,   5,   50]
        self.castCarrion = [  1,   0,   0,  100,  20,  20]

        # records variables
        self.dictMinions  = {"mage" : 0, "golem" : 0, "goblin" : 0}
        self.totalMinions = {"mage" : 0, "golem" : 0, "goblin" : 0}       
        
        return

    #------------------------------------------------------
    # intro
    #------------------------------------------------------
    def intro (self):

        self.setupGame()
        
        if self.isAlive:
            self.setupName()
            
        return

    #------------------------------------------------------
    # run
    #------------------------------------------------------
    def run (self):

        self.runMenu()
            
        if self.command == '1':
            self.summonMage()
            
        elif self.command == '2':
            self.summonGolem()
            
        elif self.command == '3':
            self.summonGoblin()
            
        elif self.command == '4':
            self.carrionEater()
            
        elif self.command == '5':
            self.commitSuicide()
            
        elif self.command == '6':
            self.restartGame()

        else:
            self.skillsInfoMenu()
            self.skillsInfoProcess()
            
        return


    #------------------------------------------------------
    # print object
    #------------------------------------------------------
    def __str__ (self):
        
        self.clearScreen()
        self.printTitle()
        print "--------------------- GAME OVER ------------------------"
        print self.name
        print "total mages   ::", self.totalMinions["mage"]
        print "total golems  ::", self.totalMinions["golem"]
        print "total goblins ::", self.totalMinions["goblin"]
        print "total minions ::", self.totalMinions["mage"] + self.totalMinions["golem"] + self.totalMinions["goblin"]
        print
        return raw_input("press any key to continue...")


    #------------------------------------------------------
    # supporting methods
    #------------------------------------------------------

    #--------------------------
    # print title
    #--------------------------
    def printTitle(self):

        print
        print "_  _ _ _  _ _ ____ _  _    _  _ ____ ____ ___ ____ ____ "
        print "|\/| | |\ | | |  | |\ |    |\/| |__| [__   |  |___ |__/ "
        print "|  | | | \| | |__| | \|    |  | |  | ___]  |  |___ |  \ "
        print
        print
        return


    #--------------------------
    # clear screen
    #--------------------------
    def clearScreen(self):

        os.system("cls")
        return


    #--------------------------
    # validate input
    #--------------------------
    def validInput(self, x):

        self.command = raw_input("input: ").lower()
        if self.command.isdigit() and not ( int(self.command)>x or int(self.command)<1 ):
            return True
        else:
            return False


    #--------------------------
    # setup game
    #--------------------------
    def setupGame(self):

        while True:
            self.clearScreen()
            self.printTitle()
            print "[1] :: start game"
            print "[2] :: exit"
            print
            if not self.validInput(2):
                print
                raw_input("invalid input! try again!")
                continue
            else:
                break
        if self.command == '1':
            self.isAlive = True
        else:
            self.isAlive = False
        return


    #--------------------------
    # setup name
    #--------------------------
    def setupName(self):

        while True:
            self.clearScreen()
            self.printTitle()
            print "[1] :: enter name"
            print "[2] :: continue with random name"
            print
            if not self.validInput(2):
                print
                raw_input("invalid input! try again!")
                continue
            else:
                break
        self.clearScreen()
        self.printTitle()
        if self.command == '1':
            self.name = raw_input("enter name: ")
        else:
            self.name = random.choice(self.tupNames)
        return


    #--------------------------
    # run menu
    #--------------------------
    def runMenu(self):
        
        while True:
            self.clearScreen()
            self.printTitle()
            print "-------------------- PLAYER INFO -----------------------"
            print self.name
            print "mages   ::", self.dictMinions["mage"]
            print "golems  ::", self.dictMinions["golem"]
            print "goblins ::", self.dictMinions["goblin"]
            print "total   ::", self.dictMinions["mage"] + self.dictMinions["golem"] + self.dictMinions["goblin"]
            print
            print "--------------------- RESOURCES ------------------------"
            print "corpses ::", self.resources[0]
            print "mana    ::", self.resources[1]
            print "health  ::", self.resources[2]
            print
            print "------------------ SKILLS & COMMANDS -------------------"
            print "[1] :: skeletal mage"
            print "[2] :: flesh golem"
            print "[3] :: grim goblin"
            print "[4] :: carrion eater"
            print "[5] :: suicide"
            print "[6] :: restart"
            print "[7] :: more info about skills"
            print
            if not self.validInput(7):
                print
                raw_input("invalid input! try again!")
            else:
                break
        return

    #--------------------------
    # summon mage
    #--------------------------
    def summonMage(self):

        if self.resources[0] >= self.castMage[0] and self.resources[1] >= self.castMage[1] and self.resources[2] > self.castMage[2]:
            rand = random.randint(1,101)
            chance = rand + self.castMage[3]
            self.resources[0] = self.resources[0] - self.castMage[0]
            self.resources[1] = self.resources[1] - self.castMage[1]
            self.resources[2] = self.resources[2] - self.castMage[2]
            if chance > 100:
                self.dictMinions["mage"] += 1
                self.totalMinions["mage"] += 1
                print
                raw_input("raising a skeletal mage! press any key to continue...")
            else:
                print
                raw_input("whoops! bad luck, spell failed! press any key to continue...")
        else:
            print
            raw_input("you must construct additional pylons! press any key to continue...")
        return


    #--------------------------
    # summon golem
    #--------------------------
    def summonGolem(self):
        if self.resources[0] >= self.castGolem[0] and self.resources[1] >= self.castGolem[1] and self.resources[2] > self.castGolem[2]:
            rand = random.randint(1,101)
            chance = rand + self.castGolem[3]
            self.resources[0] = self.resources[0] - self.castGolem[0]
            self.resources[1] = self.resources[1] - self.castGolem[1]
            self.resources[2] = self.resources[2] - self.castGolem[2]
            if chance > 100:
                self.dictMinions["golem"] += 1
                self.totalMinions["golem"] += 1
                print
                raw_input("raising a flesh golem! press any key to continue...")
            else:
                print
                raw_input("whoops! bad luck, spell failed! press any key to continue...")
        else:
            print
            raw_input("you require more vespene gas! press any key to continue...")
        return


    #--------------------------
    # summon goblin
    #--------------------------
    def summonGoblin(self):
        if self.resources[0] >= self.castGoblin[0] and self.resources[1] >= self.castGoblin[1] and self.resources[2] > self.castGoblin[2]:
            rand = random.randint(1,101)
            chance = rand + self.castGoblin[3]
            self.resources[0] = self.resources[0] - self.castGoblin[0]
            self.resources[1] = self.resources[1] - self.castGoblin[1]
            self.resources[2] = self.resources[2] - self.castGoblin[2]
            if chance > 100:
                self.dictMinions["goblin"] += 1
                self.totalMinions["goblin"] += 1
                print
                raw_input("raising a grim goblin! press any key to continue...")
            else:
                print
                raw_input("whoops! bad luck, spell failed! press any key to continue...")
        else:
            print
            raw_input("not enough minerals! press any key to continue...")
        return


    #--------------------------
    # consume corpse
    #--------------------------
    def carrionEater(self):

        if self.resources[0] >= self.castCarrion[0] and self.resources[1] >= self.castCarrion[1] and self.resources[2] > self.castCarrion[2]:
            rand = random.randint(1,101)
            chance = rand + self.castCarrion[3]
            self.resources[0] = self.resources[0] - self.castCarrion[0]
            if chance > 100:
                self.resources[1] = self.resources[1] + self.castCarrion[4]
                self.resources[2] = self.resources[2] + self.castCarrion[5]
                print
                raw_input("consuming corpse! press any key to continue...")
            else:
                print
                raw_input("whoops! bad luck, spell failed! press any key to continue...")
        else:
            print
            raw_input("spawn more overloards! press any key to continue...")
        return


    #--------------------------
    # quit game
    #--------------------------
    def commitSuicide(self):

        self.isAlive = False
        print
        raw_input("game over! press any key to continue...")
        return

    
    #--------------------------
    # restart game
    #--------------------------
    def restartGame(self):
        
        self.resources = [10,50,50]
        self.dictMinions["mage"] = 0
        self.dictMinions["golem"] = 0
        self.dictMinions["goblin"] = 0
        print
        raw_input("restarting game! press any key to continue...")
        return


    #--------------------------
    # skills info menu
    #--------------------------
    def skillsInfoMenu(self):

        while True:
            self.clearScreen()
            self.printTitle()
            print "[1] :: skeletal mage"
            print "[2] :: flesh golem"
            print "[3] :: grim goblin"
            print "[4] :: carrion eater"
            print "[5] :: go back"
            print
            if not self.validInput(5):
                print
                raw_input("invalid input! try again!")
            else:
                break
        return


    #--------------------------
    # skills info process
    #--------------------------
    def skillsInfoProcess(self):

        self.clearScreen()
        self.printTitle()
        if self.command == '1':
            print "skeletal mage"
            print "     casting :: " + str(self.castMage[3]) + "% success rate"
            print "     cost    :: " + str(self.castMage[0]) + "cp, " + str(self.castMage[1]) + "mp, " + str(self.castMage[2]) +"hp"
            print "     result  :: summon mage"
            print
        elif self.command == '2':
            print "flesh golem"
            print "     casting :: " + str(self.castGolem[3]) + "% success rate"
            print "     cost    :: " + str(self.castGolem[0]) + "cp, " + str(self.castGolem[1]) + "mp, " + str(self.castGolem[2]) +"hp"
            print "     result  :: summon golem"
            print
        elif self.command == '3':
            print "grim goblin"
            print "     casting :: " + str(self.castGoblin[3]) + "% success rate"
            print "     cost    :: " + str(self.castGoblin[0]) + "cp, " + str(self.castGoblin[1]) + "mp, " + str(self.castGoblin[2]) +"hp"
            print "     result  :: summon goblin"
            print
        elif self.command == '4':
            print "carrion eater"
            print "     casting :: " + str(self.castCarrion[3]) + "% success rate"
            print "     cost    :: " + str(self.castCarrion[0]) + "cp, " + str(self.castCarrion[1]) + "mp, " + str(self.castCarrion[2]) + "hp"
            print "     result  :: +" + str(self.castCarrion[4]) + "mp, +" + str(self.castCarrion[5]) + "hp"
            print
        else:
            print
        raw_input("press any key to go back...")
        return

if __name__ == "__main__":
    print "import this file instead!"
    raw_input("press ENTER to exit...")
