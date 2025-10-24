from pygame import Rect, mouse, transform, image, MOUSEBUTTONDOWN, draw
# =================== ЗМІНИ З КОДУ 2 ===================
# ✅ ЗМІНА 1: ЗАМІНИТИ НА: import pygame
# ✅ ЗМІНА 2: ДОДАТИ: from settings import BLACK, GREY, WHITE

class Button:
    def __init__(
        self,
        x, y, width, height,
        text: str = "",
        action=None,
        img_idle=None,
        img_hover=None,
        center: bool = False
    ):
        self.text = text
        self.action = action
        self.img_idle = img_idle
        self.img_hover = img_hover
        self.use_image = img_idle is not None

        self.color_idle = (200, 200, 200)
        self.color_hover = (180, 180, 180)
        self.color_border = (0, 0, 0)
        self.text_color = (0, 0, 0)
        # =================== ЗМІНИ З КОДУ 2 ===================
        # ✅ ЗМІНА 3: СПРОСТИТИ ПАРАМЕТРИ ДО: def __init__(self, x, y, width, height, text, action=None):
        # ✅ ЗМІНА 4: ВИДАЛИТИ: img_idle, img_hover, center, use_image
        # ✅ ЗМІНА 5: СПРОСТИТИ КОЛЬОРИ ДО:
        #    self.color_idle = GREY
        #    self.color_hover = (180, 180, 180)
        #    self.color_border = BLACK
        #    self.text_color = BLACK

        if self.use_image and (width is None or height is None):
            iw, ih = self.img_idle.get_size()
            width = width or iw
            height = height or ih

        if center:
            self.rect = Rect(0, 0, width, height)
            self.rect.center = (x, y)
        else:
            self.rect = Rect(x, y, width, height)
        # =================== ЗМІНИ З КОДУ 2 ===================
        # ✅ ЗМІНА 4 (продовження): СПРОСТИТИ ДО: self.rect = pygame.Rect(x, y, width, height)

    def draw(self, screen, font):
        mouse_pos = mouse.get_pos()
        # =================== ЗМІНИ З КОДУ 2 ===================
        # ✅ ЗМІНА 6: ЗАМІНИТИ НА: mouse_pos = pygame.mouse.get_pos()

        hovered = self.rect.collidepoint(mouse_pos)

        if self.use_image:
            surf = (self.img_hover if (hovered and self.img_hover) else self.img_idle)
            if surf.get_size() != (self.rect.w, self.rect.h):
                surf = transform.scale(surf, (self.rect.w, self.rect.h))
            screen.blit(surf, self.rect.topleft)

            if self.text:
                text_surf = font.render(self.text, True, self.text_color)
                screen.blit(text_surf, text_surf.get_rect(center=self.rect.center))
        else:
            color = self.color_hover if hovered else self.color_idle
            draw.rect(screen, color, self.rect, border_radius=8)
            draw.rect(screen, self.color_border, self.rect, 2, border_radius=8)

            if self.text:
                text_surf = font.render(self.text, True, self.text_color)
                screen.blit(text_surf, text_surf.get_rect(center=self.rect.center))
        # =================== ЗМІНИ З КОДУ 2 ===================
        # ✅ ЗМІНА 7: ВИДАЛИТИ ВСЮ УМОВУ if self.use_image (30+ рядків)
        # ✅ ЗМІНА 8: СПРОСТИТИ ДО:
        #    color = self.color_hover if self.rect.collidepoint(mouse_pos) else self.color_idle
        #    pygame.draw.rect(screen, color, self.rect)
        #    pygame.draw.rect(screen, self.color_border, self.rect, 2)
        # ✅ ЗМІНА 9: ЗАВЖДИ МАЛЮВАТИ ТЕКСТ (text обов'язковий):
        #    text_surf = font.render(self.text, True, self.text_color)
        #    text_rect = text_surf.get_rect(center=self.rect.center)
        #    screen.blit(text_surf, text_rect)

    def handle_event(self, event):
        if event.type == MOUSEBUTTONDOWN and self.rect.collidepoint(event.pos):
            if self.action:
                self.action()
        # =================== ЗМІНИ З КОДУ 2 ===================
        # ✅ ЗМІНА 10: СПРОСТИТИ ДО:
        #    if event.type == pygame.MOUSEBUTTONDOWN:
        #        if self.rect.collidepoint(event.pos) and self.action:
        #            self.action()