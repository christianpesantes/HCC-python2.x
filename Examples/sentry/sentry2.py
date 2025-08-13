
import pygame
import math
import random

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
    
class Bullet(object):

    def __init__(self,texture,position,destination):
        self.sprite = pygame.sprite.Sprite()
        self.sprite.image = texture
        self.sprite.rect = self.sprite.image.get_rect()
        self.position = position
        self.sprite.rect.left = self.position[0]
        self.sprite.rect.top = self.position[1]
        self.speed = 0.5
        self.destination = destination
        self.trayectory = [self.destination[0]-self.position[0],self.destination[1]-self.position[1]]
        self.magnitude = math.sqrt(self.trayectory[0]**2+self.trayectory[1]**2)
        self.normalizedVect = self.trayectory
        self.normalizedVect[0] /= self.magnitude
        self.normalizedVect[1] /= self.magnitude
        return

    def update(self,timePassed):
        self.trayectory = [self.destination[0]-self.position[0],self.destination[1]-self.position[1]]
        self.magnitude = math.sqrt(self.trayectory[0]**2+self.trayectory[1]**2)
        distanceMoved = timePassed * self.speed
        temp = [self.normalizedVect[0]*distanceMoved,self.normalizedVect[1]*distanceMoved]
        self.position[0] += temp[0]
        self.position[1] += temp[1]
        self.sprite.rect.left = self.position[0]-self.sprite.rect[2]/2
        self.sprite.rect.top = self.position[1]-self.sprite.rect[3]/2
        return

class Bomb(object):

    def __init__(self,texture,position,destination):
        self.sprite = pygame.sprite.Sprite()
        self.sprite.image = texture
        self.sprite.rect = self.sprite.image.get_rect()
        self.position = position
        self.sprite.rect.left = self.position[0]
        self.sprite.rect.top = self.position[1]

        self.speed = 0.05
        self.destination = destination
        self.trayectory = [self.destination[0]-self.position[0],self.destination[1]-self.position[1]]
        self.magnitude = math.sqrt(self.trayectory[0]**2+self.trayectory[1]**2)
        self.normalizedVect = self.trayectory
        self.normalizedVect[0] /= self.magnitude
        self.normalizedVect[1] /= self.magnitude

        angle = (math.acos(self.trayectory[0]/self.magnitude))*180.0/math.pi
        if self.trayectory[1]>0:
            angle = 360-angle
        self.sprite.image = pygame.transform.rotate(texture,angle)
        self.sprite.rect = self.sprite.image.get_rect()
       
        return

    def update(self,timePassed):
        self.trayectory = [self.destination[0]-self.position[0],self.destination[1]-self.position[1]]
        self.magnitude = math.sqrt(self.trayectory[0]**2+self.trayectory[1]**2)
        distanceMoved = timePassed * self.speed
        temp = [self.normalizedVect[0]*distanceMoved,self.normalizedVect[1]*distanceMoved]
        self.position[0] += temp[0]
        self.position[1] += temp[1]
        self.sprite.rect.left = self.position[0]-self.sprite.rect[2]/2
        self.sprite.rect.top = self.position[1]-self.sprite.rect[3]/2
        return

class Gun(object):

    def __init__(self,texture,screenSize,rangeArea,bullet,sound):
        self.texture = texture
        self.bullet = bullet
        self.screenSize = screenSize
        self.sound = sound
        self.sprite = pygame.sprite.Sprite()
        self.sprite.image = texture
        self.sprite.rect = self.sprite.image.get_rect()
        self.position = [screenSize[0]/2-self.sprite.rect[2]/2,screenSize[1]/2-self.sprite.rect[3]/2]
        self.sprite.rect.left = self.position[0]
        self.sprite.rect.top = self.position[1]
        
        self.rangeArea = rangeArea
        self.rangeSurfSize = [self.rangeArea*2,self.rangeArea*2]
        self.rangeSurf = pygame.Surface(self.rangeSurfSize, pygame.SRCALPHA, 32)
        self.rangeSurfPos = [self.position[0]+self.sprite.rect[2]/2-self.rangeArea,self.position[1]+self.sprite.rect[3]/2-self.rangeArea]

        self.turningSpeed = 0.5
        self.angle = 0

        self.quadGun = 0
        self.quadBomb = 0
        
        self.turningDirection = ""
        self.trackingAngle = 0
        self.tracking = False
        self.able2shoot = True
        self.trackingPosition = [0,0]
        self.trackingVect = [0,0]
        self.trackingMagnitude = 0
        self.trackingNormalized = [0,0]
        return

    def update(self,timePassed):

        if self.tracking and int(self.angle) != int(self.trackingAngle):

            if self.turningDirection == "clockwise":
                self.angle -= self.turningSpeed * timePassed                
            else:
                self.angle += self.turningSpeed * timePassed

            if self.angle < 0:
                while(self.angle < 0):
                    self.angle += 360

            if self.angle > 360:
                while(self.angle > 0):
                    self.angle -= 360
                self.angle += 360

            if self.angle == 360:
                self.angle = 0

            if self.turningDirection == "clockwise":
                if int(self.angle) <= int(self.trackingAngle):
                    self.angle = int(self.trackingAngle)
            else:
                if int(self.angle) >= int(self.trackingAngle):
                    self.angle = int(self.trackingAngle)

            self.sprite.image = pygame.transform.rotate(self.texture,self.angle)
            self.sprite.rect = self.sprite.image.get_rect()
            self.sprite.rect.left = self.screenSize[0]/2-self.sprite.rect[2]/2
            self.sprite.rect.top = self.screenSize[1]/2-self.sprite.rect[3]/2

        if self.able2shoot and int(self.angle == int(self.trackingAngle)) and self.tracking:
            self.able2shoot = False
            return True
        return False
        

class Sentry(object):

    def __init__(self):
        pygame.init()
        self.screenSize = [800,600]
        self.backgroundColor = [255,255,255]
        self.screen = pygame.display.set_mode(self.screenSize,pygame.NOFRAME,32)
        self.running = True
        self.backgroundImage = 0
        self.snowTexture = 0
        self.gameOverImage = 0
        self.fireTexture = 0

        self.showFire = False

        self.font = pygame.font.SysFont("arial", 12);
        self.font.set_bold(True)

        self.clock = pygame.time.Clock()
        self.timePassed = 0
        self.fps = 0
        self.fpsText = self.font.render("FPS: "+str(self.fps),True,[255,255,255],[0,0,0])

        self.images = ["bobomb","bulletbill","billblaster"]
        self.textures = {}

        self.gun = 0
        self.bullets = []
        self.bombs = []

        self.pending2exit = False
        self.lastSound = 0

        self.soundEffects = ["bomb","explosion","gameOver","shoot"]
        self.sounds = {}
        self.channel = pygame.mixer.Channel(0)

        self.bulletDelay = 1
        self.bulletSpawner = Countdown(self.bulletDelay,self.bulletDelay)
        self.bulletSpawnerText = self.font.render("shooting in: "+str(self.bulletSpawner.tick),True,[255,255,255],[0,0,0])
        
        self.bombSpawner = Countdown(3,1)
        self.bombSpawnerText = self.font.render("new bomb in: "+str(self.bombSpawner.tick),True,[255,255,255],[0,0,0])
        
        return

    def setup(self):
        pygame.mixer.music.load("sounds/music.mp3")
        pygame.mixer.music.play(-1)
        pygame.mixer.music.set_volume(0.3)
        
        self.backgroundImage = pygame.image.load("pics/background.jpg").convert()
        self.backgroundImage = pygame.transform.scale(self.backgroundImage,self.screenSize)
        self.backgroundImage.set_alpha(100)
        self.snowTexture = pygame.image.load("pics/snow.jpg").convert()
        self.snowTexture = pygame.transform.scale(self.snowTexture,self.screenSize)
        self.snowTexture.set_alpha(100)
        self.fireTexture = pygame.image.load("pics/fire.jpg").convert()
        self.fireTexture = pygame.transform.scale(self.fireTexture,self.screenSize)
        self.fireTexture.set_alpha(50)
        self.gameOverImage = pygame.image.load("pics/gameOver.jpg").convert()
        self.gameOverImage = pygame.transform.scale(self.gameOverImage,self.screenSize)
        self.gameOverImage.set_alpha(100)

        for i in self.images:
            self.textures[i] = pygame.image.load("pics/"+i+".png").convert_alpha()
        self.textures["bobomb"] = pygame.transform.scale(self.textures["bobomb"],[35,35])
        self.textures["bulletbill"] = pygame.transform.scale(self.textures["bulletbill"],[30,20])
        self.textures["billblaster"] = pygame.transform.scale(self.textures["billblaster"],[90,60])

        for s in self.soundEffects:
            self.sounds[s] = pygame.mixer.Sound("sounds/"+s+".wav")

        self.gun = Gun(self.textures["billblaster"],self.screenSize,250,self.textures["bulletbill"],self.sounds["shoot"])
        return

    def update(self):
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False

        self.timePassed = self.clock.tick()
        self.fps = int(self.clock.get_fps())
        self.fpsText = self.font.render("FPS: "+str(self.fps),True,[255,255,255],[0,0,0])

        if not self.pending2exit:
            
            if self.bulletSpawner.update():
                self.gun.able2shoot = True
            if self.gun.able2shoot:
                self.bulletSpawner.tick = self.bulletDelay
            if self.bombSpawner.update():
                x = random.randint(0,3)
                pos = [0,0]
                if x == 0:
                    pos[0] = random.randint(0,self.screenSize[0])
                    pos[1] = -25
                elif x == 1:
                    pos[0] = -25
                    pos[1] = random.randint(0,self.screenSize[1])
                elif x == 2:
                    pos[0] = self.screenSize[0]+25
                    pos[1] = random.randint(0,self.screenSize[1])
                else:
                    pos[0] = random.randint(0,self.screenSize[0])
                    pos[1] = self.screenSize[1]+25
                    
                self.bombs.append(Bomb(self.textures["bobomb"],pos,[self.screenSize[0]/2,self.screenSize[1]/2]))

            if not self.showFire:
                if self.gun.update(self.timePassed):
                    self.sounds["shoot"].play()
                    self.bullets.append(Bullet(pygame.transform.rotate(self.textures["bulletbill"],self.gun.angle),[self.screenSize[0]/2,self.screenSize[1]/2],self.gun.trackingPosition))        
                self.updateBombs()
                self.updateBullets()
                self.collisionsBombsGun()
                self.collisionsBombsBullets()

            if self.channel.get_busy():
               self.lastSound =  self.channel.get_sound()

            if not self.channel.get_busy() and self.lastSound == self.sounds["explosion"]:
                self.pending2exit = True
                self.channel.play(self.sounds["gameOver"])
            
            self.bombSpawnerText = self.font.render("new bomb in: "+str(self.bombSpawner.tick),True,[255,255,255],[0,0,0])
            self.bulletSpawnerText = self.font.render("shooting delay: "+str(self.bulletSpawner.tick),True,[255,255,255],[0,0,0])
        return

    def updateBombs(self):
        for i in xrange(len(self.bombs)):
            self.bombs[i].update(self.timePassed)
            if self.bombs[i].magnitude <= self.gun.rangeArea and not self.gun.tracking:
                self.gun.tracking = True
                self.gun.trackingPosition = self.bombs[i].position
                self.gun.trackingVect = [self.gun.trackingPosition[0]-self.screenSize[0]/2,self.gun.trackingPosition[1]-self.screenSize[1]/2]
                self.gun.trackingMagnitude = math.sqrt(self.gun.trackingVect[0]**2+self.gun.trackingVect[1]**2)
                self.gun.trackingAngle = (math.acos(self.gun.trackingVect[0]/self.gun.trackingMagnitude))*180.0/math.pi
                if self.gun.trackingVect[1]>0:
                    self.gun.trackingAngle = 360-self.gun.trackingAngle

                if self.gun.trackingAngle >= 0 and self.gun.trackingAngle <= 90:
                    self.gun.quadBomb = 1
                elif self.gun.trackingAngle >= 90 and self.gun.trackingAngle <= 180:
                    self.gun.quadBomb = 2
                elif self.gun.trackingAngle >= 180 and self.gun.trackingAngle <= 270:
                    self.gun.quadBomb = 3
                else:
                    self.gun.quadBomb = 4
    
                if self.gun.angle >= 0 and self.gun.angle <= 90:
                    self.gun.quadGun = 1
                elif self.gun.angle >= 90 and self.gun.angle <= 180:
                    self.gun.quadGun = 2
                elif self.gun.angle >= 180 and self.gun.angle <= 270:
                    self.gun.quadGun = 3
                else:
                    self.gun.quadGun = 4

                self.gun.turningDirection = "clockwise"
                if self.gun.quadGun == 1:
                    self.gun.turningDirection = "counter-clockwise"
                elif self.gun.quadGun == 2 and (self.gun.quadBomb == 3 or self.gun.quadBomb == 4):
                    self.gun.turningDirection = "counter-clockwise"
                elif self.gun.quadGun == 3 and self.gun.quadBomb == 4:
                    self.gun.turningDirection = "counter-clockwise"

                if self.gun.quadGun == 1 and self.gun.quadBomb == 1:
                    if self.gun.angle < self.gun.trackingAngle:
                        self.gun.turningDirection = "counter-clockwise"
                elif self.gun.quadGun == 2 and self.gun.quadBomb == 2:
                    if self.gun.angle < self.gun.trackingAngle:
                        self.gun.turningDirection = "counter-clockwise"
                elif self.gun.quadGun == 3 and self.gun.quadBomb == 3:
                    if self.gun.angle < self.gun.trackingAngle:
                        self.gun.turningDirection = "counter-clockwise"
                elif self.gun.quadGun == 4 and self.gun.quadBomb == 4:
                    if self.gun.angle < self.gun.trackingAngle:
                        self.gun.turningDirection = "counter-clockwise"
        return

    def updateBullets(self):
        for i in xrange(len(self.bullets)):
            self.bullets[i].update(self.timePassed)
        return

    def collisionsBombsGun(self):
        for i in xrange(len(self.bombs)):
            if pygame.sprite.collide_rect(self.bombs[i].sprite,self.gun.sprite):
                pygame.mixer.music.stop()
                self.channel.play(self.sounds["explosion"])
                self.showFire = True
                break   
        return

    def collisionsBombsBullets(self):
        for i in xrange(len(self.bullets)):
            for j in xrange(len(self.bombs)):
                if pygame.sprite.collide_rect(self.bullets[i].sprite,self.bombs[j].sprite):
                    del(self.bullets[i])
                    del(self.bombs[j])
                    self.sounds["bomb"].play()
                    self.gun.tracking = False
                    return
        return

    def render(self):
        self.screen.fill(self.backgroundColor)

        if not self.pending2exit:
            self.screen.blit(self.backgroundImage,[0,0])
            self.screen.blit(self.snowTexture,[0,0])
            if self.showFire:
                self.screen.blit(self.fireTexture,[0,0])

            pygame.draw.line(self.screen,[0,0,0],[self.screenSize[0]/2,0],[self.screenSize[0]/2,self.screenSize[1]],1)
            pygame.draw.line(self.screen,[0,0,0],[0,self.screenSize[1]/2],[self.screenSize[0],self.screenSize[1]/2],1)

            for b in self.bombs:
                self.screen.blit(b.sprite.image,b.sprite.rect)

            for b in self.bullets:
                self.screen.blit(b.sprite.image,b.sprite.rect)

            pygame.draw.circle(self.gun.rangeSurf,[0,0,0,20],[self.gun.rangeSurfSize[0]/2,self.gun.rangeSurfSize[1]/2],self.gun.rangeArea,0)
            self.screen.blit(self.gun.rangeSurf,self.gun.rangeSurfPos)
            self.screen.blit(self.gun.sprite.image,self.gun.sprite.rect)

            self.screen.blit(self.bombSpawnerText,[10,30])
            self.screen.blit(self.bulletSpawnerText,[10,50])
        else:
            self.screen.blit(self.gameOverImage,[0,0])
        
        self.screen.blit(self.fpsText,[10,10])
        pygame.display.update()
        return

    def end(self):
        pygame.quit()
        return


def main():

    game = Sentry()
    game.setup()
    
    while game.running:
        game.update()
        game.render()
        
    game.end()
    return

if __name__ == "__main__":
    main()
