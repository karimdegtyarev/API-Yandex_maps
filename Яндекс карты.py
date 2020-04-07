import os
import sys

import pygame
import requests

response = None
spn = int(input("Маштаб:"))
w = int(input("Широта:"))
l = int(input("Долгота:"))
print('Спасибо мы уже отправили ответ')
map_request = f"http://static-maps.yandex.ru/1.x/?ll={w},{l}&spn={spn},{spn}&l=map"
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


def moving(step):
    map_request = f"http://static-maps.yandex.ru/1.x/?ll={w + step},{l + step}&spn={spn},{spn}&l=map"
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


move_1 = ''
while pygame.event.wait().type != pygame.QUIT:
    for event in pygame.event.get():
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
    if move_1 != 'Stop':
        print('ok2')
        if move_1 == "Right":
            moving(3)
        elif move_1 == "Left":
            moving(-3)
        elif move_1 == "Up":
            moving(-3)
        elif move_1 == "Down":
            moving(3)
pygame.quit()

# Удаляем за собой файл с изображением.
os.remove(map_file)
