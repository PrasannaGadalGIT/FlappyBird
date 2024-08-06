import pygame
import random
import sys
from pygame.locals import *

#Variables

FPS = 40
SCREENWIDTH = 290
SCREENHEIGHT = 520
SCREEN = pygame.display.set_mode((SCREENWIDTH, SCREENHEIGHT))
BASE = SCREENHEIGHT * 0.4

SOUNDS = {}
SPIRITS = {}

PLAYER = 'assets/sprites/bluebird-midflap.png'
BACKGROUND = 'assets/sprites/background-night.png'
PIPE = 'assets/sprites/pipe-red.png'

if __name__ == '__main__':
    pygame.init()
    FPSCLOCK = pygame.time.Clock()
    pygame.display.set_caption("FlappyBird (Prasanna Gadal)")
    SPIRITS['background'] = pygame.image.load('assets/sprites/background-night.png').convert_alpha()
    SPIRITS['player'] = pygame.image.load(PLAYER).convert_alpha()
    SPIRITS['numbers'] = (
        pygame.image.load('assets/sprites/0.png').convert_alpha(),
        pygame.image.load('assets/sprites/1.png').convert_alpha(),
        pygame.image.load('assets/sprites/2.png').convert_alpha(),
        pygame.image.load('assets/sprites/3.png').convert_alpha(),
        pygame.image.load('assets/sprites/4.png').convert_alpha(),
        pygame.image.load('assets/sprites/5.png').convert_alpha(),
        pygame.image.load('assets/sprites/6.png').convert_alpha(),
        pygame.image.load('assets/sprites/7.png').convert_alpha(),
        pygame.image.load('assets/sprites/8.png').convert_alpha(),
        pygame.image.load('assets/sprites/9.png').convert_alpha(),
    )
    SPIRITS['base'] =  pygame.image.load('assets/sprites/base.png')
    SPIRITS['pipe'] = (
        pygame.transform.rotate(pygame.image.load(PIPE).convert_alpha(), 180),
        pygame.image.load(PIPE).convert_alpha()
    )

    #Sounds
    SOUNDS['die'] = pygame.mixer.Sound('assets/audio/die.wav')
    SOUNDS['hit'] = pygame.mixer.Sound('assets/audio/hit.wav')
    SOUNDS['wing'] = pygame.mixer.Sound('assets/audio/wing.wav')
    SOUNDS['point'] = pygame.mixer.Sound('assets/audio/point.wav')
    SOUNDS['swoosh'] = pygame.mixer.Sound('assets/audio/swoosh.wav')

    while True:
        pass


