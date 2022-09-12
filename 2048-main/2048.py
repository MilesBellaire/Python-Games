import pygame
import random

SCREEN_WIDTH, SCREEN_HEIGHT = 500, 600
GAME_HEIGHT = 500
boxes = 4
BOX_WIDTH, BOX_HEIGHT = SCREEN_WIDTH/boxes, GAME_HEIGHT/boxes
background_color = (255, 220, 175)
border_color = (150, 125, 100)
empty_sqr_color = (200, 175, 150)
random = random.Random()
pygame.font.init()
large_font = pygame.font.SysFont("comicsans", 100)
normal_font = pygame.font.SysFont("comicsans", 70)
smaller_font = pygame.font.SysFont("comicsans", 55)
borders_width = BOX_WIDTH/25

images = [pygame.image.load(r'C:\Users\mile5\Desktop\Coding Projects\Python Prjects\2048\Include\assets\Dorie10.jpg'),
          pygame.image.load(r'C:\Users\mile5\Desktop\Coding Projects\Python Prjects\2048\Include\assets\Dorie7.jpg'),
          pygame.image.load(r'C:\Users\mile5\Desktop\Coding Projects\Python Prjects\2048\Include\assets\Dorie9.jpg'),
          pygame.image.load(r'C:\Users\mile5\Desktop\Coding Projects\Python Prjects\2048\Include\assets\Dorie.JPG'),
          pygame.image.load(r'C:\Users\mile5\Desktop\Coding Projects\Python Prjects\2048\Include\assets\Dorie3.PNG'),
          pygame.image.load(r'C:\Users\mile5\Desktop\Coding Projects\Python Prjects\2048\Include\assets\Dorie1.PNG'),
          pygame.image.load(r'C:\Users\mile5\Desktop\Coding Projects\Python Prjects\2048\Include\assets\Dorie6.PNG'),
          pygame.image.load(r'C:\Users\mile5\Desktop\Coding Projects\Python Prjects\2048\Include\assets\Dorie4.jpg'),
          pygame.image.load(r'C:\Users\mile5\Desktop\Coding Projects\Python Prjects\2048\Include\assets\Dorie8.jpg'),
          pygame.image.load(r'C:\Users\mile5\Desktop\Coding Projects\Python Prjects\2048\Include\assets\Dorie2.PNG'),
          pygame.image.load(r'C:\Users\mile5\Desktop\Coding Projects\Python Prjects\2048\Include\assets\Dorie5.jpg')]

pygame.display.set_caption("2048")
WIN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))


class Block:
    def __init__(self, x, y, power):
        self.x = x
        self.y = y
        self.power = power
        self.colors = [(255, 220, 175),  (240, 200, 155), (255, 175, 100), (255, 120, 50), (255, 100, 25), (255, 75, 0), (255, 210, 110), (255, 200, 100), (255, 200, 75), (255, 200, 50), (255, 200, 25), 0]
        try:
            self.image = images[power-1]
        except:
            self.image = 'DNE'

    def draw(self, window):
        border_space = BOX_WIDTH/25
        pygame.draw.rect(window, (255, 255, 255), (self.x+borders_width/2, self.y+borders_width/2, int(BOX_WIDTH-borders_width), int(BOX_HEIGHT-borders_width)))
        if self.image == 'DNE':
            if self.power < 3:
                font_color = (120, 95, 70)
            else:
                font_color = (255, 255, 255)
            if self.power > 11:
                pygame.draw.rect(window, (self.colors[11]), (int(self.x+borders_width/2 + border_space), int(self.y+borders_width/2+border_space), int(BOX_WIDTH-borders_width-border_space*2), int(BOX_HEIGHT-borders_width-border_space*2)))
            else:
                pygame.draw.rect(window, (self.colors[self.power-1]), (int(self.x+borders_width/2+border_space), int(self.y+borders_width/2+border_space), int(BOX_WIDTH-borders_width-border_space*2), int(BOX_HEIGHT-borders_width-border_space*2)))

            power_label = normal_font.render(str(pow(2, self.power)), True, font_color)
            window.blit(power_label, (self.x + BOX_WIDTH/2 - power_label.get_width()/2, self.y + BOX_HEIGHT/2 - power_label.get_height()/2))
        else:
            fit_pic = pygame.transform.scale(self.image, (int(BOX_WIDTH-borders_width-border_space*2), int(BOX_HEIGHT-borders_width-border_space*2)))
            window.blit(fit_pic, (self.x+borders_width/2+border_space, self.y+borders_width/2+border_space))


def background(window):
    pygame.draw.rect(window, background_color, (0, 0, SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.draw.rect(window, border_color, (0, 0, SCREEN_WIDTH, GAME_HEIGHT+borders_width/2))
    for i in range(boxes):
        for j in range(boxes):
            pygame.draw.rect(window, empty_sqr_color,
                             (i*SCREEN_WIDTH/boxes + borders_width/2, j*GAME_HEIGHT/boxes + borders_width/2, BOX_WIDTH - borders_width, BOX_HEIGHT - borders_width))


def main():
    running = True
    fps = 60
    clock = pygame.time.Clock()
    blocks = []
    prev_click = 'none'
    loss, win = False, False

    loss_label = large_font.render('LOSER', True, (255, 255, 255))
    win_label = large_font.render('YOU WIN', True, (255, 255, 255))

    def redraw(window):
        background(window)
        for block in blocks:
            block.draw(window)
        if loss:
            pygame.draw.rect(window, border_color, ((SCREEN_WIDTH - loss_label.get_width())/2 - 5, (GAME_HEIGHT - loss_label.get_height())/2 - 5, loss_label.get_width() + 10, loss_label.get_height() + 5))
            window.blit(loss_label, ((SCREEN_WIDTH - loss_label.get_width())/2, (GAME_HEIGHT - loss_label.get_height())/2))
        if win:
            pygame.draw.rect(window, border_color, ((SCREEN_WIDTH - win_label.get_width())/2 - 5, (GAME_HEIGHT - win_label.get_height())/2 - 5, win_label.get_width() + 10, win_label.get_height() + 5))
            window.blit(win_label, ((SCREEN_WIDTH - win_label.get_width())/2, (GAME_HEIGHT - win_label.get_height())/2))
        pygame.display.update()

    def start(squares):
        squares = new_block(squares)
        squares = new_block(squares)
        return squares

    def new_block(squares):
        if len(squares) < 16:
            again = True
            x_sqr, y_sqr = 0, 0
            while again:
                again = False
                x_sqr = random.randrange(0, 4)
                y_sqr = random.randrange(0, 4)
                for block in squares:
                    if block.x == x_sqr*SCREEN_WIDTH/4 and block.y == y_sqr*SCREEN_WIDTH/4:
                        again = True

            power = random.randint(1, 2)

            if power == 2:
                power = random.randint(1, 2)
                if power == 2:
                    power = random.randint(1, 2)
            squares.append(Block(x_sqr*SCREEN_WIDTH/4, y_sqr*GAME_HEIGHT/4, power))
        return squares

    def move_blocks(squares, direction):
        copy = squares

        if direction == 'R':
            # Move all squares to the right
            for square in copy:
                displaced = BOX_WIDTH
                for square2 in squares:
                    if square.y == square2.y and square.x < square2.x:
                        displaced += BOX_WIDTH
                square.x = SCREEN_WIDTH - displaced

        if direction == 'L':
            # Move all squares to the right
            for square in copy:
                displaced = 0
                for square2 in squares:
                    if square.y == square2.y and square.x > square2.x:
                        displaced += BOX_WIDTH
                square.x = displaced

        if direction == 'D':
            # Move all squares to the right
            for square in copy:
                displaced = BOX_WIDTH
                for square2 in squares:
                    if square.x == square2.x and square.y < square2.y:
                        displaced += BOX_HEIGHT
                square.y = GAME_HEIGHT - displaced

        if direction == 'U':
            # Move all squares to the right
            for square in copy:
                displaced = 0
                for square2 in squares:
                    if square.x == square2.x and square.y > square2.y:
                        displaced += BOX_HEIGHT
                square.y = displaced

        return copy

    def combine_blocks(squares, direction):
        # Combine squares
        retval = squares.copy()
        again = True
        if direction == 'R':
            # Sorts the array
            while again:
                again = False
                for square1 in squares:
                    for square2 in squares:
                        index1 = squares.index(square1)
                        index2 = squares.index(square2)
                        if square1.x < square2.x and index1 < index2:
                            temp = square1
                            squares[index1] = square2
                            squares[index2] = temp
                            again = True
            again = True
            while again:
                again = False
                for square in squares:
                    for square2 in squares:
                        if square.x+BOX_WIDTH == square2.x and square.y == square2.y and square.power == square2.power:
                            again = True
                            retval.append(Block(square2.x, square2.y, square.power+1))
                            retval.remove(square)
                            retval.remove(square2)
                            squares.remove(square)
                            squares.remove(square2)

        if direction == 'L':
            while again:
                again = False
                for square1 in squares:
                    for square2 in squares:
                        index1 = squares.index(square1)
                        index2 = squares.index(square2)
                        if square1.x > square2.x and index1 < index2:
                            temp = square1
                            squares[index1] = square2
                            squares[index2] = temp
                            again = True
            again = True
            while again:
                again = False
                for square in squares:
                    for square2 in squares:
                        if square.x-BOX_WIDTH == square2.x and square.y == square2.y and square.power == square2.power:
                            again = True
                            retval.append(Block(square2.x, square2.y, square.power+1))
                            retval.remove(square)
                            retval.remove(square2)
                            squares.remove(square)
                            squares.remove(square2)

        if direction == 'D':
            while again:
                again = False
                for square1 in squares:
                    for square2 in squares:
                        index1 = squares.index(square1)
                        index2 = squares.index(square2)
                        if square1.y < square2.y and index1 < index2:
                            temp = square1
                            squares[index1] = square2
                            squares[index2] = temp
                            again = True
            again = True
            while again:
                again = False
                for square in squares:
                    for square2 in squares:
                        if square.y+BOX_WIDTH == square2.y and square.x == square2.x and square.power == square2.power:
                            again = True
                            retval.append(Block(square2.x, square2.y, square.power+1))
                            retval.remove(square)
                            retval.remove(square2)
                            squares.remove(square)
                            squares.remove(square2)

        if direction == 'U':
            while again:
                again = False
                for square1 in squares:
                    for square2 in squares:
                        index1 = squares.index(square1)
                        index2 = squares.index(square2)
                        if square1.y > square2.y and index1 < index2:
                            temp = square1
                            squares[index1] = square2
                            squares[index2] = temp
                            again = True
            again = True
            while again:
                again = False
                for square in squares:
                    for square2 in squares:
                        if square.y-BOX_WIDTH == square2.y and square.x == square2.x and square.power == square2.power:
                            again = True
                            retval.append(Block(square2.x, square2.y, square.power+1))
                            retval.remove(square)
                            retval.remove(square2)
                            squares.remove(square)
                            squares.remove(square2)

        return retval

    def game_over(squares):
        if len(squares) == 16:
            for square in squares:
                for square2 in squares:
                    if square.power == square2.power:
                        if square.y == square2.y:
                            if square.x + BOX_WIDTH == square2.x:
                                return False
                            if square.x - BOX_WIDTH == square2.x:
                                return False
                        if square.x == square2.x:
                            if square.y - BOX_WIDTH == square2.y:
                                return False
                            if square.y + BOX_WIDTH == square2.y:
                                return False
            return True
        return False

    def you_win(squares):
        for square in squares:
            if square.power == 11:
                return True
        return False

    blocks = start(blocks)
    for block in blocks:
        print(str(blocks.index(block)) + ". x: " + str(block.x) + ", y: " + str(block.y))
    print()
    while running:
        clock.tick(fps)
        keys = pygame.key.get_pressed()
        click = 'none'
        if not win or loss:
            if keys[pygame.K_d] or keys[pygame.K_LEFT]:
                click = 'R'
            if keys[pygame.K_a] or keys[pygame.K_RIGHT]:
                click = 'L'
            if keys[pygame.K_s] or keys[pygame.K_DOWN]:
                click = 'D'
            if keys[pygame.K_w] or keys[pygame.K_UP]:
                click = 'U'
        if keys[pygame.K_r]:
            click = 'r'
        if keys[pygame.K_c]:
            # Test key
            click = 'test'
        if keys[pygame.K_ESCAPE]:
            running = False

        if click != prev_click:
            if click == 'R' or click == 'L' or click == 'D' or click == 'U':
                blocks = move_blocks(blocks, click)
                redraw(WIN)
                # print("move")
                # pygame.time.wait(1000)
                blocks = combine_blocks(blocks, click)
                redraw(WIN)
                # print("combine")
                # pygame.time.wait(1000)
                blocks = move_blocks(blocks, click)
                # print("move")
                blocks = new_block(blocks)
                for block in blocks:
                    print(str(blocks.index(block)) + ". x: " + str(block.x) + ", y: " + str(block.y))
                print()

            if click == 'r':
                blocks.clear()
                start(blocks)

            if click == 'test':
                blocks = new_block(blocks)

        if you_win(blocks):
            win = True
        if game_over(blocks):
            loss = True
        redraw(WIN)
        prev_click = click
        # Checks if window is closed
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False


main()
