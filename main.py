import pygame as pg
import pygame.event
from pygame.locals import *


class Snake:
    def __init__(self, screen):
        self.screen = screen
        self.block = pg.image.load("resources\\block.jpg").convert()
        self.x = 100
        self.y = 100

    def draw(self):
        self.screen.fill((212, 198, 158))
        self.screen.blit(self.block, (self.x, self.y))
        pg.display.update()

    def move_left(self):
        self.x -= 10
        self.draw()

    def move_right(self):
        self.x += 10
        self.draw()

    def move_up(self):
        self.y -= 10
        self.draw()

    def move_down(self):
        self.y += 10
        self.draw()


class Game:
    def __init__(self):
        pg.init()
        self.surface = pg.display.set_mode((1000, 500))
        self.surface.fill((212, 198, 158))
        self.snake = Snake(self.surface)
        self.snake.draw()

    def run(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        running = False
                    if event.key == K_LEFT:
                        self.snake.move_left()
                    if event.key == K_RIGHT:
                        self.snake.move_right()
                    if event.key == K_UP:
                        self.snake.move_up()
                    if event.key == K_DOWN:
                        self.snake.move_down()
                elif event.type == QUIT:
                    running = False


if __name__ == '__main__':
    game = Game()
    game.run()
