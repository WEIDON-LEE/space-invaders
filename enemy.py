import pygame
import random
from pygame.sprite import Sprite

class Enemy(Sprite):

    def __init__(self, ai_game):
        super().__init__()
        self.setting = ai_game.setting
        self.screen = ai_game.screen
        self.image = pygame.image.load('img/enemy.png')
        self.rect = self.image.get_rect()     
        self.enemy_size = 64 
        self.enemy_speed = random.randrange(2,6)       
        self.rect.x = self.setting.screen_width
        self.rect.y = random.randrange(0 + self.enemy_size, self.setting.screen_height - self.enemy_size)

    def update(self):
        self.rect.x -= self.enemy_speed
        self.x = self.rect.x
        self.y = self.rect.y

    def blitme(self):
        self.screen.blit(self.image, self.rect)


    
    
