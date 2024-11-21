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
    [[0, 1, 0], [1, 1, 1]],  # T-образная фигура
    [[1, 1, 1, 1]],  # Линия (I-образная фигура)
    [[1, 1], [1, 1]],  # Квадрат (O-образная фигура)
    [[1, 0, 0], [1, 1, 1]],  # L-образная фигура
    [[0, 0, 1], [1, 1, 1]],  # J-образная фигура
    [[1, 1, 0], [0, 1, 1]],  # Z-образная фигура
    [[0, 1, 1], [1, 1, 0]]   # S-образная фигура
]


# Инициализация экрана
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Tetris')

# Загрузка и воспроизведение музыки
pygame.mixer.music.load('korobeyniki.mp3')  # Замените на путь к вашему файлу музыки
pygame.mixer.music.set_volume(0.3)  # Установка громкости (от 0.0 до 1.0)
pygame.mixer.music.play(-1, 0.0)  # Повторение музыки бесконечно


# Основной класс игры
class Tetris:
    def __init__(self):
        self.current_color = None
        self.next_piece_color = None  # Цвет следующей фигуры
        self.board = [[0] * COLS for _ in range(ROWS)]
        self.game_over = False
        self.is_paused = False
        self.current_piece = None
        self.next_piece = None  # Следующая фигура
        self.current_pos = None
        self.score = 0
        self.last_move_time = time.time()
        self.fall_speed = 0.5  # начальная скорость падения (в секундах)
        self.fall_speed_fast = 0.05  # ускоренная скорость падения при зажатой стрелке вниз
        self.is_fast_falling = False  # флаг, отвечающий за ускоренное падение
        self.piece_history = []  # История использованных фигур


    @staticmethod
    def draw_pause_message():
        """Рисует сообщение о паузе на экране."""
        font = pygame.font.Font(None, 48)
        text = font.render("Paused", True, (0, 0, 255))
        text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
        screen.blit(text, text_rect)

    def new_piece(self):
        """Генерация текущей и следующей фигур."""
        if self.next_piece is None:
            self.next_piece = random.choice(SHAPES)
            self.next_piece_color = random.choice(COLOR_LIST)

        self.current_piece = self.next_piece
        self.current_color = self.next_piece_color

        # Генерируем следующую фигуру
        shape_type = random.choice([
            s for s in SHAPES
            if s not in [piece for piece in self.piece_history[-3:]]
        ])
        self.next_piece = shape_type
        self.next_piece_color = random.choice(COLOR_LIST)

        self.piece_history.append(shape_type)
        if len(self.piece_history) > 5:
            self.piece_history.pop(0)

        self.current_pos = [0, COLS // 2 - len(self.current_piece[0]) // 2]

    def draw_next_piece(self):
        """Отображение следующей фигуры с прозрачностью и выделением контуров."""
        font = pygame.font.Font(None, 36)
        text = font.render("Next:", True, (0, 0, 0))
        screen.blit(text, (10, 50))  # Позиция текста

        # Создаем поверхность с поддержкой альфа-канала
        transparent_surface = pygame.Surface(
            (len(self.next_piece[0]) * BLOCK_SIZE, len(self.next_piece) * BLOCK_SIZE), pygame.SRCALPHA
        )
        transparent_surface.set_alpha(128)  # Устанавливаем прозрачность (0-255)

        # Цвет для следующей фигуры
        gray = (128, 128, 128, 128)  # Серый цвет с альфа-каналом
        border_color = (0, 0, 0, 255)  # Черный цвет для контуров (полностью непрозрачный)

        for y, row in enumerate(self.next_piece):
            for x, cell in enumerate(row):
                if cell:
                    # Рисуем сам блок
                    pygame.draw.rect(
                        transparent_surface,
                        gray,
                        (x * BLOCK_SIZE, y * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE),
                        border_radius=5,
                    )
                    # Рисуем контур блока
                    pygame.draw.rect(
                        transparent_surface,
                        border_color,
                        (x * BLOCK_SIZE, y * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE),
                        width=2,  # Толщина линии
                        border_radius=5,
                    )

        # Отображаем прозрачную поверхность на экране
        screen.blit(transparent_surface, (10, 80))  # Позиция фигуры

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
        if 10 <= self.score < 20:
            self.fall_speed = 0.45
        elif 20 <= self.score < 30:
            self.fall_speed = 0.4
        elif 30 <= self.score < 40:
            self.fall_speed = 0.35
        elif 40 <= self.score < 50:
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

    @staticmethod
    def draw_grid():
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

    @staticmethod
    def draw_game_over():
        font = pygame.font.Font(None, 48)
        text = font.render("Game Over", True, (255, 0, 0))
        text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 4))
        screen.blit(text, text_rect)

        # Кнопка перезапуска
        restart_button = pygame.Rect(SCREEN_WIDTH // 4, SCREEN_HEIGHT // 2, SCREEN_WIDTH // 2, 50)
        pygame.draw.rect(screen, (0, 0, 255), restart_button, border_radius=15)

        # Текст на кнопке
        restart_text = font.render("Restart", True, WHITE)
        screen.blit(restart_text, (restart_button.x + (restart_button.width - restart_text.get_width()) // 2,
                                   restart_button.y + (restart_button.height - restart_text.get_height()) // 2))

        return restart_button


# Главная функция
def main():
    game = Tetris()
    game.new_piece()

    clock = pygame.time.Clock()
    volume = 0.3  # Начальный уровень громкости
    volume_display_time = 0  # Таймер отображения уровня громкости

    def draw_volume_level():
        """Отображает текущий уровень громкости."""
        font = pygame.font.Font(None, 36)
        volume_text = font.render(f"Volume: {int(volume * 100)}%", True, (0, 0, 0))
        volume_rect = volume_text.get_rect(topright=(SCREEN_WIDTH - 10, 10))
        screen.blit(volume_text, volume_rect)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    game.is_paused = not game.is_paused  # Переключение паузы
                elif not game.is_paused:  # Обработка клавиш только если игра не на паузе
                    if event.key == pygame.K_LEFT:
                        game.move_piece(-1, 0)
                    elif event.key == pygame.K_RIGHT:
                        game.move_piece(1, 0)
                    elif event.key == pygame.K_DOWN:
                        game.is_fast_falling = True
                    elif event.key == pygame.K_UP:
                        game.rotate_piece()
                if event.key == pygame.K_PLUS or event.key == pygame.K_KP_PLUS:  # Увеличение громкости
                    volume = min(1.0, volume + 0.1)  # Максимум 1.0
                    pygame.mixer.music.set_volume(volume)
                    volume_display_time = pygame.time.get_ticks()  # Устанавливаем время для отображения
                elif event.key == pygame.K_MINUS or event.key == pygame.K_KP_MINUS:  # Уменьшение громкости
                    volume = max(0.0, volume - 0.1)  # Минимум 0.0
                    pygame.mixer.music.set_volume(volume)
                    volume_display_time = pygame.time.get_ticks()  # Устанавливаем время для отображения
            elif event.type == pygame.KEYUP and not game.is_paused:
                if event.key == pygame.K_DOWN:
                    game.is_fast_falling = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if game.game_over:
                    mouse_pos = pygame.mouse.get_pos()
                    restart_button = game.draw_game_over()
                    if restart_button.collidepoint(mouse_pos):
                        game.__init__()
                        game.new_piece()

        if not game.is_paused and not game.game_over:
            game.auto_fall()
            game.check_game_over()

        game.draw_board()
        game.draw_score()
        game.draw_next_piece()  # Рисуем следующую фигуру

        # Отображение уровня громкости в течение 1 секунды
        if pygame.time.get_ticks() - volume_display_time <= 1000:
            draw_volume_level()

        if game.game_over:
            game.draw_game_over()

        if game.is_paused and not game.game_over:
            game.draw_pause_message()

        pygame.display.update()
        clock.tick(30)




if __name__ == "__main__":
    main()