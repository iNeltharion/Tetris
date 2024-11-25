```markdown
# Tetris Game

Классическая игра **Тетрис**, написанная на Python с использованием библиотеки `pygame`.  
В игре предусмотрены следующие особенности:
- Классические фигуры и оформление.
- Ускорение падения фигур каждые 10 очков.
- Музыкальное сопровождение ("Коробейники").
- Всплывающее сообщение *Game Over* с кнопкой перезапуска.
```
---

## 🛠️ Требования

Для запуска игры вам потребуется:
- Python версии **3.10** или выше.
- Библиотека `pygame` версии **2.6.1** или выше.

---

## 📥 Установка

1. **Склонируйте репозиторий** или скачайте архив с проектом:
   ```bash
   git clone https://github.com/iNeltharion/Tetris.git
   cd Tetris
   ```

2. **Установите зависимости**:
   ```bash
   python -m venv venv
   ```
   ```bash   
   .venv\Scripts\activate
   ```
   ```bash	
   pip install pygame
   ```

3. **Скачайте файл музыки**:  
   Поместите файл с музыкой `korobeyniki.mp3` (или другой выбранный вами трек) в папку проекта.  

---

## 🚀 Запуск игры

1. Откройте терминал в папке проекта.  
2. Запустите игру с помощью команды:
   ```bash
   python Tetris.py
   ```

---

## 🎮 Управление

- **⬅️ Влево** – перемещение фигуры влево.
- **➡️ Вправо** – перемещение фигуры вправо.
- **⬇️ Вниз** – ускоренное падение фигуры.
- **⬆️ Вверх** – поворот фигуры.
- **⏸️ Пауза** – ставит игру на паузу или возобновляет её.
- **➖ Уменьшить громкость** – уменьшить уровень громкости.
- **➕ Увеличить громкость** – увеличить уровень громкости.

---

## 💡 Особенности

- **Музыка:** Музыкальное сопровождение играет в фоновом режиме. Вы можете изменить файл музыки, заменив `korobeyniki.mp3` на свой трек.
- **Ускорение:** Каждые 10 очков скорость падения фигур увеличивается.
- **Перезапуск:** При проигрыше появляется кнопка *Restart*, позволяющая начать игру заново.
- **Сообщение "Game Over":** Центрируется на экране при проигрыше.

---

## 🐞 Отладка

Если возникают ошибки:
1. Убедитесь, что Python установлен и работает корректно.
2. Проверьте наличие файла `korobeyniki.mp3` в папке с проектом.
3. Убедитесь, что библиотека `pygame` установлена.

Для отладки можно использовать:
```bash
   python --version
   pip list | grep pygame
```