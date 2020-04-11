import os
import sys

import pygame
import requests

response = None
map_request = "http://static-maps.yandex.ru/1.x/?ll=-2.146939,51.263611&spn=0.01,0.01&l=sat"
spn = 0.001
w = -2.146939
l = 51.263611
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
    global l
    global spn
    w += shirota
    l += dolgota
    spn += scale
    map_request = f"http://static-maps.yandex.ru/1.x/?ll={w},{l}&spn={spn},{spn}&l=sat"
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
    screen = pygame.display.set_mode((600, 450))
    # Рисуем картинку, загружаемую из только что созданного файла.
    screen.blit(pygame.image.load(map_file), (0, 0))
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

            elif event.key == 1073741921:
                move_1 = "Closely"

            elif event.key == 1073741915:
                move_1 = "Far"

            else:
                move_1 = 'Stop'

        if move_1 != 'Stop':
            if move_1 == "Right":
                moving(3, 0, 0)

            elif move_1 == "Left":
                moving(-3, 0, 0)

            elif move_1 == "Up":
                moving(0, -3, 0)

            elif move_1 == "Down":
                moving(0, 3, 0)

            elif move_1 == "Closely":
                moving(0, 0, -0.0001)

            elif move_1 == "Far":
                moving(0, 0, 0.0001)

pygame.quit()
os.remove(map_file)
