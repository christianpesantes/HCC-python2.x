
import pygame
import random

class Shapes(object):

    def __init__(self, windowSize):
        self.size = [50,50]
        self.surface = pygame.Surface(self.size,pygame.SRCALPHA,32)
        self.position = [0,0,self.size[0], self.size[1]]
        self.color = [random.randint(0,255),random.randint(0,255),random.randint(0,255),random.randint(0,255)]
        self.speed = [random.randint(1,5), random.randint(1,5)]
        return

    def draw(self):
        self.surface.fill(self.color)
        return self.surface

    def resetShape(self, windowSize):
        self.position = [self.size[0]*-1,self.size[1]*-1,self.size[0], self.size[1]]
        self.color = [random.randint(0,255),random.randint(0,255),random.randint(0,255),random.randint(0,255)]
        self.speed = [random.randint(1,5), random.randint(1,5)]
        return

    def update(self, windowSize):
        self.moveShape()
        if self.outOfRange(windowSize):
            self.resetShape(windowSize)
        return

    def moveShape(self):
        self.position[0] += self.speed[0]
        self.position[2] += self.speed[0]
        self.position[1] += self.speed[1]
        self.position[3] += self.speed[1]
        return

    def outOfRange(self, windowSize):
        if self.position[0] > windowSize[0] or self.position[1] > windowSize[1]:
            return True
        else:
            return False

class ScreenSaver(object):

    def __init__(self):
        pygame.init()
        self.windowSize = [640,480]
        self.backgroundColor = [255,255,255]
        self.screen = pygame.display.set_mode(self.windowSize,0,32)
        pygame.display.set_caption("ScreenSaver!")
        self.running = True

        self.numSprites = 100
        self.sprites = []

        self.font = pygame.font.SysFont("arial",15)
        self.font.set_bold(True)
        self.text = self.font.render(" press 'ESC' to exit ", True, [255,255,255], [0,0,0])
        return

    def setup(self):
        for _ in xrange(self.numSprites):
            self.sprites.append(Shapes(self.windowSize))
        return

    def update(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False

        for s in self.sprites:
            s.update(self.windowSize)
        return

    def render(self):
        self.screen.fill(self.backgroundColor)
        for s in self.sprites:
            self.screen.blit(s.draw(),s.position)
        self.screen.blit(self.text,[self.windowSize[0]/2-50,self.windowSize[1]-25])
        pygame.display.update()
        return

    def end(self):
        pygame.quit()
        return


def main():

    game = ScreenSaver()
    game.setup()
    
    while game.running:
        
        game.update()
        game.render()
        
    game.end()
    return

if __name__ == "__main__":
    main()
