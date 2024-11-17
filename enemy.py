import random

import pygame as pg
from settings import  *
from tools import load_image
from magicball import MagicBall

class Enemy(pg.sprite.Sprite):
    def __init__(self, folder):
        super().__init__()
        self.folder = folder
        self._load_animation()
        self.image = self.idle_animation_left[0]
        self.current_image = 0
        self.current_animation = self.idle_animation_left

        self.hp = 200

        self.rect = self.image.get_rect()
        self.rect.center = (SCREEN_WIDTH - 100, SCREEN_HEIGHT // 2)

        self.timer = pg.time.get_ticks()
        self.interval = 150
        self.side = "left"
        self.animation_mode = True

        self.charge_power = 0
        self.charge_indicator = pg.Surface((self.charge_power, 10))
        self.charge_indicator.fill("red")

        self.charge_mode = False

        self.attack_mode = False
        self.attack_interval = 500

        self.magicball = pg.sprite.Group()

        self.move_interval = 800
        self.move_duration = 0
        self.direction = 0
        self.move_timer = pg.time.get_ticks()

    def _load_animation(self):
        self.idle_animation_right = [load_image(f"images/{self.folder}/idle{i}.png", CHARACTER_WIDTH, CHARACTER_HEIGHT)
                                     for i in range(1, 4)]
        self.idle_animation_left = [pg.transform.flip(image, True, False)
                                    for image in self.idle_animation_right]
        self.move_animation_right = [load_image(f"images/{self.folder}/move{i}.png", CHARACTER_WIDTH, CHARACTER_HEIGHT)
                                     for i in range(1, 5)]
        self.move_animation_left = [pg.transform.flip(i, True, False)
                                    for i in self.move_animation_right]

        self.charge = [load_image(f"images/{self.folder}/charge.png", CHARACTER_WIDTH, CHARACTER_HEIGHT)]
        self.charge.append(pg.transform.flip(self.charge[0], True, False))

        self.attack = [load_image(f"images/{self.folder}/attack.png", CHARACTER_WIDTH, CHARACTER_HEIGHT)]
        self.attack.append(pg.transform.flip(self.attack[0], True, False))

        self.down = [load_image(f"images/{self.folder}/down.png", CHARACTER_WIDTH, CHARACTER_HEIGHT)]
        self.down.append(pg.transform.flip(self.down[0], True, False))

    def update(self, player):
        self.handle_attack(player)
        self.handle_movement()
        self.handle_animation()

    def handle_attack(self, player):

        if not self.attack_mode:
            attack_probability = 1

            if player.charge_mode:
                attack_probability += 1

            if random.randint(1, 100) <= attack_probability:
                self.attack_mode = True
                self.charge_power = random.randint(1, 100)

                if player.rect.centerx < self.rect.centerx:
                    self.side = "left"
                else:
                    self.side = "right"

                self.animation_mode = False
                self.image = self.attack[self.side != "right"]

        if self.attack_mode:
            if pg.time.get_ticks() - self.timer > self.attack_interval:
                self.attack_mode = False
                # self.animation_mode = True
                self.timer = pg.time.get_ticks()
    def handle_animation(self):
        if self.animation_mode and not self.attack_mode:
            if pg.time.get_ticks() - self.timer > self.interval:
                self.current_image += 1
                if self.current_image >= len(self.current_animation):
                    self.current_image = 0
                self.image = self.current_animation[self.current_image]
                self.timer = pg.time.get_ticks()

        if self.attack_mode and self.charge_power > 0:
            fireball_position = self.rect.topright if self . side == "right" else self.rect.topleft
            self.magicball.add(MagicBall(fireball_position, self.side, self.charge_power, self.folder))
            self.charge_power = 0
            self.charge_mode = False
            self.image = self.attack[self.side != "right"]
            self.timer = pg.time.get_ticks()

    def handle_movement(self):
        if self.attack_mode:
            return

        now = pg.time.get_ticks()  # взять количество тиков

        if now - self.move_timer < self.move_duration:
            self.animation_mode = True # включить режим анимации
            self.rect.x += self.direction # подвинуть по X координате на direction
            self.current_animation = self.move_animation_left if self.direction == -1 else self.move_animation_right
        else:
            if random.randint(1, 100) == 1 and now - self.move_timer > self.move_interval:
                self.move_timer = pg.time.get_ticks()
                self.move_duration = random.randint(400, 1500) # случайное число от 400 до 1500
                self.direction = random.choice([-1, 1])
            else:
                self.animation_mode = True # включить режим анимации
                self.current_animation = self.idle_animation_left if self.side == "left" else self.idle_animation_right

        if self.rect.right >= SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH
        elif self.rect.left <= 0:
            self.rect.left = 0