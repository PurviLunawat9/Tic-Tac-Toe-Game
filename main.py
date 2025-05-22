import pygame as pg
import sys
from random import randint

# Constants
WIN_SIZE = 700
CELL_SIZE = WIN_SIZE // 3
INF = float('inf')
vec2 = pg.math.Vector2
CELL_CENTER = vec2(CELL_SIZE / 2)
TURN_TIME_LIMIT = 10  # seconds

class TicTacToe:
    def __init__(self, game):
        self.game = game
        self.field_image = self.get_scaled_image("H://purvi//py game//board.jpg", [WIN_SIZE] * 2)

        # Resize X and O to 80% of cell size
        xo_size = int(CELL_SIZE * 0.8)
        self.O_image = self.get_scaled_image("H://purvi//py game//o.png", [xo_size] * 2)
        self.X_image = self.get_scaled_image("H://purvi//py game//x.png", [xo_size] * 2)

        # Resize and center reset button
        self.reset_button_img = self.get_scaled_image("H://purvi//py game//reset.png", [200, 200])
        self.reset_button_rect = self.reset_button_img.get_rect(center=(WIN_SIZE // 2, WIN_SIZE * 3 // 4))

        self.game_array = [[INF, INF, INF],
                           [INF, INF, INF],
                           [INF, INF, INF]]
        self.player = randint(0, 1)
        self.line_indices_array = [
            [(0, 0), (0, 1), (0, 2)],
            [(1, 0), (1, 1), (1, 2)],
            [(2, 0), (2, 1), (2, 2)],
            [(0, 0), (1, 0), (2, 0)],
            [(0, 1), (1, 1), (2, 1)],
            [(0, 2), (1, 2), (2, 2)],
            [(0, 0), (1, 1), (2, 2)],
            [(0, 2), (1, 1), (2, 0)]
        ]
        self.winner = None
        self.winner_line = None
        self.game_steps = 0
        self.font = pg.font.SysFont('Verdana', CELL_SIZE // 4, True)

        # Timer
        self.turn_timer = TURN_TIME_LIMIT
        self.last_time = pg.time.get_ticks()

    def check_winner(self):
        for line_indices in self.line_indices_array:
            sum_line = sum([self.game_array[i][j] for i, j in line_indices])
            if sum_line in {0, 3}:
                self.winner = 'XO'[sum_line == 0]
                self.winner_line = [vec2(line_indices[0][::-1]) * CELL_SIZE + CELL_CENTER,
                                    vec2(line_indices[2][::-1]) * CELL_SIZE + CELL_CENTER]

    def run_game_process(self):
        current_cell = vec2(pg.mouse.get_pos())
        col, row = map(int, current_cell // CELL_SIZE)
        left_click = pg.mouse.get_pressed()[0]

        # Cursor hover effect for reset button
        if self.winner or self.game_steps == 9:
            if self.reset_button_rect.collidepoint(pg.mouse.get_pos()):
                pg.mouse.set_cursor(pg.SYSTEM_CURSOR_HAND)
            else:
                pg.mouse.set_cursor(pg.SYSTEM_CURSOR_ARROW)
        else:
            pg.mouse.set_cursor(pg.SYSTEM_CURSOR_ARROW)

        # Handle reset button click
        if (self.winner or self.game_steps == 9) and left_click:
            if self.reset_button_rect.collidepoint(pg.mouse.get_pos()):
                self.game.new_game()
                return

        # Handle player move
        if 0 <= row < 3 and 0 <= col < 3 and left_click and self.game_array[row][col] == INF and not self.winner:
            self.game_array[row][col] = self.player
            self.player = not self.player
            self.game_steps += 1
            self.check_winner()
            self.turn_timer = TURN_TIME_LIMIT  # Reset timer
            self.last_time = pg.time.get_ticks()

    def draw_objects(self):
        for y, row in enumerate(self.game_array):
            for x, obj in enumerate(row):
                if obj != INF:
                    img = self.X_image if obj else self.O_image
                    rect = img.get_rect(center=((x + 0.5) * CELL_SIZE, (y + 0.5) * CELL_SIZE))
                    self.game.screen.blit(img, rect)

    def draw_winner(self):
        if self.winner:
            pg.draw.line(self.game.screen, 'red', *self.winner_line, CELL_SIZE // 8)
            label = self.font.render(f'Player "{self.winner}" wins!', True, 'white', 'black')
            self.game.screen.blit(label, (WIN_SIZE // 2 - label.get_width() // 2, WIN_SIZE // 4))
            self.game.screen.blit(self.reset_button_img, self.reset_button_rect)
        elif self.game_steps == 9:
            label = self.font.render('Game Draw!', True, 'white', 'black')
            self.game.screen.blit(label, (WIN_SIZE // 2 - label.get_width() // 2, WIN_SIZE // 4))
            self.game.screen.blit(self.reset_button_img, self.reset_button_rect)

    def draw_timer(self):
        # Countdown timer logic
        current_time = pg.time.get_ticks()
        elapsed = (current_time - self.last_time) / 1000
        if not self.winner and self.game_steps < 9:
            self.turn_timer -= elapsed
            if self.turn_timer <= 0:
                self.turn_timer = TURN_TIME_LIMIT
                self.player = not self.player
            self.last_time = current_time

            timer_label = self.font.render(f"Time Left: {int(self.turn_timer)}s", True, 'yellow')
            self.game.screen.blit(timer_label, (10, 10))

    def draw(self):
        self.game.screen.blit(self.field_image, (0, 0))
        self.draw_objects()
        self.draw_timer()
        self.draw_winner()

    @staticmethod
    def get_scaled_image(path, res):
        img = pg.image.load(path)
        return pg.transform.smoothscale(img, res)

    def print_caption(self):
        pg.display.set_caption(f'Player "{"OX"[self.player]}" turn!')
        if self.winner:
            pg.display.set_caption(f'Player "{self.winner}" wins! Press Reset to Restart')
        elif self.game_steps == 9:
            pg.display.set_caption('Game Draw! Press Reset to Restart')

    def run(self):
        self.print_caption()
        self.draw()
        self.run_game_process()

class Game:
    def __init__(self):
        pg.init()
        self.screen = pg.display.set_mode([WIN_SIZE] * 2)
        self.clock = pg.time.Clock()
        self.tictactoe = TicTacToe(self)

    def new_game(self):
        self.tictactoe = TicTacToe(self)

    def check_events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()
            if event.type == pg.KEYDOWN and event.key == pg.K_SPACE:
                self.new_game()

    def run(self):
        while True:
            self.check_events()
            self.tictactoe.run()
            pg.display.update()
            self.clock.tick(60)

if __name__ == "__main__":
    game = Game()
    game.run()
