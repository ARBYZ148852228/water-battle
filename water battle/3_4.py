from all_colors import *  # Предположим, этот модуль содержит нужные цвета
import pygame.mixer
pygame.mixer.init()
import pygame
pygame.init()

# Настройки окна
size = (1280, 720)
screen = pygame.display.set_mode(size)
pygame.display.set_caption('Моя Игра')
BACKGROUND = (255, 255, 255)
screen.fill(BACKGROUND)
screen_rect = screen.get_rect()

# Корабль (синий квадрат)
ship = pygame.Rect(300, 200, 50, 100)
ship.right = screen_rect.right  # Корабль будет справа
ship.centery = screen_rect.centery  # Корабль по центру вертикально

# Ракеты (маленькие красные квадраты)
MISSILE_WIDTH = 10
MISSILE_HEIGHT = 10
NUM_MISSILES = 10  # Количество ракет
missiles = [pygame.Rect(screen_rect.left + i * MISSILE_WIDTH, screen_rect.centery, MISSILE_WIDTH, MISSILE_HEIGHT)
             for i in range(NUM_MISSILES)]

# Скорости ракеты и корабля
missile_speed_x = 5  # Скорость ракеты по горизонтали
ship_speed_y = 3 # Скорость вертикального движения корабля

# Флаги состояния игры
ship_alive = True  # Жив ли корабль?
missile_active = False  # Активна ли текущая ракета?

# Здоровье корабля
hp_ship = 1  # Начальное здоровье корабля

# Частота кадров
FPS = 60
clock = pygame.time.Clock()

# Загрузка звуков
pygame.mixer.music.load('soundtrack.mp3')  # Фоновый трек (замените на путь к вашему файлу)
pygame.mixer.music.play(-1)  # Бесконечное воспроизведение

explosion_sound = pygame.mixer.Sound('explosion.wav')  # Звук взрыва (замените на путь к вашему файлу)

# Основная логика игры
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and not missile_active and len(missiles) > 0:
                missile_active = True
                missile = missiles.pop(0)  # Берём первую ракету из списка

    # Движения корабля
    if ship_alive:
        ship.move_ip(0, ship_speed_y)  # Корабль движется вверх/вниз

        # Изменение направления движения корабля при достижении границ
        if ship.top <= 0 or ship.bottom >= screen_rect.bottom:
            ship_speed_y *= -1  # Меняем направление движения

    # Движение активной ракеты
    if missile_active:
        missile.move_ip(missile_speed_x, 0)  # Ракета движется вправо

        # Проверка столкновения ракеты с кораблем
        if missile.colliderect(ship):  # Используем colliderect для проверки пересечения
            hp_ship -= 1  # Уменьшаем здоровье корабля
            missile_active = False  # Ракета исчезает
            if hp_ship <= 0:
                ship_alive = False  # Корабль разрушен
                explosion_sound.play()  # Воспроизводим звук взрыва

        # Проверка выхода ракеты за границу экрана
        if missile.left > screen_rect.right:
            missile_active = False  # Ракета улетела за экран

    # Рисование фона и объектов
    screen.fill(BACKGROUND)
    if ship_alive:
        pygame.draw.rect(screen, BLUE, ship)  # Отображаем корабль

    # Отрисовка активной ракеты
    if missile_active:
        pygame.draw.rect(screen, RED, missile)  # Отображаем ракету

    # Текстовое отображение количества ракет
    font = pygame.font.SysFont(None, 32)
    text_missiles = f'Ракеты: {len(missiles)}'
    img_missiles = font.render(text_missiles, True, BLACK)
    screen.blit(img_missiles, (20, 20))  # Показываем количество ракет в левом верхнем углу

    # Текстовое отображение здоровья корабля
    text_hp = f'Жизни: {hp_ship}'
    img_hp = font.render(text_hp, True, BLACK)
    screen.blit(img_hp, (screen_rect.width - 120, 20))  # Показываем здоровье в правом верхнем углу

    # Обновляем экран
    pygame.display.flip()

    # Ограничение частоты кадров
    clock.tick(FPS)

# Завершение работы Pygame
pygame.quit()