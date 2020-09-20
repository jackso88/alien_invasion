import pygame
from pygame.sprite import Sprite

class Bullet(Sprite):
	def __init__(self, ai_settings, screen, ship):
		super(Bullet, self).__init__()
		self.screen = screen
		self.rect = pygame.Rect(0, 0, ai_settings.bullet_width,
		ai_settings.bullet_height)
		self.rect.centery = ship.rect.centery
		self.rect.right = ship.rect.right
		self.x = float(self.rect.x)
		self.color = ai_settings.bullet_color
		self.speed_factor = ai_settings.bullet_speed_factor
		self.screen_rect = screen.get_rect()
				
	def update(self):
		"""Перемещает пулю вверх по экрану."""
		self.x += self.speed_factor
		self.rect.x = self.x
		
	def draw_bullet(self):
		"""Вывод пули на экран."""
		pygame.draw.rect(self.screen, self.color, self.rect)
