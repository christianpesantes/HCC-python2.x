

#                                           imports
#----------------------------------------------------------------
import pygame
import random


#                                           Enemy
#----------------------------------------------------------------
class Enemy(object):

    def __init__(self, texture, speed, lanes, windowSize):
        self.sprite = pygame.sprite.Sprite()
        self.sprite.image = texture
        self.sprite.rect = self.sprite.image.get_rect()
        self.lane = random.randint(0,4)

        self.position = [windowSize[0]+self.sprite.rect[2],lanes[self.lane][1]]
        self.sprite.rect.left = self.position[0]
        self.sprite.rect.top = self.position[1]
        
        self.speed = speed * -1
        return

    def timeToDelete(self, timePassed):
        self.position[0] += self.speed * timePassed
        self.sprite.rect.right = self.position[0]
        if self.sprite.rect.right <= 0:
            return True
        else:
            return False


#                                           Shell
#----------------------------------------------------------------
class Shell(object):

    def __init__(self, texture, speed, lane, windowSize, ln, color):
        self.sprite = pygame.sprite.Sprite()
        self.sprite.image = texture
        self.sprite.rect = self.sprite.image.get_rect()
        self.position = [lane[0],lane[1]]
        self.sprite.rect.left = self.position[0]
        self.sprite.rect.top = self.position[1]
        self.lane = ln
        self.color = color
        self.speed = speed
        self.limit = windowSize[0]
        return

    def timeToDelete(self, timePassed):
        self.position[0] += self.speed * timePassed
        self.sprite.rect.left = self.position[0]
        if self.sprite.rect.left >= self.limit:
            return True
        else:
            return False


#                                           Star
#----------------------------------------------------------------
class Star(object):

    def __init__(self, texture, sound, windowSize):
        self.sprite = pygame.sprite.Sprite()
        self.sprite.image = texture
        self.sprite.image = pygame.transform.scale(self.sprite.image,[50,45])
        self.sprite.rect = self.sprite.image.get_rect()

        x = random.randint(200,windowSize[0]-100)
        self.position = [x,-45]
        self.sprite.rect.left = self.position[0]
        self.sprite.rect.top = self.position[1]

        self.clickSound = sound  
        return

    def isClicked(self, mouse):
        click = False
        if self.sprite.rect.collidepoint(mouse):
            self.clickSound.play()  
            click = True
        return click


#                                           Countdown
#----------------------------------------------------------------
class Countdown(object):

    def __init__(self):
        self.startTime = pygame.time.get_ticks()
        self.finalTime = pygame.time.get_ticks()
        self.countdown = 0
        self.tick = 0
        return

    def update(self):
        rtrn = False
        self.finalTime = pygame.time.get_ticks()
        deltaTime = self.finalTime - self.startTime
        if deltaTime >= 1000.0:
            self.tick -= 1
            self.startTime = self.finalTime
            if self.tick < 0:
                rtrn = True
                self.countdown -= 3
                if self.countdown <= 3:
                    self.countdown = 3
                self.tick = self.countdown
        return rtrn


#                                           Icon
#----------------------------------------------------------------
class Icon(object):

    def __init__(self):
        self.sprite = pygame.sprite.Sprite()
        self.font = pygame.font.SysFont("arial", 20);
        self.font.set_bold(True)
        self.price = 0
        self.priceText = self.font.render(str(self.price),True,[255,255,255])
        return


#                                           ShellShock
#----------------------------------------------------------------
class ShellShock(object):
    
    def __init__(self):
        pygame.init()
        self.windowSize = [800,600]
        self.screen = pygame.display.set_mode(self.windowSize,pygame.NOFRAME,32)
        self.running = True
        self.backgroundImage = 0

        self.fontSm = pygame.font.SysFont("arial", 15);
        self.fontSm.set_bold(True)
        self.fontLg = pygame.font.SysFont("arial", 30);
        self.fontLg.set_bold(True)

        self.lives = 100
        self.livesText = self.fontLg.render(str(self.lives),True,[255,255,255])

        self.starCount = 300
        self.starCountText = self.fontLg.render(str(self.starCount),True,[255,255,255])
        self.fallingStars = []
        self.starSpeed = 0.10

        self.shellectionTextures = {"green":0,"red":0,"blue":0,"bowser":0}
        self.shellectionShow = "green"
        self.shellectionLane = 4
        self.shellectionLaneOptions = {0:[10,105],1:[10,185],2:[10,265],3:[10,345],4:[10,425]}

        self.enemies = {"goomba":0,"boo":0,"chomp":0}

        self.shootingShells = []
        self.shellSpeed = 0.75

        self.goombas = []
        self.goombaSpeed = 0.05

        self.boos = []
        self.booSpeed = 0.05

        self.chomps = []
        self.chompSpeed = 0.05

        self.clock = pygame.time.Clock()
        self.timePassed = 0
        self.fpsText = ""
        self.starText = ""
        self.goombaText = ""
        self.booText = ""
        self.chompText = ""

        self.items = ["green", "red", "blue", "bowser", "goomba", "boo", "chomp", "star", "mushroom"]
        self.textures = {}
        self.icons = {}
        self.countdowns = {"goomba":Countdown(),"boo":Countdown(),"chomp":Countdown(),"star":Countdown()}
        for i in self.items:
            self.textures[i] = 0
            self.icons[i] = Icon()

        self.soundEffects = {"star":0, "shell":0}

        self.clickPos = [0,0]
        self.mousePos = pygame.mouse.get_pos()
        self.cursorImage = 0
        
        return


    def setup(self):  
        self.backgroundImage = pygame.image.load("pics/background.png").convert()
        self.backgroundImage = pygame.transform.scale(self.backgroundImage,[700,400])

        self.cursorImage = pygame.image.load("pics/cursor.png").convert_alpha()
        self.cursorImage = pygame.transform.scale(self.cursorImage,[30,25])
        pygame.mouse.set_visible(False)

        self.soundEffects["star"] = pygame.mixer.Sound("sounds/star.wav")
        self.soundEffects["shell"] = pygame.mixer.Sound("sounds/shell.wav")

        for i in self.items:
            self.textures[i] = pygame.image.load("pics/"+i+".png").convert_alpha()

        enemy = "goomba"
        self.enemies[enemy] = self.textures[enemy]
        self.enemies[enemy] = pygame.transform.scale(self.enemies[enemy],[70,65])
        self.enemies[enemy] = pygame.transform.flip(self.enemies[enemy], False, False)

        enemy = "boo"
        self.enemies[enemy] = self.textures[enemy]
        self.enemies[enemy] = pygame.transform.scale(self.enemies[enemy],[70,65])
        self.enemies[enemy] = pygame.transform.flip(self.enemies[enemy], False, False)

        enemy = "chomp"
        self.enemies[enemy] = self.textures[enemy]
        self.enemies[enemy] = pygame.transform.scale(self.enemies[enemy],[120,65])
        self.enemies[enemy] = pygame.transform.flip(self.enemies[enemy], True, False)

        shell = "green"
        self.shellectionTextures[shell] = self.textures[shell]
        self.shellectionTextures[shell] = pygame.transform.scale(self.shellectionTextures[shell],[70,65])
        self.shellectionTextures[shell] = pygame.transform.flip(self.shellectionTextures[shell], True, False)
        
        shell = "red"
        self.shellectionTextures[shell] = self.textures[shell]
        self.shellectionTextures[shell] = pygame.transform.scale(self.shellectionTextures[shell],[70,65])
        self.shellectionTextures[shell] = pygame.transform.flip(self.shellectionTextures[shell], False, False)

        shell = "blue"
        self.shellectionTextures[shell] = self.textures[shell]
        self.shellectionTextures[shell] = pygame.transform.scale(self.shellectionTextures[shell],[80,75])
        self.shellectionTextures[shell] = pygame.transform.flip(self.shellectionTextures[shell], True, False)

        shell = "bowser"
        self.shellectionTextures[shell] = self.textures[shell]
        self.shellectionTextures[shell] = pygame.transform.scale(self.shellectionTextures[shell],[80,75])
        self.shellectionTextures[shell] = pygame.transform.flip(self.shellectionTextures[shell], True, False)

        self.setupIcon("star",[50,45],False,530,20,0)
        self.setupIcon("mushroom",[50,45],False,530,220,0)
        self.setupIcon("green",[70,65],False,10,100,5)
        self.setupIcon("red",[70,65],True,10,250,10)
        self.setupIcon("blue",[70,65],False,10,400,25)
        self.setupIcon("bowser",[70,65],False,10,550,100)

        self.countdowns["star"].countdown = 10
        self.countdowns["goomba"].countdown = 10
        self.countdowns["boo"].countdown = 15
        self.countdowns["chomp"].countdown = 20

        pygame.mixer.music.load("sounds/music.mp3")
        pygame.mixer.music.set_volume(1.0)
        pygame.mixer.music.play(-1)
        return

    def setupIcon(self,symbol,scale,flip,top,left, price):
        self.icons[symbol].sprite.image = self.textures[symbol]
        self.icons[symbol].sprite.image = pygame.transform.scale(self.icons[symbol].sprite.image,scale)
        self.icons[symbol].sprite.image = pygame.transform.flip(self.icons[symbol].sprite.image, flip, False)
        self.icons[symbol].sprite.rect = self.icons[symbol].sprite.image.get_rect()
        self.icons[symbol].sprite.rect.top = top
        self.icons[symbol].sprite.rect.left = left
        self.icons[symbol].price = price
        self.icons[symbol].priceText = self.icons[symbol].font.render(str(self.icons[symbol].price),True,[255,255,255])
        return

    def update(self):
        self.updateClocks()
        self.updateEvents()
        self.updateShellection()
        self.updateStars()
        self.updateShootingShells()
        self.updateEnemies()
        self.updateCollisions()
        return

    def updateCollisions(self):
        for s in xrange(len(self.shootingShells)):
            for gm in xrange(len(self.goombas)):
                if pygame.sprite.collide_rect(self.shootingShells[s].sprite,self.goombas[gm].sprite) and self.shootingShells[s].lane == self.goombas[gm].lane:
                    if self.shootingShells[s].color != "bowser":
                        del(self.shootingShells[s])
                    del(self.goombas[gm])
                    self.starCount += 25
                    self.soundEffects["shell"].play()
                    return
            for bo in xrange(len(self.boos)):
                if pygame.sprite.collide_rect(self.shootingShells[s].sprite,self.boos[bo].sprite) and self.shootingShells[s].lane == self.boos[bo].lane:
                    if self.shootingShells[s].color != "green":
                        del(self.boos[bo])
                        self.soundEffects["shell"].play()
                        self.starCount += 50
                        if self.shootingShells[s].color == "blue" or self.shootingShells[s].color == "red":
                            del(self.shootingShells[s])
                    return
            for ch in xrange(len(self.chomps)):
                if pygame.sprite.collide_rect(self.shootingShells[s].sprite,self.chomps[ch].sprite) and self.shootingShells[s].lane == self.chomps[ch].lane:
                    if self.shootingShells[s].color == "green" or self.shootingShells[s].color == "red":
                        del(self.shootingShells[s])
                        self.soundEffects["shell"].play()
                        self.chomps[ch].speed -= 0.2
                    elif self.shootingShells[s].color == "blue":
                        del(self.shootingShells[s])
                        self.soundEffects["shell"].play()
                        del(self.chomps[ch])
                        self.starCount += 10
                    elif self.shootingShells[s].color == "bowser":
                        del(self.chomps[ch])
                        self.soundEffects["shell"].play()
                        self.starCount += 50
                    return
        return

    def updateEnemies(self):
        for i in xrange(len(self.goombas)):
            if self.goombas[i].timeToDelete(self.timePassed):
                del(self.goombas[i])
                self.lives -= 1
                if self.lives <= 0:
                    self.lives = 0
                break

        for i in xrange(len(self.boos)):
            if self.boos[i].timeToDelete(self.timePassed):
                del(self.boos[i])
                self.lives -= 1
                if self.lives <= 0:
                    self.lives = 0
                break

        for i in xrange(len(self.chomps)):
            if self.chomps[i].timeToDelete(self.timePassed):
                del(self.chomps[i])
                self.lives -= 1
                if self.lives <= 0:
                    self.lives = 0
                break
        return

    def updateShootingShells(self):
        for i in xrange(len(self.shootingShells)):
            if self.shootingShells[i].timeToDelete(self.timePassed):
                del(self.shootingShells[i])
                break
        return

    def updateShellection(self):
        if self.mousePos[1] >= 0 and self.mousePos[1] <= self.shellectionLaneOptions[1][1]:
            self.shellectionLane = 0
        elif self.mousePos[1] >= self.shellectionLaneOptions[1][1] and self.mousePos[1] <= self.shellectionLaneOptions[2][1]:
            self.shellectionLane = 1
        elif self.mousePos[1] >= self.shellectionLaneOptions[2][1] and self.mousePos[1] <= self.shellectionLaneOptions[3][1]:
            self.shellectionLane = 2
        elif self.mousePos[1] >= self.shellectionLaneOptions[3][1] and self.mousePos[1] <= self.shellectionLaneOptions[4][1]:
            self.shellectionLane = 3
        elif self.mousePos[1] >= self.shellectionLaneOptions[4][1]:
            self.shellectionLane = 4
        return

    def changeShellection(self,up):
        if up:
            if self.shellectionShow == "green":
                self.shellectionShow = "bowser"
            elif self.shellectionShow == "bowser":
                self.shellectionShow = "blue"
            elif self.shellectionShow == "blue":
                self.shellectionShow = "red"
            elif self.shellectionShow == "red":
                self.shellectionShow = "green"           
        else:
            if self.shellectionShow == "green":
                self.shellectionShow = "red"
            elif self.shellectionShow == "red":
                self.shellectionShow = "blue"
            elif self.shellectionShow == "blue":
                self.shellectionShow = "bowser"
            elif self.shellectionShow == "bowser":
                self.shellectionShow = "green"      
        return

    def shellShoot(self):
        if self.starCount >= self.icons[self.shellectionShow].price:
            self.starCount -= self.icons[self.shellectionShow].price
            self.shootingShells.append(Shell(self.shellectionTextures[self.shellectionShow],self.shellSpeed,self.shellectionLaneOptions[self.shellectionLane],self.windowSize,self.shellectionLane,self.shellectionShow))
        return

    def updateEvents(self):
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    self.clickPos = pygame.mouse.get_pos()
                if event.button == 3:
                    self.shellShoot()
                if event.button == 4:
                    self.changeShellection(True)
                if event.button == 5:
                    self.changeShellection(False)
        self.mousePos = pygame.mouse.get_pos()
        return

    def updateStars(self):
        for i in xrange(len(self.fallingStars)):
            self.fallingStars[i].position[1] += self.starSpeed * self.timePassed
            self.fallingStars[i].sprite.rect.top = self.fallingStars[i].position[1]
            if self.fallingStars[i].isClicked(self.clickPos):
                self.starCount += 25
                del(self.fallingStars[i])
                break
            elif self.fallingStars[i].sprite.rect.top >= self.windowSize[1]:
                del(self.fallingStars[i])
                break
        self.clickPos = [0,0]
        self.starCountText = self.fontLg.render(str(self.starCount),True,[255,255,255])
        self.livesText = self.fontLg.render(str(self.lives),True,[255,255,255])
        return

    def updateClocks(self):
        self.timePassed = self.clock.tick()
        fps = int(self.clock.get_fps())
        self.fpsText = self.fontSm.render("FPS: "+str(fps),True,[80,80,80])

        if self.countdowns["star"].update():
            self.fallingStars.append(Star(self.textures["star"],self.soundEffects["star"],self.windowSize))

        if self.countdowns["goomba"].update():
            self.goombas.append(Enemy(self.enemies["goomba"],self.goombaSpeed,self.shellectionLaneOptions,self.windowSize))
        
        if self.countdowns["boo"].update():
            self.boos.append(Enemy(self.enemies["boo"],self.booSpeed,self.shellectionLaneOptions,self.windowSize))

        if self.countdowns["chomp"].update():
            self.chomps.append(Enemy(self.enemies["chomp"],self.chompSpeed,self.shellectionLaneOptions,self.windowSize))

        self.starText = self.fontSm.render("new star in: "+str(self.countdowns["star"].tick),True,[80,80,80])
        self.goombaText = self.fontSm.render("new goomba in: "+str(self.countdowns["goomba"].tick),True,[80,80,80])
        self.booText = self.fontSm.render("new boo in: "+str(self.countdowns["boo"].tick),True,[80,80,80])
        self.chompText = self.fontSm.render("new chomp in: "+str(self.countdowns["chomp"].tick),True,[80,80,80])
        return

    def render(self):
        self.renderLayout()
        self.screen.blit(self.shellectionTextures[self.shellectionShow],self.shellectionLaneOptions[self.shellectionLane])
        self.renderEnemies()
        self.renderShells()
        self.renderStars()
        self.screen.blit(self.cursorImage, self.mousePos)
        pygame.display.update()
        return

    def renderEnemies(self):
        for i in self.goombas:
            self.screen.blit(i.sprite.image,i.sprite.rect)

        for i in self.boos:
            self.screen.blit(i.sprite.image,i.sprite.rect)

        for i in self.chomps:
            self.screen.blit(i.sprite.image,i.sprite.rect)
        return

    def renderStars(self):
        for i in self.fallingStars:
            self.screen.blit(i.sprite.image,i.sprite.rect)
        return

    def renderShells(self):
        for i in self.shootingShells:
            self.screen.blit(i.sprite.image,i.sprite.rect)
        return

    def renderLayout(self):
        self.screen.fill([0,0,0])
        self.screen.fill([255,255,255],[0,90,800,420])
        self.screen.fill([80,80,80],[0,100,90,80])
        self.screen.fill([50,50,50],[0,180,90,80])
        self.screen.fill([80,80,80],[0,260,90,80])
        self.screen.fill([50,50,50],[0,340,90,80])
        self.screen.fill([80,80,80],[0,420,90,80])
        self.screen.blit(self.backgroundImage,[100,100])

        self.screen.blit(self.icons["star"].sprite.image,self.icons["star"].sprite.rect)
        self.screen.blit(self.starCountText,[80,538])

        self.screen.blit(self.icons["mushroom"].sprite.image,self.icons["mushroom"].sprite.rect)
        self.screen.blit(self.livesText,[280,538])

        self.screen.blit(self.icons["green"].sprite.image,self.icons["green"].sprite.rect)
        self.screen.blit(self.icons["green"].priceText,[170,50])
        self.screen.blit(self.icons["red"].sprite.image,self.icons["red"].sprite.rect)
        self.screen.blit(self.icons["red"].priceText,[320,50])
        self.screen.blit(self.icons["blue"].sprite.image,self.icons["blue"].sprite.rect)
        self.screen.blit(self.icons["blue"].priceText,[470,50])
        self.screen.blit(self.icons["bowser"].sprite.image,self.icons["bowser"].sprite.rect)
        self.screen.blit(self.icons["bowser"].priceText,[620,50])

        self.screen.blit(self.fpsText,[650,565])
        self.screen.blit(self.starText,[650,525])
        self.screen.blit(self.goombaText,[450,525])
        self.screen.blit(self.booText,[450,545])
        self.screen.blit(self.chompText,[450,565])

        return

    def end(self):
        pygame.quit()
        return


#                                           main
#----------------------------------------------------------------
def main():

    game = ShellShock()
    game.setup()
    
    while game.running:
        
        game.update()
        game.render()
        
    game.end()
    return

if __name__ == "__main__":
    main()
