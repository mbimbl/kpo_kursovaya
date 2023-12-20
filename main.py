# --------------------------------------------------------------------------------------------
# Москва, МАИ, 2023.
#
# Курсовая работа по дисциплине "Конструирование программного обеспечения".
# Тема: "Мини-игры и демонстрационные примеры (анимация механики) - Прыжки (с учётом веса)".
#
# Автор: Богомольский В.Р.
# Преподаватель: Гагарин А.П.
# --------------------------------------------------------------------------------------------
# Описание программы.
#
# Концепт:
# Данная программа моделирует подпрыгивание тела с заданной массой. Заложенные в
# программу формулы вторят известным математическим моделям из физики. Пользователь может
# перед каждым прыжком задавать новую массу тела и наблюдать на экране эффект своих действий.
#
# Управление:
# С помощью клавиш WASD пользователь перемещает прыгуна по экрану.
# При нажатии Пробел прыгун совершает прыжок.
# Массу прыгуна можно изменять с помощью клавиш 1 и 2, соответственно уменьшая и увеличивая ее.
#
# Отчетность:
# Игровое окно снабжено полями с информацией о текущих значениях параметров игры, таких как масса
# прыгуна, его скорость, длительность и высота последнего прыжка. Кроме этого, после выхода из
# игры автоматически строится отчет о последнем прыжке прыгуна.
#
# --------------------------------------------------------------------------------------------

# Импорт необходимых библиотек
import pygame  # Основная библиотека для работы с окном и графикой
import matplotlib.pyplot as plt  # Библиотека для построения графиков
import numpy as np  # Вспомогательная математическая библиотека

# --------------------------------------------------------------------
# 1. Объявление и инициализация переменных
# --------------------------------------------------------------------

# --- Параметры окна ---
WINDOW_WIDTH = 1000  # Ширина игрового окна
WINDOW_HEIGHT = 1000  # Высота игрового окна
WINDOW_FPS = 30  # Частота обновления кадров окна

# --- Игровые константы ---
# Прыгун:
JUMPER_STARTING_X = WINDOW_WIDTH / 2  # Начальные положение по оси абсцисс (устанавливается посередине окна)
JUMPER_STARTING_Y = WINDOW_HEIGHT / 2  # Начальные положение по оси ординат (устанавливается посередине окна)
JUMPER_WIDTH = 40  # Ширина прыгуна в пикселях
JUMPER_HEIGHT = 60  # Высота прыгуна в пикселях
JUMPER_WALKING_SPEED = 10  # Скорость прыгуна при перемещении нажатием на стрелки
JUMPER_JUMP_ENERGY = 1000  # Энергия для прыжка
# Игровой мир:
WORLD_G = 9.8  # Ускорение свободного падения
# Кнопки пользователя:
BUTTON_WEIGHT_SHIFT = 0.01  # Изменение веса прыгуна при нажатии кнопки изменения веса

# --- Игровые переменные ---
# Прыгун:
jumper_x = JUMPER_STARTING_X  # Текущие координаты прыгуна по оси абсцисс
jumper_y = JUMPER_STARTING_Y  # Текущие координаты прыгуна по оси ординат
jumper_weight = 1  # Текущий вес прыгуна
# Игровое событие прыжок:
jump_t = 0  # Текущий момент прыжка
jump_total_time = 0  # Длительность прыжка
jump_time_delta = 100  # Точность временного отображения на графике
prev_jump_t = 0  # Длительность предыдущего прыжка
jump_starting_y = JUMPER_STARTING_X  # Координаты прыгуна по оси ординат прыгуна в момент отскока
jump_starting_velocity = 0  # Скорость прыгуна при старте прыжка
jump_state = False  # Флаг. Находится ли прыгун в прыжке
# Общий процесс игры:
game_stop = False  # Флаг. Необходимо ли прервать игру

# --- Переменные для отчета о прыжке ---
report_coordinates = [0]  # Запись координат прыгуна при прыжке

# --------------------------------------------------------------------
# 2. Подготовка окна к работе
# --------------------------------------------------------------------

pygame.init()  # Инициализация необходимых модулей для работы с игровым окном

game_window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))  # Установка размеров окна
pygame.display.set_caption("Прыжки (с учетом веса)")  # Установка заголовка окна

clock = pygame.time.Clock()  # Часы для поддержки выбранной частоты кадров

# --------------------------------------------------------------------
# 3. Основной игровой цикл
# --------------------------------------------------------------------

while True:

    # --- Игровая логика ---

    # Проверка, получен ли сигнал на прерывание игры:

    for event in pygame.event.get():  # Проверяем все события на наличия сигнала о прерывании игры
        if event.type == pygame.QUIT:
            game_stop = True

    if game_stop:  # Если был сигнал прервать игру, прерываем
        break

    # Считывание ввода пользователя:

    keys = pygame.key.get_pressed()

    # Изменение значений переменных в соответствии с вводом пользователя:

    if not jump_state:  # Когда прыгун не находится в состоянии прыжка

        if keys[pygame.K_KP_MINUS]:  # Уменьшение веса
            if jumper_weight - BUTTON_WEIGHT_SHIFT > 0:
                jumper_weight -= BUTTON_WEIGHT_SHIFT

        if keys[pygame.K_KP_PLUS]:  # Увеличение веса
            jumper_weight += BUTTON_WEIGHT_SHIFT

        if keys[pygame.K_LEFT] and jumper_x > JUMPER_WALKING_SPEED:  # Движение влево
            jumper_x -= JUMPER_WALKING_SPEED

        if keys[pygame.K_RIGHT] and jumper_x < WINDOW_WIDTH - JUMPER_WALKING_SPEED - JUMPER_WIDTH:  # Движение вправо
            jumper_x += JUMPER_WALKING_SPEED

        if keys[pygame.K_UP] and jumper_y > JUMPER_WALKING_SPEED:  # Движение вверх
            jumper_y -= JUMPER_WALKING_SPEED

        if keys[pygame.K_DOWN] and jumper_y < WINDOW_HEIGHT - JUMPER_HEIGHT - JUMPER_WALKING_SPEED:  # Движение вниз
            jumper_y += JUMPER_WALKING_SPEED

        if keys[pygame.K_SPACE]:  # Начало прыжка
            report_coordinates = []  # Начинаем записывать координаты и будем это делать каждый миг до приземления
            jump_state = True
            jump_starting_y = jumper_y  # "Запоминаем" начальную высоту прыжка
            jump_starting_velocity = (2 * JUMPER_JUMP_ENERGY / jumper_weight) ** 0.5  # Расчет начальной скорости из кинетической энергии
            jump_total_time = 2 * jump_starting_velocity / WORLD_G

    else:  # Когда прыгун уже находится в состоянии прыжка

        prev_jump_t = jump_t  # Время предыдущего прыжка необходимо зафиксировать в начале цикла

        jumper_y = jump_starting_y - jump_starting_velocity * jump_t + WORLD_G * (jump_t ** 2) / 2

        if jumper_y < jump_starting_y or jump_t == 0:  # Если прыгун еще выше исходной высоты
            jump_t += jump_total_time / jump_time_delta
            report_coordinates.append(jump_starting_y-jumper_y)

        else:  # Конец прыжка
            jump_t = 0
            report_coordinates.append(jump_starting_y-jumper_y)
            jump_state = False

    if int(jump_t) == int(prev_jump_t) and jump_t != 0:
        continue

    game_window.fill((0, 0, 0))  # Очистка экрана

    # --- Экран и графика ---

    # Настройка шрифтов:
    pygame.font.init()
    comicsans_font = pygame.font.SysFont('Comic Sans MS', 30)

    # Подготовка текста:
    text_weight = comicsans_font.render("Вес: " +
                                        str("%.2f" % jumper_weight),
                                        False, (100, 0, 0))
    text_starting_velocity = comicsans_font.render("Начальная скорость: " +
                                                   str("%.2f" % jump_starting_velocity),
                                                   False, (100, 0, 0))

    # Отрисовка текста:
    game_window.blit(text_weight, (0, 0))
    game_window.blit(text_starting_velocity, (0, 40))
    if not jump_state:  # Обновление следующих данных происходит только не во время прыжка
        jump_height_time_text = comicsans_font.render("Высота прыжка: " + str("%.2f" % max(report_coordinates)), False, (100, 0, 0))
    game_window.blit(jump_height_time_text, (0, 80))

    # Отрисовка прыгуна:
    pygame.draw.rect(game_window, (255, 0, 0), (jumper_x, jumper_y, JUMPER_WIDTH, JUMPER_HEIGHT))

    # Обновление экрана:
    pygame.display.update()

    # Прошествие времени, с выбранной частотой обновления:
    clock.tick(WINDOW_FPS)

# --------------------------------------------------------------------
# 4. Выход из игры
# --------------------------------------------------------------------

pygame.quit()  # Выход из игры

# --------------------------------------------------------------------
# 5. Выводим отчет о последнем прыжке прыгуна
# --------------------------------------------------------------------

if len(report_coordinates) > 1:  # Если есть необходимость создавать отчет
    x = np.arange(0, len(report_coordinates), 1)  # Моменты прыжка во времени
    for i in range(len(x)):
        x[i] = 1000 * jump_total_time * x[i] / jump_time_delta  # Перевод в мс
    y = report_coordinates  # Моменты прыжка в пространстве
    plt.plot(x, y)  # Подготовка к выводу
    plt.ylabel('Высота прыжка (м)')
    plt.xlabel('Время (мс)')
    plt.title('Отчет о последнем прыжке прыгуна')
    plt.show()