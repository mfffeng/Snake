import pygame as pg
import pygame.event
from pygame.locals import *
import time


class Snake:
    def __init__(self, screen):
        self.screen = screen
        self.block = pg.image.load("resources\\block.jpg").convert()
        self.x = 100
        self.y = 100
        self.direction = 'down'

    def draw(self):
        self.screen.fill((212, 198, 158))
        self.screen.blit(self.block, (self.x, self.y))
        pg.display.update()

    def move_left(self):
        self.direction = 'left'

    def move_right(self):
        self.direction = 'right'

    def move_up(self):      # Remember that (0, 0) lies at the top left corner.
        self.direction = 'up'

    def move_down(self):
        self.direction = 'down'

    def crawl(self):
        if self.direction == 'up':
            self.y -= 10
        if self.direction == 'down':
            self.y += 10
        if self.direction == 'left':
            self.x -= 10
        if self.direction == 'right':
            self.x += 10
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
            self.snake.crawl()
            time.sleep(0.2)


if __name__ == '__main__':
    game = Game()
    game.run()
