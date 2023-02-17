# ========================================================================
# Name: Trung Dam and Hien Anh
# Google Dino Game

# ========================================================================

# This project attempts to develop a simple version of the Dinosaur game (the Dino game built into the Google Chrome
# web browser). Users would use the ↑, SPACE and ↓ buttons on the keyboard to help a Tyrannosaurus avoid obstacles on
# its track. The longer the time played, the higher the scores would be.

# ========================================================================

import math
import sys
import pygame as pg
from pygame import mixer
import random

pg.init()
mixer.init()

# ========================================================================

# Screen Creation
pg.display.set_caption('Dinosaur Game')
screenWidth = 1200
screenHeight = 500

screen = pg.display.set_mode((screenWidth, screenHeight))  # Create game screen

# ========================================================================

# Import Background, Elements
BackGround = pg.image.load('DinoPic/Track.png')
PinkDino = pg.image.load('DinoPic/PinkDino.png')
PinkDinoDuck = pg.image.load('DinoPic/PinkDinoDuck.png')
smCactus1 = pg.image.load('DinoPic/SmallCactus1.png')
smCactus2 = pg.image.load('DinoPic/SmallCactus2.png')
BlueBird = pg.image.load('DinoPic/BlueBird.png')

cactusLst = [smCactus1, smCactus2]


# ========================================================================

class BG:

    def __init__(self, x):
        """This function takes in the initial x-coordinate of the track. It then creates and sets up a running track in
        the background"""
        self.width = screenWidth
        self.height = screenHeight
        self.x = x
        self.scaledown()
        self.show()

    def update(self, newX):
        """This function takes new distance between initial coordinate and wanted coordinate to make the screen move by
        that input distance"""
        self.x -= newX
        if self.x <= -screenWidth:
            self.x = screenWidth

    def show(self):
        """Make the background track appear on the game screen"""
        screen.blit(BackGround, (self.x, 400))

    def scaledown(self):
        """Scale down the size of the track image to fit in the screen"""
        self.bg = pg.transform.scale(BackGround, (self.width, self.height))


class Dino:
    def __init__(self):
        """Set up and display the dinosaur and its movements: jumping, ducking"""
        self.x = 40
        self.y = 330
        self.y_duck = 380
        self.yPos = self.y
        self.textureNum = 0
        self.standing = True
        self.jumping = False
        self.falling = False
        self.ducking = False
        self.dino = PinkDino
        self.dinoDuck = PinkDinoDuck
        self.image = self.dino
        self.show()
        self.width = self.image.get_width()
        self.height = self.image.get_height()

    def update(self):
        """Set up conditions for the dinosaur to jump and fall"""
        if self.jumping:
            self.yPos -= 2.0  # Jump Step
            if self.yPos <= 70:
                self.fall()
        elif self.falling:
            self.yPos += 2.4  # Gravity so that dinosaur falls faster than it jumps
            if self.yPos >= 330:
                self.touchGround()

    def jump(self):
        """Set up the conditions of jumping feature"""
        self.image = self.dino
        self.jumping = True
        self.falling = False
        self.standing = False
        self.ducking = False

    def fall(self):
        """Set up the conditions of falling feature"""
        self.image = self.dino
        self.falling = True
        self.standing = False
        self.jumping = False
        self.ducking = False

    def touchGround(self):
        """Set up the conditions of standing feature"""
        self.image = self.dino
        self.falling = False
        self.standing = True
        self.ducking = False
        self.yPos = self.y

    def duck(self):
        """Set up the conditions of ducking feature"""
        self.ducking = True
        self.falling = False
        self.standing = False
        self.jumping = False
        self.image = self.dinoDuck
        self.yPos = self.y_duck

    def show(self):
        """Display the dinosaur on the screen at the wanted position"""
        screen.blit(self.image, (self.x, self.yPos))


class Cactus:
    def __init__(self, x):
        """This function takes initial x-coordinate of the cacti. It then sets up and displays the cacti randomly on the
        screen"""
        self.x = x
        self.y = 340
        self.randomCactus()
        self.show()

    def update(self, newX):
        """This function takes new distance between initial coordinate of the cactus and new wanted coordinate of the
        cactus to make the cactus change location"""
        self.x -= newX

    def randomCactus(self):
        """Choose the displayed cactus by randomization"""
        self.randomNum = random.randint(0, len(cactusLst) - 1)

    def show(self):
        """Display the cactus on the screen at the wanted position"""
        screen.blit(cactusLst[self.randomNum], (self.x, self.y))


class Bird:
    def __init__(self, x):
        """This function takes initial x-coordinate of the birds. It then sets up and displays the birds randomly on the
        screen"""
        self.x = x
        self.y = 285
        self.show()

    def update(self, newX):
        """This function takes new distance between initial coordinate of the bird and new wanted coordinate of the
        bird to make it change location"""
        self.x -= newX

    def show(self):
        """Display the bird on the screen at the wanted position"""
        screen.blit(BlueBird, (self.x, self.y))


class Obstacles:
    def __init__(self):
        """Set up an obstacle list"""
        self.obstacleList = []

    def showObstacles(self):
        """Display obstacles at randomized positions"""
        if len(self.obstacleList) == 0:
            xPos = random.randint(screenWidth + 100, 2000)
        else:
            beforeObstacle = self.obstacleList[-1]
            xPos = random.randint(beforeObstacle.x + 900, screenWidth + beforeObstacle.x + 900)

        if random.randint(0, 2) == 0 or random.randint(0, 2) == 1:
            cactus = Cactus(xPos)
            self.obstacleList.append(cactus)
        else:
            bird = Bird(xPos)
            self.obstacleList.append(bird)

    def clearObstacle(self):
        """Clear obstacle list"""
        self.obstacleList = []


class Score:

    def __init__(self):
        """Create and set up the score box's properties"""
        self.actualScore = 0
        self.font = pg.font.SysFont('Monaco', 30)
        self.color = (0, 0, 0)
        self.show()

    def update(self, loops):
        """This function takes loops as an input. It makes the score only increase by 10 in one second"""
        self.actualScore = loops // 10

    def show(self):
        """Display the score box on the screen at the wanted position"""
        self.label = self.font.render(f'SCORE {self.actualScore}', 1, self.color)
        labelWidth = self.label.get_rect().width
        screen.blit(self.label, (screenWidth - labelWidth - 10, 10))


class Crash:
    def distance(self, object1, object2):
        """This function takes two objects as input. It then calculates the distance between those two and returns True
        if the distance is smaller than 60"""
        dist = math.sqrt((object1.x - object2.x) ** 2 + (object1.yPos - object2.y) ** 2)
        return dist < 60


class Settings:
    def __init__(self):
        """Combine and set up the game's features"""
        self.movingBG = [BG(0), BG(screenWidth)]  # display the screen at 0 and 1200 in the x-axis to create an
        # infinite scrolling background
        self.score = Score()
        self.crash = Crash()
        self.set_labels()
        self.playing = False

    def set_labels(self):
        """Create label to give instructions to player on how to restart the game"""
        font1 = pg.font.SysFont('M+', 24, "bold")
        font2 = pg.font.SysFont('M+', 20)
        self.overLabel = font1.render(f'GAME OVER', 1, "#006400")
        self.restartLabel = font2.render(f'Press Space to restart', 1, "#4F7942")

    def over(self):
        """Set up the screen's display, sound, condition when the game is over"""
        mixer.music.stop()
        screen.blit(self.overLabel, (600 - self.overLabel.get_width() // 2, 250))
        screen.blit(self.restartLabel, (600 - self.restartLabel.get_width() // 2, 250 + self.overLabel.get_height()))
        self.playing = False

    def start(self):
        """Set up the sound and conditions when the game starts"""
        self.playing = True
        self.soundPlay()

    def soundPlay(self):
        """Play music in the background"""
        mixer.music.load('DinoPic/BabyShark.wav')
        mixer.music.play(-1)

    def restart(self):
        """Restart the game"""
        self.__init__()


# ========================================================================

def main():
    """Set the game running"""
    running = True
    speed = 1
    default = Settings()
    obstacles = Obstacles()
    loops = 0
    over = False
    dino = Dino()
    clock = pg.time.Clock()

    while running:

        if default.playing:
            screen.fill((255, 240, 245))  # Change the screen's color to pink
            loops += 1  # Increment the loop by 1 each time the main loop runs

            for bg in default.movingBG:  # Make the screen move
                bg.update(speed)
                bg.show()

            dino.update()
            dino.show()

            if loops % 500 == 0:  # Display the obstacles when the loop is divisible by 500
                obstacles.showObstacles()

            obsLst2 = []

            for obs in obstacles.obstacleList:
                obs.update(speed)
                obs.show()
                if obs.x < 0:
                    obsLst2.append(obs)  # Append the obstacles to the second obstacles list after they disappear
                    # from the screen
                if default.crash.distance(dino, obs):
                    over = True  # Set the game condition to over if the dino and obstacles crash

            for el in obsLst2:
                obstacles.obstacleList.remove(el)  # Clear obstacles in the first obstacles list if the second
                # obstacles list contains the same object

            if over:
                default.over()
                obstacles.clearObstacle()

            default.score.update(loops)
            default.score.show()

        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()

            if event.type == pg.KEYDOWN:  # Set up user keyboard's interaction
                if event.key == pg.K_SPACE or event.key == pg.K_UP:
                    if not over and dino.standing and not dino.ducking:
                        dino.jump()
                    if not default.playing:
                        default.start()
                if event.key == pg.K_DOWN:
                    if not over and dino.standing:
                        dino.duck()
                else:
                    if dino.ducking:
                        dino.touchGround()
                if over:
                    if event.key == pg.K_SPACE:
                        screen.fill((0, 0, 0))
                        mixer.music.stop()
                        default.restart()
                        dino = Dino()
                        loops = 0
                        over = False
        clock.tick(400)  # Set up 400 frames per second
        pg.display.update()


# ========================================================================

# Execution
main()

# ========================================================================

# Test Method: We run the game and check if the designated keyboard's keys work properly. We also test how the score
# increments as well as the dinosaur's movements and obstacles' behaviour. In addition, we check if the screen
# behaves correctly when it changes states from start to over and vice versa.
