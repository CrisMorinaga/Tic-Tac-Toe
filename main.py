from collections import Counter
import pygame
from sys import exit
from cpu import ComputerBrain

SCREEN_WIDTH = 600
SCREEN_HEIGHT = 600

pygame.init()
pygame.key.set_repeat(0)
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pygame.time.Clock()
pygame.display.set_caption('Tic Tac Toe')


class Circle(pygame.sprite.Sprite):
    """Creates a Circle on the selected x and y coordinate"""
    def __init__(self, radius: int, line_width: int):
        super().__init__()
        self.radius = radius
        self.image = pygame.Surface((radius * 2, radius * 2), pygame.SRCALPHA)  # Makes the surface transparent
        pygame.draw.circle(self.image, 'white', (radius, radius), radius, line_width)
        self.rect = None

    def create_rect(self, x_pos, y_pos):
        self.rect = pygame.Rect(x_pos - self.radius, y_pos - self.radius, self.radius * 2, self.radius * 2)


class X(pygame.sprite.Sprite):
    """Creates the X figure on the selected x and y coordinate"""
    def __init__(self, length: int, x_pos: int, y_pos: int, line_width: int):
        super().__init__()
        self.half_of_line = length / 2
        self.image = pygame.Surface((length, length), pygame.SRCALPHA)  # Create a transparent surface
        pygame.draw.line(self.image, 'white', (0, 0), (length, length), line_width)
        pygame.draw.line(self.image, 'white', (length, 0), (0, length), line_width)
        self.rect = self.image.get_rect(center=(x_pos, y_pos))


class UI(pygame.sprite.Sprite):
    """Creates the UI text elements present in the main menu"""
    def __init__(self, size: int, text: str, color: str, x_pos: int, y_pos: int, antialias=False,
                 font: str = None, header_type=False, difficulty_selection_menu=False):
        super().__init__()
        self.title = header_type
        self.difficulty = difficulty_selection_menu
        self.size = size
        self.text = text
        self.color = color
        self.antialias = antialias
        self.font = font
        self.x = x_pos
        self.y = y_pos
        self.config = pygame.font.Font(self.font, self.size)
        self.image = self.config.render(self.text, self.antialias, self.color)
        self.rect = self.image.get_rect(center=(self.x, self.y))

    def update_text_color(self, color):
        self.color = color
        self.image = self.config.render(self.text, self.antialias, self.color)
        self.rect = self.image.get_rect(center=(self.x, self.y))


class Mouse(pygame.sprite.Sprite):
    """Creates a tiny square that replaces the users mouse"""
    def __init__(self):
        super().__init__()
        self.mouse = pygame.mouse.set_visible(False)
        self.image = pygame.Surface((10, 10))
        self.rect = self.image.get_rect()
        self.image.fill('red')
        self.mask = pygame.mask.from_surface(self.image)
        self.mouse_color = 'green'

    def update(self):
        mouse_pos = pygame.mouse.get_pos()
        self.rect.center = mouse_pos
        self.image.fill(self.mouse_color)


def check_mouse_position():
    mouse_position = pygame.mouse.get_pos()
    mouse_position_game = []

    mouse_x = mouse_position[0]
    if mouse_x < 195:
        mouse_position_game.append(120)
    elif 205 < mouse_x < 395:
        mouse_position_game.append(300)
    elif 405 < mouse_x < 595:
        mouse_position_game.append(480)

    mouse_y = mouse_position[1]
    if mouse_y < 195:
        mouse_position_game.append(120)
    elif 205 < mouse_y < 395:
        mouse_position_game.append(300)
    elif 405 < mouse_y < 595:
        mouse_position_game.append(480)

    return mouse_position_game


def draw_winning_line(surface, start_pos, end_pos):
    return pygame.draw.line(surface, 'red', start_pos, end_pos, 5)


def check_winning_condition(group, used_pos: list):
    if len(used_pos) >= 5:
        x_coordinate = Counter(form.rect.center[0] for form in group)
        y_coordinate = Counter(form.rect.center[1] for form in group)
        left_start_diagonal = [form for form in group if form.rect.center in [(120, 120), (300, 300), (480, 480)]]
        right_start_diagonal = [form for form in group if form.rect.center in [(120, 480), (300, 300), (480, 120)]]

        for y_coord, count in y_coordinate.items():
            if count == 3:
                horizontal_line = draw_winning_line(screen, (25, y_coord), (575, y_coord))
                return horizontal_line

        for x_coord, count in x_coordinate.items():
            if count == 3:
                vertical_line = draw_winning_line(screen, (x_coord, 25), (x_coord, 575))
                return vertical_line

        if len(left_start_diagonal) == 3:
            left_to_right_diagonal_line = draw_winning_line(screen, (25, 25), (575, 575))
            return left_to_right_diagonal_line
        elif len(right_start_diagonal) == 3:
            right_to_left_diagonal_line = draw_winning_line(screen, (575, 25), (25, 575))
            return right_to_left_diagonal_line


def win_screen(render_text, color, text_size):
    game_over_font_config = pygame.font.Font(None, text_size)
    restart_or_menu_font_config = pygame.font.Font(None, 25)
    # Black surface to draw the text in
    game_over_surf = pygame.Surface((250, 100))
    game_over_surf_rect = game_over_surf.get_rect(center=(300, 300))

    restart_or_menu_surf = pygame.Surface((350, 50))
    restart_or_menu_surf_rect = restart_or_menu_surf.get_rect(center=(300, 400))
    # Calculate the center position of the surfaces
    game_over_center_x = game_over_surf.get_width() // 2
    game_over_center_y = game_over_surf.get_height() // 2

    restart_or_menu_center_x = restart_or_menu_surf.get_width() // 2
    restart_or_menu_center_y = restart_or_menu_surf.get_height() // 2
    # Text generation and positioning
    game_over_text = game_over_font_config.render(render_text, False, color)
    game_over_text_rect = game_over_text.get_rect(center=(game_over_center_x, game_over_center_y))

    restart_or_menu_text = restart_or_menu_font_config.render("Press 'R' to Reset and 'M' for Main menu", True, color)
    restart_or_menu_text_rect = restart_or_menu_text.get_rect(center=(restart_or_menu_center_x,
                                                                      restart_or_menu_center_y))
    # Positioning of the texts on the black surface
    game_over_surf.blit(game_over_text, game_over_text_rect)
    restart_or_menu_surf.blit(restart_or_menu_text, restart_or_menu_text_rect)
    # Positioning of the black surfaces on the screen
    screen.blit(game_over_surf, game_over_surf_rect)
    screen.blit(restart_or_menu_surf, restart_or_menu_surf_rect)
    # Drawing a white border around the surfaces
    pygame.draw.rect(screen, 'white', game_over_surf_rect, 5)
    pygame.draw.rect(screen, 'white', restart_or_menu_surf_rect, 5)


# Groups
circle_group = pygame.sprite.Group()
x_group = pygame.sprite.Group()

title = UI(100, 'Tic Tac Toe', 'white', 300, 180, header_type=True)
two_players = UI(50, '2 Players', 'white', 300, 300)
vs_cpu = UI(50, 'Against computer', 'white', 300, 400)
easy = UI(35, 'Easy', 'white', 300, 200, difficulty_selection_menu=True)
medium = UI(35, 'Medium', 'white', 300, 300, difficulty_selection_menu=True)
hard = UI(35, 'Hard', 'white', 300, 400, difficulty_selection_menu=True)

ui_group = pygame.sprite.Group()
ui_group.add(
    title,
    two_players,
    vs_cpu,
    easy,
    medium,
    hard,
)

mouse = Mouse()
mouse_group = pygame.sprite.GroupSingle()
mouse_group.add(mouse)

# Variables
current_turn = 1
cpu_turn = False

used_positions = []
user_movement = []

game_active = False
player_vs_player = False
player_vs_cpu = False
player_vs_cpu_config = False
tie = False
restart = False
menu = False
difficulty = 0

# Cleaning project 'variable can be undefined' errors
x_win = None
circle_win = None
game_type = None

########################################################################################################################
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                exit()

            if game_active:
                if event.key == pygame.K_r and (x_win or circle_win or tie):
                    restart = True

                if event.key == pygame.K_m:
                    menu = True

        if event.type == pygame.MOUSEBUTTONDOWN:
            pos = check_mouse_position()
            # Main menu and options
            if not game_active:
                if game_type == 1:
                    # Player vs player starts
                    player_vs_player = True
                    game_active = True
                elif game_type == 2:
                    player_vs_cpu_config = True
                    if difficulty > 0:
                        # A difficulty option is made and the game starts
                        game_active = True
                        player_vs_cpu = True
                        player_vs_cpu_config = False
            # Game starts
            elif player_vs_player:
                # Check for winning conditions, if nothing is found then the game continues
                if x_win is None and circle_win is None:
                    if current_turn % 2 == 0:
                        # Assigns circle to player 2
                        shape = "circle"
                    else:
                        # Assigns X to player 1
                        shape = "x"
                    if pos not in used_positions and len(pos) > 1:
                        used_positions.append(pos)
                        current_turn += 1
                        if shape == "x":
                            x = X(100, x_pos=pos[0], y_pos=pos[1], line_width=5)
                            x_group.add(x)
                        else:
                            circle = Circle(75, 5)
                            circle.create_rect(x_pos=pos[0], y_pos=pos[1])
                            circle_group.add(circle)

            elif player_vs_cpu:
                if x_win is None and circle_win is None:
                    if pos not in used_positions and len(pos) > 1:
                        used_positions.append(pos)
                        user_movement.append(pos)
                        x = X(100, x_pos=pos[0], y_pos=pos[1], line_width=5)
                        x_group.add(x)
                        cpu_turn = True

    black_surface = pygame.Surface((600, 600))
    screen.blit(black_surface, (0, 0))

    # Main menu
    if not game_active and not player_vs_cpu_config:
        for ui in ui_group:
            if not ui.difficulty:
                screen.blit(ui.image, ui.rect)

        # Hover text color change and game option choosing
        game_type = 0
        for option in ui_group:
            if not option.title and not option.difficulty and not game_active and not player_vs_cpu:
                if pygame.sprite.spritecollide(option, mouse_group, False):
                    option.update_text_color('red')
                    if '2' in option.text:
                        game_type = 1
                    elif 'computer' in option.text:
                        game_type = 2
                else:
                    option.update_text_color('white')

    # Difficulty select menu
    if player_vs_cpu_config:
        difficulty = 0
        screen.fill('black')
        for ui in ui_group:
            if ui.difficulty:
                screen.blit(ui.image, ui.rect)
            if ui.difficulty and ui.title:
                screen.blit(ui.image, ui.rect)
                pygame.draw.rect(screen, 'white', ui.rect, 5)

        # Hover text color change and difficulty choosing
        for option in ui_group:
            if not game_active and not option.title:
                if pygame.sprite.spritecollide(option, mouse_group, False):
                    option.update_text_color('red')
                    if 'Easy' in option.text:
                        difficulty = 1
                    elif 'Medium' in option.text:
                        difficulty = 2
                    elif 'Hard' in option.text:
                        difficulty = 3
                else:
                    option.update_text_color('white')

# -------------------------------------------------------------------------------------------------------------------- #
    if game_active:
        screen.fill('black')

        if restart or menu:
            current_turn = 1
            used_positions = []
            user_movement = []
            circle_group.empty()
            x_group.empty()
            x_win = None
            circle_win = None
            tie = False

        if restart:
            restart = False

        if menu:
            menu = False
            game_active = False
            player_vs_player = False
            player_vs_cpu = False
            player_vs_cpu_config = False
            difficulty = 0

        # Drawing the lines of the game
        for n in range(1, 3):
            start = 200
            pygame.draw.line(screen, 'white', (start * n, 50), (start * n, 550), 5)
            pygame.draw.line(screen, 'white', (50, start * n), (550, start * n), 5)

        circle_group.draw(screen)
        x_group.draw(screen)

        x_win = check_winning_condition(x_group, used_positions)
        circle_win = check_winning_condition(circle_group, used_positions)

        # Computer
        if x_win is None and circle_win is None:
            if cpu_turn:
                cpu = ComputerBrain(used_positions, circle_shape=Circle(75, 5),
                                    circle_group=circle_group, user_movements=user_movement)
                if difficulty == 1:
                    cpu.easy()
                elif difficulty == 2:
                    cpu.medium()
                elif difficulty == 3:
                    cpu.hard()
                cpu_turn = False

        if x_win:
            win_screen('Player 1 wins', 'white', 50)
        elif circle_win:
            win_screen('Player 2 wins', 'white', 50)
        elif len(used_positions) == 9 and not x_win and not circle_win:
            win_screen('Draw', 'white', 50)
            tie = True

    mouse_group.draw(screen)
    mouse_group.update()

    pygame.display.update()
    clock.tick(60)
