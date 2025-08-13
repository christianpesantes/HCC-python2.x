
import pygame
import random


class Zombie(object):

    def __init__(self, texture, windowSize, position, speed):
        texture = pygame.transform.scale(texture,[130,200])
        if speed < 0:
            texture = pygame.transform.flip(texture, True, False)
        self.sprite = pygame.sprite.Sprite()
        self.sprite.image = texture
        self.sprite.rect = self.sprite.image.get_rect()
        self.position = position
        if speed > 0:
            self.position[0] -= self.sprite.image.get_width()
        self.sprite.rect.left = self.position[0]
        self.sprite.rect.top = self.position[1]
        self.speed = speed
        return

    def update(self, timePassed):
        self.position[0] += self.speed * timePassed
        self.sprite.rect.left = self.position[0]
        return

class Countdown(object):

    def __init__(self, countdown, minSpawnTime):
        self.startTime = pygame.time.get_ticks()
        self.finalTime = pygame.time.get_ticks()
        self.countdown = countdown
        self.tick = 0
        self.minSpawnTime = minSpawnTime
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
                self.countdown -= 2
                if self.countdown <= self.minSpawnTime:
                    self.countdown = self.minSpawnTime
                self.tick = self.countdown
        return rtrn


class Redfield(object):

    def __init__(self,texture,windowSize):
        texture = pygame.transform.scale(texture,[100,200])
        self.textures = {"right":pygame.transform.flip(texture, True, False),"left":texture}
        self.sprite = pygame.sprite.Sprite()
        self.sprite.image = self.textures["right"]
        self.sprite.rect = self.sprite.image.get_rect()
        self.position = [windowSize[0]/2-self.sprite.rect[2]/2,self.sprite.rect[3]-self.sprite.rect[3]/3]
        self.sprite.rect.left = self.position[0]
        self.sprite.rect.top = self.position[1]
        self.facing = "right"
        return

    def update(self,cursorPos):
        if cursorPos[0] >= self.position[0]+self.sprite.rect[2]/3:
            self.facing = "right"
        else:
            self.facing = "left"
        self.sprite.image = self.textures[self.facing]
        return


class Bullet(object):

    def __init__(self, texture, windowSize, position, speed):
        self.sprite = pygame.sprite.Sprite()
        self.sprite.image = texture
        self.sprite.rect = self.sprite.image.get_rect()
        self.position = position
        self.sprite.rect.left = self.position[0]
        self.sprite.rect.top = self.position[1]
        self.limit = 0
        self.speed = speed
        if self.speed > 0:
            self.limit = windowSize[0]
        else:
            self.limit = 0
        return

    def update(self, timePassed):
        self.position[0] += self.speed * timePassed
        self.sprite.rect.left = self.position[0]
        if self.speed > 0:
            if self.position[0] > self.limit:
                return True
            else:
                return False
        else:
            if self.position[0] < self.limit:
                return True
            else:
                return False
        return

class Outbreak(object):

    def __init__(self):
        pygame.init()
        self.windowSize = [800,300]
        self.screen = pygame.display.set_mode(self.windowSize,pygame.NOFRAME,32)
        self.backgroundColor = [0,0,0]
        self.backgroundImage = 0
        self.running = True

        self.images = ["redfield","zombie","bullet"]
        self.textures = {}
        
        self.effects = ["shoot","reload"]
        self.sounds = {}
        self.channels = {}

        self.cursor = 0
        self.cursorPos = [0,0]
        self.font = pygame.font.SysFont("arial", 15);

        self.clock = pygame.time.Clock()
        self.clockText = ""
        self.timePassed = 0

        self.ammoMax = 6
        self.ammo = self.ammoMax
        self.ammoText = ""

        self.redfield = 0
        self.bullets = []
        self.zombies = []

        self.bulletsText = ""
        self.zombiesText = ""

        self.bulletSpeed = 10
        self.zombieSpeed = 0.05
        self.zombieGenerator = Countdown(11,0)
        self.zombieGeneratorText = ""
        return

    def setup(self):
        self.font.set_bold(True)
        self.ammoText = self.font.render(" ammo: "+str(self.ammo)+" ",True,[255,0,0],[100,100,100])
        self.clockText = self.font.render(" fps: ",True,[255,0,0],[100,100,100])
        self.zombieGeneratorText = self.font.render(" new zombie in: "+str(self.zombieGenerator.tick)+" ",True,[255,0,0],[100,100,100])
        self.bulletsText = self.font.render(" number of bullets: "+str(len(self.bullets))+" ",True,[255,0,0],[100,100,100])
        self.zombiesText = self.font.render(" number of zombies: "+str(len(self.zombies))+" ",True,[255,0,0],[100,100,100])
        
        pygame.mixer.music.load("sounds/music.mp3")
        pygame.mixer.music.play(-1)
        pygame.mixer.music.set_volume(1.0)
        
        self.backgroundImage = pygame.image.load("pics/background.jpg").convert()
        self.cursor = pygame.image.load("pics/cursor.png").convert_alpha()
        pygame.mouse.set_visible(False)
        
        for i in self.images:
            self.textures[i] = pygame.image.load("pics/"+i+".png").convert_alpha()
        x = 0
        for i in self.effects:
            self.sounds[i] = pygame.mixer.Sound("sounds/"+i+".wav")
            self.channels[i] = pygame.mixer.Channel(x)
            x += 1
        self.redfield = Redfield(self.textures["redfield"],self.windowSize)
        return

    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False
                if event.key == pygame.K_r:
                    if not self.channels["shoot"].get_busy() and not self.channels["reload"].get_busy() and self.ammo < self.ammoMax:
                        self.ammo = self.ammoMax
                        self.channels["reload"].play(self.sounds["reload"])
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if not self.channels["shoot"].get_busy() and not self.channels["reload"].get_busy() and self.ammo <= 0:
                        self.ammo = self.ammoMax
                        self.channels["reload"].play(self.sounds["reload"])
                    elif not self.channels["shoot"].get_busy() and not self.channels["reload"].get_busy() and self.ammo > 0:
                        self.channels["shoot"].play(self.sounds["shoot"])
                        self.ammo -= 1
                        pos = [0,0]
                        speed = self.bulletSpeed
                        if self.redfield.facing == "right":
                            pos = [self.redfield.sprite.rect[0]+self.redfield.sprite.rect[2],self.redfield.sprite.rect[1]+10]
                        else:
                            pos = [self.redfield.sprite.rect[0],self.redfield.sprite.rect[1]+10]
                            speed *= -1
                        self.bullets.append(Bullet(self.textures["bullet"],self.windowSize,pos,speed))
        return

    def clockUpdate(self):
        self.timePassed = self.clock.tick()
        if self.zombieGenerator.update():
            pos = [0,130]
            speed = self.zombieSpeed
            x = random.randint(0,1)
            if x == 1:
                speed *= -1
                pos[0] = self.windowSize[0]  
            self.zombies.append(Zombie(self.textures["zombie"],self.windowSize,pos,speed))
        self.zombieGeneratorText = self.font.render(" new zombie in: "+str(self.zombieGenerator.tick)+" ",True,[255,0,0],[100,100,100])
        return

    def shootingBullets(self):
        for i in xrange(len(self.bullets)):
            if self.bullets[i].update(self.timePassed):
                del(self.bullets[i])
                break   
        return

    def walkingZombies(self):
        for i in xrange(len(self.zombies)):
            if self.zombies[i].update(self.timePassed):
                del(self.zombies[i])
                break
        return

    def cursorUpdate(self):
        self.cursorPos = list(pygame.mouse.get_pos())
        r = self.cursor.get_rect()
        self.cursorPos[0] -= r[2]/2
        self.cursorPos[1] = self.windowSize[1]/2
        return

    def updateTexts(self):
        if self.channels["reload"].get_busy():
            self.ammoText = self.font.render(" ammo: reloading ",True,[255,0,0],[100,100,100])
        else:
            self.ammoText = self.font.render(" ammo: "+str(self.ammo)+" ",True,[255,0,0],[100,100,100])

        fps = int(self.clock.get_fps())
        self.clockText = self.font.render(" fps: "+str(fps)+" ",True,[255,0,0],[100,100,100])
        self.redfield.update(self.cursorPos)
        self.bulletsText = self.font.render(" number of bullets: "+str(len(self.bullets))+" ",True,[255,0,0],[100,100,100])
        self.zombiesText = self.font.render(" number of zombies: "+str(len(self.zombies))+" ",True,[255,0,0],[100,100,100])
        return

    def update(self):
        self.events()
        self.clockUpdate()
        self.shootingBullets()
        self.walkingZombies()
        self.collisions()
        self.cursorUpdate()
        self.updateTexts()        
        return

    def collisions(self):
        for i in xrange(len(self.bullets)):
            for x in xrange(len(self.zombies)):
                if self.bullets[i].speed > 0 and self.zombies[x].speed < 0:
                    if pygame.sprite.collide_rect(self.bullets[i].sprite,self.zombies[x].sprite) or self.bullets[i].position[0] > self.zombies[x].position[0]+self.zombies[x].sprite.rect[2]/2:
                        del(self.bullets[i])
                        del(self.zombies[x])
                        return
                elif self.bullets[i].speed < 0 and self.zombies[x].speed > 0:
                    if pygame.sprite.collide_rect(self.bullets[i].sprite,self.zombies[x].sprite) or self.bullets[i].position[0] < self.zombies[x].position[0]+self.zombies[x].sprite.rect[2]/2:
                        del(self.bullets[i])
                        del(self.zombies[x])
                        return
        for x in xrange(len(self.zombies)):
            if pygame.sprite.collide_rect(self.zombies[x].sprite,self.redfield.sprite):
                del(self.zombies[x])
                return
        return

    def render(self):
        self.screen.fill(self.backgroundColor)
        self.screen.blit(self.backgroundImage,[0,0])
        self.screen.blit(self.redfield.sprite.image,self.redfield.sprite.rect)
        for i in self.bullets:
            self.screen.blit(i.sprite.image,i.sprite.rect)
        for i in self.zombies:
            self.screen.blit(i.sprite.image,i.sprite.rect)
        self.screen.blit(self.ammoText,[10,10])
        self.screen.blit(self.clockText,[700,10])
        self.screen.blit(self.zombieGeneratorText,[10,30])
        self.screen.blit(self.bulletsText,[320,10])
        self.screen.blit(self.zombiesText,[320,30])
        self.screen.blit(self.cursor,self.cursorPos)
        pygame.display.update()
        return

    def end(self):
        pygame.quit()
        return

def main():

    game = Outbreak()
    game.setup()

    while game.running:      
        game.update()
        game.render()

    game.end()
    return

if __name__ == "__main__":
    main()
