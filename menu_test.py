import pygame_menu
import pygame as pg

pg.init()


class Menu:
    def __init__(self):
        self.surface = pg.display.set_mode((900, 550))
        self.menu = pygame_menu.Menu(
            height=550,
            width=900,
            theme=pygame_menu.themes.THEME_SOLARIZED,
            title="Пример меню"
        )

        self.menu.add.text_input("Имя: ", default="Player", onchange=self.set_name)
        self.menu.add.selector("Сложность: ",
                               [("Лёгкая", 1),
                                ("Нормальная", 2),
                                ("Сложная", 3)],
                               onchange=self.set_difficulty)
        self.menu.add.label(title="Это ярлык")
        self.menu.add.button("Играть", self.start_game)
        self.menu.add.button("Выйти", self.quit_game)

    def set_name(self, value):
        print(f"Ваше имя {value}")

    def set_difficulty(self, selected, value):
        print(selected, value)

    def start_game(self):
        ...

    def quit_game(self):
        ...

    def run(self):
        self.menu.mainloop(self.surface)


if __name__ == "__main__":
    Menu().run()
