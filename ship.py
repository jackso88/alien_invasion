import pygame
from pygame.sprite import Sprite

class Ship():
	"""Создает корабль"""
	def __init__(self, screen, ai_settings):
		"""инициирует корабль"""
		self.screen = screen
		self.image = pygame.image.load('images/ship.png')
		self.rect = self.image.get_rect()
		self.screen_rect = screen.get_rect()
		self.rect.left = self.screen_rect.left
		self.rect.centery = self.screen_rect.centery
		self.moving_right = False
		self.moving_left = False
		self.moving_up = False
		self.moving_down = False
		self.ai_settings = ai_settings
		self.left = float(self.screen_rect.left)
		self.centery = float(self.screen_rect.centery)
			
	def update(self):
		"""Обновляет позицию корабля с учетом флага."""
		if self.moving_right and self.rect.right < self.screen_rect.right - 1000:
			self.left += self.ai_settings.ship_speed_factor
		if self.moving_left and self.rect.left > 0:
			self.left -= self.ai_settings.ship_speed_factor
		if self.moving_up and self.rect.top > 0:
			self.centery -= self.ai_settings.ship_speed_factor
		if self.moving_down and self.rect.bottom < self.screen_rect.bottom:
			self.centery += self.ai_settings.ship_speed_factor
		self.rect.left = self.left
		self.rect.centery = self.centery
	
	def center_ship(self):
		self.left = self.screen_rect.left
		self.centery = self.screen_rect.centery
	
	def blitme(self):
		"""Рисует корабль в текущей позиции."""
		self.screen.blit(self.image, self.rect)
		
		
class ShipL(Sprite):
	def __init__(self, ai_settings, screen):
		super(ShipL, self).__init__()
		self.screen = screen
		self.image = pygame.image.load('images/shipl.png')
		self.ai_settings = ai_settings
		self.rect = self.image.get_rect()
