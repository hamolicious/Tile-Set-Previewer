import json
from hashlib import md5
import pygame
import os
from time import sleep

with open('settings.json') as file:
    settings, tiles = json.load(file)

class Tile():
    def __init__(self, path_to_image, pos):
        self.pos = pos

        self.path_to_image = path_to_image
        self.image = pygame.image.load(self.path_to_image)

        self.image_hash = md5()

    def check_update(self):
        with open(self.path_to_image, 'rb') as file:
            content = file.read()
            temp_hash = md5(content).hexdigest()

        try:
            if self.image_hash != temp_hash:
                self.image = pygame.image.load(self.path_to_image)
                self.image_hash = temp_hash
        except pygame.error:
            self.check_update()

    def draw(self, screen):
        self.check_update()

        screen.blit(pygame.transform.scale(self.image, (settings['tile-size'][0] * settings['visual-increase'], settings['tile-size'][1] * settings['visual-increase'])), self.pos)


