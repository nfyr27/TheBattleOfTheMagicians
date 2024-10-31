import pygame as pg
from settings import *
from tools import load_image

class MagicBall(pg.sprite.Sprite):
    def __init__(self, coord, side, power, folder):
        super().__init__()
        self.side = side
        self.power = power
        self.image = load_image(f"images/{folder}/magicball.png", 200, 150)
        if side == "right":
            self.image = pg.transform.flip(self.image, True, False)
        self.rect = self.image.get_rect()
        self.rect.center = coord[0], coord[1] + 120

    def update(self):
        if self.side == "left":
            self.rect.x -= 4
        elif self.side == "right":
            self.rect.x += 4
        if self.rect.left > SCREEN_WIDTH or self.rect.right < 0:
            self.kill()