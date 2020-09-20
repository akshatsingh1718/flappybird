import pygame
import sys
import random
from pygame.locals import *

FPS = 32
SCREEN_WIDTH = 289
SCREEN_HEIGHT = 511
SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
GROUND_Y = int(SCREEN_HEIGHT * 0.8)
GAME_SPRITES = {}
GAME_SOUNDS = {}
PLAYER = 'gallery/sprites/bird.png'
BACKGROUND = 'gallery/sprites/bg.png'
PIPE = 'gallery/sprites/pipe.png'


def welcomeScreen():
    """
    Shows welcome images on the screen
    """
    playerX = int(SCREEN_WIDTH/5)
    playerY = int((SCREEN_HEIGHT - GAME_SPRITES['player'].get_height())/2)
    # messageX = int(SCREEN_WIDTH - GAME_SPRITES['message'].get_width())/2
    messageY = int(SCREEN_HEIGHT * 0.13)
    # Base Cordinates
    baseX = 0
    while True:
        for event in pygame.event.get():
            # Ig user clicks on cross button then close the game
            if event.type == QUIT or (event.type == K_DOWN and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()

            # if user presses space or up arrow key then return and call mainGame()
            elif event.type == KEYDOWN and (event.key == K_SPACE or event.key == K_UP):
                return
            else:
                SCREEN.blit(GAME_SPRITES['background'], (0, 0))
                # SCREEN.blit(GAME_SPRITES['message'], (baseX, GROUND_Y))
                SCREEN.blit(GAME_SPRITES['base'], (baseX, GROUND_Y))
                SCREEN.blit(GAME_SPRITES['player'], (playerX, playerY))
                pygame.display.update()
                FPSCLOCK.tick(FPS)


def mainGame():
    score = 0
    playerX = int(SCREEN_WIDTH/5)
    playerY = int(SCREEN_WIDTH/2)
    baseX = 0

    # Create 2 pipes for blitting on screen
    newPipe1 = getRandomPipe()
    newPipe2 = getRandomPipe()

    # List of upper pipes
    upperPipes = [
        {
            'x': SCREEN_WIDTH+200,
            'y': newPipe1[0]['y']
        },
        {
            'x': SCREEN_WIDTH+200+(SCREEN_WIDTH/2),
            'y': newPipe2[0]['y']
        }
    ]
    # List of lower pipes
    lowerPipes = [
        {
            'x': SCREEN_WIDTH+200,
            'y': newPipe1[1]['y']
        },
        {
            'x': SCREEN_WIDTH+200+(SCREEN_WIDTH/2),
            'y': newPipe2[1]['y']
        }
    ]

    pipeVelX = -4
    playerVelY = -9
    playerMaxVelY = 10
    playerMinVelY = -8
    playerAccY = 1

    playerFlapAccv = -8  # Velocity while flapping
    playerFlapped = False  # True only when the bird is flapping

    while True:
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN and (event.key == K_SPACE or event.key == K_UP):
                if playerY > 0:
                    playerVelY = playerFlapAccv
                    playerFlapped = True
                    # GAME_SOUNDS['wing'].play()

        crashTest = isCollide(playerX, playerY, upperPipes, lowerPipes)
        if crashTest:
            return

        # Check for score
        playerMidPos = playerX + GAME_SPRITES['player'].get_width()/2
        for pipe in upperPipes:
            pipeMidPos = pipe['x'] + GAME_SPRITES['pipe'][0].get_width()/2
            if pipeMidPos <= playerMidPos < pipeMidPos + 4:
                score += 1
                print(f'Your Score is {score}')
                # GAME_SOUNDS['point'].play()

        if playerVelY < playerMaxVelY and not playerFlapped:
            """
            If the player is not flapping meaning it is coming downwards and
            playerVelY shoudl be less than playerMaxVelY as we dont want to
            increase bird downwards vel more than a specific point.
            """
            playerVelY += playerAccY

        if playerFlapped:
            """
            always change playerFlapped to false beacause if we dont then
            user only one hit will keep bird flapping and it won't come down.
            """
            playerFlapped = False

        playerHeight = GAME_SPRITES['player'].get_height()
        # This is for bird not to go under the ground
        playerY = playerY + min(playerVelY, GROUND_Y - playerY - playerHeight)

        # Moving pipes to the left
        for upperpipe, lowerpipe in zip(upperPipes, lowerPipes):
            upperpipe['x'] += pipeVelX
            lowerpipe['x'] += pipeVelX

        # Add a new pipe when the 1st pipe is about to move out of the screen
        if 0 < upperPipes[0]['x'] < 5:
            newPipe = getRandomPipe()
            upperPipes.append(newPipe[0])
            lowerPipes.append(newPipe[1])

        # If the pipes is out of the screen, remove it
        if upperPipes[0]['x'] < -GAME_SPRITES['pipe'][0].get_width():
            upperPipes.pop(0)
            lowerPipes.pop(0)

        # Blitting all the sprites
        SCREEN.blit(GAME_SPRITES['background'], (0, 0))
        for upperpipe, lowerpipe in zip(upperPipes, lowerPipes):
            SCREEN.blit(GAME_SPRITES['pipe'][0],
                        (int(upperpipe['x']), int(upperpipe['y'])))
            SCREEN.blit(GAME_SPRITES['pipe'][1],
                        (int(lowerpipe['x']), int(lowerpipe['y'])))

        SCREEN.blit(GAME_SPRITES['base'], (baseX, GROUND_Y))
        SCREEN.blit(GAME_SPRITES['player'], (playerX, playerY))

        # Displaying digits
        '''
        myDigits = [int(x) for x in list(str(score))]
        width = 0
        for digit in myDigits:
            width += GAME_SPRITES['numbers'][digit].get_width()
        xOffset = (SCREEN_WIDTH - width)/2
        for digit in myDigits:
            SCREEN.blit(GAME_SPRITES['numbers'][digit],
                        (xOffset, SCREEN_HEIGHT*0.12))
            xOffset += GAME_SPRITES['numbers'][digit].get_width()
        '''
        pygame.display.update()
        FPSCLOCK.tick(FPS)


def isCollide(playerX, playerY, upperPipes, lowerPipes):
    # If bird touches ground or hits the top of the window
    if playerY > GROUND_Y - 25 or playerY < 0:
        # GAME_SPRITES['hit'].play()
        return True
    for pipe in upperPipes:
        pipeHeight = GAME_SPRITES['pipe'][0].get_height()
        if (playerY < pipeHeight + pipe['y'] and abs(playerX - pipe['x']) < GAME_SPRITES['pipe'][0].get_width()):
            # GAME_SOUNDS['hit'].play()
            return True
    for pipe in lowerPipes:
        playerHeight = GAME_SPRITES['player'].get_height()
        if (playerY + playerHeight > pipe['y']) and abs(playerX - pipe['x']) < GAME_SPRITES['pipe'][0].get_width():
            # GAME_SOUNDS['hit'].play()
            return True
    return False


def getRandomPipe():
    """
    generate positions of two pipes(one bottom and top) for blitting on the screen
    """
    pipeHeight = GAME_SPRITES['pipe'][0].get_height()
    offset = SCREEN_HEIGHT/3
    y2 = offset + random.randrange(0, int(SCREEN_HEIGHT -
                                          GAME_SPRITES['base'].get_height() - 1.2*offset))
    pipeX = SCREEN_WIDTH + 10
    y1 = pipeHeight - y2 + offset
    pipe = [
        {'x': pipeX, 'y': -y1, },  # Upper Pipe
        {'x': pipeX, 'y': y2}  # Lower Pipe
    ]

    return pipe


if __name__ == '__main__':
    pygame.init()
    FPSCLOCK = pygame.time.Clock()
    pygame.display.set_caption('Flappy Bird')

    # Numbers Images
    GAME_SPRITES['numbers'] = (
        pygame.image.load('gallery/sprites/0.png').convert_alpha(),
        pygame.image.load('gallery/sprites/1.jpg').convert_alpha(),
        pygame.image.load('gallery/sprites/2.jpg').convert_alpha(),
        pygame.image.load('gallery/sprites/3.png').convert_alpha(),
        pygame.image.load('gallery/sprites/4.jpg').convert_alpha(),
        pygame.image.load('gallery/sprites/5.jpeg').convert_alpha(),
        pygame.image.load('gallery/sprites/6.png').convert_alpha(),
        pygame.image.load('gallery/sprites/7.png').convert_alpha(),
        pygame.image.load('gallery/sprites/8.png').convert_alpha(),
        pygame.image.load('gallery/sprites/9.png').convert_alpha()
    )

    # Message Image
    # GAME_SPRITES['message'] = pygame.image.load(
    #     'gallery/sprites/message.png').convert_aplha()

    # Base Image
    GAME_SPRITES['base'] = pygame.image.load('gallery/sprites/base.png')

    # Pipe Images
    GAME_SPRITES['pipe'] = (
        pygame.transform.rotate(pygame.image.load(PIPE).convert_alpha(), 180),
        pygame.image.load(PIPE).convert_alpha()
    )

    # Game Sounds

    # Background Image
    GAME_SPRITES['background'] = pygame.image.load(BACKGROUND).convert()

    # Bird Image
    GAME_SPRITES['player'] = pygame.image.load(PLAYER).convert_alpha()

    while True:
        welcomeScreen()
        mainGame()
