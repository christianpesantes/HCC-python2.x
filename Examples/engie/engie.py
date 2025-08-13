
import pygame 

class Player(object):

    def __init__(self,texture,position,speed):
        self.sprite = pygame.sprite.Sprite()
        self.sprite.image = texture
        self.sprite.rect = self.sprite.image.get_rect()
        self.position = position
        self.sprite.rect.left = self.position[0]
        self.sprite.rect.top = self.position[1]
        self.speed = speed
        return

class Dispenser(object):

    def __init__(self,texture,position):
        self.sprite = pygame.sprite.Sprite()
        self.sprite.image = texture
        self.sprite.rect = self.sprite.image.get_rect()
        self.position = position
        self.sprite.rect.left = self.position[0]
        self.sprite.rect.top = self.position[1]
        return

class Engie(object):

    def __init__(self):
        pygame.init()
        self.screenSize = [640,480]
        self.backgroundColor = [255,255,255]
        self.screen = pygame.display.set_mode(self.screenSize,pygame.NOFRAME,32)
        self.running = True

        self.backgroundImage = 0

        self.images = ["health","metal","engie","dispenser"]
        self.textures = {}

        self.soundEffects = ["erectingDispenser","dispenserDown"]
        self.sounds = {}
        self.channel = pygame.mixer.Channel(0)

        self.font = pygame.font.SysFont("arial", 30);
        self.font.set_bold(True)

        self.font2 = pygame.font.SysFont("arial", 12);
        self.font2.set_bold(True)
        
        self.clock = pygame.time.Clock()
        self.timePassed = 0
        self.fps = 0
        self.fpsText = self.font2.render("FPS: "+str(self.fps),True,[255,255,255],[0,0,0])

        self.healthMAX = 125
        self.health = 10
        self.healthText = self.font.render(str(self.health),True,[0,0,0])

        self.metalMAX = 200
        self.metal = self.metalMAX
        self.metalText = self.font.render(str(self.metal),True,[0,0,0])

        self.player = 0
        self.dispenser = 0
        self.dispensed = False

        self.finalTime = pygame.time.get_ticks()
        self.initialTime = pygame.time.get_ticks()
        return

    def setup(self):
        self.backgroundImage = pygame.image.load("pics/background.jpg").convert()
        self.backgroundImage = pygame.transform.scale(self.backgroundImage,self.screenSize)
        self.backgroundImage.set_alpha(50)

        pygame.mixer.music.load("sounds/music.mp3")
        pygame.mixer.music.play(-1)
        pygame.mixer.music.set_volume(1.0)

        for i in self.images:
            self.textures[i] = pygame.image.load("pics/"+i+".png").convert_alpha()

        for i in self.soundEffects:
            self.sounds[i] = pygame.mixer.Sound("sounds/"+i+".wav")

        self.player = Player(self.textures["engie"],[220,150],0.25)
        return

    def update(self):
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1 and not self.dispensed and self.metal >= 100 and not self.channel.get_busy():
                    self.channel.play(self.sounds["erectingDispenser"])
                    self.dispensed = True
                    self.metal -= 100
                    self.dispenser = Dispenser(self.textures["dispenser"],[self.player.position[0]+20,self.player.position[1]+50])
                if event.button == 3 and self.dispensed and not self.channel.get_busy():
                    self.channel.play(self.sounds["dispenserDown"])
                    self.dispensed = False

        self.timePassed = self.clock.tick()
        self.fps = int(self.clock.get_fps())
        self.fpsText = self.font2.render("FPS: "+str(self.fps),True,[255,255,255],[0,0,0])

        pressed_keys = pygame.key.get_pressed()
        if pressed_keys[pygame.K_a] and self.player.position[0] >= 150:
            self.player.position[0] -= self.timePassed * self.player.speed
        if pressed_keys[pygame.K_d] and self.player.position[0] <= 400:
            self.player.position[0] += self.timePassed * self.player.speed 
        self.player.sprite.rect.left = self.player.position[0]

        self.finalTime = pygame.time.get_ticks()
        if (self.finalTime - self.initialTime) >= 3000.0:
            self.initialTime = self.finalTime
            if self.dispensed and pygame.sprite.collide_rect(self.player.sprite,self.dispenser.sprite):
                self.health += 15
                if self.health >= self.healthMAX:
                    self.health = self.healthMAX
                self.metal += 10
                if self.metal >= self.metalMAX:
                    self.metal = self.metalMAX

        self.healthText = self.font.render(str(self.health),True,[0,0,0])
        self.metalText = self.font.render(str(self.metal),True,[0,0,0])        
        return

    def render(self):
        self.screen.fill(self.backgroundColor)
        self.screen.blit(self.backgroundImage,[0,0])

        self.screen.blit(self.player.sprite.image,self.player.sprite.rect)
        
        if self.dispensed:
            self.screen.blit(self.dispenser.sprite.image,self.dispenser.sprite.rect)
        
        self.screen.fill([255,255,255],[0,300,150,60])
        self.screen.blit(self.textures["health"],[10,305])
        self.screen.blit(self.healthText,[80,312])
        
        self.screen.fill([255,255,255],[0,380,150,60])
        self.screen.blit(self.textures["metal"],[10,385])
        self.screen.blit(self.metalText,[80,392])

        self.screen.blit(self.fpsText,[10,10])
        pygame.display.update()
        return

    def end(self):
        pygame.quit()
        return


def main():

    game = Engie()
    game.setup()
    
    while game.running:
        game.update()
        game.render()
        
    game.end()
    return

if __name__ == "__main__":
    main()
