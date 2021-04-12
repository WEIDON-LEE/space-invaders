import pygame
from pygame.sprite import Sprite

class Enemybullet(Sprite):
    def __init__(self, ai_game, boss_x, boss_y):
        super().__init__()
        self.screen = ai_game.screen
        self.setting = ai_game.setting
        self.color = self.setting.enemybullet_color
        self.rect = pygame.Rect(boss_x, boss_y, self.setting.enemybullet_width, self.setting.enemybullet_height)      
        self.x = float(self.rect.x)
        
    def update(self):
        self.x -= self.setting.enemybullet_speed
        self.rect.x = self.x
    def draw_bullet(self):
        pygame.draw.rect(self.screen, self.color, self.rect)