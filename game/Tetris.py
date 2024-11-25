import pygame

from game.System.Class_tetris import Tetris, SCREEN_WIDTH, screen

# Загрузка и воспроизведение музыки
try:
    pygame.mixer.music.load('korobeyniki.mp3')
    pygame.mixer.music.set_volume(0.3)
    pygame.mixer.music.play(-1, 0.0)
except pygame.error as e:
    print(f"Ошибка загрузки музыки: {e}")


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
        # --- Обработка событий ---
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return

            # Обработка нажатий клавиш
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    game.is_paused = not game.is_paused
                elif not game.is_paused:  # Действия только если игра активна
                    if event.key == pygame.K_LEFT:
                        game.move_piece(-1, 0)
                    elif event.key == pygame.K_RIGHT:
                        game.move_piece(1, 0)
                    elif event.key == pygame.K_DOWN:
                        game.is_fast_falling = True
                    elif event.key == pygame.K_UP:
                        game.rotate_piece()
                    elif event.key in (pygame.K_PLUS, pygame.K_KP_PLUS):
                        volume = min(1.0, volume + 0.1)
                        pygame.mixer.music.set_volume(volume)
                        volume_display_time = pygame.time.get_ticks()
                    elif event.key in (pygame.K_MINUS, pygame.K_KP_MINUS):
                        volume = max(0.0, volume - 0.1)
                        pygame.mixer.music.set_volume(volume)
                        volume_display_time = pygame.time.get_ticks()

            # Обработка отпускания клавиш
            if event.type == pygame.KEYUP and not game.is_paused:
                if event.key == pygame.K_DOWN:
                    game.is_fast_falling = False

            # Обработка нажатия мыши
            if event.type == pygame.MOUSEBUTTONDOWN and game.game_over:
                mouse_pos = pygame.mouse.get_pos()
                restart_button = game.draw_game_over()
                if restart_button.collidepoint(mouse_pos):
                    game.__init__()
                    game.new_piece()

        # --- Обновление состояния игры ---
        if not game.is_paused and not game.game_over:
            game.auto_fall()

        # --- Отрисовка игрового поля ---
        game.draw_board()
        game.draw_score()
        game.draw_next_piece()

        # Отображение уровня громкости
        if pygame.time.get_ticks() - volume_display_time <= 1000:
            draw_volume_level()

        # Отображение сообщений (Game Over, Pause)
        if game.game_over:
            game.draw_game_over()
        if game.is_paused and not game.game_over:
            game.draw_pause_message()

        # --- Обновление экрана ---
        pygame.display.update()
        clock.tick(30)


if __name__ == "__main__":
    main()