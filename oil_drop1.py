import pygame
import random

class Oil_drop1():
    def __init__(self, x, y, sprite_sheet, data):
        self.image_scale = 5
        self.offset = [-3.2,-4.2]
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


    def move(self, sc_width, sc_height, surface, target):
        GRAVITY = 0.1
        dy = 0
        dx = 0
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
        dy += 1


        #player on screen
        # if self.rect.left + dx < -500:
        #     dx = -500
        # if self.rect.right + dx > sc_width:
        #     dx = sc_width - self.rect.right
        # if self.rect.bottom + dy > sc_height - 195:
        #     self.vel_y = 0
        #     dy = sc_height - 195 - self.rect.bottom
        #     self.jump = False

        #update player position
        self.rect.x += dx
        self.rect.y += dy



        #pygame.draw.rect(surface, (0,255, 0), attacking_rect)



        #pygame.draw.rect(surface, (0,255, 0), attacking_rect)dr

    def attack3(self, start_time, target):
        if pygame.time.get_ticks() == start_time:
            self.rect.x = target.rect.x
            self.rect.y = -150


    def startposition(self):
         self.rect.x = -200

    def draw(self, surface):
        self.image = pygame.transform.scale(self.image, (17 * self.image_scale, 21 * self.image_scale))
        img = pygame.transform.flip(self.image, True, False)
        surface.blit(img, (self.rect.x - (self.offset[0] * self.image_scale), self.rect.y - (self.offset[1] * self.image_scale)))
