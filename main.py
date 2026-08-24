import pygame
import sys
import math
import random

pygame.init()

# =========================================================
# WINDOW
# =========================================================

WIDTH = 700
HEIGHT = 850

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Tic Tac Toe - Minimax AI")

clock = pygame.time.Clock()

# =========================================================
# COLORS
# =========================================================

BG_TOP = (8, 10, 28)
BG_BOTTOM = (30, 8, 45)

WHITE = (240, 245, 255)
GRAY = (145, 150, 175)

X_COLOR = (50, 220, 255)
O_COLOR = (255, 70, 180)

GREEN = (70, 255, 150)

GRID_COLOR = (75, 85, 130)

BUTTON_COLOR = (45, 50, 80)
BUTTON_HOVER = (70, 80, 125)

# =========================================================
# FONTS
# =========================================================

TITLE_FONT = pygame.font.Font(None, 78)
SUBTITLE_FONT = pygame.font.Font(None, 30)
STATUS_FONT = pygame.font.Font(None, 48)
BUTTON_FONT = pygame.font.Font(None, 36)
SMALL_FONT = pygame.font.Font(None, 27)

# =========================================================
# PLAYERS
# =========================================================

HUMAN = "X"
AI = "O"

# =========================================================
# BOARD
# =========================================================

BOARD_SIZE = 600
CELL_SIZE = BOARD_SIZE // 3

START_X = (WIDTH - BOARD_SIZE) // 2
START_Y = 145

board = [
    ["", "", ""],
    ["", "", ""],
    ["", "", ""]
]

# =========================================================
# GAME STATE
# =========================================================

game_state = "menu"

difficulty = "HARD"

player_turn = True
game_over = False
winner = None

winning_cells = []

animations = {}

# =========================================================
# AI ANIMATION
# =========================================================

ai_thinking = False
thinking_timer = 0
thinking_dots = 0

# =========================================================
# WIN ANIMATION
# =========================================================

win_animation = 0

# =========================================================
# SCORE
# =========================================================

player_score = 0
ai_score = 0
draw_score = 0


# =========================================================
# BACKGROUND
# =========================================================

def draw_background():

    for y in range(HEIGHT):

        ratio = y / HEIGHT

        r = int(
            BG_TOP[0] * (1 - ratio)
            + BG_BOTTOM[0] * ratio
        )

        g = int(
            BG_TOP[1] * (1 - ratio)
            + BG_BOTTOM[1] * ratio
        )

        b = int(
            BG_TOP[2] * (1 - ratio)
            + BG_BOTTOM[2] * ratio
        )

        pygame.draw.line(
            screen,
            (r, g, b),
            (0, y),
            (WIDTH, y)
        )


# =========================================================
# RESET BOARD
# =========================================================

def reset_board():

    global board
    global game_over
    global winner
    global player_turn
    global winning_cells
    global animations
    global win_animation
    global ai_thinking
    global thinking_timer
    global thinking_dots

    board = [
        ["", "", ""],
        ["", "", ""],
        ["", "", ""]
    ]

    game_over = False
    winner = None
    player_turn = True

    winning_cells = []
    animations = {}

    win_animation = 0

    ai_thinking = False
    thinking_timer = 0
    thinking_dots = 0


# =========================================================
# WINNER CHECK
# =========================================================

def get_winner(board_state):

    # Rows
    for row in range(3):

        if (
            board_state[row][0] != ""
            and board_state[row][0] == board_state[row][1]
            and board_state[row][1] == board_state[row][2]
        ):
            return board_state[row][0]

    # Columns
    for col in range(3):

        if (
            board_state[0][col] != ""
            and board_state[0][col] == board_state[1][col]
            and board_state[1][col] == board_state[2][col]
        ):
            return board_state[0][col]

    # Main diagonal
    if (
        board_state[0][0] != ""
        and board_state[0][0] == board_state[1][1]
        and board_state[1][1] == board_state[2][2]
    ):
        return board_state[0][0]

    # Other diagonal
    if (
        board_state[0][2] != ""
        and board_state[0][2] == board_state[1][1]
        and board_state[1][1] == board_state[2][0]
    ):
        return board_state[0][2]

    return None


# =========================================================
# GET WINNING CELLS
# =========================================================

def get_winning_cells(board_state):

    # Rows
    for row in range(3):

        if (
            board_state[row][0] != ""
            and board_state[row][0] == board_state[row][1]
            and board_state[row][1] == board_state[row][2]
        ):
            return [
                (row, 0),
                (row, 1),
                (row, 2)
            ]

    # Columns
    for col in range(3):

        if (
            board_state[0][col] != ""
            and board_state[0][col] == board_state[1][col]
            and board_state[1][col] == board_state[2][col]
        ):
            return [
                (0, col),
                (1, col),
                (2, col)
            ]

    # Main diagonal
    if (
        board_state[0][0] != ""
        and board_state[0][0] == board_state[1][1]
        and board_state[1][1] == board_state[2][2]
    ):
        return [
            (0, 0),
            (1, 1),
            (2, 2)
        ]

    # Other diagonal
    if (
        board_state[0][2] != ""
        and board_state[0][2] == board_state[1][1]
        and board_state[1][1] == board_state[2][0]
    ):
        return [
            (0, 2),
            (1, 1),
            (2, 0)
        ]

    return []


# =========================================================
# BOARD FULL
# =========================================================

def is_board_full(board_state):

    for row in range(3):

        for col in range(3):

            if board_state[row][col] == "":
                return False

    return True


# =========================================================
# MINIMAX
# =========================================================

def minimax(board_state, is_maximizing, depth):

    result = get_winner(board_state)

    # AI wins
    if result == AI:

        return 10 - depth

    # Human wins
    if result == HUMAN:

        return depth - 10

    # Draw
    if is_board_full(board_state):

        return 0

    # =====================================================
    # MAXIMIZING PLAYER = AI
    # =====================================================

    if is_maximizing:

        best_score = -math.inf

        for row in range(3):

            for col in range(3):

                if board_state[row][col] == "":

                    board_state[row][col] = AI

                    score = minimax(
                        board_state,
                        False,
                        depth + 1
                    )

                    # Undo move
                    board_state[row][col] = ""

                    best_score = max(
                        best_score,
                        score
                    )

        return best_score

    # =====================================================
    # MINIMIZING PLAYER = HUMAN
    # =====================================================

    else:

        best_score = math.inf

        for row in range(3):

            for col in range(3):

                if board_state[row][col] == "":

                    board_state[row][col] = HUMAN

                    score = minimax(
                        board_state,
                        True,
                        depth + 1
                    )

                    # Undo move
                    board_state[row][col] = ""

                    best_score = min(
                        best_score,
                        score
                    )

        return best_score


# =========================================================
# BEST MOVE
# =========================================================

def get_best_move():

    best_score = -math.inf
    best_move = None

    for row in range(3):

        for col in range(3):

            if board[row][col] == "":

                board[row][col] = AI

                score = minimax(
                    board,
                    False,
                    0
                )

                board[row][col] = ""

                if score > best_score:

                    best_score = score
                    best_move = (row, col)

    return best_move


# =========================================================
# EASY MOVE
# =========================================================

def easy_move():

    empty_cells = []

    for row in range(3):

        for col in range(3):

            if board[row][col] == "":
                empty_cells.append((row, col))

    if empty_cells:

        return random.choice(empty_cells)

    return None


# =========================================================
# MEDIUM MOVE
# =========================================================

def medium_move():

    # Try Minimax half of the time

    if random.random() < 0.5:

        return get_best_move()

    return easy_move()


# =========================================================
# AI MOVE
# =========================================================

def ai_move():

    if difficulty == "EASY":

        move = easy_move()

    elif difficulty == "MEDIUM":

        move = medium_move()

    else:

        move = get_best_move()

    if move is not None:

        row, col = move

        board[row][col] = AI

        animations[(row, col)] = 0


# =========================================================
# GET CELL FROM MOUSE
# =========================================================

def get_cell(mouse_x, mouse_y):

    if not (
        START_X <= mouse_x <= START_X + BOARD_SIZE
        and
        START_Y <= mouse_y <= START_Y + BOARD_SIZE
    ):

        return None

    col = (mouse_x - START_X) // CELL_SIZE
    row = (mouse_y - START_Y) // CELL_SIZE

    return row, col


# =========================================================
# GLOW
# =========================================================

def draw_glow_circle(
    position,
    radius,
    color
):

    for glow in range(20, 0, -4):

        alpha = max(
            10,
            80 - glow * 3
        )

        surface = pygame.Surface(
            (
                radius * 2 + glow * 2,
                radius * 2 + glow * 2
            ),
            pygame.SRCALPHA
        )

        pygame.draw.circle(
            surface,
            (*color, alpha),
            (
                radius + glow,
                radius + glow
            ),
            radius + glow
        )

        screen.blit(
            surface,
            (
                position[0] - radius - glow,
                position[1] - radius - glow
            )
        )


# =========================================================
# DRAW X / O
# =========================================================

def draw_symbol(symbol, row, col):

    center_x = (
        START_X
        + col * CELL_SIZE
        + CELL_SIZE // 2
    )

    center_y = (
        START_Y
        + row * CELL_SIZE
        + CELL_SIZE // 2
    )

    progress = animations.get(
        (row, col),
        30
    )

    scale = min(
        1,
        progress / 15
    )

    color = (
        X_COLOR
        if symbol == "X"
        else O_COLOR
    )

    # Glow
    draw_glow_circle(
        (
            center_x,
            center_y
        ),
        int(55 * scale),
        color
    )

    # =====================================================
    # X
    # =====================================================

    if symbol == "X":

        size = int(
            55 * scale
        )

        pygame.draw.line(
            screen,
            color,
            (
                center_x - size,
                center_y - size
            ),
            (
                center_x + size,
                center_y + size
            ),
            10
        )

        pygame.draw.line(
            screen,
            color,
            (
                center_x + size,
                center_y - size
            ),
            (
                center_x - size,
                center_y + size
            ),
            10
        )

    # =====================================================
    # O
    # =====================================================

    else:

        radius = int(
            58 * scale
        )

        pygame.draw.circle(
            screen,
            color,
            (
                center_x,
                center_y
            ),
            radius,
            10
        )


# =========================================================
# DRAW WINNING LINE
# =========================================================

def draw_winning_line():

    if not winning_cells:

        return

    first_row, first_col = winning_cells[0]
    last_row, last_col = winning_cells[-1]

    start_x = (
        START_X
        + first_col * CELL_SIZE
        + CELL_SIZE // 2
    )

    start_y = (
        START_Y
        + first_row * CELL_SIZE
        + CELL_SIZE // 2
    )

    end_x = (
        START_X
        + last_col * CELL_SIZE
        + CELL_SIZE // 2
    )

    end_y = (
        START_Y
        + last_row * CELL_SIZE
        + CELL_SIZE // 2
    )

    progress = min(
        1,
        win_animation / 30
    )

    current_x = (
        start_x
        + (end_x - start_x)
        * progress
    )

    current_y = (
        start_y
        + (end_y - start_y)
        * progress
    )

    pygame.draw.line(
        screen,
        GREEN,
        (
            start_x,
            start_y
        ),
        (
            current_x,
            current_y
        ),
        12
    )


# =========================================================
# DRAW BOARD
# =========================================================

def draw_board():

    mouse_x, mouse_y = pygame.mouse.get_pos()

    hovered_cell = get_cell(
        mouse_x,
        mouse_y
    )

    # =====================================================
    # CELL HOVER
    # =====================================================

    for row in range(3):

        for col in range(3):

            rect = pygame.Rect(
                START_X
                + col * CELL_SIZE
                + 5,

                START_Y
                + row * CELL_SIZE
                + 5,

                CELL_SIZE - 10,
                CELL_SIZE - 10
            )

            if (
                hovered_cell == (row, col)
                and board[row][col] == ""
                and not game_over
                and player_turn
                and not ai_thinking
            ):

                pygame.draw.rect(
                    screen,
                    (
                        35,
                        40,
                        65
                    ),
                    rect,
                    border_radius=18
                )

    # =====================================================
    # GRID
    # =====================================================

    for i in range(1, 3):

        x = (
            START_X
            + i * CELL_SIZE
        )

        pygame.draw.line(
            screen,
            GRID_COLOR,
            (
                x,
                START_Y
            ),
            (
                x,
                START_Y + BOARD_SIZE
            ),
            5
        )

    for i in range(1, 3):

        y = (
            START_Y
            + i * CELL_SIZE
        )

        pygame.draw.line(
            screen,
            GRID_COLOR,
            (
                START_X,
                y
            ),
            (
                START_X + BOARD_SIZE,
                y
            ),
            5
        )

    # =====================================================
    # SYMBOLS
    # =====================================================

    for row in range(3):

        for col in range(3):

            if board[row][col] != "":

                draw_symbol(
                    board[row][col],
                    row,
                    col
                )

    # =====================================================
    # WIN LINE
    # =====================================================

    if game_over and winning_cells:

        draw_winning_line()


# =========================================================
# AI THINKING
# =========================================================

def draw_ai_thinking():

    if not ai_thinking:

        return

    dots = "." * thinking_dots

    text = SMALL_FONT.render(
        f"AI IS THINKING{dots}",
        True,
        O_COLOR
    )

    rect = text.get_rect(
        center=(
            WIDTH // 2,
            745
        )
    )

    screen.blit(
        text,
        rect
    )


# =========================================================
# BUTTON
# =========================================================

def draw_button(
    rect,
    text
):

    mouse_pos = pygame.mouse.get_pos()

    color = (
        BUTTON_HOVER
        if rect.collidepoint(mouse_pos)
        else BUTTON_COLOR
    )

    pygame.draw.rect(
        screen,
        color,
        rect,
        border_radius=15
    )

    text_surface = BUTTON_FONT.render(
        text,
        True,
        WHITE
    )

    text_rect = text_surface.get_rect(
        center=rect.center
    )

    screen.blit(
        text_surface,
        text_rect
    )


# =========================================================
# MENU
# =========================================================

def draw_menu():

    draw_background()

    title = TITLE_FONT.render(
        "TIC TAC TOE",
        True,
        WHITE
    )

    title_rect = title.get_rect(
        center=(
            WIDTH // 2,
            125
        )
    )

    screen.blit(
        title,
        title_rect
    )

    subtitle = SUBTITLE_FONT.render(
        "ARTIFICIAL INTELLIGENCE • MINIMAX",
        True,
        GRAY
    )

    subtitle_rect = subtitle.get_rect(
        center=(
            WIDTH // 2,
            175
        )
    )

    screen.blit(
        subtitle,
        subtitle_rect
    )

    select_text = STATUS_FONT.render(
        "SELECT DIFFICULTY",
        True,
        WHITE
    )

    select_rect = select_text.get_rect(
        center=(
            WIDTH // 2,
            270
        )
    )

    screen.blit(
        select_text,
        select_rect
    )

    # =====================================================
    # BUTTONS
    # =====================================================

    easy_rect = pygame.Rect(
        200,
        330,
        300,
        60
    )

    medium_rect = pygame.Rect(
        200,
        415,
        300,
        60
    )

    hard_rect = pygame.Rect(
        200,
        500,
        300,
        60
    )

    start_rect = pygame.Rect(
        200,
        625,
        300,
        70
    )

    draw_button(
        easy_rect,
        "EASY"
    )

    draw_button(
        medium_rect,
        "MEDIUM"
    )

    draw_button(
        hard_rect,
        "HARD • MINIMAX"
    )

    draw_button(
        start_rect,
        "START GAME"
    )

    # =====================================================
    # CURRENT DIFFICULTY
    # =====================================================

    current = SMALL_FONT.render(
        f"Selected: {difficulty}",
        True,
        GREEN
    )

    current_rect = current.get_rect(
        center=(
            WIDTH // 2,
            580
        )
    )

    screen.blit(
        current,
        current_rect
    )

    return (
        easy_rect,
        medium_rect,
        hard_rect,
        start_rect
    )


# =========================================================
# GAME SCREEN
# =========================================================

def draw_game():

    draw_background()

    # =====================================================
    # TITLE
    # =====================================================

    title = TITLE_FONT.render(
        "TIC TAC TOE",
        True,
        WHITE
    )

    title_rect = title.get_rect(
        center=(
            WIDTH // 2,
            55
        )
    )

    screen.blit(
        title,
        title_rect
    )

    # =====================================================
    # DIFFICULTY
    # =====================================================

    difficulty_text = SUBTITLE_FONT.render(
        f"DIFFICULTY: {difficulty}",
        True,
        GRAY
    )

    difficulty_rect = difficulty_text.get_rect(
        center=(
            WIDTH // 2,
            100
        )
    )

    screen.blit(
        difficulty_text,
        difficulty_rect
    )

    # =====================================================
    # SCORE
    # =====================================================

    score_text = SMALL_FONT.render(
        f"YOU  {player_score}"
        f"      DRAW  {draw_score}"
        f"      AI  {ai_score}",
        True,
        WHITE
    )

    score_rect = score_text.get_rect(
        center=(
            WIDTH // 2,
            125
        )
    )

    screen.blit(
        score_text,
        score_rect
    )

    # =====================================================
    # BOARD
    # =====================================================

    draw_board()

    # =====================================================
    # STATUS
    # =====================================================

    if game_over:

        if winner == HUMAN:

            message = "YOU WIN!"

        elif winner == AI:

            message = "AI WINS!"

        else:

            message = "DRAW!"

    elif ai_thinking:

        message = ""

    elif player_turn:

        message = "YOUR TURN • X"

    else:

        message = "AI TURN • O"

    if message:

        status = STATUS_FONT.render(
            message,
            True,
            GREEN
            if game_over
            else WHITE
        )

        status_rect = status.get_rect(
            center=(
                WIDTH // 2,
                745
            )
        )

        screen.blit(
            status,
            status_rect
        )

    # =====================================================
    # AI THINKING
    # =====================================================

    draw_ai_thinking()

    # =====================================================
    # GAME OVER BUTTONS
    # =====================================================

    if game_over:

        play_again = pygame.Rect(
            150,
            790,
            180,
            45
        )

        menu_button = pygame.Rect(
            370,
            790,
            180,
            45
        )

        draw_button(
            play_again,
            "PLAY AGAIN"
        )

        draw_button(
            menu_button,
            "MENU"
        )

        return (
            play_again,
            menu_button
        )

    return None, None


# =========================================================
# MAIN LOOP
# =========================================================

running = True

while running:

    # =====================================================
    # EVENTS
    # =====================================================

    for event in pygame.event.get():

        if event.type == pygame.QUIT:

            running = False

        # =================================================
        # MENU
        # =================================================

        if game_state == "menu":

            if event.type == pygame.MOUSEBUTTONDOWN:

                (
                    easy_rect,
                    medium_rect,
                    hard_rect,
                    start_rect
                ) = draw_menu()

                if easy_rect.collidepoint(
                    event.pos
                ):

                    difficulty = "EASY"

                elif medium_rect.collidepoint(
                    event.pos
                ):

                    difficulty = "MEDIUM"

                elif hard_rect.collidepoint(
                    event.pos
                ):

                    difficulty = "HARD"

                elif start_rect.collidepoint(
                    event.pos
                ):

                    reset_board()

                    game_state = "game"

        # =================================================
        # GAME
        # =================================================

        elif game_state == "game":

            if event.type == pygame.MOUSEBUTTONDOWN:

                # =========================================
                # GAME OVER
                # =========================================

                if game_over:

                    play_again = pygame.Rect(
                        150,
                        790,
                        180,
                        45
                    )

                    menu_button = pygame.Rect(
                        370,
                        790,
                        180,
                        45
                    )

                    if play_again.collidepoint(
                        event.pos
                    ):

                        reset_board()

                    elif menu_button.collidepoint(
                        event.pos
                    ):

                        reset_board()

                        game_state = "menu"

                # =========================================
                # PLAYER MOVE
                # =========================================

                elif (
                    player_turn
                    and not ai_thinking
                ):

                    mouse_x, mouse_y = event.pos

                    cell = get_cell(
                        mouse_x,
                        mouse_y
                    )

                    if cell is not None:

                        row, col = cell

                        if board[row][col] == "":

                            # Human move
                            board[row][col] = HUMAN

                            animations[
                                (row, col)
                            ] = 0

                            winner = get_winner(
                                board
                            )

                            # =================================
                            # HUMAN WINS
                            # =================================

                            if winner:

                                game_over = True

                                winning_cells = (
                                    get_winning_cells(
                                        board
                                    )
                                )

                                player_score += 1

                            # =================================
                            # DRAW
                            # =================================

                            elif is_board_full(
                                board
                            ):

                                game_over = True

                                draw_score += 1

                            # =================================
                            # AI TURN
                            # =================================

                            else:

                                player_turn = False

                                ai_thinking = True

                                thinking_timer = 0

                                thinking_dots = 0

                                pygame.display.flip()

                                # Small thinking delay
                                pygame.time.delay(
                                    450
                                )

                                ai_move()

                                ai_thinking = False

                                winner = get_winner(
                                    board
                                )

                                # =================================
                                # AI WINS
                                # =================================

                                if winner:

                                    game_over = True

                                    winning_cells = (
                                        get_winning_cells(
                                            board
                                        )
                                    )

                                    ai_score += 1

                                # =================================
                                # DRAW
                                # =================================

                                elif is_board_full(
                                    board
                                ):

                                    game_over = True

                                    draw_score += 1

                                else:

                                    player_turn = True

    # =====================================================
    # MOVE ANIMATION
    # =====================================================

    for key in animations:

        if animations[key] < 15:

            animations[key] += 1

    # =====================================================
    # AI THINKING ANIMATION
    # =====================================================

    if ai_thinking:

        thinking_timer += 1

        if thinking_timer >= 10:

            thinking_timer = 0

            thinking_dots += 1

            if thinking_dots > 3:

                thinking_dots = 0

    # =====================================================
    # WIN ANIMATION
    # =====================================================

    if game_over and winning_cells:

        if win_animation < 30:

            win_animation += 1

    # =====================================================
    # DRAW
    # =====================================================

    if game_state == "menu":

        draw_menu()

    else:

        draw_game()

    pygame.display.flip()

    clock.tick(60)


# =========================================================
# QUIT
# =========================================================

pygame.quit()
sys.exit()