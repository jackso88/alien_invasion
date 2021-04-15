class Settings():
    """задаются настройки"""
    def __init__(self):
        """инициализация класса"""
        self.screen_width = 1366
        self.screen_height = 700
        self.bg_color = (0, 0, 0)
        self.bullet_width = 25
        self.bullet_height = 3
        self.bullet_color = 255, 0, 0
        self.bullets_allowed = 3
        self.fleet_drop_speed = 10
        self.ship_limit = 3
        self.speedup_scale = 1.1
        self.score_scale = 1.5
        self.initialize_dynamic_settings()

    def initialize_dynamic_settings(self):
        """Инициализирует настройки, изменяющиеся в ходе игры."""
        self.ship_speed_factor = 1.5
        self.bullet_speed_factor = 3
        self.alien_speed_factor = 1
        self.fleet_direction = 1
        self.alien_points = 50

    def increase_speed(self):
        """Увеличивает настройки скорости."""
        self.ship_speed_factor *= self.speedup_scale
        self.bullet_speed_factor *= self.speedup_scale
        self.alien_speed_factor *= self.speedup_scale
        self.alien_points = int(self.alien_points * self.score_scale)
