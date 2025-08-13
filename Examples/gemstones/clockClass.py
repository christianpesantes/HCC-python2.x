
#--------------------------------
# imports
#--------------------------------
import time

class clock(object):

    #--------------------------------
    # constructor
    #--------------------------------
    def __init__(self):
        self.isAlive = False
        self.seconds = 0
        self.startTime = 0
        self.currentTime = 0
        
        self.isPaused = False
        self.psdSeconds = 0
        self.psdStartTime = 0
        self.psdcurrentTime = 0
        return

    #--------------------------------
    # start
    #--------------------------------
    def start(self, x):
        self.isAlive = True
        self.startTime = time.clock()
        self.currentTime = time.clock()
        self.seconds = x
        return

    #--------------------------------
    # stop
    #--------------------------------
    def stop(self):
        self.isAlive = False
        return

    #--------------------------------
    # isTicking
    #--------------------------------
    def isTicking(self):
        isReady = False
        if self.isAlive:
            if not self.isPaused:
                self.currentTime = time.clock()
                if (self.currentTime - self.startTime) >= self.seconds:
                    isReady = True
                    self.deltaTime = 0
                    self.startTime = time.clock()
            else:
                self.psdDeltaTime = time.clock()
                if (self.psdDeltaTime - self.psdStartTime) > self.psdSeconds:
                    self.isPaused = False
                    self.startTime += self.psdSeconds
        return isReady

    #--------------------------------
    # pause
    #--------------------------------
    def pause(self, x):
        self.isPaused = True
        self.psdStartTime = time.clock()
        self.psdSeconds = x
        return


    #--------------------------------
    # print
    #--------------------------------
    def __str__(self):
        if self.isPaused:
            print "pause: " + str(abs(int(self.psdDeltaTime - self.psdStartTime)))
        return str(abs(int(self.deltaTime - self.startTime)))

            

#--------------------------------
# main
#--------------------------------
def main():

    raw_input("testing class... press any key to start...")
    swatch = clock()
    swatch.start(10)

    start = time.clock()
    for x in xrange(1, 1000000):

        print swatch
        if swatch.isTicking():
            break
        if x == 100:
            swatch.pause(5)

    print "it took", time.clock() - start, "seconds!"
    print
    
    print "this is just a class definition!"
    print "please run 'gems.py'..."
    print
    raw_input("press any key to continue...")
    return

if __name__ == "__main__":
    main()
