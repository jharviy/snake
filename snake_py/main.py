import pygame
import random

# COLOR CONSTANTS
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
DARK_GREEN = (0, 125, 0)
BLUE = (0, 0, 255)
OFF_WHITE = (125, 125, 125)


class Game:
    def __init__(self, dim):
        pygame.init()
        pygame.display.set_caption("jharvi's Snekgame")

        self.x, self.y = dim[0], dim[1]
        self.px = 40  # OBJECT SIZE
        self.surface = pygame.display.set_mode(dim)
        self.clock = pygame.time.Clock()

        self.snake = self.Snake(self)  # Create a snake object
        self.food = self.Food(self)  # Create a food object
        self.score = 0
        self.lose = False

    def new_game(self):
        # Create a new game
        self.snake = self.Snake(self)  # Create a snake object
        self.food = self.Food(self)  # Create a food object
        self.score = 0
        self.lose = False

    def game_over(self):
        # Show "Game Over" on screen
        font = pygame.font.Font(None, 144)
        text_surface = font.render("Game Over", True, RED)
        text_rect = text_surface.get_rect()
        text_rect.center = (self.x / 2, self.y / 2)
        self.surface.blit(text_surface, text_rect)

        # Show ""Press SPACE for NEW GAME"" on screen
        font = pygame.font.Font(None, 36)
        text_surface = font.render("Press SPACE for NEW GAME", True, RED)
        text_rect = text_surface.get_rect()
        text_rect.center = (self.x / 2, (144 / 2) + self.y / 2)
        self.surface.blit(text_surface, text_rect)

    def check(self):
        # Checks if food collides with the snake parts
        if self.food.point.collideobjects([self.snake.head] + self.snake.body):
            self.score += 1
            self.food = self.Food(self)  # Generate new food
            self.snake.grow()  # Extend the snake body

        # Checks if snake head collides to its body parts. Show game over screen if lost
        if self.lose or self.snake.head.collideobjects(self.snake.body):
            self.lose = True
            self.game_over()

    def update(self, key):
        # KEY PRESS updates game events
        if key == "UP":
            self.snake.update([0, 1])
        elif key == "DOWN":
            self.snake.update([0, -1])
        elif key == "LEFT":
            self.snake.update([-1, 0])
        elif key == "RIGHT":
            self.snake.update([1, 0])
        elif key == "SPACE" and self.lose:
            self.new_game()

    def draw(self):
        # First to draw on back, last to draw on front. Front always overlap the back
        self.surface.fill(BLACK)  # Draw BACKGROUND First
        self.snake.update() if not self.lose else None  # Only update if not lose(GameOver)
        self.check()  # Check food and snake collision for score and game lose condition
        self.snake.draw()
        self.food.draw()

        # Display score
        font = pygame.font.Font(None, 36)
        text_surface = font.render("Score: " + str(self.score), True, WHITE)
        text_rect = text_surface.get_rect()
        self.surface.blit(text_surface, text_rect)

    class Snake:
        def __init__(self, game):
            # Initial Snake head and body coordinates (rect object)
            self.game = game
            self.head = pygame.Rect(game.x / 2, game.y / 2, game.px, game.px)
            self.body = [self.head.move(-i * game.px, 0) for i in range(1, 4)]

            self.move = [1, 0]  # Initial moving direction [x,y] --> [1,0] means moving right

        def grow(self):
            # Add new body for snake
            self.body.append(self.body[-1])

        def update(self, move=None):
            # True if event.move occurred and move is valid
            if move is not None and (self.move[0] * move[0] != -1) and (self.move[1] * move[1] != -1):
                self.move = move

            # Update snake head based on move direction and then follow body to the head and next
            for i in range(len(self.body) - 1, 0, -1):
                self.body[i] = self.body[i - 1]
            self.body[0] = self.head
            self.head = self.head.move(self.move[0] * self.game.px, -self.move[1] * self.game.px)

            # If snake head crossed the screen dimension, will be moved and appear to the other side
            if self.head[0] < 0:
                self.head[0] = self.game.x
            elif self.head[0] >= self.game.x:
                self.head[0] = 0
            if self.head[1] < 0:
                self.head[1] = self.game.y
            elif self.head[1] >= self.game.y:
                self.head[1] = 0

        def draw(self):
            # DRAW all snake parts (head and body)
            pygame.time.delay(120)
            pygame.draw.rect(self.game.surface, DARK_GREEN, self.head)
            for i in self.body:
                pygame.draw.rect(self.game.surface, DARK_GREEN, i, 2)

    class Food:
        def __init__(self, game):
            self.game = game
            # Random coordinates within the game dimension
            # values only a multiple of object size (to ensure centered object)
            self.x = random.choice([x for x in range(0, game.x, game.px)]) + game.px / 2
            self.y = random.choice([y for y in range(0, game.y, game.px)]) + game.px / 2
            self.point = pygame.draw.circle(self.game.surface, BLUE, (self.x, self.y), self.game.px / 3)

        def draw(self):
            self.point = pygame.draw.circle(self.game.surface, BLUE, (self.x, self.y), self.game.px / 3)


if __name__ == '__main__':

    DIMENSION = (1280, 720)
    snakegame = Game(DIMENSION)
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                if event.key == pygame.K_SPACE:
                    snakegame.update("SPACE")
                if (event.key == pygame.K_UP) or (event.key == pygame.K_w):
                    snakegame.update("UP")
                if (event.key == pygame.K_DOWN) or (event.key == pygame.K_s):
                    snakegame.update("DOWN")
                if (event.key == pygame.K_LEFT) or (event.key == pygame.K_a):
                    snakegame.update("LEFT")
                if (event.key == pygame.K_RIGHT) or (event.key == pygame.K_d):
                    snakegame.update("RIGHT")

        snakegame.draw()
        snakegame.clock.tick(60)
        pygame.display.flip()

    pygame.quit()
