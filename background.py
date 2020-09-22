import pygame
from pygame.sprite import Sprite

class Background(Sprite):
	"""Класс, представляющий фоновый рисунок."""
	def __init__(self, ai_settings, screen):
		"""Инициализирует фон и задает его начальную позицию."""
		super(Background, self).__init__()
		self.screen = screen
		self.ai_settings = ai_settings
		self.screen_rect = screen.get_rect()
		# Загрузка фонового изображения и назначение атрибута rect.
		self.image = pygame.image.load('images/space.bmp')
		self.rect = self.image.get_rect()
		self.rect.x = 0
		self.rect.y = 0

	def blitme(self):
		self.screen.blit(self.image, self.rect)

