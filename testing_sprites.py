import pygame
import random

# Initialize Pygame
pygame.init()

# Constants
SCREEN_WIDTH = 900
SCREEN_HEIGHT = 900  # Increased height for timer display
CELL_SIZE = 60
MAZE_WIDTH = 15
MAZE_HEIGHT = 15 # Adjusted height for timer display
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
GRAY = (192, 192, 192)
BLUE = (0, 0, 255)

# Create Maze
def create_maze():
    maze = [[0] * MAZE_WIDTH for _ in range(MAZE_HEIGHT)]
    # Randomly add obstacles
    for _ in range(200):
        x = random.randint(0, MAZE_WIDTH - 1)
        y = random.randint(0, MAZE_HEIGHT - 1) 
        maze[y][x] = 1
    # Set endpoint
    maze[MAZE_HEIGHT - 1][MAZE_WIDTH - 1] = 2
    return maze

# Draw Maze
def draw_maze(screen, maze):
    for y in range(MAZE_HEIGHT):
        for x in range(MAZE_WIDTH):
            if maze[y][x] == 1:
                pygame.draw.rect(screen, BLACK, (x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE))
            elif maze[y][x] == 2:
                pygame.draw.rect(screen, RED, (x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE))

# Player class
class Player:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def move(self, dx, dy, maze):
        new_x = self.x + dx
        new_y = self.y + dy
        if 0 <= new_x < MAZE_WIDTH and 0 <= new_y < MAZE_HEIGHT and maze[new_y][new_x] != 1:
            self.x = new_x
            self.y = new_y

    def draw(self, screen, player_num):
        shift = 10
        if(player_num == 1):
            pygame.draw.rect(screen, GREEN, ((self.x * CELL_SIZE)+shift, (self.y * CELL_SIZE)+shift, CELL_SIZE - 20, CELL_SIZE - 20))
        else:
            pygame.draw.rect(screen, BLUE, ((self.x * CELL_SIZE)+shift, (self.y * CELL_SIZE)+shift, CELL_SIZE - 20, CELL_SIZE - 20))

# Main function
def main():
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    font = pygame.font.SysFont(None, 36)
    pygame.display.set_caption("Maze Game")
    clock = pygame.time.Clock()

    maze = create_maze()
    player1 = Player(0, 0)
    player2 = Player(1, 0)

    running = True
    won = False
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    player1.move(0, -1, maze)
                elif event.key == pygame.K_DOWN:
                    player1.move(0, 1, maze)
                elif event.key == pygame.K_LEFT:
                    player1.move(-1, 0, maze)
                elif event.key == pygame.K_RIGHT:
                    player1.move(1, 0, maze)

        screen.fill(WHITE)
        draw_maze(screen, maze)

        player1.draw(screen, 1)
        player2.draw(screen, 2)

        if maze[player1.y][player1.x] == 2:
            won = True
            running = False

        pygame.display.flip()
        clock.tick(30)

    screen.fill(WHITE)
    if won:
        time_text = font.render('You won!', True, BLACK)
    else:
        time_text = font.render('Time is up!', True, BLACK)
    screen.blit(time_text, (SCREEN_WIDTH // 2 - time_text.get_width() // 2, SCREEN_HEIGHT // 2 - time_text.get_height() // 2))
    pygame.display.flip()
    pygame.time.wait(3000)

    pygame.quit()

if __name__ == "__main__":
    main()