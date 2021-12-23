import pygame
import random
import math
from pygame import mixer
pygame.init()
# create the screen
screen = pygame.display.set_mode((800, 600))

# title nad logo
pygame.display.set_caption('SPACE INVADER')
# logo=pygame.image.load('cbse.png')
# pygame.display.set_icon(logo)

# player name
#name= input("what is ur name")
name = "RAGHVENDRA"
name.upper()
font1 = pygame.font.Font('freesansbold.ttf', 52)

# player
playerimg = pygame.image.load('spaceship.png')
playerX = 380
playerX_change = 0
playerY = 510
pygame.display.update()


# enemy
enemyimg = []
enemyX_change = []
enemyY_change = []
enemyX = []

enemyY = []
num_of_enemies = 7

for i in range(num_of_enemies):
    enemyimg.append(pygame.image.load("monster.png"))
    enemyX_change.append(7)
    enemyY_change.append(40)
    enemyX.append(random.randint(0, 730))
    enemyY.append(random.randint(0, 50))
    pygame.display.update()

# bullet
bulletimg = pygame.image.load("bullet1.png")
bulletX = 0
bulletX_change = 0
bulletY_change = 40
bulletY = 400
bullet_state = "ready"  # ready- you can't see bullet on screen #fire- bullet moving

# score
score_value = 0
font = pygame.font.Font('freesansbold.ttf', 32)
textX = 42
textY = 16

# game over text

over_font = pygame.font.Font('freesansbold.ttf', 76)
high_font = pygame.font.Font('freesansbold.ttf', 46)


# background
background = pygame.image.load("space.png")
bck = pygame.image.load("start.png")
# walls
wall = pygame.image.load('bricks.png')

# background sound
mixer.music.load('background.wav')
mixer.music.play(-1)


def show_name(x, y):
    nam_e = font1.render("HELLO " + name.upper(), True, (225, 0, 0))
    screen.blit(nam_e, (x, y))


def show_score(x, y):
    score = font.render("Score :" + str(score_value), True, (0, 255, 0))
    screen.blit(score, (x, y))


def game_over_text():
    over_text = over_font.render("Game Over ", True, (0, 255, 0))
    screen.blit(over_text, (220, 220))


def high_score():
    high_text = high_font.render(
        "Your Highscore : " + str(score_value), True, (0, 255, 0))
    screen.blit(high_text, (220, 310))


def player(x, y):
    screen.blit(playerimg, (x, y))  # blit means draw


def enemy(x, y, i):
    screen.blit(enemyimg[i], (x, y))


def fire_bullet(x, y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bulletimg, (x + 15, y+17))


def isCollision(enemyX, enemyY, bulletX, bulletY):
    distance = math.sqrt((math.pow(enemyX - bulletX, 2)) +
                         (math.pow(enemyY - bulletY, 2)))
    if distance <= 30:
        return True
    else:
        return False


# game loop
menu = True
running = True
while running:
    while menu:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                menu = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()

            screen.fill((0, 0, 0))
            screen.blit(bck, (-260, 80))
            show_name(174, 150)
            pygame.display.update()

    # background
    screen.fill((0, 0, 250))
    screen.blit(background, (0, 0))
    screen.blit(wall, (0, 450))

    # knowing keys
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            quit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerX_change = -15
            if event.key == pygame.K_RIGHT:
                playerX_change = 15
            if event.key == pygame.K_p:
                menu = True
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
            if event.key == pygame.K_SPACE:
                if bullet_state is "ready":
                    # bullet sound
                    bullet_sound = mixer.Sound('laser.mp3')
                    bullet_sound.play()
                    bulletX = playerX
                    fire_bullet(playerX, bulletY)
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_change = 0  # if it is not 0 then player remain moving

# player movement
    playerX += playerX_change
    if playerX <= 0:
        playerX = 0
    elif playerX >= 750:
        playerX = 750

# enemy movement
    for i in range(num_of_enemies):
        enemyX[i] += enemyX_change[i]
        if enemyX[i] <= 0:
            enemyX_change[i] = 5
            enemyY[i] += enemyY_change[i]
        elif enemyX[i] >= 700:
            enemyX_change[i] = -5
            enemyY[i] += enemyY_change[i]
         # game over
        if enemyY[i] > 390:
            for j in range(num_of_enemies):
                enemyY[j] = 2000
            game_over_text()
            high_score()

            continue
            pygame.display.update()


# collision
        collision = isCollision(enemyX[i], enemyY[i], bulletX, bulletY)
        if collision:
            bomb_sound = mixer.Sound('bomb.mp3')
            bomb_sound.play()
            bulletY = 510
            bullet_state = "ready"
            score_value += 1
            enemyX[i] = random.randint(0, 730)
            enemyY[i] = random.randint(0, 50)

        enemy(enemyX[i], enemyY[i], i)
        # bullet movement
    if bulletY <= 0:
        bulletY = 510
        bullet_state = "ready"
    if bullet_state is "fire":
        fire_bullet(bulletX, bulletY)
        bulletY -= bulletY_change

    player(playerX, playerY)
    show_score(textX, textY)
    pygame.display.update()
