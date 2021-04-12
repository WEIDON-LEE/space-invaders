import pygame
import random

class Setting:
    def __init__(self):
        #screen
        self.screen_width = 1000
        self.screen_height = 750
        self.bg_img = pygame.image.load('img/bg_sky.png')

        #ship
        self.ship_speed = 5
        self.ship_limit = 3 
        self.ship_health = 4
        self.ship_damage = 1
        
        #bullet
        self.bullet_speed = 6
        self.bullet_width = 10
        self.bullet_height = 4
        self.bullet_color = (225, 225, 0)
        self.bullets_allowed = 10
        
        #enemy_bullet
        self.enemybullet_speed = 3
        self.enemybullet_width = 8
        self.enemybullet_height = 6
        self.enemybullet_color = (255, 0, 0)
        
        #scoring
        self.enemy_points = 10
        self.boss_points = 50
        
        