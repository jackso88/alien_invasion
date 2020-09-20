import sys
import pygame
from random import randint
from time import sleep
import json

from bullet import Bullet
from alien import Alien


def check_keydown_events(event, ai_settings, screen, ship, bullets):
	"""Реагирует на нажатие клавиш."""
	if event.key == pygame.K_d:
		ship.moving_right = True
	elif event.key == pygame.K_a:
		ship.moving_left = True
	elif event.key == pygame.K_w:
		ship.moving_up = True
	elif event.key == pygame.K_s:
		ship.moving_down = True
	elif event.key == pygame.K_SPACE:
		fire_bullet(ai_settings, screen, ship, bullets)
	elif event.key == pygame.K_ESCAPE:
		sys.exit()
		
			
def fire_bullet(ai_settings, screen, ship, bullets):			
	if len(bullets) < ai_settings.bullets_allowed:
		new_bullet = Bullet(ai_settings, screen, ship)
		bullets.add(new_bullet)
		
def check_keyup_events(event, ship):
	"""Реагирует на отпускание клавиш."""
	if event.key == pygame.K_d:
		ship.moving_right = False
	elif event.key == pygame.K_a:
		ship.moving_left = False
	elif event.key == pygame.K_w:
		ship.moving_up = False
	elif event.key == pygame.K_s:
		ship.moving_down = False
		
def check_events(ai_settings, screen, stats, sb, play_button, ship, aliens,
	bullets):
	"""Обрабатывает нажатия клавиш и события мыши."""
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			sys.exit()
		elif event.type == pygame.MOUSEBUTTONDOWN:
			mouse_x, mouse_y = pygame.mouse.get_pos()
			check_play_button(ai_settings, screen, stats, sb, play_button,
			ship, aliens, bullets, mouse_x, mouse_y)
		elif event.type == pygame.KEYDOWN:
			check_keydown_events(event, ai_settings, screen, ship, bullets)
		elif event.type == pygame.KEYUP:
			check_keyup_events(event, ship)
					
def update_screen(ai_settings, screen, stats, sb, ship, bullets, aliens, 
	background, play_button):
	background.blitme()
	for bullet in bullets.sprites():
		bullet.draw_bullet()
	ship.blitme()
	aliens.draw(screen)
	if not stats.game_active:
		play_button.draw_button()
	sb.show_score()
	pygame.display.flip()
	
	
def update_bullets(ai_settings, screen, stats, sb, ship, aliens, bullets):
	"""Обновляет позиции пуль и уничтожает старые пули."""
	bullets.update()
	for bullet in bullets.copy():
		if bullet.rect.left >= bullet.screen_rect.right:
			bullets.remove(bullet)
	check_bullet_alien_collisions(ai_settings, screen, stats, sb, ship,
		aliens, bullets)
			
def check_bullet_alien_collisions(ai_settings, screen, stats, sb, ship,
		aliens, bullets):
	"""Обработка коллизий пуль с пришельцами."""
	# Удаление пуль и пришельцев, участвующих в коллизиях.
	collisions = pygame.sprite.groupcollide(bullets, aliens, True, True)
	if collisions:
		for aliens in collisions.values():
			stats.score += ai_settings.alien_points * len(aliens)
		sb.prep_score()
		check_high_score(stats, sb)
	if len(aliens) == 0:
		ship.center_ship()
		bullets.empty()
		ai_settings.increase_speed()
		stats.level += 1
		sb.prep_level()
		create_fleet(ai_settings, screen, ship, aliens)
			
def get_number_aliens_y(ai_settings, alien_height):
	"""Вычисляет количество пришельцев в ряду."""
	available_space_y = ai_settings.screen_height - 2 * alien_height
	number_aliens_y = int(available_space_y / (2 * alien_height))
	return number_aliens_y
	
def create_alien(ai_settings, screen, aliens, alien_number, row_number):
	"""Создает пришельца и размещает его в ряду."""
	alien = Alien(ai_settings, screen)
	alien_height = alien.rect.height
	alien.y = alien_height + 2 * alien_height * alien_number
	alien.rect.y = alien.y
	alien.rect.x = ai_settings.screen_width - (
		alien.rect.width + 2 * alien.rect.width * row_number
		)
	aliens.add(alien)
	
def ship_hit(ai_settings, screen, stats, sb, ship, aliens, bullets):
	"""Обрабатывает столкновение корабля с пришельцем."""
	# Уменьшение ships_left.
	if stats.ships_left > 0:
		stats.ships_left -= 1
		sb.prep_ships()
	# Очистка списков пришельцев и пуль.
		aliens.empty()
		bullets.empty()
	# Создание нового флота и размещение корабля в центре.
		ship.center_ship()
		create_fleet(ai_settings, screen, ship, aliens)
	# Пауза.
		sleep(0.5)
	else:
		stats.game_active = False
		pygame.mouse.set_visible(True)
	
def create_fleet(ai_settings, screen, ship, aliens):
	"""Создает флот пришельцев."""
	# Создание пришельца и вычисление количества пришельцев в ряду.
	alien = Alien(ai_settings, screen)
	number_aliens_y = get_number_aliens_y(ai_settings, alien.rect.height)
	number_rows = get_number_rows(ai_settings, ship.rect.width,
		alien.rect.width)
	# Создание флота
	for row_number in range(number_rows):
		for alien_number in range(number_aliens_y):
			create_alien(ai_settings, screen, aliens, alien_number,
				row_number)
		
def get_number_rows(ai_settings, ship_width, alien_width):
	"""Определяет количество рядов, помещающихся на экране."""
	available_space_x = (ai_settings.screen_width - 
		(3 * alien_width) - ship_width)
	number_rows = int(available_space_x / (3 * alien_width))
	return number_rows

def check_fleet_edges(ai_settings, aliens):
	"""Реагирует на достижение пришельцем края экрана."""
	for alien in aliens.sprites():
		if alien.check_edges():
			change_fleet_direction(ai_settings, aliens)
			break

def change_fleet_direction(ai_settings, aliens):
	"""Опускает весь флот и меняет направление флота."""
	for alien in aliens.sprites():
		alien.rect.x -= ai_settings.fleet_drop_speed
	ai_settings.fleet_direction *= -1

def update_aliens(ai_settings, screen, stats, sb, ship, aliens, bullets):
	"""
	Проверяет, достиг ли флот края экрана,
	после чего обновляет позиции всех пришельцев во флоте.
	"""
	check_fleet_edges(ai_settings, aliens)
	aliens.update()
	if pygame.sprite.spritecollideany(ship, aliens):
		ship_hit(ai_settings, screen, stats, sb, ship, aliens, bullets)
	check_aliens_left(ai_settings, screen, stats, sb, ship, aliens, bullets)
		
def check_aliens_left(ai_settings, screen, stats, sb, ship, aliens, bullets):
	"""Проверяет, добрались ли пришельцы до нижнего края экрана."""
	screen_rect = screen.get_rect()
	for alien in aliens.sprites():
		if alien.rect.left <= screen_rect.left:
	# Происходит то же, что при столкновении с кораблем.
			ship_hit(ai_settings, screen, stats, sb, ship, aliens, bullets)
			break

def check_play_button(ai_settings, screen, stats, sb, play_button, ship,
	aliens, bullets, mouse_x, mouse_y):
	"""Запускает новую игру при нажатии кнопки Play."""
	button_clicked = play_button.rect.collidepoint(mouse_x, mouse_y)
	if button_clicked and not stats.game_active:
		pygame.mouse.set_visible(False)
		ai_settings.initialize_dynamic_settings()
		stats.reset_stats()
		stats.game_active = True
		ship.center_ship()
		sb.prep_score()
		sb.prep_high_score()
		sb.prep_level()
		sb.prep_ships()
		aliens.empty()
		bullets.empty()
		create_fleet(ai_settings, screen, ship, aliens)
		
def check_high_score(stats, sb):
	"""Проверяет, появился ли новый рекорд."""
	if stats.score > stats.high_score:
		stats.high_score = stats.score
		sb.prep_high_score()
		filename = 'hight_score.json'
		with open(filename, 'w') as f_obj:
			json.dump(stats.score, f_obj)
			return stats.high_score
