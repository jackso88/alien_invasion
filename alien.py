import pygame
from pygame.sprite import Sprite

class Alien(Sprite):
	"""Класс, представляющий одного пришельца."""
	def __init__(self, ai_settings, screen):
		"""Инициализирует пришельца и задает его начальную позицию."""
		super(Alien, self).__init__()
		self.screen = screen
		self.ai_settings = ai_settings
		self.screen_rect = screen.get_rect()
		# Загрузка изображения пришельца и назначение атрибута rect.
		self.image = pygame.image.load('images/alien.png')
		self.rect = self.image.get_rect()
		# Каждый новый пришелец появляется в правом верхнем углу экрана.
		self.rect.x = self.screen_rect.right - self.rect.width
		self.rect.y = self.screen_rect.top
		# Сохранение точной позиции пришельца.
		self.y = float(self.rect.y)
	
	def blitme(self):
		"""Выводит пришельца в текущем положении."""
		self.screen.blit(self.image, self.rect)
		
	def update(self):
		"""Перемещает пришельца вверх или вниз."""
		self.y -= (self.ai_settings.alien_speed_factor *
		self.ai_settings.fleet_direction)
		self.rect.y= self.y
	
	def check_edges(self):
		"""Возвращает True, если пришелец находится у края экрана."""
		screen_rect = self.screen.get_rect()
		if self.rect.bottom >= screen_rect.bottom:
			return True
		elif self.rect.top <= 0:
			return True
