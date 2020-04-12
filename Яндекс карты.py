import os
import sys

import pygame
import requests

response = None
map_request = "http://static-maps.yandex.ru/1.x/?ll=-2.146939,51.263611&spn=0.001,0.001&l=sat"
spn = 0.001
w = -2.146939
le = 51.263611
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
screen = pygame.display.set_mode((600, 450))
# Рисуем картинку, загружаемую из только что созданного файла.
screen.blit(pygame.image.load(map_file), (0, 0))
# Переключаем экран и ждем закрытия окна.
pygame.display.flip()

move_1 = ''


def moving(shirota, dolgota, scale):
    global w
    global le
    global spn
    w += shirota
    le += dolgota
    if 0.001 <= spn * scale <= 90 and w < 180 and le < 90:
        spn *= scale
        new_map_request = f"http://static-maps.yandex.ru/1.x/?ll={w},{le}&spn={spn},{spn}&l=sat"
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
        new_screen = pygame.display.set_mode((600, 450))
        # Рисуем картинку, загружаемую из только что созданного файла.
        new_screen.blit(pygame.image.load(new_map_file), (0, 0))
        # Переключаем экран и ждем закрытия окна.
        pygame.display.flip()


running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
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
                    moving(3, 0, 1)

                elif move_1 == "Left":
                    moving(-3, 0, 1)

                elif move_1 == "Up":
                    moving(0, 3, 1)

                elif move_1 == "Down":
                    moving(0, -3, 1)

                elif move_1 == "Closely":
                    moving(0, 0, 0.5)

                elif move_1 == "Far":
                    moving(0, 0, 2)

pygame.quit()
os.remove(map_file)
