import pygame
import random
import scipy

from pygame.locals import *

import generateBeatmap as bmap
import bandSplit as bsplit
import pitchAnalysis as pitchgen

from aubio import source, pitch

# Initialize Pygame
pygame.init()

# Set FPS
FPS = 60
FrameClock = pygame.time.Clock()

# Declare colors
RED = pygame.Color(255, 0, 0)
BLACK = pygame.Color(0, 0, 0)
BLUE = pygame.Color(0, 0, 255)
GREEN = pygame.Color(0, 255, 0)
PURPLE = pygame.Color(255, 0, 180)
GRAY = pygame.Color(100, 100, 100)

# Set up the main game window
SCREEN = pygame.display.set_mode((800, 640))
SCREEN.fill(BLACK)

blocks = []
#fullMap = []

# Set music
music = "piano.wav"
#pygame.mixer.music.load(music)

pitchgen.generatePitches(music, "pitches.txt")

bmap.generateBeatmap(music, "complex", "fullMap.txt", 0.50)

fullMap = []
beatmap_pos = []

inFile = open("beatmaps/fullMap.txt")
on_line = 0
for line in inFile:
    if(on_line == 0):
        on_line += 1
    else:
        fullMap.append(round(float(line), 2))
inFile.close()

on_line = 0

inFile = open("pitchmaps/pitches.txt")
for line in inFile:
    on_line += 1
    time = on_line / (44100 / 512) # samplerate / hop size
    if(round(time, 2) in fullMap):
        beatmap_pos.append(float(line))
        print(line + "\n")
inFile.close()

#fullMap = Beatmap("beatmaps/fullMap.txt", 0)


##class Beatmap():
##
##    def __init__(self, path, pos):
##        self.beats = []
##        
##        self.current_beat_int = 0
##        self.next_beat = 0
##        self.position = pos
##        
##        inFile = open(path)
##        for line in inFile:
##            self.beats.append(float(line))
##        inFile.close()
##
##        # await_beat is the *time* of the next beat in the "queue"
##        self.await_beat = self.beats[0]
##
##    def progress(self, time):
##        if time >= self.await_beat:
##            #if(round(self.beats[self.current_beat_int], 2) in fullMap):
##            #    newBlock = Block(self.position, PURPLE)
##            #else:
##            #    newBlock = Block(self.position, GRAY)
##            newBlock = Block(self.position, PURPLE)
##            
##            blocks.append(newBlock)
##
##            self.current_beat_int += 1
##            self.await_beat = self.beats[self.current_beat_int]
##            #self.current_beat_int += 1
##            #self.next_beat += 1

class Block(pygame.sprite.Sprite):

    color = RED
    position = 0
    font = pygame.font.Font(None, 20)
    textstr = " "
    
    def __init__(self, position, color, freq):
        # Define a surface for the Block
        self.surf = pygame.Surface((32,32))
        #if position == 0:
        #    self.color = RED
        #if position == 1:
        #    self.color = GREEN
        #if position == 2:
        #    self.color = BLUE
        #if position == 3:
        #    self.color = PURPLE
        self.color = color

        
        self.textstr = str(freq) 

        
        column = random.randint(1, 4)
        self.rect = self.surf.get_rect(center = ((position*200)+column*40, 0))

    def move(self):
        self.rect.move_ip(0, 16)

    def draw(self, surface):        
        pygame.draw.rect(surface, self.color, self.rect)
        text = self.font.render(self.textstr, False, GREEN, BLACK)
        surface.blit(text, (400, 300))
        #self.image = self.font.render("Blabla", 0, RED)



# Divide into frequency bands
bsplit.bandSplit(music)

# Generate beatmaps
#bmap.generateBeatmap("music_bass.wav", "complex", "bassMap.txt", 0.05)
#bmap.generateBeatmap("music_mid.wav", "complex", "midMap.txt", 0.4)
#bmap.generateBeatmap("music_treb.wav", "complex", "trebMap.txt", 0.4)


#inFile = open("beatmaps/fullMap.txt")

#for line in inFile:
#    fullMap.append(round(float(line), 2))

#inFile.close()

#bassMap = Beatmap("beatmaps/bassMap.txt", 0)
#midMap = Beatmap("beatmaps/midMap.txt", 1)
#trebMap = Beatmap("beatmaps/trebMap.txt", 2)
#beatmaps = []
#beatmaps.append(bassMap)
#beatmaps.append(midMap)
#beatmaps.append(trebMap)
#beatmaps.append(fullMap)



#music = "brink.wav"
pygame.mixer.music.load(music)
#pygame.mixer.music.play(-1)

time_passed = 0
music_started = 0

await_beat = fullMap[0]
next_beat = 0

# Game loop
while True:
    time_passed += (1/FPS)
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()

    if music_started == 0:
        pygame.mixer.music.play(-1)
        music_started = 1

    if time_passed >= await_beat:
        newBlock = Block(0, RED, round(beatmap_pos[next_beat]))
        blocks.append(newBlock)
        next_beat += 1
        await_beat = fullMap[next_beat]

    #for bm in beatmaps:
    #    bm.progress(time_passed)
    
    SCREEN.fill(BLACK)

    for aBlock in blocks:
        aBlock.move()
        aBlock.draw(SCREEN)

    pygame.display.update()

    # Wait for one frame-time unit to pass before continuing the game loop
    FrameClock.tick(FPS)
