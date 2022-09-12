import pygame

# Changed
WIDTH, HEIGHT = 800, 600
color_icon_size = 50
pygame.init()
pygame.font.init()

WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Mouse")


class Color:
    def __init__(self, color):
        self.color = color
        self.size = color_icon_size
        self.x = 0
        self.y = 0
        self.rect = pygame.rect.Rect(self.x, self.y, self.size, self.size)

    def set_xy(self, x, y):
        self.x = x
        self.y = y
        self.rect = pygame.rect.Rect(self.x, self.y, self.size, self.size)

    def draw(self, window):
        pygame.draw.rect(window, self.color, self.rect)


def background(window):
    window.fill('white')


def main():
    running = True
    fps = 60
    color = (0, 0, 0)
    brush_size = 5
    prev_point = (int, int)
    color_icons = [Color((255, 0, 0)), Color((0, 0, 255)), Color((0, 255, 0)), Color((0, 0, 0)), Color((255, 255, 255))]
    lines = []
    clock = pygame.time.Clock()

    def redraw(window):
        sidebar = pygame.surface.Surface((200, HEIGHT))
        sidebar.fill((240, 240, 240))
        window.blit(sidebar, (600, 0))

        x, y = 625, 200
        for color_icon in color_icons:
            color_icon.set_xy(x, y)
            color_icon.draw(window)
            if x < 700:
                x += color_icon_size
            else:
                x = 625
                y += 50

        pygame.display.update()

    background(WIN)
    while running:
        clock.tick(fps)

        if pygame.mouse.get_pressed()[0] and 0 < pygame.mouse.get_pos()[0] < 601:
            if prev_point == (int, int):
                pygame.draw.circle(WIN, color, pygame.mouse.get_pos(), 2*brush_size/5)
            else:
                pygame.draw.line(WIN, color, prev_point, pygame.mouse.get_pos(), brush_size)
            prev_point = pygame.mouse.get_pos()
        else:
            if prev_point != (int, int):
                pygame.draw.line(WIN, color, prev_point, pygame.mouse.get_pos(), brush_size)
                pygame.draw.circle(WIN, color, pygame.mouse.get_pos(), brush_size / 2)
            prev_point = (int, int)

        redraw(WIN)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()
            if event.type == pygame.KEYDOWN:
                if pygame.key.get_pressed()[pygame.K_c]:
                    pygame.draw.rect(WIN, 'white', (0, 0, 600, 600))
            if event.type == pygame.MOUSEBUTTONDOWN and pygame.mouse.get_pressed()[0]:
                for color_icon in color_icons:
                    if color_icon.rect.collidepoint(pygame.mouse.get_pos()):
                        if color_icon.color == (255, 255, 255):
                            brush_size = 10
                        else:
                            brush_size = 5
                        color = color_icon.color


main()
