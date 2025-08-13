
import pygame

class PyBomb(object):

    def __init__(self):
        pygame.init()
        self.windowSize = [640,480]
        self.bgColor = [0,0,0]
        self.screen = pygame.display.set_mode(self.windowSize,pygame.NOFRAME,32)
        self.running = True

        self.clock = pygame.time.Clock()

        self.images = ["game","end"]
        self.imageIndex = "game"
        self.bgImages = {}

        self.fontSM = pygame.font.SysFont("arial", 15);
        self.fontSM.set_bold(True)
        self.textESC = self.fontSM.render("press ESC to exit", True, [255,255,255])
        self.textFPS = self.fontSM.render("FPS:", True, [255,255,255])

        self.startCountdown = False
        self.stopCountdown = False
        self.playedOnce = False
        self.textSPA = self.fontSM.render("press SPACEBAR to start countdown!", True, [255,255,255])

        self.startTime = pygame.time.get_ticks()
        self.finalTime = pygame.time.get_ticks()
        self.min = 2
        self.sec = 10
        
        self.fontLG = pygame.font.SysFont("arial", 75);
        self.fontLG.set_bold(True)
        self.textTIM = self.fontLG.render("00:00", True, [255,255,255])

        self.sounds = ["2min","60sec","30sec","10sec","5sec","4sec","3sec","2sec","1sec","wtfboom","beep"]
        self.soundEffects = {}
        self.channel = pygame.mixer.Channel(0) 
        return

    def setup(self):
        for i in self.images:
            self.bgImages[i] = pygame.image.load("pics/"+i+".jpg").convert()
            self.bgImages[i] = pygame.transform.scale(self.bgImages[i],self.windowSize)
            self.bgImages[i].set_alpha(150, pygame.RLEACCEL)

        for s in self.sounds:
            self.soundEffects[s] = pygame.mixer.Sound("sounds/"+s+".wav")   
        return

    def tick(self):
        if self.startCountdown:
            self.finalTime = pygame.time.get_ticks()
            deltaTime = self.finalTime - self.startTime
            if deltaTime >= 1000.0:
                self.startTime = self.finalTime
                self.sec -= 1
                
                if self.sec == 0 and self.min == 2:
                    self.channel.play(self.soundEffects["2min"])
                if self.sec == 0 and self.min == 1:
                    self.channel.play(self.soundEffects["60sec"])
                if self.sec == 30 and self.min == 0:
                    self.channel.play(self.soundEffects["30sec"])
                if self.sec == 10 and self.min == 0:
                    self.channel.play(self.soundEffects["10sec"])
                if self.sec == 5 and self.min == 0:
                    self.channel.play(self.soundEffects["5sec"])
                if self.sec == 4 and self.min == 0:
                    self.channel.play(self.soundEffects["4sec"])
                if self.sec == 3 and self.min == 0:
                    self.channel.play(self.soundEffects["3sec"])
                if self.sec == 2 and self.min == 0:
                    self.channel.play(self.soundEffects["2sec"])
                if self.sec == 1 and self.min == 0:
                    self.channel.play(self.soundEffects["1sec"])

                if self.sec <= 0 and self.min <= 0 and not self.playedOnce:
                    self.channel.play(self.soundEffects["wtfboom"])
                    self.playedOnce = True
                elif not self.channel.get_busy():
                    self.soundEffects["beep"].play()
                if self.sec < 0 and self.min > 0:
                    self.sec = 59
                    self.min -= 1
                    if self.min < 0:
                        self.min = 0
                elif self.sec < 0 and self.min <= 0:
                    self.sec = 0
                    self.stopCountdown = True
                    self.imageIndex = "end"
        return

    def update(self):
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False
                if event.key == pygame.K_SPACE:
                    self.startCountdown =  True
                    self.startTime = pygame.time.get_ticks()
                    self.finalTime = pygame.time.get_ticks()

        if not self.stopCountdown:
            self.tick()
        self.clock.tick()
        fps = int(self.clock.get_fps())
        self.textFPS = self.fontSM.render("FPS: "+str(fps), True, [255,255,255])
        time = ""
        if self.min > 9:
            time += str(self.min)
        else: 
            time += "0"+str(self.min)
        time += ":"
        if self.sec > 9:
            time += str(self.sec)
        else: 
            time += "0"+str(self.sec)
        self.textTIM = self.fontLG.render(time, True, [255,255,255])
        return

    def render(self):
        self.screen.fill(self.bgColor)
        self.screen.blit(self.bgImages[self.imageIndex],[0,0])
        self.screen.blit(self.textESC,[10,10])
        self.screen.blit(self.textFPS,[10,35])
        if self.startCountdown and not self.stopCountdown:
            self.screen.blit(self.textTIM,[225,370])
        elif not self.stopCountdown:
            self.screen.blit(self.textSPA,[190,420])
        pygame.display.update()
        return

    def end(self):
        pygame.quit()
        return


def main():

    game = PyBomb()
    game.setup()

    while game.running:
        game.update()
        game.render()

    game.end()
    return

if __name__ == "__main__":
    main()
