import pygame
from character import Character
from rtentacle import Rtentacle
from ltentacle import Ltentacle
from oil_drop1 import Oil_drop1
import random

pygame.init()

#creat pygame window
sc_width = 1000
sc_height = 600
screen = pygame.display.set_mode((sc_width, sc_height))
pygame.display.set_caption("Kraken Battle")

#define character variables
SQUID_SIZE = 24
SQUID_OFFSET = [8, 5.5]
SQUID_SCALE = 4.5
SQUID_DATA = [SQUID_SIZE, SQUID_SCALE, SQUID_OFFSET]

#define boss variables
TENTACLE_OFFSET = [-5, -7]
TENTACLE_SCALE = 3
TENTACLE_DATA = [TENTACLE_SCALE, TENTACLE_OFFSET]

TENTACLE2_OFFSET = [350, -7]
TENTACLE2_DATA = [TENTACLE_SCALE, TENTACLE2_OFFSET]

#load background image
bg_image = pygame.image.load("Assets/background.png").convert_alpha()

#load character image
squid_sheet = pygame.image.load("Assets/full_spritesheet.png").convert_alpha()

#load boss sprites
tentacle = pygame.image.load("Assets/tentacle.png").convert_alpha()
ink_drop =pygame.image.load("Assets/ink_drop.png").convert_alpha()

#load win_screen
win_screen =pygame.image.load("Assets/Win_Screen.jpg").convert_alpha()

#health sprites
health_scale = 4
health_sheet = pygame.image.load("Assets/health_sprites.png").convert_alpha()
health5 = pygame.image.load("Assets/health_5.png").convert_alpha()
health5 = pygame.transform.scale(health5, (75 * health_scale, 13 * health_scale))
health4 = pygame.image.load("Assets/health_4.png").convert_alpha()
health4 = pygame.transform.scale(health4, (75 * health_scale, 13 * health_scale))
health3 = pygame.image.load("Assets/health_3.png").convert_alpha()
health3 = pygame.transform.scale(health3, (75 * health_scale, 13 * health_scale))
health2 = pygame.image.load("Assets/health_2.png").convert_alpha()
health2 = pygame.transform.scale(health2, (75 * health_scale, 13 * health_scale))
health1 = pygame.image.load("Assets/health_1.png").convert_alpha()
health1 = pygame.transform.scale(health1, (75 * health_scale, 13 * health_scale))
health0 = pygame.image.load("Assets/health_0.png").convert_alpha()
health0 = pygame.transform.scale(health0, (75 * health_scale, 13 * health_scale))

#define number of frames for each
SQUID_ANIMATION_STEPS = [10, 5, 7, 9]

#function for drawing the background
def draw_bg():
    scaled_bg = pygame.transform.scale(bg_image, (sc_width, sc_height))
    screen.blit(scaled_bg, (0, 0))

#function for drawing the health bar
def draw_hb(health, x, y):
    if health == 5:
        screen.blit(health5, (x, y))
    elif health == 4:
        screen.blit(health4, (x, y))
    elif health == 3:
        screen.blit(health3, (x, y))
    elif health == 2:
        screen.blit(health2, (x, y))
    elif health == 1:
        screen.blit(health1, (x, y))
    else:
        screen.blit(health0, (x,y))



def draw_bosshb(health, x, y):
    ratio = health / 100
    pygame.draw.rect(screen, (255, 255, 255), (x - 2, y - 2, 504, 34))
    pygame.draw.rect(screen, (0, 0, 0), (x, y, 500, 30))
    pygame.draw.rect(screen, (255, 0, 0), (x, y, 500 * ratio, 30))

#timers
jump_timer = 0
dash_timer = 0
attack_time = pygame.time.get_ticks()
rain_time = pygame.time.get_ticks()
bossspeed = 0

#create player
player = Character(125, 250, SQUID_DATA, squid_sheet, SQUID_ANIMATION_STEPS, health_sheet)

#create boss
rtentacle = Rtentacle(1000, 0, tentacle, TENTACLE_DATA)
ltentacle = Ltentacle(-100, 0, tentacle, TENTACLE2_DATA)
oil_drop1 = Oil_drop1(-200, 500, ink_drop, TENTACLE2_DATA)

#game loop
run = True
while run:
    attack = False
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                attack = True


    #timers
    dash_timer += 1

    #boss attack
    if rtentacle.health > 50:
        cooldown = 2000
    else:
        cooldown = 1000
    if pygame.time.get_ticks() - attack_time > cooldown:
        if pygame.time.get_ticks() - attack_time < 2006:
            rtentacle.startposition()
            ltentacle.startposition()
            attack_start = pygame.time.get_ticks()
            randomnum = random.randint(0,1)
        if randomnum == 0:
            bossspeed = rtentacle.attack1(attack_start)
        if randomnum == 1:
            bossspeed = ltentacle.attack2(attack_start)
        if pygame.time.get_ticks() - attack_time > 4000:
            attack_time = pygame.time.get_ticks()

    if pygame.time.get_ticks() - rain_time > cooldown:
        if pygame.time.get_ticks() - rain_time < 2006:
            oil_drop1.attack3(attack_start, player)
        if pygame.time.get_ticks() - rain_time > 4000:
            rain_time = pygame.time.get_ticks()

    if rtentacle.health > 50:
        if pygame.time.get_ticks() - rain_time > cooldown:
            if pygame.time.get_ticks() - rain_time < 2006:
                oil_drop1.attack3(attack_start, player)
            if pygame.time.get_ticks() - rain_time > 4000:
                rain_time = pygame.time.get_ticks()

    #draw background
    draw_bg()

    #show player stats
    draw_hb(player.health, 20, 20)
    draw_bosshb(rtentacle.health, 250, 550)

    #move fighter
    player.move(sc_width, sc_height, screen, rtentacle, ltentacle, attack, dash_timer)
    rtentacle.move(sc_width, sc_height, screen, player, bossspeed)
    ltentacle.move(sc_width, sc_height, screen, player, bossspeed)
    oil_drop1.move(sc_width, sc_height, screen, player)

    #update players
    player.update()

    #draw player
    rtentacle.draw(screen)
    ltentacle.draw(screen)
    oil_drop1.draw(screen)
    player.draw(screen)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
    pygame.display.update()

    if player.health < 1:
        run = False
    while rtentacle.health < 1:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break

        #this is purposeful
        scaled_bg = pygame.transform.scale(win_screen, (sc_width, sc_height))
        screen.blit(scaled_bg, (0, 0))
        pygame.display.update()


#exit pygame
pygame.quit()
