import pygame

from structures.board import Board, BOARD_HEIGHT, BOARD_WIDTH
from structures.cell import Cell, Objective
from structures.direction import Direction 
from structures.pawn import Pawn
from structures.player import Player

# Initialize Pygame
pygame.init()

# Constants
SCREEN_WIDTH = 900
SCREEN_HEIGHT = 900  # Increased height for timer display
CELL_SIZE = 60
NUM_TILES = 5

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
GRAY = (192, 192, 192)
YELLOW = (255, 255, 0)
PURPLE = (128, 0, 128)

def _create_board(filename: str) -> Board:
    board = Board(BOARD_HEIGHT, BOARD_WIDTH, filename) 
    return board 

def _create_transparencies():
    transparency_surfaces = []
    transparencies = []
    for _ in range(NUM_TILES * NUM_TILES):
        transparencies.append(255)
    for row in range(NUM_TILES):
        for col in range(NUM_TILES):
            transparency_surface = pygame.Surface((SCREEN_WIDTH // NUM_TILES, SCREEN_HEIGHT // NUM_TILES), pygame.SRCALPHA)
            transparency_surface.fill((0,0,0,255))  # rgpA, A = 0 is transparent, A = 255 is opaque
            transparency_surface.scroll(row * SCREEN_WIDTH // NUM_TILES, col * SCREEN_HEIGHT // NUM_TILES)
            pygame.display.flip()
            transparency_surfaces.append(transparency_surface)
    return transparency_surfaces, transparencies

# Draw board
def _draw_board(screen, board):
    for x in range(BOARD_WIDTH):
        for y in range(BOARD_HEIGHT):
            image = Cell.get_wall_image(board.cells[Board.cartesian_to_id(x, y)].adjacency_matrix)
            screen.blit(image, (x * CELL_SIZE, y *  CELL_SIZE))
            # pygame.draw.rect(screen, GRAY, (x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE), 2)

            match board.cells[Board.cartesian_to_id(x, y)].objective:
                case Objective.EXIT:
                    pygame.draw.rect(screen, RED, (x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE))
                case Objective.PRESSURE_PLATE:
                    pygame.draw.rect(screen, GRAY, (x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE))
                case Objective.OXYGEN_TANK:
                    pygame.draw.rect(screen, BLUE, (x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE))

# Draw pawns
def _draw_pawns(screen, pawns):
    shift = 10
    size_shift = 20
    for pawn in pawns:
        pygame.draw.rect(
            screen, pawn.color, 
            ((pawn.x * CELL_SIZE) + shift, (pawn.y * CELL_SIZE) + shift, CELL_SIZE - size_shift, CELL_SIZE - size_shift)
        )

def main():
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    font = pygame.font.SysFont(None, 36)
    pygame.display.set_caption("Miners (nooooo Johns)")
    clock = pygame.time.Clock()

    board = _create_board(None)  # Gives access to access to all cells
    transparency_surfaces, transparencies = _create_transparencies()

    pawns = [Pawn(6, 6, GREEN), Pawn(8, 8, BLUE)]
    first_player = Player(0, pawns, {Direction.NORTH, Direction.SOUTH})
    second_player = Player(1, pawns, {Direction.WEST, Direction.EAST})

    running = True
    win = False
    exit_open = False
    
    while running:
        # Draw board and other elements
        screen.fill(WHITE)
        _draw_board(screen, board)
        _draw_pawns(screen, pawns)

        for i in range(len(transparency_surfaces)):
            row = i // NUM_TILES
            col = i % NUM_TILES
            screen.blit(transparency_surfaces[i], (row * SCREEN_WIDTH // NUM_TILES, col * SCREEN_HEIGHT // NUM_TILES))

        for pawn in pawns:
            curr_x = pawn.x // 3
            curr_y = pawn.y // 3
            transparencies[curr_x * 5 + curr_y] -= 20
        
        for i in range(len(transparencies)):
            transparencies[i] += 0.6
            if transparencies[i] > 255:
                transparencies[i] = 255
            if transparencies[i] < 0:
                transparencies[i] = 0
            transparency_surfaces[i].fill((0,0,0,transparencies[i]))

        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                # if the player is able to move in that direction, then move
                match event.key: 
                    # PLAYER 1 controls
                    case pygame.K_UP:
                        first_player.move(0, -1, Direction.NORTH, board)
                    case pygame.K_DOWN:
                        first_player.move(0, 1, Direction.SOUTH, board)
                    # PLAYER 2 controls
                    case pygame.K_a:
                        second_player.move(-1, 0, Direction.WEST, board)
                    case pygame.K_d:
                        second_player.move(1, 0, Direction.EAST, board)
                    case pygame.K_k:
                        first_player.rotate_pawn()
                    case pygame.K_f:
                        second_player.rotate_pawn()
        
        # Describe game logic
        if all(board.cells[Board.cartesian_to_id(pawn.x, pawn.y)].objective == Objective.PRESSURE_PLATE for pawn in pawns):
            exit_open = True
            print("Exit open")
            
        for pawn in pawns:
            if board.cells[Board.cartesian_to_id(pawn.x, pawn.y)].objective == Objective.EXIT and exit_open:
                pawns.remove(pawn)

        if not pawns:
            win = True
            running = False

        pygame.display.flip()
        clock.tick(30)

    if win and exit_open:
        time_text = font.render('You won!', True, BLACK)  
    else:
        time_text = font.render('Time is up!', True, BLACK)
        
        screen.blit(time_text, (SCREEN_WIDTH // 2 - time_text.get_width() // 2, SCREEN_HEIGHT // 2 - time_text.get_height() // 2))
        pygame.time.wait(3000)
        pygame.display.flip()
        pygame.quit()
    

if __name__ == "__main__":
    main()
     