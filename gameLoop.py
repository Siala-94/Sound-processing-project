import pygame
import random
import scipy

from pygame.locals import *

import generateBeatmap as bmap
import bandSplit_4 as bsplit

# Set music
music = "fm.wav"

# Initialize Pygame
pygame.init()

# Set FPS
FPS = 60
FrameClock = pygame.time.Clock()

# Config
use_only_fullmap = 0

# Declare colors
RED = pygame.Color(255, 0, 0)
BLACK = pygame.Color(0, 0, 0)
BLUE = pygame.Color(0, 0, 255)
GREEN = pygame.Color(0, 255, 0)
YELLOW = pygame.Color(255, 255, 0)
PURPLE = pygame.Color(255, 0, 255)
TEAL = pygame.Color(0, 255, 255)
WHITE = pygame.Color(255, 255, 255)
GRAY = pygame.Color(100, 100, 100)

BONUSCOLOR = TEAL

# Set up the main game window
SCREEN = pygame.display.set_mode((800, 640))
SCREEN.fill(BLACK)

#Time for the blocks to reach the line should be
# 480/12 = 40 frames

blocks = []
fullMap = []

global SCORE
activeParticles = []

class ParticleSystem:
    def __init__(self):
        self.particles = []

    def emit(self):
        if self.particles: # true if list has entries
            self.delete_particles()
            for particle in self.particles:
                #move
                #particle[0].move_ip(particle[2][0], particle[2][1])
                #particle[0] += particle[2][0]
                #particle[1] += particle[2][1]
                #shrink
                particle[1] -= 0.1
                particle[0].width = int(particle[1])
                particle[0].height = int(particle[1])
                particle[3][0] += particle[2][0]
                particle[3][1] += particle[2][1]
                particle[0].left = int(particle[3][0])
                particle[0].top = int(particle[3][1])
                #draw
                pygame.draw.rect(SCREEN, BONUSCOLOR, particle[0])

    def add_particles(self, x, y):
        pos_x = x
        pos_y = y
        floatpos_x = x
        floatpos_y = y
        radius = 20
        size = 30
        direction_x = random.uniform(-0.8, 0.8)
        direction_y = random.uniform(-0.8, 0.8)
        #particle_circle = [[pos_x, pos_y],radius,[direction_x, direction_y]]
        particle_rect = [Rect(pos_x, pos_y, size, size), size, [direction_x, direction_y], [floatpos_x, floatpos_y]]
        self.particles.append(particle_rect)

    def delete_particles(self):
        particle_copy = [particle for particle in self.particles if particle[1] > 0]
        self.particles = particle_copy

class Score(pygame.sprite.Sprite):
    score = 0

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.font = pygame.font.Font(None, 40)
        self.color = WHITE

    def addPoints(self, points):
        self.score += points
        #print("Score: " + str(self.score))

    def draw(self, surface):
        msg = "Score: " + str(self.score)
        text = self.font.render(msg, 0, self.color)
        surface.blit(text, (100, 540))

SCORE = Score()

class Beatmap():

    def __init__(self, path, pos):
        self.beats = []
        self.current_beat = 0
        self.next_beat = 0
        self.position = pos
        
        inFile = open(path)
        for line in inFile:
            self.beats.append(float(line))
        inFile.close()

    def progress(self, time, on_main):
        if time >= self.current_beat:
            if self.next_beat >= len(self.beats):
                print("Out of range")
                self.current_beat = 9999999
            else:
                if on_main:
                    newBlock = Block(self.position, 1)
                    blocks.append(newBlock)
                else:
                    newBlock = Block(self.position, 0)
                    blocks.append(newBlock)
                self.current_beat = self.beats[self.next_beat]
                self.next_beat += 1

class Block(pygame.sprite.Sprite):

    color = RED
    position = 0
    goodblock = 0
    global SCORE
    
    def __init__(self, position, good):
        # Define a surface for the Block
        self.surf = pygame.Surface((60,60))
        self.goodblock = good
        if self.goodblock == 0:
            self.color = GRAY
        elif self.goodblock == 1:
            self.color = BONUSCOLOR

        column = random.randint(0, 1)
        self.rect = self.surf.get_rect(center = (64+(position*192)+column*96, 0))

    def move(self):
        self.rect.move_ip(0, 12)

    def checkCollision(self, player):
        if self.rect.colliderect(player):
            blocks.remove(self)
            if(self.goodblock == 1):
                SCORE.addPoints(1)
                particle = ParticleSystem()
                parts = random.randint(4, 12)
                for p in range(parts):
                    particle.add_particles(self.rect.centerx, self.rect.centery)
                    activeParticles.append(particle)
            else:
                SCORE.addPoints(-1)

    def draw(self, surface):
        pygame.draw.rect(surface, self.color, self.rect)

class Player(pygame.sprite.Sprite):

    l_pressed = False
    r_pressed = False
    
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("triangle2.png")
        self.rect = self.image.get_rect()
        self.rect.center=(448, 480)

    def move(self):
        pressed_keys = pygame.key.get_pressed()
        if pressed_keys[K_LEFT] and not self.l_pressed:
            self.rect.move_ip(-96, 0)
            self.l_pressed = True
        elif not pressed_keys[K_LEFT]:
            self.l_pressed = False
            
        if pressed_keys[K_RIGHT] and not self.r_pressed:
            self.rect.move_ip(96, 0)
            self.r_pressed = True
        elif not pressed_keys[K_RIGHT]:
            self.r_pressed = False

    def draw(self, surface):
        surface.blit(self.image, self.rect)
    


#pygame.mixer.music.load(music)

# Divide into frequency bands
bsplit.bandSplit(music)

# Generate beatmaps
bmap.generateBeatmap("music_band1.wav", "energy", 1.2, "band1Map.txt")
bmap.generateBeatmap("music_band2.wav", "energy", 1.5, "band2Map.txt")
bmap.generateBeatmap("music_band3.wav", "energy", 1.5, "band3Map.txt")
bmap.generateBeatmap("music_band4.wav", "energy", 1.6, "band4Map.txt")
#bmap.generateBeatmap("music_band5.wav", "complex", 0.3, "band5Map.txt")
#bmap.generateBeatmap("music_band6.wav", "complex", 0.3, "band6Map.txt")
bmap.generateBeatmap(music, "complex", 0.8, "fullMap.txt")

beatmaps = []

if use_only_fullmap == 1:
    fullMap = Beatmap("beatmaps/fullMap.txt", 3)
    beatmaps.append(fullMap)
else:
    band1Map = Beatmap("beatmaps/band1Map.txt", 0)
    band2Map = Beatmap("beatmaps/band2Map.txt", 1)
    band3Map = Beatmap("beatmaps/band3Map.txt", 2)
    band4Map = Beatmap("beatmaps/band4Map.txt", 3)
    #band5Map = Beatmap("beatmaps/band5Map.txt", 4)
    #band6Map = Beatmap("beatmaps/band6Map.txt", 5)
    beatmaps.append(band1Map)
    beatmaps.append(band2Map)
    beatmaps.append(band3Map)
    beatmaps.append(band4Map)
    #beatmaps.append(band5Map)
    #beatmaps.append(band6Map)

inFile = open("beatmaps/fullMap.txt")
for line in inFile:
    fullMap.append(round(float(line), 1))

inFile.close()

time_passed = 0

#music = "brink.wav"
pygame.mixer.music.load(music)
#pygame.mixer.music.play(-1)

music_started = 0
frames_until_music = 40 # 0.5 seconds at 60 FPS
frames_passed = 0

PLAYER = Player()

fallingblocks = pygame.sprite.Group()
players = pygame.sprite.Group()

Player.containers = players
Block.containers = fallingblocks

testing = 0



# Game loop
while True:
    #time_passed += (1/FPS)
    time_passed = pygame.mixer.music.get_pos() / 1000
    frames_passed += 1
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()

    if music_started == 0 and frames_passed >= frames_until_music:
        pygame.mixer.music.play(-1)
        music_started = 1

    #testing += 1
    #if testing >= 200:
    #    particle1 = ParticleSystem()
    #    particle1.add_particles()
    #    activeParticles.append(particle1)
    #    print("shoulda created a particle")
    #    testing = 0

    #random.shuffle(beatmaps)
    if(round(time_passed, 1) in fullMap):
        #on main, send a green note
        for bmap in beatmaps:
            if(random.randint(0,2) == 0):
                bmap.progress(time_passed, True)
            else:
                bmap.progress(time_passed, False)
    else:
        for bmap in beatmaps:
            bmap.progress(time_passed, False)
    
    SCREEN.fill(BLACK)
    beatLine = pygame.draw.line(SCREEN, WHITE, (0, 480), (800, 480))

    PLAYER.move()
    PLAYER.draw(SCREEN)

    for aBlock in blocks:
        aBlock.move()
        aBlock.checkCollision(PLAYER)
        aBlock.draw(SCREEN)

    # Check for collision
    for collision in pygame.sprite.groupcollide(players, fallingblocks, 0, 1):
        print("Block touched")

    SCORE.draw(SCREEN)

    for part in activeParticles:
        part.emit()

    pygame.display.update()

    # Wait for one frame-time unit to pass before continuing the game loop
    FrameClock.tick(FPS)
