import pygame, sys, copy, random, numpy as np
from constants import *

# --- PYGAME SETUP ---
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("TIC-TAC TOE")
screen.fill(BG_COLOR)


# --- CLASSES ---
class Board:
    def __init__(self):
        self.squares = np.zeros((ROWS, COLS))
        self.marked_squares = 0
        self.empty_squares = self.squares  # [squares]

    def final_state(self, show=False):
        """
        @return 0 if there is no win yet
        @return 1 if player 1 wins
        @return 2 if player 2 wins
        """

        # Vertical Lines
        for col in range(COLS):
            if (
                self.squares[0][col]
                == self.squares[1][col]
                == self.squares[2][col]
                != 0
            ):
                if show:
                    color = CIRC_COLOR if self.squares[0][col] == 2 else CROSS_COLOR
                    iPos = (col * SQSIZE + SQSIZE // 2, 20)
                    fPos = (col * SQSIZE + SQSIZE // 2, HEIGHT - 20)
                    pygame.draw.line(screen, color, iPos, fPos, LINE_WIDTH)
                return self.squares[0][col]

        # Horizontal Lines
        for row in range(ROWS):
            if (
                self.squares[row][0]
                == self.squares[row][1]
                == self.squares[row][2]
                != 0
            ):
                if show:
                    color = CIRC_COLOR if self.squares[row][0] == 2 else CROSS_COLOR
                    iPos = (20, row * SQSIZE + SQSIZE // 2)
                    fPos = (WIDTH - 20, row * SQSIZE + SQSIZE // 2)
                    pygame.draw.line(screen, color, iPos, fPos, LINE_WIDTH)
                return self.squares[row][0]

        # Descending Diagonal
        if self.squares[0][0] == self.squares[1][1] == self.squares[2][2] != 0:
            if show:
                color = CIRC_COLOR if self.squares[1][1] == 2 else CROSS_COLOR
                iPos = (20, 20)
                fPos = (WIDTH - 20, HEIGHT - 20)
                pygame.draw.line(screen, color, iPos, fPos, CROSS_WIDTH)
            return self.squares[1][1]

        # Ascending Diagonal
        if self.squares[2][0] == self.squares[1][1] == self.squares[0][2] != 0:
            if show:
                color = CIRC_COLOR if self.squares[1][1] == 2 else CROSS_COLOR
                iPos = (20, HEIGHT - 20)
                fPos = (WIDTH - 20, 20)
                pygame.draw.line(screen, color, iPos, fPos, CROSS_WIDTH)
            return self.squares[1][1]

        # No win yet
        return 0

    def mark_square(self, row, col, player):
        self.squares[row][col] = player
        self.marked_squares += 1

    def empty_square(self, row, col):
        return self.squares[row][col] == 0

    def get_empty_squares(self):
        empty_squares = []
        for row in range(ROWS):
            for col in range(COLS):
                if self.empty_square(row, col):
                    empty_squares.append((row, col))

        return empty_squares

    def isfull(self):
        return self.marked_squares == 9

    def isempty(self):
        return self.marked_squares == 0


class AI:
    def __init__(self, level=1, player=2):
        self.level = level
        self.player = player

    # --- RANDOM ---
    def rnd(self, board):
        empty_squares = board.get_empty_squares()
        index = random.randrange(0, len(empty_squares))

        return empty_squares[index]  # row, col

    # --- MINIMAX ---
    def minimax(self, board, maximizing):

        # Terminal case
        case = board.final_state()

        # Player 1 wins
        if case == 1:
            return 1, None  # eval, move

        # Player 2 wins
        if case == 2:
            return -1, None

        # Tie/Draw
        elif board.isfull():
            return 0, None

        if maximizing:
            max_eval = -100
            best_move = None
            empty_squares = board.get_empty_squares()

            for row, col in empty_squares:
                temp_board = copy.deepcopy(board)
                temp_board.mark_square(row, col, 1)
                eval = self.minimax(temp_board, False)[0]
                if eval > max_eval:
                    max_eval = eval
                    best_move = (row, col)

            return max_eval, best_move

        elif not maximizing:
            min_eval = 100
            best_move = None
            empty_squares = board.get_empty_squares()

            for row, col in empty_squares:
                temp_board = copy.deepcopy(board)
                temp_board.mark_square(row, col, self.player)
                eval = self.minimax(temp_board, True)[0]
                if eval < min_eval:
                    min_eval = eval
                    best_move = (row, col)

            return min_eval, best_move

    # --- MAIN EVAL ---
    def eval(self, main_board):
        if self.level == 0:
            # Random choice
            eval = "random"
            move = self.rnd(main_board)
        else:
            # Minimax algorithm choice
            eval, move = self.minimax(main_board, False)

        print(f"AI has chosen to mark the square in pos {move} with an eval of: {eval}")

        return move  # row, col


class Game:
    def __init__(self):
        self.board = Board()
        self.ai = AI()
        self.player = 1  # 1-cross  #2-circles
        self.gamemode = "ai"  # AI or PVP
        self.running = True
        self.show_lines()

    # --- DRAW METHODS ---
    def show_lines(self):
        # BG
        screen.fill(BG_COLOR)

        # Vertical
        pygame.draw.line(screen, LINE_COLOR, (SQSIZE, 0), (SQSIZE, HEIGHT), LINE_WIDTH)
        pygame.draw.line(
            screen,
            LINE_COLOR,
            (WIDTH - SQSIZE, 0),
            (WIDTH - SQSIZE, HEIGHT),
            LINE_WIDTH,
        )

        # Horizontal
        pygame.draw.line(screen, LINE_COLOR, (0, SQSIZE), (WIDTH, SQSIZE), LINE_WIDTH)
        pygame.draw.line(
            screen,
            LINE_COLOR,
            (0, HEIGHT - SQSIZE),
            (WIDTH, HEIGHT - SQSIZE),
            LINE_WIDTH,
        )

    def draw_fig(self, row, col):
        if self.player == 1:
            # Draw Cross
            # Descending Line
            start_desc = (col * SQSIZE + OFFSET, row * SQSIZE + OFFSET)
            end_desc = (col * SQSIZE + SQSIZE - OFFSET, row * SQSIZE + SQSIZE - OFFSET)
            pygame.draw.line(screen, CROSS_COLOR, start_desc, end_desc, CROSS_WIDTH)
            # Ascending Line
            start_asc = (col * SQSIZE + OFFSET, row * SQSIZE + SQSIZE - OFFSET)
            end_asc = (col * SQSIZE + SQSIZE - OFFSET, row * SQSIZE + OFFSET)
            pygame.draw.line(screen, CROSS_COLOR, start_asc, end_asc, CROSS_WIDTH)
        elif self.player == 2:
            # Draw Circle
            center = (col * SQSIZE + SQSIZE // 2, row * SQSIZE + SQSIZE // 2)
            pygame.draw.circle(screen, CIRC_COLOR, center, RADIUS, CIRC_WIDTH)

    # --- OTHER METHODS ---
    def make_move(self, row, col):
        self.board.mark_square(row, col, self.player)
        self.draw_fig(row, col)
        self.next_turn()

    def next_turn(self):
        self.player = self.player % 2 + 1

    def change_gamemode(self):
        self.gamemode = "ai" if self.gamemode == "pvp" else "pvp"

    def isover(self):
        return self.board.final_state(show=True) != 0 or self.board.isfull()

    def reset(self):
        self.__init__()


def main():

    # Objects

    game = Game()
    board = game.board
    ai = game.ai

    # --- MAINLOOP ---

    while True:

        # Pygame events
        for event in pygame.event.get():

            # Quit event
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            # Keydown event
            if event.type == pygame.KEYDOWN:

                # Press g-game mode
                if event.key == pygame.K_g:
                    game.change_gamemode()

                # Press r-restart
                if event.key == pygame.K_r:
                    game.reset()
                    board = game.board
                    ai = game.ai

                # Press 0-random ai
                if event.key == pygame.K_0:
                    ai.level = 0

                # Press 1-random ai
                if event.key == pygame.K_1:
                    ai.level = 1

            # Click event
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = event.pos
                row = pos[1] // SQSIZE
                col = pos[0] // SQSIZE

                # Human mark sqr
                if board.empty_square(row, col) and game.running:
                    game.make_move(row, col)

                    if game.isover():
                        game.running = False

        # AI initial call
        if game.gamemode == "ai" and game.player == ai.player and game.running:

            # AUpdate the screen
            pygame.display.update()

            # AI methods
            row, col = ai.eval(board)
            game.make_move(row, col)

            if game.isover():
                game.running = False

        pygame.display.update()


main()
