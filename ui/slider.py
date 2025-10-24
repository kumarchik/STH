import pygame # Імпорт бібліотеки Pygame

class Slider: # Визначення класу Slider
    # Метод-конструктор класу, що викликається при створенні нового слайдера
    def __init__(self, x, y, width, min_val, max_val, step=1, initial=None, label="", value_to_text=None):
        # Створення прямокутника для "доріжки" слайдера (x, y, ширина, висота)
        self.track_rect = pygame.Rect(x, y, width, 6) 
        self.handle_radius = 10 # Радіус круглої ручки (повзунка) слайдера
        
        # Встановлення мінімального, максимального та крокового значень, приведених до типу float
        self.min = float(min_val)
        self.max = float(max_val)
        self.step = float(step)
        
        # Встановлення початкового значення. Якщо 'initial' не задано, використовується 'min_val'
        if initial is not None:
            self.value = float(initial)
        else:
            self.value = float(min_val)
            
        self.label = label # Текст підпису, що відображається над слайдером
        self.value_to_text = value_to_text # Функція для форматування поточного значення у рядок (наприклад, для відображення "%")
        self.dragging = False # Прапор, який вказує, чи перетягує користувач ручку слайдера
        
        # Прямокутник для визначення області кліку навколо ручки (трохи більший за саму ручку для зручності)
        self._hit_rect = pygame.Rect(0, 0, self.handle_radius * 2 + 8, self.handle_radius * 2 + 8)

    # Метод для встановлення функції зворотного виклику (callback), яка спрацює при зміні значення
    def set_on_change(self, cb):
        self.on_change = cb

    # Приватний метод для обмеження (клампінгу) значення v в межах [min, max] та округлення до кроку
    def _clamp(self, v: float) -> float:
        # Обмеження значення v між self.min і self.max
        v = max(self.min, min(self.max, v))
        
        # Округлення значення до найближчого кратного кроку, якщо крок > 0
        if self.step > 0:
            v = round(v / self.step) * self.step
            
        # Повторне обмеження на випадок похибок округлення
        return max(self.min, min(self.max, v))

    # Приватний метод для перетворення позиції X (координати пікселя) на значення слайдера (float)
    def _pos_to_val(self, px: int) -> float:
        # Обчислення співвідношення позиції ручки відносно ширини доріжки (від 0 до 1)
        ratio = (px - self.track_rect.left) / self.track_rect.width
        # Перетворення співвідношення на значення в діапазоні [min, max] і застосування _clamp
        return self._clamp(self.min + ratio * (self.max - self.min))

    # Приватний метод для перетворення поточного значення слайдера (float) на позицію X (координату пікселя)
    def _val_to_pos(self) -> int:
        # Якщо min == max, ручка завжди на лівому краю
        if self.max == self.min:
            return self.track_rect.left
        # Обчислення співвідношення поточного значення в діапазоні [min, max] (від 0 до 1)
        ratio = (self.value - self.min) / (self.max - self.min)
        # Перетворення співвідношення на координату X на доріжці
        return int(self.track_rect.left + ratio * self.track_rect.width)

    # Метод для малювання (відображення) слайдера на екрані
    def draw(self, screen, font=None):
        # Малювання "доріжки" слайдера (світло-сірий прямокутник)
        pygame.draw.rect(screen, (210, 210, 210), self.track_rect, border_radius=3)
        # Малювання контуру "доріжки" (темно-сірий прямокутник, товщина 1)
        pygame.draw.rect(screen, (60, 60, 60), self.track_rect, 1, border_radius=3)

        # Обчислення позиції ручки
        hx = self._val_to_pos() # Координата X ручки
        hy = self.track_rect.centery # Координата Y ручки (центр доріжки)
        # Малювання круглої ручки (темно-сіре коло)
        pygame.draw.circle(screen, (40, 40, 40), (hx, hy), self.handle_radius)

        # Відображення підпису (label) та поточного значення
        if font and self.label:
            # Використання функції value_to_text, якщо вона надана
            if callable(self.value_to_text):
                vtxt = self.value_to_text(self.value)
            # Інакше просто форматування в ціле число
            else:
                vtxt = f"{int(self.value)}"
            # Рендеринг тексту: "Підпис: Значення"
            text = font.render(f"{self.label}: {vtxt}", True, (0, 0, 0))
            # Відображення тексту над доріжкою
            screen.blit(text, (self.track_rect.left, self.track_rect.top - 28))

        # Оновлення прямокутника області кліку, щоб він був центрований на ручці
        self._hit_rect.center = (hx, hy)

    # Метод для обробки подій Pygame (взаємодія користувача)
    def handle_event(self, event):
        old = self.value # Зберігаємо старе значення для перевірки, чи відбулася зміна
        
        # Обробка натискання кнопки миші
        if event.type == pygame.MOUSEBUTTONDOWN:
            # Перевірка, чи клікнули по доріжці або по ручці
            if self.track_rect.collidepoint(event.pos) or self._hit_rect.collidepoint(event.pos):
                self.dragging = True # Початок перетягування
                # Оновлення значення відповідно до позиції кліку
                self.value = self._pos_to_val(event.pos[0])
                
        # Обробка руху миші під час перетягування
        elif event.type == pygame.MOUSEMOTION and self.dragging:
            # Оновлення значення відповідно до поточної позиції миші
            self.value = self._pos_to_val(event.pos[0])
            
        # Обробка відпускання кнопки миші
        elif event.type == pygame.MOUSEBUTTONUP and self.dragging:
            self.dragging = False # Завершення перетягування
            # Фінальне оновлення значення на випадок, якщо відпустили кнопку поза подією MOUSEMOTION
            self.value = self._pos_to_val(event.pos[0])

        # Перевірка, чи змінилося значення, і чи встановлена функція зворотного виклику on_change
        if self.value != old and hasattr(self, "on_change") and self.on_change:
            self.on_change(self.value) # Виклик функції on_change з новим значенням