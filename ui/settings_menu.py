import pygame # Імпорт бібліотеки Pygame для розробки ігор та мультимедіа
from buttons import Button # Імпорт класу Button з локального модуля buttons
from ui.slider import Slider # Імпорт класу Slider з локального модуля ui.slider


class SettingsMenu: # Визначення класу SettingsMenu, який представляє меню налаштувань
    # Метод-конструктор класу, що викликається при створенні об'єкта
    def __init__(self, screen_rect, initial_volume, initial_keys, min_keys, max_keys, on_change, on_back):
        self.screen_rect = screen_rect # Зберігання прямокутника екрана для позиціонування елементів
        self.on_change = on_change # Функція зворотного виклику, яка викликається при зміні налаштувань (гучності або кількості клавіш)
        self.on_back = on_back # Функція зворотного виклику, яка викликається при натисканні кнопки "Назад"

        cx = screen_rect.centerx # Координата X центру екрана
        top = 140 # Початкова координата Y для першого елемента інтерфейсу

        # Завантаження та масштабування зображень для кнопки "Назад" (неактивний/звичайний стан)
        back_idle = pygame.transform.scale(
            pygame.image.load('assets/images/buttons/exit_unhover.png'), (48, 48)
        )
        # Завантаження та масштабування зображень для кнопки "Назад" (стан при наведенні курсору)
        back_hover = pygame.transform.scale(
            pygame.image.load('assets/images/buttons/exit_hover.png'), (48, 48)
        )

        # Створення об'єкта кнопки "Назад"
        self.back_btn = Button(
            40, 30, 48, 48, # Позиція (x, y) та розміри (ширина, висота)
            "", # Текст кнопки (порожній, оскільки використовується зображення)
            self._back, # Функція, яка викликається при натисканні кнопки
            img_idle=back_idle, # Зображення для неактивного стану
            img_hover=back_hover # Зображення для стану при наведенні
        )

        # Локальна функція для форматування значення гучності у відсотках
        def volume_to_text(v):
            return f"{int(v * 100)}%"

        # Створення об'єкта слайдера для налаштування гучності
        self.volume_slider = Slider(
            cx - 200, top, 400, # Позиція (x, y) та ширина
            0.0, 1.0, step=0.01, initial=initial_volume, # Мінімальне, максимальне значення, крок та початкове значення
            label="Гучність", # Текст підпису слайдера
            value_to_text = volume_to_text # Функція для відображення поточного значення
        )
        # Встановлення функції зворотного виклику, яка викликається при зміні значення гучності
        self.volume_slider.set_on_change(self._on_volume)

        # Локальна функція для форматування значення кількості клавіш (просто перетворення в ціле число і рядок)
        def keys_to_text(v):
            return str(int(v))

        # Створення об'єкта слайдера для налаштування кількості клавіш
        self.keys_slider = Slider(
            cx - 200, top + 120, 400, # Позиція (зміщення вниз від попереднього слайдера) та ширина
            min_keys, max_keys, step=1, initial=initial_keys, # Мінімальне, максимальне значення, крок та початкове значення
            label="Кількість клавіш", # Текст підпису слайдера
            value_to_text = keys_to_text # Функція для відображення поточного значення
        )
        # Встановлення функції зворотного виклику, яка викликається при зміні кількості клавіш
        self.keys_slider.set_on_change(self._on_keys)

    # Приватний метод, що викликається при зміні значення гучності
    def _on_volume(self, v):
        if self.on_change: # Перевірка, чи встановлена функція on_change
            # Виклик on_change, передаючи нову гучність (v) та поточне значення кількості клавіш
            self.on_change(float(v), int(self.keys_slider.value))

    # Приватний метод, що викликається при зміні значення кількості клавіш
    def _on_keys(self, v):
        if self.on_change: # Перевірка, чи встановлена функція on_change
            # Виклик on_change, передаючи поточне значення гучності та нову кількість клавіш (v)
            self.on_change(float(self.volume_slider.value), int(v))

    # Приватний метод, що викликається при натисканні кнопки "Назад"
    def _back(self):
        if self.on_back: # Перевірка, чи встановлена функція on_back
            self.on_back() # Виклик функції on_back

    # Метод для малювання (відображення) меню налаштувань на екрані
    def draw(self, screen, font):
        # Рендеринг заголовка меню
        title = font.render("Налаштування", True, (0, 0, 0)) # Створення поверхні з текстом
        # Відображення заголовка по центру екрана
        screen.blit(title, title.get_rect(center=(self.screen_rect.centerx, 80)))

        # Малювання кнопки "Назад"
        self.back_btn.draw(screen, font)
        # Малювання слайдера гучності
        self.volume_slider.draw(screen, font)
        # Малювання слайдера кількості клавіш
        self.keys_slider.draw(screen, font)

    # Метод для обробки подій Pygame (наприклад, кліки миші)
    def handle_event(self, event):
        # Передача події на обробку кнопці "Назад"
        self.back_btn.handle_event(event)
        # Передача події на обробку слайдеру гучності
        self.volume_slider.handle_event(event)
        # Передача події на обробку слайдеру кількості клавіш
        self.keys_slider.handle_event(event)