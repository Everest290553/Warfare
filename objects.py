import random
import math
import pygame.mouse
import database as db
from settings import *

class GameSprite(pygame.sprite.Sprite):
    def __init__(self, image, x, y, width, height, speed):
        super().__init__()
        self.width = width
        self.height = height
        self.speed = speed
        self.image = pygame.transform.scale(pygame.image.load(image), (width, height))
        self.start_image = self.image

        self.rect = self.image.get_rect()
        self.rect.center = (x,y)

        self.hitbox = pygame.Rect(self.rect.x, self.rect.y, width/2, height/2)
    def change_image(self, new_image):
        self.image = pygame.transform.scale(pygame.image.load(new_image), (self.width, self.height))
        self.start_image = self.image
    def rotate(self, angle):
        self.image = pygame.transform.rotate(self.start_image, angle)
        self.rect = self.image.get_rect(center=(self.rect.centerx, self.rect.centery))
    def draw(self):
        window.blit(self.image, self.rect)

class Player(GameSprite):
    def __init__(self, image, x, y, width, height, speed):
        super().__init__(image, x, y, width, height, speed)
        self.max_hp = 100
        self.hp = self.max_hp
        self.reload = 0
        for arm in arms:
            if db.is_active(arms.index(arm)):
                self.rate = reload[arms.index(arm)]
    def update(self):
        self.hitbox.center = self.rect.center

        button = pygame.mouse.get_pressed()
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a] and self.rect.x > 0:
            self.rect.centerx -= self.speed
        if keys[pygame.K_LEFT] and self.rect.x > 0:
            self.rect.centerx -= self.speed
        if keys[pygame.K_d] and self.rect.x < window_width - self.rect.width:
            self.rect.centerx += self.speed
        if keys[pygame.K_RIGHT] and self.rect.x < window_width - self.rect.width:
            self.rect.centerx += self.speed
        if keys[pygame.K_w] and self.rect.y > 50:
            self.rect.centery -= self.speed
        if keys[pygame.K_UP] and self.rect.y > 50:
            self.rect.centery -= self.speed
        if keys[pygame.K_s] and self.rect.y < window_height-55:
            self.rect.centery += self.speed
        if keys[pygame.K_DOWN] and self.rect.y < window_height-55:
            self.rect.centery += self.speed
        if button[0]:
            if self.reload == 0:
                self.fire()
                fire_sound.play()
                self.reload += 1
        if self.reload !=0:
            self.reload += 1
        if self.reload == self.rate:
            self.reload = 0
        pos = pygame.mouse.get_pos()
        dx = pos[0] - self.rect.centerx
        dy = -(pos[1] - self.rect.centery)
        ang = math.degrees(math.atan2(dy, dx))
        self.rotate(ang - 90)
    def fire(self):
        pos = pygame.mouse.get_pos()
        dx = pos[0] - self.rect.centerx
        dy = -(pos[1] - self.rect.centery)
        ang = -math.atan2(dy, dx)

        bul = Bullet(bullet_image, self.rect.centerx, self.rect.centery, 7, 20, 70, ang)
        bullets.add(bul)

class Bullet(GameSprite):
    def __init__(self, image, x, y, width, height, speed, angle):
        super().__init__(image, x, y, width, height, speed)
        self.angle = angle
    def update(self):
        self.hitbox.center = self.rect.center
        self.rotate(math.degrees(-self.angle)-90)
        self.rect.x += math.cos(self.angle) * self.speed
        self.rect.y += math.sin(self.angle) * self.speed

class Enemy(GameSprite):
    def __init__(self, image, x, y, width, height, speed):
        super().__init__(image, x, y, width, height, speed)
        self.max_hp = 1
        self.hp = self.max_hp
    def spawn(self):
        self.hp = self.max_hp
        if self in boss_list:
            self.change_image(enemy_images[1])
        else:
            self.change_image(enemy_images[0])
        place = random.randint(1,4)
        if place == 1:
            self.rect.x = random.randint(0, window_width)
            self.rect.y = -100
        elif place == 2:
            self.rect.x = random.randint(0, window_width)
            self.rect.y = window_height + 100
        elif place == 3:
            self.rect.x = -100
            self.rect.y = random.randint(0, window_height)
        elif place == 4:
            self.rect.x = window_width + 100
            self.rect.y = random.randint(0, window_height)
    def update(self, angle):
        self.hitbox.center = self.rect.center
        self.rotate(math.degrees(-angle)-90)
        self.rect.x += math.cos(angle) * self.speed
        self.rect.y += math.sin(angle) * self.speed

class Button(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, color, label, callback = None):
        super().__init__()
        if callback is not None:
            self.callback = callback
        else:
            self.callback = self.cb_fun
        
        self.color = color
        r = color[0] + 15 if (color[0] + 15) <= 255 else 255
        g = color[1] + 15 if (color[1] + 15) <= 255 else 255
        b = color[2] + 15 if (color[2] + 15) <= 255 else 255

        self.light_color = (r,g,b)
        self.width = width
        self.height = height
        self.pressed = False

        self.surface = pygame.Surface((width, height))

        self.rect = self.surface.get_rect()
        self.rect.centerx = x
        self.rect.centery= y

        self.text = label
        self.label_rect = self.text.get_rect()
        self.label_rect.centerx = width / 2
        self.label_rect.centery = height / 2

        self.surface.fill(self.color)
        self.surface.blit(label, self.label_rect)
    def cb_fun(self):
        print(1)
    def change_color(self, color):
        self.color = color
        r = color[0] + 15 if (color[0] + 15) <= 255 else 255
        g = color[1] + 15 if (color[1] + 15) <= 255 else 255
        b = color[2] + 15 if (color[2] + 15) <= 255 else 255
        self.light_color = (r,g,b)
    def is_on(self):
        x, y = pygame.mouse.get_pos()
        on = self.rect.collidepoint(x,y)
        if on:
            self.surface.fill(self.light_color)
        else:
            self.surface.fill(self.color)
        return on
    def is_pressed(self):
        button = pygame.mouse.get_pressed()
        if self.is_on() and button[0] and not self.pressed:
            choice_sound.play()
            self.pressed = True
            self.callback()
        if not button[0]:
            self.pressed = False
    def update(self):
        self.is_pressed()
        self.surface.blit(self.text, self.label_rect)
    def draw(self):
        window.blit(self.surface, (self.rect.x, self.rect.y))

class Heal(GameSprite):
    def __init__(self, image, x, y, width, height):
        super().__init__(image, x, y, width, height, 0)
    def spawn(self):
        self.rect.x = random.randint(100, window_width - 100)
        self.rect.y = random.randint(100, window_height - 100)
