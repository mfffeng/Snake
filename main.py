import pygame as pg
import pygame.event
from pygame.locals import *
import time
import random


class CollisionException(Exception):  # A customized exception
    pass


class Apple:
    def __init__(self, screen):
        self.image = pg.image.load("resources\\apple.jpg").convert()
        self.screen = screen
        self.x = 120
        self.y = 120

    def draw(self):
        self.screen.blit(self.image, (self.x, self.y))
        pygame.display.update()

    def move(self):
        self.x = random.randint(0, 24) * 40
        self.y = random.randint(0, 11) * 40


class Snake:
    def __init__(self, screen, length):
        self.screen = screen
        self.block = pg.image.load("resources\\block.jpg").convert()
        self.x = [40] * length
        self.y = [40] * length
        self.direction = 'down'
        self.length = length

    def eat(self):
        self.length += 1
        self.x.append(-1)
        self.y.append(-1)

    def draw(self):
        # self.screen.fill((212, 198, 158))
        for i in range(self.length):
            self.screen.blit(self.block, (self.x[i], self.y[i]))
        pg.display.update()

    def move_left(self):
        self.direction = 'left'

    def move_right(self):
        self.direction = 'right'

    def move_up(self):  # Remember that (0, 0) lies at the top left corner.
        self.direction = 'up'

    def move_down(self):
        self.direction = 'down'

    def crawl(self):
        for i in range(self.length - 1, 0, -1):  # Mind the logic here!
            self.x[i] = self.x[i - 1]
            self.y[i] = self.y[i - 1]
        if self.direction == 'up':
            self.y[0] -= 40
        if self.direction == 'down':
            self.y[0] += 40
        if self.direction == 'left':
            self.x[0] -= 40
        if self.direction == 'right':
            self.x[0] += 40
        self.draw()


def collision(x1, y1, x2, y2):
    if x2 <= x1 < x2 + 40:
        if y2 <= y1 < y2 + 40:
            return True
    return False


def play_sound(sound):      # Another use of f-string.
    sound = pg.mixer.Sound(f"resources\\{sound}.mp3")
    pg.mixer.Sound.play(sound)


class Game:
    def __init__(self):
        pg.init()
        self.surface = pg.display.set_mode((1000, 500))
        pg.mixer.init()     # Initialize sound module.
        pygame.mixer.music.load('resources\\bg_music_1.mp3')     # Background music.
        pygame.mixer.music.play(-1, 0)      # -1 means the music loops indefinitely.
        # self.surface.fill((212, 198, 158))
        self.snake = Snake(self.surface, 1)
        self.snake.draw()
        self.apple = Apple(self.surface)
        self.apple.draw()

    def reset(self):
        self.snake = Snake(self.surface, 1)
        self.apple = Apple(self.surface)

    def run(self):
        running = True
        pause = False
        while running:
            for event in pygame.event.get():
                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        running = False
                    if event.key == K_RETURN:  # This is the return key.
                        pause = False
                        pg.mixer.music.unpause()
                    if not pause:
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
            try:
                if not pause:
                    bg = pg.image.load("resources\\background.jpg")
                    self.surface.blit(bg, (0, 0))
                    self.snake.crawl()
                    self.apple.draw()
                    self.display_score()
                    pg.display.update()
                    if collision(self.snake.x[0], self.snake.y[0], self.apple.x, self.apple.y):
                        play_sound("1_snake_game_resources_ding")
                        self.snake.eat()
                        self.apple.move()
                    # Snake colliding with itself.
                    for i in range(3, self.snake.length):  # Why starting at 3?
                        if collision(self.snake.x[0], self.snake.y[0], self.snake.x[i], self.snake.y[i]):
                            play_sound("1_snake_game_resources_crash")
                            raise CollisionException("Collision with yourself!")
                    if not (0 <= self.snake.x[0] <= 500 and 0 <= self.snake.y[0] <= 500):
                        play_sound("1_snake_game_resources_crash")
                        raise CollisionException("Collision with boundary!")
            except CollisionException:
                self.game_over()
                pause = True
                self.reset()
            time.sleep(0.25)

    def display_score(self):
        font = pygame.font.SysFont('arial', 30)
        score = font.render(f"Score: {self.snake.length - 1}", True, (255, 255, 255))  # Use of f-string here.
        self.surface.blit(score, (800, 100))

    def game_over(self):
        bg = pg.image.load("resources\\background.jpg")
        self.surface.blit(bg, (0, 0))
        font_over = pg.font.SysFont('arial', 30)
        over = font_over.render(f"Score: {self.snake.length - 1}", True, (255, 255, 255))
        self.surface.blit(over, (250, 150))
        line2 = font_over.render("To play again press Enter. To exit press Escape!", True, (255, 255, 255))
        self.surface.blit(line2, (250, 250))
        pygame.display.flip()
        pygame.mixer.music.pause()      # Pause the background music.


if __name__ == '__main__':
    game = Game()
    game.run()
