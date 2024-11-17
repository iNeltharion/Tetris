import pygame
import random
import time

# Инициализация pygame
pygame.init()

# Размеры экрана и блоков
SCREEN_WIDTH = 300
SCREEN_HEIGHT = 600
BLOCK_SIZE = 30
COLS = SCREEN_WIDTH // BLOCK_SIZE
ROWS = SCREEN_HEIGHT // BLOCK_SIZE

# Цвета
WHITE = (255, 255, 255)
LIGHT_BLUE = (103, 191, 250)
SOFT_ORANGE = (255, 150, 56)
PALE_YELLOW = (255, 221, 51)
SOFT_GREEN = (116, 194, 89)
DEEP_RED = (209, 58, 58)
SOFT_PURPLE = (151, 74, 180)
COLOR_LIST = [LIGHT_BLUE, SOFT_ORANGE, PALE_YELLOW, SOFT_GREEN, DEEP_RED, SOFT_PURPLE]
GRID_COLOR = (220, 220, 220)  # Мягкий серый цвет для сетки
GRID_LINE_WIDTH = 2  # Толщина линии сетки

# Фигуры (классический вид)
SHAPES = [
    [[1, 1, 1], [0, 1, 0]],  # T-образная
    [[1, 1, 1, 1]],  # Линия
    [[1, 1], [1, 1]],  # Квадрат
    [[1, 0, 0], [1, 1, 1]],  # L-образная
    [[0, 0, 1], [1, 1, 1]],  # Z-образная
    [[0, 0, 1], [1, 1, 1]],  # S-образная
    [[1, 0], [1, 0], [1, 1]]  # J-образная
]

# Инициализация экрана
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Tetris')


# Основной класс игры
class Tetris:
    def __init__(self):
        self.board = [[0] * COLS for _ in range(ROWS)]
        self.game_over = False
        self.current_piece = None
        self.current_pos = None
        self.score = 0
        self.last_move_time = time.time()
        self.fall_speed = 0.5  # начальная скорость падения (в секундах)
        self.fall_speed_fast = 0.05  # ускоренная скорость падения при зажатой стрелке вниз
        self.is_fast_falling = False  # флаг, отвечающий за ускоренное падение
        self.piece_history = []  # История использованных фигур

    def new_piece(self):
        # Генерация новой фигуры, которая не повторяется сразу после предыдущей
        shape = random.choice([s for s in SHAPES if s not in self.piece_history[-3:]])  # Избегаем повторений
        self.piece_history.append(shape)
        if len(self.piece_history) > 5:
            self.piece_history.pop(0)

        color = random.choice(COLOR_LIST)
        self.current_piece = shape
        self.current_color = color
        self.current_pos = [0, COLS // 2 - len(self.current_piece[0]) // 2]

    def rotate_piece(self):
        rotated_piece = [list(row) for row in zip(*self.current_piece[::-1])]  # Поворот фигуры
        if self.is_valid_position(rotated_piece, self.current_pos[0], self.current_pos[1]):
            self.current_piece = rotated_piece  # Выполняем поворот, если позиция валидна

    def is_valid_position(self, piece, new_y, new_x):
        """Проверка, можно ли поместить фигуру в указанное место."""
        for y, row in enumerate(piece):
            for x, cell in enumerate(row):
                if cell:
                    nx, ny = new_x + x, new_y + y
                    if nx < 0 or nx >= COLS or ny >= ROWS or self.board[ny][nx]:
                        return False
        return True

    def valid_move(self):
        for y, row in enumerate(self.current_piece):
            for x, cell in enumerate(row):
                if cell:
                    nx, ny = self.current_pos[1] + x, self.current_pos[0] + y
                    # Проверка на выход за границы по бокам и вниз
                    if nx < 0 or nx >= COLS or ny >= ROWS or self.board[ny][nx]:
                        return False
        return True

    def fix_piece(self):
        for y, row in enumerate(self.current_piece):
            for x, cell in enumerate(row):
                if cell:
                    nx, ny = self.current_pos[1] + x, self.current_pos[0] + y
                    if ny < 0:  # Защита от выхода за верхнюю границу
                        continue
                    self.board[ny][nx] = self.current_color
        self.clear_lines()
        self.new_piece()

    def clear_lines(self):
        full_lines = [i for i, row in enumerate(self.board) if all(cell != 0 for cell in row)]
        for i in full_lines:
            del self.board[i]
            self.board.insert(0, [0] * COLS)
        self.score += len(full_lines)

    def move_piece(self, dx, dy):
        self.current_pos[0] += dy
        self.current_pos[1] += dx
        if not self.valid_move():
            self.current_pos[0] -= dy
            self.current_pos[1] -= dx
            if dy > 0:
                self.fix_piece()

    def auto_fall(self):
        # Увеличиваем скорость падения каждые 10 очков
        if self.score >= 10 and self.score < 20:
            self.fall_speed = 0.45
        elif self.score >= 20 and self.score < 30:
            self.fall_speed = 0.4
        elif self.score >= 30 and self.score < 40:
            self.fall_speed = 0.35
        elif self.score >= 40 and self.score < 50:
            self.fall_speed = 0.3
        elif self.score >= 50:
            self.fall_speed = 0.25

        if self.is_fast_falling:
            fall_speed = self.fall_speed_fast
        else:
            fall_speed = self.fall_speed

        if time.time() - self.last_move_time >= fall_speed:
            self.move_piece(0, 1)
            self.last_move_time = time.time()

    def draw_grid(self):
        # Рисуем вертикальные линии
        for x in range(0, SCREEN_WIDTH, BLOCK_SIZE):
            pygame.draw.line(screen, GRID_COLOR, (x, 0), (x, SCREEN_HEIGHT), GRID_LINE_WIDTH)

        # Рисуем горизонтальные линии
        for y in range(0, SCREEN_HEIGHT, BLOCK_SIZE):
            pygame.draw.line(screen, GRID_COLOR, (0, y), (SCREEN_WIDTH, y), GRID_LINE_WIDTH)

    def draw_board(self):
        screen.fill(WHITE)
        # Рисуем игровую сетку
        self.draw_grid()

        # Рисуем блоки на поле
        for y, row in enumerate(self.board):
            for x, cell in enumerate(row):
                if cell:
                    pygame.draw.rect(screen, cell, (x * BLOCK_SIZE, y * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE),
                                     border_radius=5)

        # Рисуем текущую фигуру
        for y, row in enumerate(self.current_piece):
            for x, cell in enumerate(row):
                if cell:
                    pygame.draw.rect(screen, self.current_color, ((self.current_pos[1] + x) * BLOCK_SIZE,
                                                                  (self.current_pos[0] + y) * BLOCK_SIZE,
                                                                  BLOCK_SIZE, BLOCK_SIZE), border_radius=5)

    def draw_score(self):
        font = pygame.font.Font(None, 36)
        text = font.render(f"Score: {self.score}", True, (0, 0, 0))
        screen.blit(text, (10, 10))

    def check_game_over(self):
        # Если верхняя строка заполнена, игра заканчивается
        if any(self.board[0][x] != 0 for x in range(COLS)):
            self.game_over = True

    def draw_game_over(self):
        font = pygame.font.Font(None, 72)
        text = font.render("Game Over", True, (255, 0, 0))
        text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 3))
        screen.blit(text, text_rect)

        # Кнопка "Restart" с красивым оформлением
        button_width, button_height = 200, 50
        restart_button = pygame.Rect((SCREEN_WIDTH - button_width) // 2, SCREEN_HEIGHT // 2 + 50, button_width,
                                     button_height)
        pygame.draw.rect(screen, (30, 144, 255), restart_button, border_radius=15)  # Синий фон с закругленными углами

        # Эффект при наведении
        mouse_pos = pygame.mouse.get_pos()
        if restart_button.collidepoint(mouse_pos):
            pygame.draw.rect(screen, (70, 130, 180), restart_button, border_radius=15)

        restart_text = font.render("Restart", True, WHITE)
        screen.blit(restart_text, (restart_button.x + (button_width - restart_text.get_width()) // 2,
                                   restart_button.y + (button_height - restart_text.get_height()) // 2))

        return restart_button


# Главная функция
def main():
    game = Tetris()
    game.new_piece()

    clock = pygame.time.Clock()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    game.move_piece(-1, 0)
                elif event.key == pygame.K_RIGHT:
                    game.move_piece(1, 0)
                elif event.key == pygame.K_DOWN:
                    game.is_fast_falling = True
                elif event.key == pygame.K_UP:
                    game.rotate_piece()
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_DOWN:
                    game.is_fast_falling = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if game.game_over:
                    mouse_pos = pygame.mouse.get_pos()
                    restart_button = game.draw_game_over()
                    if restart_button.collidepoint(mouse_pos):
                        game.__init__()
                        game.new_piece()

        if not game.game_over:
            game.auto_fall()
            game.check_game_over()

        game.draw_board()
        game.draw_score()

        if game.game_over:
            game.draw_game_over()

        pygame.display.update()
        clock.tick(30)


if __name__ == "__main__":
    main()
