import random

import pygame as pg
from settings import  *
from tools import load_image
from magicball import MagicBall


class Player(pg.sprite.Sprite):
    def __init__(self, folder="fire wizard", first_player=True):
        super().__init__()
        self.folder = folder
        self._load_animation()



        if first_player:
            self.coord = (100, SCREEN_HEIGHT // 2)
            self.current_animation = self.move_right
            self.side = "right"
            self.key_right = pg.K_d
            self.key_left = pg.K_a
            self.key_down = pg.K_s
            self.key_charge = pg.K_SPACE
        else:
            self.coord = (SCREEN_WIDTH - 100, SCREEN_HEIGHT // 2)
            self.current_animation = self.move_left
            self.side = "left"
            self.key_right = pg.K_RIGHT
            self.key_left = pg.K_LEFT
            self.key_down = pg.K_DOWN
            self.key_charge = pg.K_RCTRL

        self.hp = 200
        self.image = self.current_animation[0]
        self.current_image = 0
        self.rect = self.image.get_rect()
        self.rect.center = self.coord

        self.timer = pg.time.get_ticks()
        self.interval = 150
        # self.side = "right"
        self.animation_mode = True

        self.charge_power = 0
        self.charge_indicator = pg.Surface((self.charge_power, 10))
        self.charge_indicator.fill("red")

        self.charge_mode = False

        self.attack_mode = False
        self.attack_interval = 500

        self.magicball = pg.sprite.Group()

    def _load_animation(self):
        self.idle_animation_right = [load_image(f"images/{self.folder}/idle{i}.png", CHARACTER_WIDTH, CHARACTER_HEIGHT)
                                     for i in range(1, 4)]
        self.idle_animation_left = [pg.transform.flip(image, True, False)
                                    for image in self.idle_animation_right]
        self.move_right = [load_image(f"images/{self.folder}/move{i}.png", CHARACTER_WIDTH, CHARACTER_HEIGHT)
                           for i in range(1, 5)]
        self.move_left = [pg.transform.flip(i, True, False)
                          for i in self.move_right]

        self.charge = [load_image(f"images/{self.folder}/charge.png", CHARACTER_WIDTH, CHARACTER_HEIGHT)]
        self.charge.append(pg.transform.flip(self.charge[0], True, False))

        self.attack = [load_image(f"images/{self.folder}/attack.png", CHARACTER_WIDTH, CHARACTER_HEIGHT)]
        self.attack.append(pg.transform.flip(self.attack[0], True, False))

        self.down = [load_image(f"images/{self.folder}/down.png", CHARACTER_WIDTH, CHARACTER_HEIGHT)]
        self.down.append(pg.transform.flip(self.down[0], True, False))

    def update(self):
        keys = pg.key.get_pressed()
        direction = 0
        if keys[self.key_left]:
            direction = -1
            self.side = "left"
        if keys[self.key_right]:
            direction = 1
            self.side = "right"
        self.handle_attack()
        self.handle_animation()
        self.handle_movement(direction, keys)


    def handle_animation(self):
        if not self.charge_mode and self.charge_power > 0:
            self.attack_mode = True

        if self.animation_mode and not self.attack_mode:
            if pg.time.get_ticks() - self.timer > self.interval:
                self.current_image += 1
                if self.current_image >= len(self.current_animation):
                    self.current_image = 0
                self.image = self.current_animation[self.current_image]
                self.timer = pg.time.get_ticks()
        if self.charge_mode:
            self.charge_power += 1
            self.charge_indicator = pg.Surface((self.charge_power, 10))
            self.charge_indicator.fill("red")
            if self.charge_mode == 100:
                self.attack_mode = True

        if self.attack_mode and self.charge_power > 0:
            fireball_position = self.rect.topright if self.side == "right" else self.rect.topleft
            self.magicball.add(MagicBall(fireball_position, self.side, self.charge_power, self.folder))
            self.charge_power = 0
            self.charge_mode = False
            self.image = self.attack[self.side != "right"]
            self.timer = pg.time.get_ticks()

    def handle_movement(self, direction, keys):
        if self.attack_mode:
            return
        if direction != 0:
            self.animation_mode = True
            self.charge_mode = False
            self.rect.x += direction
            if direction == -1:
                self.current_animation = self.move_left
            else:
                self.current_animation = self.move_right
        elif keys[self.key_charge]:
            self.animation_mode = False
            self.charge_mode = True
            self.image = self.charge[self.side != "right"]
        elif keys[self.key_down]:
            self.animation_mode = False
            self.charge_mode = False
            self.image = self.down[self.side != "right"]
        else:
            self.animation_mode = True
            self.charge_mode = False
            if self.side == "left":
                self.current_animation = self.idle_animation_left
            else:
                self.current_animation = self.idle_animation_right

        if self.rect.right >= SCREEN_WIDTH + CHARACTER_WIDTH // 3:
            self.rect.right = SCREEN_WIDTH
        elif self.rect.left <= -CHARACTER_WIDTH // 3:
            self.rect.left = -CHARACTER_WIDTH // 3



    def handle_attack(self):
        if self.attack_mode:
            if pg.time.get_ticks() - self.timer > self.attack_interval:
                self.attack_mode = False
                self.timer = pg.time.get_ticks()