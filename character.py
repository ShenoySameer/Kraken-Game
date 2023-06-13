import pygame
import time

class Character():
    def __init__(self, x, y, data, sprite_sheet, animation_steps, health_sheet):
        self.size = data[0]
        self.image_scale = data[1]
        self.animation_list = self.load_images(sprite_sheet, animation_steps)
        self.health_list = self.load_health(health_sheet)
        self.offset = data[2]
        self.action = 0
        self.frame_index = 0
        self.image = self.animation_list[self.frame_index]
        self.update_time = pygame.time.get_ticks()
        self.attack_time = pygame.time.get_ticks()
        self.rect = pygame.Rect((x,y, 40, 70))
        self.vel_y = 0
        self.running = False
        self.jump = False
        self.attacking = False
        self.dashing = False
        self.health = 5
        self.looking = "Right"

    def load_images(self, sprite_sheet, animation_steps):
        #extract images from sprite sheet
        animation_list = []
        for y, animation in enumerate(animation_steps):
            temp_img_list = []
            for i in range(animation):
                temp_img = sprite_sheet.subsurface(i * self.size, y * self.size, self.size, self.size)
                temp_img_list.append(pygame.transform.scale(temp_img, (self.size * self.image_scale, self.size * self.image_scale)))
            animation_list.append(temp_img_list)

        return animation_list

    def load_health(self, health_sheet):
        #extract images from sprite sheet
        health_list = []
        for y, animation in enumerate([5,5,5,5,5,5]):
            temp_health_list = []
            for i in range(animation):
                temp_img = health_sheet.subsurface(i * 15, y * 13, 15, 13)
                temp_health_list.append(pygame.transform.scale(temp_img, (15,13)))
            health_list.append(temp_health_list)

        return health_list

    def move(self, sc_width, sc_height, surface, target, target2, attack, dash_timer):
        SPEED = 1
        GRAVITY = 0.018
        dx = 0
        dy = 0
        self.running = False


        #attack cool down method
        attack_cooldown = 500
        if pygame.time.get_ticks() - self.attack_time > attack_cooldown:
            self.attacking = False
            self.attack_time = pygame.time.get_ticks()

        #get keypress
        key = pygame.key.get_pressed()


        #movement
        if key[pygame.K_a]:
            dx = -SPEED
            self.looking = "Left"
            self.running = True
        if key[pygame.K_d]:
            dx = SPEED
            self.looking = "Right"
            self.running = True

        #jump
        if key[pygame.K_SPACE] and self.jump == False:
            self.vel_y = -3
            self.jump = True

        #attack
        if key[pygame.K_r] and self.attacking == False:
            self.attack(surface, target, target2)
            key[pygame.K_r] == False

        #dash
        # if key[pygame.K_q] and not self.dashing:
        #     if self.looking == "Right":
        #             self.rect.x += 2
        #     if self.looking == "left":
        #             self.rect.x -= 2
        #     self.dashing = True

        #apply gravity
        self.vel_y += GRAVITY
        dy += self.vel_y


        #player on screen
        if self.rect.left + dx < 0:
            dx = -self.rect.left
        if self.rect.right + dx > sc_width:
            dx = sc_width - self.rect.right
        if self.rect.bottom + dy > sc_height - 150:
            self.vel_y = 0
            dy = sc_height - 150 - self.rect.bottom
            self.jump = False

        #update player position
        self.rect.x += dx
        self.rect.y += dy

    #handle animatyion updates
    def update(self):
        #check what action the player is performing
        if self.attacking == True:
            self.update_action(1)
        elif self.jump == True:
            self.update_action(3)
        elif self.running == True:
            self.update_action(2)
        else:
            self.update_action(0)

        animation_cooldown = 80
        self.image = self.animation_list[self.action][self.frame_index]

        #check if enough time has passed since the last update
        if pygame.time.get_ticks() - self.update_time > animation_cooldown:
            self.frame_index += 1
            self.update_time = pygame.time.get_ticks()
        #check if the animation has finished
        if self.frame_index >= len(self.animation_list[self.action]):
            self.frame_index = 0

    def attack(self, surface, target, target2):
        self.attacking = True
        self.attack_time = pygame.time.get_ticks()
        if self.looking == "Right":
            attacking_rect = pygame.Rect(self.rect.centerx, self.rect.y, 3.5 * self.rect.width, 1/2 * self.rect.height)
        if self.looking == "Left":
            attacking_rect = pygame.Rect(self.rect.centerx - (3.5 * self.rect.width), self.rect.y, 3.5 * self.rect.width, 1/2 * self.rect.height)
        if attacking_rect.colliderect(target.rect):
            target.health -= 2
        if attacking_rect.colliderect(target2.rect):
            target.health -= 2



        #pygame.draw.rect(surface, (0,255, 0), attacking_rect)

    def update_action(self, new_action):
        #check if the new action is different to the previous one
        if new_action != self.action:
            self.action = new_action
            #update the animation settings
            self.frame_index = 0
            self.update_time = pygame.time.get_ticks()

    def draw(self, surface):
        if self.looking == "Right":
            flip = False
        if self.looking == "Left":
            flip = True
        img = pygame.transform.flip(self.image, flip, False)
        #pygame.draw.rect(surface, (255, 0, 0), self.rect)
        surface.blit(img, (self.rect.x - (self.offset[0] * self.image_scale), self.rect.y - (self.offset[1] * self.image_scale)))
