import pygame as pg

pg.init()

SCREEN_WIDTH = 900
SCREEN_HEIGHT = 550

CHARACTER_WIDTH = 300
CHARACTER_HEIGHT = 375


FPS = 60

font = pg.font.Font(None, 40)


def load_image(file, width, height):
    image = pg.image.load(file).convert_alpha()
    image = pg.transform.scale(image, (width, height))
    return image


def text_render(text):
    return font.render(str(text), True, "black")


class Player(pg.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self._load_animation()
        self.image = self.idle_animation_right[0]
        self.current_image = 0
        self.current_animation = self.move_right

        self.rect = self.image.get_rect()
        self.rect.center = (100, SCREEN_HEIGHT // 2)

        self.timer = pg.time.get_ticks()
        self.interval = 100
        self.side = "right"
        self.animation_mode = True

    def _load_animation(self):
        self.idle_animation_right = []
        self.move_right = []
        for i in range(1, 5):
            self.move_right.append(load_image(f"images/earth monk/move{i}.png", CHARACTER_WIDTH, CHARACTER_HEIGHT))
        self.move_left = []
        for i in self.move_right:
            self.move_left.append(pg.transform.flip(i, True, False))

        for i in range(1, 4):
            self.idle_animation_right.append(
                load_image(f"images/earth monk/idle{i}.png", CHARACTER_WIDTH, CHARACTER_HEIGHT))

        self.idle_animation_left = []
        for image in self.idle_animation_right:
            self.idle_animation_left.append(pg.transform.flip(image, True, False))


    def update(self):
        self.handle_animation()

    def handle_animation(self):
        if self.animation_mode:
            if pg.time.get_ticks() - self.timer > self.interval:
                self.current_image += 1
                if self.current_image >= len(self.current_animation):
                    self.current_image = 0
                self.image = self.current_animation[self.current_image]
                self.timer = pg.time.get_ticks()

class Game:
    def __init__(self):

        # Создание окна
        self.screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pg.display.set_caption("Битва магов")

        self.background = load_image("images/background.png", SCREEN_WIDTH, SCREEN_HEIGHT)

        self.player = Player()
        self.clock = pg.time.Clock()
        self.run()

    def run(self):
        while True:
            self.event()
            self.update()
            self.draw()
            self.clock.tick(FPS)

    def event(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                quit()

    def update(self):
        self.player.update()

    def draw(self):
        # Отрисовка интерфейса
        self.screen.blit(self.background, (0, 0))
        self.screen.blit(self.player.image, self.player.rect)
        pg.display.flip()


if __name__ == "__main__":
    Game()