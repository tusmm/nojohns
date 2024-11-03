import pygame

from structures.board import Board, BOARD_HEIGHT, BOARD_WIDTH
from structures.cell import Cell, Objective
from structures.direction import Direction
from structures.enemy import Enemy
from structures.pawn import Pawn
from structures.player import Player

# Initialize Pygame
pygame.init()
pygame.joystick.init()

# Constants
SCREEN_WIDTH = 1100
SCREEN_HEIGHT = 900  # Increased height for timer display
CELL_SIZE = 60
NUM_TILES = 5

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
DARK_RED = (192, 0, 0)
GRAY = (192, 192, 192)
YELLOW = (255, 255, 0)
PURPLE = (128, 0, 128)
DARK_BROWN = (101, 67, 33)

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
            width = SCREEN_WIDTH - 200
            transparency_surface = pygame.Surface((width // NUM_TILES, SCREEN_HEIGHT // NUM_TILES), pygame.SRCALPHA)
            transparency_surface.fill((0, 0, 0, 255))  # rgpA, A = 0 is transparent, A = 255 is opaque
            transparency_surface.scroll(row * width // NUM_TILES, col * SCREEN_HEIGHT // NUM_TILES)
            pygame.display.flip()
            transparency_surfaces.append(transparency_surface)
    return transparency_surfaces, transparencies

def _create_oxygen_panel():
    oxygen_image_view = pygame.Surface((100, SCREEN_WIDTH - 200))
    oxygen_image_view.fill(GRAY)
    pygame.draw.rect(oxygen_image_view, DARK_BROWN, (SCREEN_WIDTH - 200, 0, 100, 10))
    scale_image_view = pygame.Surface((100, 1000))
    return oxygen_image_view, scale_image_view

def _create_player_indicators(screen, startx, starty, player_text):
    player_indicator_surface = pygame.Surface((100, 450))
    player_indicator_surface.fill(GRAY)
    pygame.draw.rect(player_indicator_surface, RED, (startx, starty, 100, 450))
    font = pygame.font.SysFont('Arial', 25)
    screen.blit(font.render(player_text, True, (255,0,0)), (200, 100))
    return player_indicator_surface

# Draw board
def _draw_board(screen, board, exit_image):
    for x in range(BOARD_WIDTH):
        for y in range(BOARD_HEIGHT):
            image = Cell.get_wall_image(board.cells[Board.cartesian_to_id(x, y)].adjacency_matrix)
            screen.blit(image, (x * CELL_SIZE, y *  CELL_SIZE))
            # pygame.draw.rect(screen, GRAY, (x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE), 2)
            match board.cells[Board.cartesian_to_id(x, y)].objective:
                case Objective.EXIT:
                    shift = 10
                    size_shift = 20
                    exit_image = pygame.image.load(exit_image)
                    screen.blit(exit_image, (x * CELL_SIZE + 5, y * CELL_SIZE + shift, CELL_SIZE - size_shift, CELL_SIZE - size_shift))
                case Objective.PRESSURE_PLATE:
                    shift = 10
                    size_shift = 20
                    PRESSURE_PLATE_IMAGE = pygame.image.load("assets/objectives/pressure_plate.png")
                    screen.blit(PRESSURE_PLATE_IMAGE, (x * CELL_SIZE + shift, y * CELL_SIZE + shift + 10, CELL_SIZE, CELL_SIZE))
                case Objective.OXYGEN_TANK:
                    shift = 10
                    size_shift = 20
                    OXYGEN_IMAGE = pygame.image.load("assets/objectives/oxygen.png")
                    screen.blit(OXYGEN_IMAGE, (x * CELL_SIZE + shift, y * CELL_SIZE + shift, CELL_SIZE - size_shift, CELL_SIZE - size_shift))

def _draw_transparencies(screen, transparency_surfaces):
    for i in range(len(transparency_surfaces)):
        width = SCREEN_WIDTH - 200
        (row, column) = divmod(i, NUM_TILES)
        screen.blit(transparency_surfaces[i], (row * width // NUM_TILES, column * SCREEN_HEIGHT // NUM_TILES))

def _draw_oxygen_panel(screen, oxygen_image_view, scale_image_view, oxygen):
    scale_image_view.fill(DARK_BROWN)
    height = oxygen * scale_image_view.get_height() // 100
    y = scale_image_view.get_height() - height
    pygame.draw.rect(scale_image_view, GREEN, (40, y, 20, height), 0, 3)
        
    screen.blit(oxygen_image_view, oxygen_image_view.get_rect(center = (950, 450)))
    screen.blit(scale_image_view, scale_image_view.get_rect(center = (950, 450)))

def _draw_player_indicator(screen, player_indicator_surface, player, dx, dy):
    match player.pawns[player.pawn_index].color:
        case "BLUE":
            PLAYER_IMAGE = pygame.image.load("assets/pawns/miner1.png")
        case "RED":
            PLAYER_IMAGE = pygame.image.load("assets/pawns/miner2.png")
    
    PLAYER_IMAGE = pygame.transform.scale_by(PLAYER_IMAGE, 2)
    screen.blit(PLAYER_IMAGE, player_indicator_surface.get_rect(center = (dx + 15, dy + 185)))

    if player.possible_movement == {Direction.NORTH, Direction.SOUTH}:
        DIRECTION_IMAGE = pygame.image.load("assets/decals/up_down.png")
    else:
        DIRECTION_IMAGE = pygame.image.load("assets/decals/left_right.png")

    DIRECTION_IMAGE = pygame.transform.scale_by(DIRECTION_IMAGE, 0.7)
    screen.blit(DIRECTION_IMAGE, player_indicator_surface.get_rect(center = (dx + 5, dy + 225)))
    font = pygame.font.SysFont('luxiserif', 50)
    screen.blit(font.render("P1", True, WHITE), (1025, 10))
    screen.blit(font.render("P2", True, WHITE), (1025, 510))

# Draw pawns
def _draw_pawns(screen, pawns):
    shift = 10
    size_shift = 20
    for pawn in pawns:
        match pawn.color:
            case "BLUE":
                PIC_IMAGE = pygame.image.load("assets/pawns/miner1.png")
            case "RED":
                PIC_IMAGE = pygame.image.load("assets/pawns/miner2.png")
        screen.blit(PIC_IMAGE, ((pawn.x * CELL_SIZE) + shift, (pawn.y * CELL_SIZE) + shift, CELL_SIZE - size_shift, CELL_SIZE - size_shift))

def _draw_enemy(screen, enemy):
    size_shift = 20
    ENEMY_IMAGE = pygame.image.load("assets/pawns/major.png")
    screen.blit(ENEMY_IMAGE, ((enemy.x * CELL_SIZE), (enemy.y * CELL_SIZE), CELL_SIZE - size_shift, CELL_SIZE - size_shift))
    
def main():
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Miner Issues")
    clock = pygame.time.Clock()
    joy = None

    board = _create_board(None)  # Gives access to access to all cells
    transparency_surfaces, transparencies = _create_transparencies()
    oxygen_image_view, scale_image_view = _create_oxygen_panel()
    first_player_indicator_surface = _create_player_indicators(screen, 1000, 0, "Player 1")
    second_player_indicator_surface = _create_player_indicators(screen, 1000, 450, "Player 2")
    
    do_something_image = pygame.image.load("assets/decals/dosomething.png").convert_alpha()
    do_something_transparency = 0
     
    running = True
    win = False

    pawns = [Pawn(6, 6, "BLUE"), Pawn(8, 8, "RED")]
    first_player = Player(0, pawns, {Direction.NORTH, Direction.SOUTH})
    second_player = Player(1, pawns, {Direction.WEST, Direction.EAST})

    oxygen = 100
    exit_open = False
    enemy = Enemy(7, 1, False, -1)

    while running:
        # Draw board and other elements
        if exit_open:
            _draw_board(screen, board, "assets/objectives/exit.png")
        else:
            _draw_board(screen, board, "assets/objectives/exit_cover.png")
        _draw_pawns(screen, pawns)
        _draw_oxygen_panel(screen, oxygen_image_view, scale_image_view, oxygen)
        _draw_transparencies(screen, transparency_surfaces)
        _draw_player_indicator(screen, first_player_indicator_surface, first_player, 1050, 225)
        _draw_player_indicator(screen, second_player_indicator_surface, second_player, 1050, 675)

        for pawn in pawns:
            current_x = pawn.x // 3
            current_y = pawn.y // 3
            transparencies[current_x * NUM_TILES + current_y] -= 20

        do_something_transparency -= 30
        if do_something_transparency < 0:
            do_something_transparency = 0
        do_something_image.set_alpha(do_something_transparency)
        screen.blit(do_something_image, (250, 250))
        
        for i in range(len(transparencies)):
            transparencies[i] += 0.6
            if transparencies[i] > 255:
                transparencies[i] = 255
            if transparencies[i] < 0:
                transparencies[i] = 0
            transparency_surfaces[i].fill((0, 0, 0, transparencies[i]))

        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                match event.key: 
                    case pygame.K_UP:
                        first_player.move(Direction.NORTH, board)
                    case pygame.K_DOWN:
                        first_player.move(Direction.SOUTH, board)
                    case pygame.K_a:
                        second_player.move(Direction.WEST, board)
                    case pygame.K_d:
                        second_player.move(Direction.EAST, board)
                    case pygame.K_k:
                        first_player.rotate_pawn()
                    case pygame.K_f:
                        second_player.rotate_pawn() 
                    case pygame.K_h:
                        do_something_transparency = 255
            elif event.type==pygame.JOYDEVICEADDED:
                joy = pygame.joystick.Joystick(event.device_index)
            elif event.type == pygame.JOYBUTTONDOWN:
                if event.button == 1:
                    if event.joy == 0:
                        first_player.rotate_pawn()
                    else:
                        second_player.rotate_pawn()
                if event.button == 4:
                    do_something_transparency = 255
            elif event.type == pygame.JOYAXISMOTION:
                if event.joy == 0:
                    if event.axis == 1 and event.value < -0.5:
                        first_player.move(Direction.NORTH, board)
                    elif event.axis == 1 and event.value > 0.5:
                        first_player.move(Direction.SOUTH, board)
                else:
                    if event.axis == 0 and event.value < -0.5:
                        second_player.move(Direction.WEST, board)
                    elif event.axis == 0 and event.value > 0.5:
                        second_player.move(Direction.EAST, board)

        oxygen -= 0.05
        if oxygen < 0:
            break
        
        for pawn in pawns:
            if board.cells[Board.cartesian_to_id(pawn.x, pawn.y)].objective == Objective.OXYGEN_TANK:
                oxygen += 25
                if oxygen > 100:
                    oxygen = 100
                board.cells[Board.cartesian_to_id(pawn.x, pawn.y)].objective = Objective.EMPTY

        if all(board.cells[Board.cartesian_to_id(pawn.x, pawn.y)].objective == Objective.PRESSURE_PLATE for pawn in pawns):
            exit_open = True
            enemy.interact(board, pawns)

        if enemy.enabled:
            _draw_enemy(screen, enemy)
            enemy.interact(board, pawns)
            if any(pawn.x == enemy.x and pawn.y == enemy.y for pawn in pawns):
                pygame.display.flip()
                break
        
        for pawn in pawns:
            if board.cells[Board.cartesian_to_id(pawn.x, pawn.y)].objective == Objective.EXIT and exit_open:
                pawns.remove(pawn)

        if not pawns:
            win = True
            running = False

        pygame.display.flip()
        clock.tick(60)

    font = pygame.font.SysFont("luxiserif", 100)
    if win and exit_open:
        time_text = font.render('YOU ESCAPED', True, WHITE)  
    else:
        time_text = font.render('YOU MINED', True, DARK_RED)
    screen.blit(time_text, (SCREEN_WIDTH // 2 - time_text.get_width() // 2 - 100, SCREEN_HEIGHT // 2 - time_text.get_height() // 2))
    pygame.display.flip()
    pygame.time.wait(2000)
    pygame.quit()

if __name__ == "__main__":
    main()
