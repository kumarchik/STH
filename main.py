from pygame import *
# Пояснення: Імпортуємо ВСІ класи та функції з основного модуля pygame (*).
from settings import *
# Пояснення: Імпортуємо всі константи (наприклад, WINDOW_WIDTH, WHITE, KEYS) з файлу налаштувань.
from sounds import load_sounds
# Пояснення: Функція для завантаження всіх звукових файлів.
from keys import draw_keys, create_key_rects
# Пояснення: Функції для малювання піаніно та створення його прямокутних областей.
from buttons import Button
# Пояснення: Клас для створення інтерактивних кнопок.

# =================== ЗМІНА 1: +МЕНЮ НАЛАШТУВАНЬ ===================
from ui.settings_menu import SettingsMenu  # Тепер кнопка "Settings" працює!
# Пояснення: Імпортуємо клас, який реалізує інтерфейс меню налаштувань (слайдери, кнопки).

# =================== ЗМІНА 2: ШВИДШИЙ СТАРТ ===================
mixer.init()  # Тільки звук (швидше, ніж init())
# Пояснення: Ініціалізуємо лише звуковий модуль (mixer), що прискорює запуск програми.
display.set_caption("Piano Game")
# Пояснення: Встановлюємо заголовок вікна.
font.init()   # Тільки шрифти (незалежно від звуку)
# Пояснення: Ініціалізуємо лише модуль шрифтів.

# =================== ЗМІНА 3: ЗВУК ДО ЕКРАНУ ===================
sounds = load_sounds(KEYS)  # Завантажуємо ПЕРЕД екраном (без затримок)
# Пояснення: Завантажуємо звуки всіх нот, визначених у константі KEYS. Це робиться до створення екрана.
my_font = font.SysFont("Arial", 24)
# Пояснення: Створюємо системний об'єкт шрифту для використання в тексті (наприклад, на кнопках).
pressed_keys = set()
# Пояснення: Множина, що зберігає індекси (0, 1, 2, ...) **активних** клавіш піаніно, які натиснуті в даний момент.

# =================== ЗМІНА 4: 2 РЕЖИМИ ЕКРАНУ ===================
screen_mode = "main"          # "main" = піаніно, "settings" = меню
# Пояснення: Змінна, що визначає, який інтерфейс зараз відображається.
settings_menu = None          # None = меню закрите
# Пояснення: Об'єкт класу SettingsMenu. При "main" він None; при "settings" – об'єкт.

# =================== ЗМІНА 5: СЛАЙДЕР ГУЧНОСТІ ===================
current_volume = 1.0          # 0.0=тихо ... 1.0=гучно
# Пояснення: Глобальна змінна для зберігання поточної гучності.
for s in sounds.values():     # Встановлюємо гучність ВСІМ звукам
    try:
        s.set_volume(current_volume)
    except Exception:
        pass  # Захист від старих звуків
# Пояснення: Застосовуємо початкову гучність (1.0) до кожного завантаженого звукового об'єкта.

# =================== ЗМІНА 6: СЛАЙДЕР КІЛЬКОСТІ КЛАВІШ ===================
num_keys = len(KEYS)          # Початково ВСІ клавіші
# Пояснення: Початкова кількість відображуваних клавіш.
keys_list = list(KEYS.keys())[:num_keys]  # Обрізаємо список
# Пояснення: Створюємо список назв клавіш, які АКТИВНІ для поточної кількості (наприклад, ['A', 'S', 'D', 'F', ...]).
key_rects = create_key_rects(num_keys)    # Створюємо ТІЛЬКИ активні
# Пояснення: Створюємо прямокутники Pygame лише для активних клавіш.

# =================== ЗМІНА 7: ФУНКЦІЯ "ЗАСТОСУВАТИ" ===================
def apply_settings(volume: float, key_count: int):
    # Пояснення: Функція, що викликається меню налаштувань для застосування змін гучності та кількості клавіш.
    global current_volume, num_keys, keys_list, key_rects, pressed_keys
    
    # Гучність: обмежуємо 0.0-1.0
    current_volume = float(max(0.0, min(1.0, volume)))
    for s in sounds.values():
        try:
            s.set_volume(current_volume)
        except Exception:
            pass
    
    # Клавіші: обмежуємо 1-max
    key_count = max(1, min(len(KEYS), int(key_count)))
    if key_count != num_keys:
        num_keys = key_count
        keys_list = list(KEYS.keys())[:num_keys]      # Обрізаємо: Оновлюємо список АКТИВНИХ клавіш
        key_rects = create_key_rects(num_keys)        # Нові прямокутники: Перебудовуємо візуальні області
        # Очищаємо pressed_keys від індексів, які тепер не існують (якщо клавіш стало менше)
        pressed_keys = {i for i in pressed_keys if i < num_keys} 

# =================== ЗМІНА 8: КНОПКА "SETTINGS" ПРАЦЮЄ ===================
def open_settings():
    # Пояснення: Функція-обробник для кнопки "Settings", що відкриває меню.
    global screen_mode, settings_menu
    screen_mode = "settings"  # Переходимо в режим меню
    settings_menu = SettingsMenu(
        screen.get_rect(),                # Прямокутник, що покриває весь екран
        initial_volume=current_volume,    # Передаємо поточні налаштування
        initial_keys=num_keys,            
        min_keys=1, max_keys=len(KEYS),   # Обмеження слайдерів
        on_change=apply_settings,         # Функція, що викликається при зміні значень слайдерів
        on_back=lambda: _back_to_main(),  # Функція, що викликається при натисканні "Назад"
    )

# =================== ЗМІНА 9: КНОПКА "НАЗАД" ===================
def _back_to_main():
    # Пояснення: Функція для повернення з меню налаштувань до основного екрана піаніно.
    global screen_mode, settings_menu
    screen_mode = "main"      # Повертаємося до головного режиму
    settings_menu = None      # Знищуємо (приховуємо) об'єкт меню

def exit_game(): quit()  # Без змін

# =================== ЗМІНА 10: ІКОНКИ ДЛЯ КНОПКИ ===================
SETTINGS_IDLE = transform.scale(  # Звичайна шестерня
    image.load('assets/images/buttons/settings_unhover.png'), (50, 50))
SETTINGS_HOVER = transform.scale( # Блискуча шестерня
    image.load('assets/images/buttons/settings_hover.png'), (50, 50))
# Пояснення: Завантажуємо та масштабуємо зображення для кнопки налаштувань (звичайний та при наведенні).

# =================== ЗМІНА 11: КНОПКА 50x50 З ІКОНКОЮ ===================
buttons = [
    Button(
        60, 20, 50, 50,              # Координати та розмір (квадратна 50x50)
        "",                          # Без тексту, оскільки використовуємо іконку
        open_settings,               # Обробник події кліку
        img_idle=SETTINGS_IDLE,      # Звичайна іконка
        img_hover=SETTINGS_HOVER     # Іконка при наведенні
    )
]
# Пояснення: Створюємо список кнопок (зараз лише одна - "Settings").

# =================== ЗМІНА 12: ЕКРАН ПІСЛЯ РЕСУРСІВ ===================
screen = display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT)) 
# Пояснення: Створюємо об'єкт екрана. Це робиться після завантаження більшості ресурсів для оптимізації.

running = True
while running:
    screen.fill(WHITE)
    
    # =================== ЗМІНА 13: МЕНЮ ХОВАЄ ПІАНІНО ===================
    if screen_mode == "settings" and settings_menu:
        settings_menu.draw(screen, my_font)  # Малюємо ТІЛЬКИ меню, покриваючи все
    else:
        # Головний екран
        for button in buttons:
            button.draw(screen, my_font) # Малюємо кнопку налаштувань
        draw_keys(screen, key_rects, pressed_keys) # Малюємо клавіші піаніно та ефекти нот

    display.flip()
    # Пояснення: Оновлюємо екран, щоб відобразити всі зміни.

    for e in event.get():
        if e.type == QUIT:
            running = False

        # =================== ЗМІНА 14: МЕНЮ БЛокує ПІАНІНО ===================
        if screen_mode == "settings" and settings_menu:
            settings_menu.handle_event(e)  # Обробляємо події (кліки, рухи) ТІЛЬКИ для меню
            continue  # Не обробляємо жодні події для піаніно (кнопки, клавіші)

        # Головний екран
        for button in buttons:
            button.handle_event(e) # Обробляємо події для кнопки "Settings"
        
        # =================== ЗМІНА 15: КЛАВІАТУРА ТІЛЬКИ АКТИВНІ ===================
        # Обробка натискання клавіш клавіатури
        if e.type == KEYDOWN:
            k = key.name(e.key) # Отримуємо назву клавіші (наприклад, 'a', 's')
            # Перевіряємо, чи клавіша є нотою І чи вона є в списку АКТИВНИХ клавіш
            if k in sounds and k in keys_list:  # ДОДАНО: k in keys_list!
                sounds[k].play()
                idx = keys_list.index(k)
                pressed_keys.add(idx)

        # Обробка відпускання клавіш клавіатури
        if e.type == KEYUP:
            k = key.name(e.key)
            # Перевіряємо, чи клавіша є нотою І чи вона є в списку АКТИВНИХ клавіш
            if k in sounds and k in keys_list:  # ДОДАНО: k in keys_list!
                idx = keys_list.index(k)
                if idx in pressed_keys:
                    pressed_keys.remove(idx)

        # Обробка натискання миші по клавішах піаніно
        if e.type == MOUSEBUTTONDOWN:
            pos = e.pos
            for i, rect in enumerate(key_rects):
                if rect.collidepoint(pos): # Якщо клік відбувся в області клавіші
                    sounds[keys_list[i]].play() # Відтворюємо звук активної клавіші
                    pressed_keys.add(i)

        # Обробка відпускання миші
        if e.type == MOUSEBUTTONUP:
            pos = e.pos
            for i, rect in enumerate(key_rects):
                # Перевірка на індекс потрібна, щоб зняти натиск лише з тих клавіш, що були натиснуті
                if i in pressed_keys and rect.collidepoint(pos):
                    pressed_keys.remove(i)