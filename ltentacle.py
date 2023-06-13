import pygame
import random

class Ltentacle():
    def __init__(self, x, y, sprite_sheet, data):
        self.image_scale = data[0]
        self.offset = data[1]
        self.rect = pygame.Rect((x,y, 60, 90))
        self.image = sprite_sheet
        self.vel_y = 0
        self.jump = False
        self.attacking = False
        self.health = 100
        self.hit_time = pygame.time.get_ticks()
        self.attack = False
        self.attack_time = pygame.time.get_ticks()
        self.attack_start = pygame.time.get_ticks()


    def move(self, sc_width, sc_height, surface, target, bossspeed):
        SPEED = 5
        GRAVITY = 0.1
        dy = 0
        dx = bossspeed

        #attack pattern
        # attack_cooldown = 200000
        # attack_duration = 3000
        # (pygame.time.get_ticks() - self.attack_time)
        # if self.attack == False:
        #     if pygame.time.get_ticks() - self.attack_time > attack_cooldown:
        #         self.attack = True
        #         self.attack_start = pygame.time.get_ticks()
        #         self.rect.x = 10000
        #
        # if self.attack == True:
        #     if pygame.time.get_ticks() - self.attack_start > attack_duration:
        #         self.attack = False
        #         self.attack_time = pygame.time.get_ticks()
        #
        # if self.attack == True:
        #     if pygame.time.get_ticks() - self.attack_start > attack_duration/2:
        #         dx = -SPEED
        #     elif pygame.time.get_ticks() - self.attack_start < attack_duration/7:
        #         dx = -1
        #if self.rect.left < 0:
            #self.attack_time = pygame.time.get_ticks()





        #attack
        hit_cooldown = 2500
        if pygame.time.get_ticks() - self.hit_time > hit_cooldown:
            self.attacking = False
            self.hit_time = pygame.time.get_ticks()


        attacking_rect = pygame.Rect(self.rect.centerx, self.rect.centery, self.rect.width, self.rect.height)

        if attacking_rect.colliderect(target.rect) and self.attacking == False:
                target.health -= 1
                self.attacking = True



        #apply gravity
        self.vel_y += GRAVITY
        dy += self.vel_y


        #player on screen
        if self.rect.left + dx < -100:
            dx = -100
        if self.rect.right + dx > sc_width:
            dx = sc_width - self.rect.right
        if self.rect.bottom + dy > sc_height - 195:
            self.vel_y = 0
            dy = sc_height - 195 - self.rect.bottom
            self.jump = False

        #update player position
        self.rect.x += dx
        self.rect.y += dy




        #pygame.draw.rect(surface, (0,255, 0), attacking_rect)

    def attack2(self, start_time):
        if pygame.time.get_ticks() == start_time:
            self.rect.x = -100

        bossspeed = 0

        if pygame.time.get_ticks() - start_time > 1500:
                bossspeed = 5
        elif pygame.time.get_ticks() - start_time < 400:
                bossspeed = 1

        return bossspeed

    def startposition(self):
         self.rect.x = -100

    def draw(self, surface):
        self.image = pygame.transform.scale(self.image, (383 * self.image_scale, 41 * self.image_scale))
        img = pygame.transform.flip(self.image, True, False)
        surface.blit(img, (self.rect.x - (self.offset[0] * self.image_scale), self.rect.y - (self.offset[1] * self.image_scale)))
