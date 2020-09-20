import pygame
from pygame.sprite import Sprite

class Background(Sprite):
	"""Класс, представляющий одного пришельца."""
	def __init__(self, ai_settings, screen):
		"""Инициализирует пришельца и задает его начальную позицию."""
		super(Background, self).__init__()
		self.screen = screen
		self.ai_settings = ai_settings
		self.screen_rect = screen.get_rect()
		# Загрузка изображения пришельца и назначение атрибута rect.
		self.image = pygame.image.load('images/space.bmp')
		self.rect = self.image.get_rect()
		# Каждый новый пришелец появляется в левом верхнем углу экрана.
		self.rect.x = 0
		self.rect.y = 0

	def blitme(self):
		"""Выводит пришельца в текущем положении."""
		self.screen.blit(self.image, self.rect)

