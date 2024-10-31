import pygame as pg
from settings import *
from tools import load_image
from magicball import MagicBall
from enemy import Enemy

pg.init()

font = pg.font.Font(None, 40)


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
        self.interval = 150
        self.side = "right"
        self.animation_mode = True

        self.charge_power = 0
        self.charge_indicator = pg.Surface((self.charge_power, 10))
        self.charge_indicator.fill("red")

        self.charge_mode = False

        self.attack_mode = False
        self.attack_interval = 500

        self.fireball = pg.sprite.Group()

    def _load_animation(self):
        self.idle_animation_right = [load_image(f"images/earth monk/idle{i}.png", CHARACTER_WIDTH, CHARACTER_HEIGHT)
                                     for i in range(1, 4)]
        self.idle_animation_left = [pg.transform.flip(image, True, False)
                                    for image in self.idle_animation_right]
        self.move_right = [load_image(f"images/earth monk/move{i}.png", CHARACTER_WIDTH, CHARACTER_HEIGHT)
                           for i in range(1, 5)]
        self.move_left = [pg.transform.flip(i, True, False)
                          for i in self.move_right]

        self.charge = [load_image("images/earth monk/charge.png", CHARACTER_WIDTH, CHARACTER_HEIGHT)]
        self.charge.append(pg.transform.flip(self.charge[0], True, False))

        self.attack = [load_image("images/earth monk/attack.png", CHARACTER_WIDTH, CHARACTER_HEIGHT)]
        self.attack.append(pg.transform.flip(self.attack[0], True, False))

        self.down = [load_image("images/earth monk/down.png", CHARACTER_WIDTH, CHARACTER_HEIGHT)]
        self.down.append(pg.transform.flip(self.down[0], True, False))

    def update(self):
        keys = pg.key.get_pressed()
        direction = 0
        if keys[pg.K_a]:
            direction = -1
            self.side = "left"
        if keys[pg.K_d]:
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
            fireball_position = self.rect.topright if self . side == "right" else self.rect.topleft
            self.fireball.add(MagicBall(fireball_position, self.side, self.charge_power, "earth monk"))
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
        elif keys[pg.K_SPACE]:
            self.animation_mode = False
            self.charge_mode = True
            self.image = self.charge[self.side != "right"]
        elif keys[pg.K_s]:
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

    def handle_attack(self):
        if self.attack_mode:
            if pg.time.get_ticks() - self.timer > self.attack_interval:
                self.attack_mode = False
                self.timer = pg.time.get_ticks()


class Game:
    def __init__(self):

        # Создание окна
        self.screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pg.display.set_caption("Битва магов")

        self.background = load_image("images/background.png", SCREEN_WIDTH, SCREEN_HEIGHT)
        self.foreground = load_image("images/foreground.png", SCREEN_WIDTH, SCREEN_HEIGHT)

        self.player = Player()
        self.enemy = Enemy("fire wizard")
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
        self.enemy.update(self.player)
        self.player.fireball.update()

        self.enemy.fireball.update()

    def draw(self):
        # Отрисовка интерфейса
        self.screen.blit(self.background, (0, 0))
        self.screen.blit(self.player.image, self.player.rect)
        self.screen.blit(self.enemy.image, self.enemy.rect)

        if self.player.charge_mode:
            self.screen.blit(self.player.charge_indicator, (self.player.rect.x + 120, self.player.rect.top))

        self.player.fireball.draw(self.screen)
        self.enemy.fireball.draw(self.screen)
        self.screen.blit(self.foreground, (0, 0))
        pg.display.flip()


if __name__ == "__main__":
    Game()
