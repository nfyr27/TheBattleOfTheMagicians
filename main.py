from random import random

import pygame as pg
import pygame_menu

from settings import *
from tools import load_image
from magicball import MagicBall
from enemy import Enemy
from player import Player
from menu import Menu

pg.init()

font = pg.font.Font(None, 40)


def text_render(text):
    return font.render(str(text), True, "black")


class Game:
    def __init__(self):

        # Создание окна
        self.screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pg.display.set_caption("Битва магов")

        self.background = load_image("images/background.png", SCREEN_WIDTH, SCREEN_HEIGHT)
        self.foreground = load_image("images/foreground.png", SCREEN_WIDTH, SCREEN_HEIGHT)

        self.clock = pg.time.Clock()

        self.is_running = True
        # self.run()
        self.win = None

    def run(self, mode, wizards):
        self.mode = mode

        if self.mode == "one player":
            self.player = Player()
            self.enemy = Enemy(wizards[0])
        elif self.mode == "two players":
            self.player = Player(wizards[0])
            self.enemy = Player(wizards[1], first_player=False)

        while self.is_running:
            self.event()
            self.update()
            self.draw()
            self.clock.tick(FPS)

    def event(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.is_running = False

    def event(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.is_running = False

            # if GESTURE_MODE:
            #     if event.type == self.GET_GESTURE:
            #         self.gesture = self.g.get_gesture()

            if event.type == pg.KEYDOWN and self.win is not None:
                self.is_running = False

    def update(self):
        if self.win is None:
            self.player.update()
            if self.mode == "one player":
                self.enemy.update(self.player)
            else:
                self.enemy.update()

            self.player.magicball.update()
            self.enemy.magicball.update()

            if self.enemy.image not in self.enemy.down:
                hits = pg.sprite.spritecollide(self.enemy, self.player.magicball, True,
                                               collided=pg.sprite.collide_rect_ratio(0.3))

                for hit in hits:
                    self.enemy.hp -= hit.power
            if self.player.image not in self.player.down:
                hits = pg.sprite.spritecollide(self.player, self.enemy.magicball, True,
                                               collided=pg.sprite.collide_rect_ratio(0.3))

                for hit in hits:
                    self.player.hp -= hit.power

            if self.player.hp <= 0:
                self.win = self.enemy
            elif self.enemy.hp <= 0:
                self.win = self.player

    def draw(self):
        # Отрисовка интерфейса
        self.screen.blit(self.background, (0, 0))
        self.screen.blit(self.player.image, self.player.rect)
        self.screen.blit(self.enemy.image, self.enemy.rect)

        if self.player.charge_mode:
            self.screen.blit(self.player.charge_indicator, (self.player.rect.x + 120, self.player.rect.top))
        elif self.enemy.charge_mode:
            self.screen.blit(self.enemy.charge_indicator, (self.enemy.rect.x + 120, self.enemy.rect.top))

        self.player.magicball.draw(self.screen)
        self.enemy.magicball.draw(self.screen)
        self.screen.blit(self.foreground, (0, 0))

        pg.draw.rect(self.screen, pg.Color(0, 0, 0),
                     (10 - HP_BAR_STROKE // 2, 10, 200 + HP_BAR_STROKE, 20 + HP_BAR_STROKE))
        pg.draw.rect(self.screen, pg.Color(0, 255, 0), (10, 10, self.player.hp, 20))

        pg.draw.rect(self.screen, pg.Color(0, 0, 0),
                     (SCREEN_WIDTH - 210 - HP_BAR_STROKE // 2, 10, 200 + HP_BAR_STROKE, 20 + HP_BAR_STROKE))
        pg.draw.rect(self.screen, pg.Color(0, 255, 0), (SCREEN_WIDTH - 210, 10, self.enemy.hp, 20))

        if self.win == self.player:
            text = text_render("ПОБЕДА")
            text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
            self.screen.blit(text, text_rect)
            text2 = text_render("Маг в левом углу")
            text_rect2 = text2.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 100))
            self.screen.blit(text2, text_rect2)

        elif self.win == self.enemy:
            text = text_render("ПОБЕДА")
            text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
            self.screen.blit(text, text_rect)
            text2 = text_render("Маг в правом углу")
            text_rect2 = text2.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 100))
            self.screen.blit(text2, text_rect2)

        pg.display.flip()


if __name__ == "__main__":
    Menu(Game).run()
