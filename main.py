import pygame
from time import time
import os
import json
import tile_manager
clear = lambda : os.system('cls')
clear()

with open('settings.json') as file:
    settings, _ = json.load(file)

# region pygame init
tile_width = (settings['tile-size'][0] * settings['visual-increase'])
tile_height = (settings['tile-size'][1] * settings['visual-increase'])

pygame.init()
size = (tile_width * settings['tiles-horizontaly'], tile_height * settings['tiles-verticaly'])
screen = pygame.display.set_mode(size)
screen.fill([255, 255, 255])
pygame.display.set_icon(screen)
clock, fps = pygame.time.Clock(), 0

delta_time = 0
frame_start_time = 0
# endregion

state = 'draw'
def preview(tiles):
    for tile in tiles:
        tile.draw(screen)

def load_tile_image(index):
    path = os.path.join(settings['tiles-path'], os.listdir(settings['tiles-path'])[index])

    return pygame.transform.scale(pygame.image.load(path), (settings['tile-size'][0] * settings['visual-increase'], settings['tile-size'][1] * settings['visual-increase']))

tiles = []
selected_tile_index = 0
selected_tile_image = load_tile_image(selected_tile_index)
keyblock = False
def create_envir(key, mouse_pos, mouse_pressed):
    global state, keyblock, selected_tile_index, selected_tile_image, tiles

    grid = []
    for y in range(settings['tiles-verticaly']):
        for x in range(settings['tiles-horizontaly']):
            rect = pygame.Rect(x * tile_width, y * tile_height, tile_width, tile_height)
            grid.append(rect)
            pygame.draw.rect(screen, [51, 51, 51], rect, 1)

    preview(tiles)
    screen.blit(selected_tile_image, (mouse_pos[0] - tile_width/2, mouse_pos[1] - tile_height/2))

    if key[pygame.K_LEFT] and not keyblock:
        selected_tile_index -= 1
        keyblock = True
    if key[pygame.K_RIGHT] and not keyblock:
        selected_tile_index += 1
        keyblock = True
    
    if not (key[pygame.K_LEFT] or key[pygame.K_RIGHT] or mouse_pressed[0]):
        keyblock = False

    if selected_tile_index < 0:
        selected_tile_index = 0
    if selected_tile_index > (length := len(os.listdir(settings['tiles-path']))-1):
        selected_tile_index = length

    selected_tile_image = load_tile_image(selected_tile_index)

    if mouse_pressed[0] == 1 and not keyblock:
        keyblock = True

        rect = pygame.Rect(mouse_pos[0], mouse_pos[1], settings['tile-size'][0] * settings['visual-increase'], settings['tile-size'][1] * settings['visual-increase'])
        if (index := rect.collidelist(grid)) != -1:
            collided_with = grid[index]
            rect.clamp_ip(collided_with)

            path_to_image = os.path.join(settings['tiles-path'], os.listdir(settings['tiles-path'])[selected_tile_index])
            tile = tile_manager.Tile(path_to_image, (rect.x, rect.y))
            tiles.append(tile)
    
    if key[pygame.K_RETURN]:
        state = 'preview'
        return

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()
    frame_start_time = time()
    screen.fill([100, 100, 100])

    key = pygame.key.get_pressed()
    mouse_pos = pygame.mouse.get_pos()
    mouse_pressed = pygame.mouse.get_pressed()

    if state == 'draw':
        create_envir(key, mouse_pos, mouse_pressed)
    else:
        preview(tiles)

    pygame.display.update()
    clock.tick(fps)
    delta_time = time() - frame_start_time
    pygame.display.set_caption(f'Framerate: {int(clock.get_fps())}')
