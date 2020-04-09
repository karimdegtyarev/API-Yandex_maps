import os
import sys

import pygame
import requests

response = None
map_request = "http://static-maps.yandex.ru/1.x/?ll=-2.146939,51.263611&spn=0.001,0.001&l=sat"
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
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN and event.key == pygame.K_LEFT:
            move_1 = "Left"

        elif event.type == pygame.KEYDOWN and event.key == pygame.K_RIGHT:
            move_1 = "Right"

        elif event.type == pygame.KEYDOWN and event.key == pygame.K_LEFT:
            move_1 = "Up"

        elif event.type == pygame.KEYDOWN and event.key == pygame.K_RIGHT:
            move_1 = "Down"
        else:
            move_1 = 'Stop'
pygame.quit()
os.remove(map_file)
