import pygame
import random
import sys
from pygame.locals import *

#Variables

FPS = 40
SCREENWIDTH = 289
SCREENHEIGHT = 511
SCREEN = pygame.display.set_mode((SCREENWIDTH, SCREENHEIGHT))
BASE = SCREENHEIGHT * 0.78


SOUNDS = {}
SPRITES = {}

PLAYER = 'assets/sprites/bluebird-midflap.png'
BACKGROUND = 'assets/sprites/background-night.png'
PIPE = 'assets/sprites/pipe-green.png'

def homeScreen():
    playerx = int(SCREENWIDTH / 5)
    playery = int((SCREENHEIGHT - SPRITES['player'].get_height()) / 2)
    messagex = int((SCREENWIDTH - SPRITES['message'].get_width()) / 2)
    messagey = int(SCREENHEIGHT * 0.13)
    basex = 0
    while True:
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()
            elif event.type == KEYDOWN and (event.key == K_SPACE or event.key == K_UP):
                return
            else:
                SCREEN.blit(SPRITES['background'], (0, 0))
                SCREEN.blit(SPRITES['player'], (playerx, playery))
                SCREEN.blit(SPRITES['message'], (messagex, messagey))
                SCREEN.blit(SPRITES['base'], (basex, BASE))
                pygame.display.update()
                FPSCLOCK.tick(FPS)


def getRandomPipe():
    pipeheight = SPRITES['pipe'][0].get_height()
    offset = SCREENHEIGHT / 3
    y2 = offset + random.randrange(0, int(SCREENHEIGHT - SPRITES['base'].get_height() - 1.2 * offset))
    pipeX = SCREENWIDTH + 10
    y1 = pipeheight - y2 + offset
    pipe = [
        {'x' : pipeX, 'y': -y1},
        {'x' : pipeX, 'y' : y2}
    ]
    return pipe


def mainGame():
    score = 0
    playerx = int(SCREENWIDTH / 5)
    playery = int(SCREENHEIGHT / 2)
    basex = 0

    newpipe1 = getRandomPipe()
    newpipe2 = getRandomPipe()

    upperPipes = [
        {'x': SCREENWIDTH + 200, 'y': newpipe1[0]['y']},
        {'x': SCREENWIDTH + 200 + (SCREENWIDTH / 2), 'y': newpipe2[0]['y']},
    ]
    lowerPipes = [
        {'x': SCREENWIDTH + 200, 'y': newpipe1[1]['y']},
        {'x': SCREENWIDTH + 200 + (SCREENWIDTH / 2), 'y': newpipe2[1]['y']},
    ]

    pipeVelX = -4
    playerVelY = -9
    playerMaxVelY = 10
    playerMinVelY = -8
    playerAccY = 1
    playerFlappAccv = -8
    playerFlapped = False

    while True:
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN and (event.key == K_SPACE or event.key == K_UP):
                if playery > 0:
                    playerVelY = playerFlappAccv
                    playerFlapped = True
                    SOUNDS['wing'].play()

        testCrash = isCollided(playerx, playery, upperPipes, lowerPipes)
        if testCrash:
            gameOverScreen()
            return

        playerMidPos = playerx + SPRITES['player'].get_width() / 2
        for pipe in upperPipes:
            pipeMidPos = pipe['x'] + SPRITES['pipe'][0].get_width() / 2
            if pipeMidPos <= playerMidPos < pipeMidPos + 4:
                score += 1
                SOUNDS['point'].play()
                print(f"Your Score {score}")

        if playerVelY < playerMaxVelY and not playerFlapped:
            playerVelY += playerAccY
        if playerFlapped:
            playerFlapped = False

        playerHeight = SPRITES['player'].get_height()
        playery = playery + min(playerVelY, BASE - playery - playerHeight)

        if 0 < upperPipes[0]['x'] < 5:
            newPipe = getRandomPipe()
            upperPipes.append(newPipe[0])
            lowerPipes.append(newPipe[1])

        for upperPipe, lowerPipe in zip(upperPipes, lowerPipes):
            upperPipe['x'] += pipeVelX
            lowerPipe['x'] += pipeVelX

        if upperPipes[0]['x'] < -SPRITES['pipe'][0].get_width():
            upperPipes.pop(0)
            lowerPipes.pop(0)

        SCREEN.blit(SPRITES['background'], (0, 0))
        for upperPipe, lowerPipe in zip(upperPipes, lowerPipes):
            SCREEN.blit(SPRITES['pipe'][0], (upperPipe['x'], upperPipe['y']))
            SCREEN.blit(SPRITES['pipe'][1], (lowerPipe['x'], lowerPipe['y']))
        SCREEN.blit(SPRITES['base'], (basex, BASE))
        SCREEN.blit(SPRITES['player'], (playerx, playery))

        myDigits = [int(x) for x in list(str(score))]
        width = 0

        for digit in myDigits:
            width += SPRITES['numbers'][digit].get_width()
        Xoffset = (SCREENWIDTH - width) / 2

        for digit in myDigits:
            SCREEN.blit(SPRITES['numbers'][digit], (Xoffset, SCREENHEIGHT * 0.12))
            Xoffset += SPRITES['numbers'][digit].get_width()

        pygame.display.update()
        FPSCLOCK.tick(FPS)

def gameOverScreen():
    gameOverX = int((SCREENWIDTH - SPRITES['gameover'].get_width()) / 2)
    gameOverY = int(SCREENHEIGHT * 0.4)
    SCREEN.blit(SPRITES['gameover'], (gameOverX, gameOverY))
    pygame.display.update()
    pygame.time.wait(2000)

def isCollided(playerx, playery, upperPipes, lowerPipes):
    if playery + SPRITES['player'].get_height() >= BASE - 1:
        return True

    playerRect = pygame.Rect(playerx, playery, SPRITES['player'].get_width(), SPRITES['player'].get_height())
    for pipe in upperPipes:
        pipeRect = pygame.Rect(pipe['x'], pipe['y'], SPRITES['pipe'][0].get_width(), SPRITES['pipe'][0].get_height())
        if playerRect.colliderect(pipeRect):
            return True

    for pipe in lowerPipes:
        pipeRect = pygame.Rect(pipe['x'], pipe['y'], SPRITES['pipe'][1].get_width(), SPRITES['pipe'][1].get_height())
        if playerRect.colliderect(pipeRect):
            return True

    return False

if __name__ == '__main__':
    pygame.init()
    FPSCLOCK = pygame.time.Clock()
    pygame.display.set_caption("FlappyBird (Prasanna Gadal)")
    SPRITES['background'] = pygame.image.load('assets/sprites/background-night.png').convert_alpha()
    SPRITES['message'] = pygame.image.load('assets/sprites/message.png')
    SPRITES['player'] = pygame.image.load(PLAYER).convert_alpha()
    SPRITES['numbers'] = (
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
    SPRITES['base'] =  pygame.image.load('assets/sprites/base.png')
    SPRITES['pipe'] = (
        pygame.transform.rotate(pygame.image.load(PIPE).convert_alpha(), 180),
        pygame.image.load(PIPE).convert_alpha()
    )
    SPRITES['gameover'] = pygame.image.load('assets/sprites/gameover.png').convert_alpha()
    #Sounds
    SOUNDS['die'] = pygame.mixer.Sound('assets/audio/die.wav')
    SOUNDS['hit'] = pygame.mixer.Sound('assets/audio/hit.wav')
    SOUNDS['wing'] = pygame.mixer.Sound('assets/audio/wing.wav')
    SOUNDS['point'] = pygame.mixer.Sound('assets/audio/point.wav')
    SOUNDS['swoosh'] = pygame.mixer.Sound('assets/audio/swoosh.wav')

    while True:
        homeScreen()
        mainGame()


