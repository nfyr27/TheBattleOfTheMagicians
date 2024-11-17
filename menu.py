import random

import pygame_menu
import pygame as pg

# from main import Game

pg.init()


class Menu:
    def __init__(self, game):
        self.surface = pg.display.set_mode((900, 550))
        font = pygame_menu.font.FONT_MUNRO
        mytheme = pygame_menu.themes.THEME_SOLARIZED.copy()
        # mytheme.title_background_color = (255, 0, 0)
        # mytheme.widget_font = font
        self.game = game
        self.menu = pygame_menu.Menu(
            height=550,
            width=900,
            theme=mytheme,
            title="Menu"
        )

        self.menu.add.label(title="Режим на одного")
        self.menu.add.selector("Противник: ",
                               [("Маг огня", 1),
                                ("Маг молний", 2),
                                ("Маг земли", 3),
                                ("Случайный", 4)],
                               onchange=self.set_difficulty)
        self.menu.add.button("Играть", self.start_one_player_game)
        self.menu.add.label(title="Режим на двоих")
        self.menu.add.selector("Левый игрок: ",
                               [("Маг огня", 1),
                                ("Маг молний", 2),
                                ("Маг земли", 3),
                                ("Случайный", 4)],
                               onchange=self.set_left_player)
        self.menu.add.selector("Правый игрок: ",
                               [("Маг огня", 1),
                                ("Маг молний", 2),
                                ("Маг земли", 3),
                                ("Случайный", 4)],
                               onchange=self.set_right_player)
        self.menu.add.button("Играть", self.start_two_player_game)
        self.menu.add.button("Выход", self.quit_game)

        self.enemy = "fire wizard"
        self.enemies = ["fire wizard", "lightning wizard", "earth monk"]
        self.players = ["fire wizard", "lightning wizard", "earth monk"]
        self.left_player = self.players[0]
        self.right_player = self.players[0]

    def set_difficulty(self, selected, value):
        print(value)
        if value in (1, 2, 3):
            self.enemy = self.enemies[value - 1]
        else:
            self.enemy = random.choice(self.enemies)

    def set_left_player(self, selected, value):
        if value == 4:
            self.left_player = random.choice(self.enemies)
        else:
            self.left_player = self.players[value - 1]
    def set_right_player(self, selected, value):
        if value == 4:
            self.right_player = random.choice(self.enemies)
        else:
            self.right_player = self.players[value - 1]

    def start_one_player_game(self):
        self.game().run("one player", (self.enemy,))

    def start_two_player_game(self):
        self.game().run("two players", (self.left_player, self.right_player))

    def quit_game(self):
        ...

    def run(self):
        self.menu.mainloop(self.surface)


if __name__ == "__main__":
    Menu().run()
