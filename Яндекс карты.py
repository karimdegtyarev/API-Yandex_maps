import os
import sys

import pygame
import requests

response = None
map_request = "http://static-maps.yandex.ru/1.x/?ll=-2.146939,51.263611&spn=0.001,0.001&l=sat"
spn = 0.001
w = -2.146939
le = 51.263611
map_vid = ['sat', 'map', 'sat,skl']
for_change = ['map', 'sat,skl']
vid = 'sat'
response = requests.get(map_request)

if not response:
    print("Ошибка выполнения запроса:")
    print(map_request)
    print("Http статус:", response.status_code, "(", response.reason, ")")
    sys.exit(1)

# Запишем полученное изображение в файл.
map_file = "map.png"
with open(map_file, "wb") as file:
    file.write(response.content)

# Инициализируем pygame
pygame.init()
screen = pygame.display.set_mode((1100, 450))
screen.fill((210, 0, 0))
# Рисуем картинку, загружаемую из только что созданного файла.
screen.blit(pygame.image.load(map_file), (0, 0))
f1 = pygame.font.Font(None, 36)
text1 = f1.render('Сейчас используется: sat', 1, (255, 255, 255))
text2 = f1.render('Изменить на:', 1, (255, 255, 255))
text3 = f1.render('map', 1, (255, 255, 255))
text4 = f1.render('sat,skl', 1, (255, 255, 255))
screen.blit(text1, (700, 50))
screen.blit(text2, (700, 100))
screen.blit(text3, (750, 130))
screen.blit(text4, (850, 130))
# Переключаем экран и ждем закрытия окна.
pygame.display.flip()

move_1 = ''


def changes(shirota, dolgota, scale, view):
    global f1
    global vid
    global w
    global le
    global spn
    global for_change
    vid = view
    w += shirota
    le += dolgota
    if 0.001 <= spn * scale <= 90 and w < 180 and le < 90:
        spn *= scale
        new_map_request = f"http://static-maps.yandex.ru/1.x/?ll={w},{le}&spn={spn},{spn}&l={view}"
        print(new_map_request)
        new_response = requests.get(new_map_request)

        if not new_response:
            print("Ошибка выполнения запроса:")
            print(new_map_request)
            print("Http статус:", new_response.status_code, "(", new_response.reason, ")")
            sys.exit(1)

        # Запишем полученное изображение в файл.
        new_map_file = "map.png"
        with open(new_map_file, "wb") as new_file:
            new_file.write(new_response.content)

        # Инициализируем pygame
        new_screen = pygame.display.set_mode((1100, 450))
        new_screen.fill((210, 0, 0))
        # Рисуем картинку, загружаемую из только что созданного файла.
        new_screen.blit(pygame.image.load(new_map_file), (0, 0))
        f1 = pygame.font.Font(None, 36)
        new_text1 = f1.render(f'Сейчас используется: {view}', 1, (255, 255, 255))
        new_text2 = f1.render('Изменить на:', 1, (255, 255, 255))
        if view == 'map':
            for_change = ['sat', 'sat,skl']
        elif view == 'sat':
            for_change = ['map', 'sat,skl']
        else:
            for_change = ['sat', 'map']
        new_text3 = f1.render(for_change[0], 1, (255, 255, 255))
        new_text4 = f1.render(for_change[1], 1, (255, 255, 255))
        screen.blit(new_text1, (700, 50))
        screen.blit(new_text2, (700, 100))
        screen.blit(new_text3, (750, 130))
        screen.blit(new_text4, (850, 130))
        new_screen.blit(new_text1, (700, 50))
        # Переключаем экран и ждем закрытия окна.
        pygame.display.flip()


running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            if 750 <= event.pos[0] <= 750 + 20 * len(for_change[0]) and 130 <= event.pos[1] <= 155:
                changes(0, 0, 1, for_change[0])
            elif 850 <= event.pos[0] <= 850 + 20 * len(for_change[1]) and 130 <= event.pos[1] <= 155:
                changes(0, 0, 1, for_change[1])
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                move_1 = "Left"

            elif event.key == pygame.K_RIGHT:
                move_1 = "Right"

            elif event.key == pygame.K_UP:
                move_1 = "Up"

            elif event.key == pygame.K_DOWN:
                move_1 = "Down"

            elif event.key == pygame.K_PAGEUP:
                move_1 = "Closely"

            elif event.key == pygame.K_PAGEDOWN:
                move_1 = "Far"

            if move_1 != 'Stop':
                if move_1 == "Right":
                    changes(3, 0, 1, vid)

                elif move_1 == "Left":
                    changes(-3, 0, 1, vid)

                elif move_1 == "Up":
                    changes(0, 3, 1, vid)

                elif move_1 == "Down":
                    changes(0, -3, 1, vid)

                elif move_1 == "Closely":
                    changes(0, 0, 0.5, vid)

                elif move_1 == "Far":
                    changes(0, 0, 2, vid)

pygame.quit()
os.remove(map_file)
