import json

class GameStats():
	"""Отслеживание статистики для игры Alien Invasion."""
	def __init__(self, ai_settings):
		"""Инициализирует статистику."""
		self.ai_settings = ai_settings
		self.reset_stats()
		self.game_active = False
		self.high_score = self.get_high_score()
						
	def reset_stats(self):
		"""Инициализирует статистику, изменяющуюся в ходе игры."""
		self.ships_left = self.ai_settings.ship_limit
		self.score = 0
		self.level = 1

	def get_high_score(self):
		"""Загружает рекорд"""
		filename = 'hight_score.json'
		try:
			with open(filename) as f_obj:
				self.high_score = json.load(f_obj)
				return self.high_score
		except FileNotFoundError:
			self.high_score = 0
			return self.high_score
					
				
	
	
