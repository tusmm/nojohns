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

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
GRAY = (192, 192, 192)
YELLOW = (255, 255, 0)
PURPLE = (128, 0, 128)

PAWN_COLORS = (GREEN, BLUE, YELLOW, PURPLE)

def _create_board(filename: str) -> Board:
    board = Board(BOARD_HEIGHT, BOARD_WIDTH, filename) 
    return board 

def _create_transparencies():
    pass

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
    for index, pawn in enumerate(pawns):
        print(index, pawn)
        pygame.draw.rect(
            screen, PAWN_COLORS[index], 
            ((pawn.x * CELL_SIZE) + shift, (pawn.y * CELL_SIZE) + shift, CELL_SIZE - size_shift, CELL_SIZE - size_shift)
        )

def main():
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    font = pygame.font.SysFont(None, 36)
    pygame.display.set_caption("Miners (nooooo Johns)")
    clock = pygame.time.Clock()

    board = _create_board(None)  # Gives access to access to all cells
    tile_size = 5
    transparency_surfaces = []
    transparencies = []
    for i in range(25):
        transparencies.append(255)
    for row in range(tile_size):
        for col in range(tile_size):
            transparency_surface = pygame.Surface((SCREEN_WIDTH // tile_size,SCREEN_HEIGHT // tile_size), pygame.SRCALPHA)
            transparency_surface.fill((0,0,0,255))  # rgpA, A = 0 is transparent, A = 255 is opaque
            transparency_surface.scroll(row * SCREEN_WIDTH // tile_size, col * SCREEN_HEIGHT // tile_size)
            pygame.display.flip()
            transparency_surfaces.append(transparency_surface)

    pawns = [Pawn(6, 6), Pawn(8, 8)]
    first_player = Player(0, pawns, {Direction.NORTH, Direction.SOUTH})
    second_player = Player(1, pawns, {Direction.WEST, Direction.EAST})

    running = True
    won = False
    exit_open = False
    
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                # PLAYER 1 controls
                # if the player is able to move in that direction, then move
                if event.key == pygame.K_UP:
                    first_player.move(0, -1, Direction.NORTH, board)
                elif event.key == pygame.K_DOWN:
                    first_player.move(0, 1, Direction.SOUTH, board)
                # PLAYER 2 controls
                elif event.key == pygame.K_a:
                    second_player.move(-1, 0, Direction.WEST, board)
                elif event.key == pygame.K_d:
                    second_player.move(1, 0, Direction.EAST, board)
                # SWAPS
                elif event.key == pygame.K_k:
                    # player1 wants to swap pawns
                    first_player.rotate_pawn()
                elif event.key == pygame.K_f:
                    # player2 wants to swap pawns
                    second_player.rotate_pawn()
        
        if board.cells[Board.cartesian_to_id(pawns[0].x, pawns[0].y)].objective == Objective.PRESSURE_PLATE and \
              board.cells[Board.cartesian_to_id(pawns[1].x, pawns[1].y)].objective == Objective.PRESSURE_PLATE:
                exit_open = True
                print("Exit open")
            
        screen.fill(WHITE)
        _draw_board(screen, board)
        _draw_pawns(screen, pawns)

        for i in range(len(transparency_surfaces)):
            row = i // 5
            col = i % 5
            screen.blit(transparency_surfaces[i], (row * SCREEN_WIDTH // tile_size, col * SCREEN_HEIGHT // tile_size))

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

        if any(board.cells[Board.cartesian_to_id(pawn.x, pawn.y)].objective == Objective.EXIT for pawn in pawns):
            won = True
            running = False

        pygame.display.flip()
        clock.tick(30)

    if won and exit_open:
        time_text = font.render('You won!', True, BLACK)
    else:
        time_text = font.render('Time is up!', True, BLACK)
    screen.blit(time_text, (SCREEN_WIDTH // 2 - time_text.get_width() // 2, SCREEN_HEIGHT // 2 - time_text.get_height() // 2))
    pygame.display.flip()
    pygame.time.wait(100)

    pygame.quit()

if __name__ == "__main__":
    main()
     