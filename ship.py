import pygame
from pygame.sprite import Sprite


class Ship(Sprite):
    def __init__(self, ai_game):
        super().__init__()
        self.screen = ai_game.screen
        self.setting = ai_game.setting
        self.screen_rect = ai_game.screen.get_rect()

        self.image = pygame.image.load('img/ship.png')
        self.rect = self.image.get_rect()
        self.rect.midleft = self.screen_rect.midleft

        self.x = float(self.rect.x)
        self.y = float(self.rect.y)

        self.moving_right = False
        self.moving_left = False
        self.moving_up = False
        self.moving_down = False
        self.health = self.setting.ship_health
        
  
    def update(self):
        if self.moving_right and self.rect.right < self.screen_rect.right:
            self.x += self.setting.ship_speed
        if self.moving_left and self.rect.left > 0:
            self.x -= self.setting.ship_speed
        if self.moving_up and self.rect.top > 0:
            self.y -= self.setting.ship_speed
        if self.moving_down and self.rect.bottom < self.screen_rect.bottom:
            self.y += self.setting.ship_speed

        self.rect.x = self.x
        self.rect.y = self.y


    def blitme(self):
        self.screen.blit(self.image, self.rect)

    def center_ship(self):
        self.rect.midleft = self.screen_rect.midleft
        self.y = float(self.rect.y)
           
    def revive(self):
        self.health = self.setting.ship_health

    def take_damage(self):
        self.health -= self.setting.ship_damage
     
    def draw_health_bar(self):
        self.width = 80
        self.height = 30
        self.green = (0, 225, 0)
        self.red = (225, 0, 0)
        
        pygame.draw.rect(self.screen, self.red, pygame.Rect(240, 35, self.width, self.height))
        pygame.draw.rect(self.screen, self.green, pygame.Rect(240, 35, self.width/self.setting.ship_health*self.health, self.height))
       
        
            
                                                        