import pygame
import random
from pygame.sprite import Sprite
from enemybullet import Enemybullet

class Enemy_boss(Sprite):

    def __init__(self, ai_game):
        super().__init__()
        self.setting = ai_game.setting
        self.screen = ai_game.screen
        self.image = pygame.image.load('img/enemy2.png')
        self.rect = self.image.get_rect() 
        self.enemy_boss_size = 65
        self.enemy_boss_speed = random.randrange(1,2)
        self.rect.x = self.setting.screen_width
        self.rect.y = random.randrange(0 + self.enemy_boss_size, self.setting.screen_height - self.enemy_boss_size)
        #enemy bullet
        self.shoot_delay = 3000
        self.last_shot = pygame.time.get_ticks()
        self.num_of_shots = 2
        self.ai_game = ai_game
        self.bullets = pygame.sprite.Group()
        
    def update(self):
        self.rect.x -= self.enemy_boss_speed
        self.x = self.rect.x
        self.y = self.rect.y
        self.shoot()
        self.bullets.update()

    def blitme(self):
        self.screen.blit(self.image, self.rect)
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()
    
    def shoot(self):
        current_time = pygame.time.get_ticks()
        if current_time - self.last_shot > self.shoot_delay:
            self.last_shot = current_time
            bullet = Enemybullet(self.ai_game, self.x, self.y + self.enemy_boss_size/2)
            self.bullets.add(bullet)
           
            