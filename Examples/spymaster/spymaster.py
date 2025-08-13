
import pygame


class Logo(object):

    def __init__(self):
        self.red = 0
        self.blu = 0
        self.show = 0
        self.pos = [0,0]
        self.isSelected = False
        return

    def __repr__(self):
        return str(self.isSelected)

    def loadImages(self, name):
        self.red = pygame.image.load("pics/red/"+name+".png").convert_alpha()
        self.blu = pygame.image.load("pics/blu/"+name+".png").convert_alpha()
        self.show = self.blu
        return

    def setSize(self, size):
        self.red = pygame.transform.scale(self.red,size)
        self.blu = pygame.transform.scale(self.blu,size)
        self.show = self.blu
        return

class Disguise(object):

    def __init__(self):
        self.image = 0
        self.medic = 0
        return

class Spy(object):

    def __init__(self):
        self.show = 0
        self.pos = [0,0]
        self.index = ["scout",   "soldier", "pyro",
                      "demoman", "heavy",   "engineer",
                      "medic",   "sniper",  "spy",
                      "normal"]
        self.menu = {}
        self.medicChannel = pygame.mixer.Channel(1)
        self.disguisedAs = "normal"
        for i in self.index:
            self.menu[i] = Disguise()
        return

    def setup(self):
        for i in self.index:
            self.loadImages(i)
            self.loadSounds(i)
        self.disguising(self.disguisedAs)
        self.pos = [160,70]
        return

    def loadImages(self, name):
        self.menu[name].image = pygame.image.load("pics/disguise/"+name+".png").convert_alpha()
        return

    def loadSounds(self, name):
        self.menu[name].medic = pygame.mixer.Sound("sounds/medic/"+name+".wav")
        return

    def disguising(self, name):
        self.disguisedAs = name
        self.show = self.menu[self.disguisedAs].image
        return

    def callMedic(self):
        if not self.medicChannel.get_busy():
            self.medicChannel.play(self.menu[self.disguisedAs].medic)
        return

class Spymaster(object):

    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((640,480),0,32)
        pygame.display.set_caption("spymaster!")
        self.running = True
        self.background = 0
        self.fadeImage = 0
        self.fadeIndex = 255
        self.fading = False
        self.font = pygame.font.SysFont("arial",15)
        self.font.set_bold(True)
        self.text1 = self.font.render("scroll up/down to travel around menu", True, [255,255,255])
        self.text2 = self.font.render("left click to disguise", True, [255,255,255])
        self.text3 = self.font.render("right click to undisguise", True, [255,255,255])
        self.text4 = self.font.render("press 'e' to call 'medic!'", True, [255,255,255])
        self.text5 = self.font.render("press 'ESC' to exit", True, [255,255,255])
        self.cloak = 0
        self.cloakChannel = pygame.mixer.Channel(0)
        self.click = 0
        self.spy = Spy()
        self.chosenOne = "spy"
        self.index = ["scout",   "soldier", "pyro",
                      "demoman", "heavy",   "engineer",
                      "medic",   "sniper",  "spy"]
        self.menu = {}
        for i in self.index:
            self.menu[i] = Logo()
        return

    def __repr__(self):
        return str(self.menu)

    def setup(self):
        self.loading()
        for i in self.index:
            self.menu[i].setSize([80,80])
        self.menu["scout"].pos    = [60,80]
        self.menu["soldier"].pos  = [60,160]
        self.menu["pyro"].pos     = [60,240]
        self.menu["demoman"].pos  = [60,320]
        self.menu["heavy"].pos    = [500,80]
        self.menu["engineer"].pos = [500,160]
        self.menu["medic"].pos    = [500,240]
        self.menu["sniper"].pos   = [500,320]
        self.menu["spy"].pos      = [280,400]
        self.choose(self.chosenOne)
        self.spy.setup()
        return

    def choose(self, name):
        for i in self.index:
            self.menu[i].isSelected = False
            self.menu[i].show = self.menu[i].blu
        self.menu[name].isSelected = True
        self.menu[name].show = self.menu[name].red
        return

    def loading(self):
        self.cloak = pygame.mixer.Sound("sounds/cloak.ogg")
        self.cloak.set_volume(0.7)
        self.click = pygame.mixer.Sound("sounds/click.wav")
        pygame.mixer.music.load("sounds/theme.mp3")
        pygame.mixer.music.play(-1)
        pygame.mixer.music.set_volume(0.3)
        self.background = pygame.image.load("pics/blu.jpg").convert()
        self.background = pygame.transform.scale(self.background,[640,480])
        self.background.set_alpha(100,pygame.RLEACCEL)
        self.fadeImage = pygame.image.load("pics/black.jpg").convert()
        self.fadeImage = pygame.transform.scale(self.fadeImage,[640,480])
        for i in self.index:
            self.menu[i].loadImages(i)
        return

    def processEvents(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False
                if event.key == pygame.K_e:
                    self.spy.callMedic()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if not self.cloakChannel.get_busy() and not self.fading and not self.chosenOne == self.spy.disguisedAs:
                        self.cloakChannel.play(self.cloak)
                        self.fading = True
                        self.spy.disguising(self.chosenOne)
                if event.button == 3:
                    if not self.cloakChannel.get_busy() and not self.spy.disguisedAs == "normal" and not self.fading:
                        self.cloakChannel.play(self.cloak)
                        self.fading = True
                        self.spy.disguising("normal")
                if event.button == 4:
                    self.click.play()
                    self.scrollUp()
                if event.button == 5:
                    self.click.play()
                    self.scrollDown()
        return

    def scrollUp(self):
        if self.chosenOne == "scout":
            self.chosenOne = "sniper"
        elif self.chosenOne == "soldier":
            self.chosenOne = "scout"
        elif self.chosenOne == "pyro":
            self.chosenOne = "soldier"
        elif self.chosenOne == "demoman":
            self.chosenOne = "pyro"
        elif self.chosenOne == "heavy":
            self.chosenOne = "spy"
        elif self.chosenOne == "engineer":
            self.chosenOne = "heavy"
        elif self.chosenOne == "medic":
            self.chosenOne = "engineer"
        elif self.chosenOne == "sniper":
            self.chosenOne = "medic"
        elif self.chosenOne == "spy":
            self.chosenOne = "demoman"
        self.choose(self.chosenOne)
        return

    def scrollDown(self):
        if self.chosenOne == "scout":
            self.chosenOne = "soldier"
        elif self.chosenOne == "soldier":
            self.chosenOne = "pyro"
        elif self.chosenOne == "pyro":
            self.chosenOne = "demoman"
        elif self.chosenOne == "demoman":
            self.chosenOne = "spy"
        elif self.chosenOne == "heavy":
            self.chosenOne = "engineer"
        elif self.chosenOne == "engineer":
            self.chosenOne = "medic"
        elif self.chosenOne == "medic":
            self.chosenOne = "sniper"
        elif self.chosenOne == "sniper":
            self.chosenOne = "scout"
        elif self.chosenOne == "spy":
            self.chosenOne = "heavy"
        self.choose(self.chosenOne)
        return

    def update(self):
        self.processEvents()
        return

    def render(self):
        self.screen.blit(self.background,[0,0])
        self.screen.blit(self.text1,[10,10])
        self.screen.blit(self.text4,[10,30])
        self.screen.blit(self.text2,[450,10])
        self.screen.blit(self.text3,[450,30])
        self.screen.blit(self.text5,[10,450])
        for i in self.index:
            self.screen.blit(self.menu[i].show,self.menu[i].pos)
        if not self.fading or self.fadeIndex < 250:
            self.screen.blit(self.spy.show,self.spy.pos)
        if self.fading:
            self.screen.blit(self.fadeImage,[0,0])
            self.fadeImage.set_alpha(self.fadeIndex,pygame.RLEACCEL)
            self.fadeIndex -= 0.5
            if self.fadeIndex <= 0:
                self.fading = False
                self.fadeIndex = 255
        pygame.display.update()
        return

    def end(self):
        pygame.quit()
        return
    

def main():
    
    game = Spymaster()
    game.setup()

    while game.running:
        game.update()
        game.render()

    game.end()
    return

if __name__ == "__main__":
    main()
