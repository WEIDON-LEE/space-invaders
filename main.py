# WEIDONG LI COLLIN COLLEGE TEXAS 2020

import sys
from time import sleep
import pygame
import random
from pygame.sprite import Sprite
from setting import Setting
from game_stats import GameStats
from scoreboard import Scoreboard
from button import Button
from ship import Ship
from bullet import Bullet
from enemy import Enemy
from enemy_boss import Enemy_boss


class Main:
  def __init__(self):
      pygame.init()
      self.setting = Setting()
      pygame.mixer.music.load('./sound/wave.mp3')
      pygame.mixer.music.play(-1)     
      self.screen = pygame.display.set_mode(
          (self.setting.screen_width, self.setting.screen_height))
      pygame.display.set_caption("Air Combat")
      self.stats = GameStats(self)
      self.sb = Scoreboard(self)
      self.ship = Ship(self)
      self.ship.draw_health_bar()
      self.bullets = pygame.sprite.Group()
      self.enemy_group = pygame.sprite.Group()
      self.boss_group = pygame.sprite.Group()
      self.play_button = Button(self, "Play")
      self.enemybullet_group = pygame.sprite.Group()
    
  def run_game(self):
      while True:
        self._check_events()
        if self.stats.game_active:
           self.ship.update()
           self._add_enemy()
           self._add_boss()
           self._update_enemies()
           self._update_boss()
           self._update_bullets()
        self._update_screen()
        pygame.display.flip()

  def _add_enemy(self):
      if random.randrange(1,150) < 3:
         self.enemy_group.add(Enemy(self))
      
  def _add_boss(self):
      if random.randrange(1,300) < 2:
          self.boss_group.add(Enemy_boss(self))

  def _update_enemies(self):
      self.enemy_group.update()
      for enemy in self.enemy_group.copy():
        if enemy.rect.right < 0:
            self.enemy_group.remove(enemy)
      collide_enemy = pygame.sprite.spritecollideany(self.ship, self.enemy_group,)
      if collide_enemy:
        self._ship_hit(collide_enemy)
      
  def _update_boss(self):
      self.boss_group.update()
      for boss in self.boss_group.copy():
          if boss.rect.right < 0:
              self.boss_group.remove(boss)
      collide_enemy = pygame.sprite.spritecollideany(self.ship, self.boss_group,)
      if collide_enemy:
        self._ship_hit(collide_enemy)
      for boss in self.boss_group:  
          collide_bullet = pygame.sprite.spritecollideany(self.ship, boss.bullets)
          if collide_bullet:
              self._ship_hit(collide_bullet)

  def _update_bullets(self):
      self.bullets.update()
      for bullet in self.bullets.copy():
        if bullet.rect.right >= 1000:
            self.bullets.remove(bullet)
      self._check_bullet_enemy_collisions()
      self._check_bullet_boss_collisions()
  #enemy hit by ship bullet
  def _check_bullet_enemy_collisions(self):
      collisions = pygame.sprite.groupcollide(self.bullets, self.enemy_group, True, True)
      if collisions:
         for enemy in collisions.values():
            self.stats.score += self.setting.enemy_points * len(enemy)
         self.sb.prep_score()
         self.sb.check_high_score()
      if not self.enemy_group:
          self._add_enemy()
  #enemy boss hit by ship bullet
  def _check_bullet_boss_collisions(self):
      collisions = pygame.sprite.groupcollide(self.bullets, self.boss_group, True, True)
      if collisions:
         for boss in collisions.values():
            self.stats.score += self.setting.boss_points * len(boss)
         self.sb.prep_score()
         self.sb.check_high_score()
      if not self.boss_group:
        #   self.bullets.empty()
          self._add_boss()
  #key control function
  def _check_events(self):
      for event in pygame.event.get():
        if event.type == pygame.QUIT:
           sys.exit()
        elif event.type == pygame.KEYDOWN:
           self._check_keydown_events(event)
        elif event.type == pygame.KEYUP:
           self._check_keyup_events(event)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            self._check_play_button(mouse_pos)
  # click button to start gaame
  def _check_play_button(self, mouse_pos):    
        button_clicked = self.play_button.rect.collidepoint(mouse_pos)
        if button_clicked and not self.stats.game_active:
            self.stats.reset_stats()
            self.stats.game_active = True
            self.sb.prep_score()
            self.sb.prep_ships()
            self.enemy_group.empty()
            self.bullets.empty()
            self.ship.center_ship()
            self._add_enemy()
            pygame.mouse.set_visible(False)
  #when key down
  def _check_keydown_events(self,event):
        if event.key == pygame.K_UP:
            self.ship.moving_up = True
        elif event.key == pygame.K_DOWN:
            self.ship.moving_down = True
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = True
        elif event.key == pygame.K_RIGHT:
            self.ship.moving_right = True
        elif event.key == pygame.K_q:
            sys.exit()
        elif event.key == pygame.K_SPACE:
            self._fire_bullet()
  #when key up
  def _check_keyup_events(self,event):
        if event.key == pygame.K_UP:
            self.ship.moving_up = False
        elif event.key == pygame.K_DOWN:
            self.ship.moving_down = False
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = False
        elif event.key == pygame.K_RIGHT:
            self.ship.moving_right = False
  #ship bullet
  def _fire_bullet(self):
      if len(self.bullets) < self.setting.bullets_allowed:
         new_bullet =Bullet(self)
         self.bullets.add(new_bullet)
  #ship damage condition and result
  def _ship_hit(self, collide_enemy):
      self.ship.take_damage()
      if self.ship.health > 0:
         self.enemy_group.remove(collide_enemy)
         self.boss_group.remove(collide_enemy)
         for boss in self.boss_group:
             boss.bullets.remove(collide_enemy)
         return
      if self.stats.ships_left > 0:
         self.stats.ships_left -= 1
         self.sb.prep_ships()        
         self.bullets.empty()
         self.enemy_group.empty()
         self.boss_group.empty()
         self.ship.center_ship()
         self.ship.revive()        
         sleep(0.5)
      else:
         self.stats.game_active =False
         pygame.mouse.set_visible(True)
  #loop screen
  def _update_screen(self):
      self.screen.blit(self.setting.bg_img, self.setting.bg_img.get_rect())
      self.sb.show_score()
      self.ship.draw_health_bar()
      if not self.stats.game_active:
          self.play_button.draw_button()
      self.ship.blitme()
      for enemy in self.enemy_group.sprites():
          enemy.blitme()
      for boss in self.boss_group.sprites():
          boss.blitme()
      for bullet in self.bullets.sprites():
          bullet.draw_bullet()
      
if __name__=='__main__':
    ai = Main()
    ai.run_game()