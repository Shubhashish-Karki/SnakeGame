import pygame
from pygame.locals import *
import OpenGL
from OpenGL.GL import *
from OpenGL.GLU import *
import random
import time

# Initialize Pygame
pygame.init()

# Define constants
COLUMNS = 40
ROWS = 40
CELL_SIZE = 20
WINDOW_WIDTH = COLUMNS * CELL_SIZE
WINDOW_HEIGHT = ROWS * CELL_SIZE

# Define colors
BLACK = (0.0, 0.0, 0.0)
GREEN = (0.0, 1.0, 0.0)
BLUE = (0.0, 0.0, 1.0)
RED = (1.0, 0.0, 0.0)

# Set up the display
screen = pygame.display.set_mode(
    (WINDOW_WIDTH, WINDOW_HEIGHT), DOUBLEBUF | OPENGL)
pygame.display.set_caption("Snake Game")

# Initialize OpenGL
glClearColor(*BLACK, 1.0)
glMatrixMode(GL_PROJECTION)
glLoadIdentity()
gluOrtho2D(0, COLUMNS, 0, ROWS)
glMatrixMode(GL_MODELVIEW)

# Define snake and food positions
snake_pos = [(COLUMNS // 2, ROWS // 2 + i) for i in range(5)]
food_pos = (random.randint(1, COLUMNS - 2), random.randint(1, ROWS - 2))

# Define direction and game state
direction = (0, -1)  # Start moving up
game_over = False
score = 0
fps = 10


def draw_snake():
    for segment in snake_pos:
        if segment == snake_pos[0]:
            glColor3f(*GREEN)
        else:
            glColor3f(*BLUE)
        glRectf(segment[0], segment[1], segment[0] + 1, segment[1] + 1)


def draw_food():
    glColor3f(*RED)
    glRectf(food_pos[0], food_pos[1], food_pos[0] + 1, food_pos[1] + 1)


def game_loop():
    global direction, game_over, score, fps, food_pos

    # Game loop
    clock = pygame.time.Clock()
    while not game_over:
        # Handle events
        for event in pygame.event.get():
            if event.type == QUIT:
                game_over = True
            elif event.type == KEYDOWN:
                if event.key == K_UP and direction != (0, -1):
                    direction = (0, 1)
                elif event.key == K_DOWN and direction != (0, 1):
                    direction = (0, -1)
                elif event.key == K_LEFT and direction != (1, 0):
                    direction = (-1, 0)
                elif event.key == K_RIGHT and direction != (-1, 0):
                    direction = (1, 0)

        # Move the snake
        new_head = (
            (snake_pos[0][0] + direction[0]) % COLUMNS,
            (snake_pos[0][1] + direction[1]) % ROWS,
        )
        snake_pos.insert(0, new_head)

        # Check for collisions
        if (
            new_head in snake_pos[1:]
            or new_head[0] < 1
            or new_head[0] >= COLUMNS - 1
            or new_head[1] < 1
            or new_head[1] >= ROWS - 1
        ):
            game_over = True

        # Check for food
        if new_head == food_pos:
            score += 1
            if score % 9 == 0:
                fps += 5
            food_pos = (random.randint(1, COLUMNS - 2),
                        random.randint(1, ROWS - 2))
        else:
            snake_pos.pop()

        # Clear the screen
        glClear(GL_COLOR_BUFFER_BIT)

        # Draw the game
        draw_snake()
        draw_food()

        pygame.display.flip()
        clock.tick(fps)

    # Game over message
    font = pygame.font.Font(None, 36)
    game_over_text = font.render(f"Game Over! Score: {score}", True, RED)
    game_over_rect = game_over_text.get_rect(
        center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2))
    screen.blit(game_over_text, game_over_rect)
    pygame.display.update()

    # Wait for user input to quit
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                return


# Start the game
game_loop()
