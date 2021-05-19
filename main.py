import pygame
import copy as c
import grid_generator_main as gen


pygame.init()
#RGB colors
black = (0, 0, 0)
white = (255, 255, 255)
blue = (50, 50, 225)
red = (255, 0, 0)
green = (0, 175, 0)
grey = (230, 230, 230)
dark_grey = (220, 220, 220)

class Window:
    def __init__(self, size: tuple, background_color:tuple, caption:str = "Window", solution = None, user_grid = None):
        # self.size is size of pygame window
        self.size = size
        # self.background_color is the background color of original window
        self.background_color = background_color
        # self.window is the actual created window that is resizable
        self.window = pygame.display.set_mode(self.size, pygame.RESIZABLE)
        # changes the header of pygame window (top left)
        pygame.display.set_caption(caption)
        # functions stored in self.button_numb_press_actions to edit self.numb_pressed
        self.button_numb_press_actions = [[self.action_press_1, self.action_press_2, self.action_press_3],
                                          [self.action_press_4, self.action_press_5, self.action_press_6],
                                          [self.action_press_7, self.action_press_8, self.action_press_9]]
        # self.solution is the grid solution
        self.solution = solution
        # self.user_grid = user_grid
        # self.numb_pressed is the numb user pressed
        self.numb_pressed = None
        # self.display_grid_lis is the hint grid for user
        self.display_grid_lis = user_grid(40)
        self.copy_user_grid = []
        for row in self.display_grid_lis:
            self.copy_user_grid.append(c.deepcopy(row))
        # self.numb_pad is the numbs displayed on button numbpad
        self.numb_pad = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
        # self.grid_button_numb is dic of coords with represented numbs
        self.grid_button_numb = {}
        # self.active_box is the coords of the box that the user clicked
        self.active_box = None
        # self.wrong_coord is the coords of the incorrect numbers of the user
        self.wrong_coord = []
        # self.click_solve is the bool that is true when the user clicked "SOLVE" button but false when user clicked "RESET"
        # self.click_solve is there to make sure game doesnt end when user clicks solve when checking if user_grid is good
        self.click_solve = False

    def add_grid(self):
        x = 10
        y = 10
        for i in range(9):
            for j in range(9):
                if str(self.display_grid_lis[i][j]) != str(g.grid[i][j]) and str(self.display_grid_lis[i][j]) != " ":
                    if self.active_box == (j, i):
                        self.button_grid(self.window, str(self.display_grid_lis[i][j]), x, y, 50, 50, blue, blue, red, (j, i))
                    else:
                        self.button_grid(self.window, str(self.display_grid_lis[i][j]), x, y, 50, 50, white, dark_grey, red, (j, i))

                elif self.active_box == (j, i):
                    if (j, i) not in user_grid_given_coords:
                        self.button_grid(self.window, str(self.display_grid_lis[i][j]), x, y, 50, 50, blue, blue, black, (j, i))
                    else:
                        self.button_grid(self.window, str(self.display_grid_lis[i][j]), x, y, 50, 50, white, dark_grey, green, (j, i))

                else:
                    if (j, i) in user_grid_given_coords:
                        self.button_grid(self.window, str(self.display_grid_lis[i][j]), x, y, 50, 50, white, dark_grey, green, (j, i))
                    else:
                        self.button_grid(self.window, str(self.display_grid_lis[i][j]), x, y, 50, 50, white, dark_grey, black, (j, i))

                x+=60
            x = 10
            y+=60

    def divide_grid(self):
        vertical_left = pygame.Rect((182, 10), (6, 530))
        pygame.draw.rect(self.window, grey, vertical_left)
        vertical_right = pygame.Rect(362, 10, 6, 530)
        pygame.draw.rect(self.window, grey, vertical_right)

        horizontal_top = pygame.Rect((10,182), (530, 6))
        pygame.draw.rect(self.window, grey, horizontal_top)
        horizontal_bot = pygame.Rect((10, 362), (530, 6))
        pygame.draw.rect(self.window, grey, horizontal_bot)

    def text_objects(self, text, font, txt_color = black):
        textSurface = font.render(text, True, txt_color)
        return textSurface, textSurface.get_rect()

    def message_display(self, text, gameDisplay, x, y, size_font, txt_color):
        largeText = pygame.font.Font('freesansbold.ttf', size_font)
        TextSurf, TextRect = self.text_objects(text, largeText, txt_color = txt_color)
        TextRect.center = (x, y)
        gameDisplay.blit(TextSurf, TextRect)

    def button(self, display, msg, x, y, w, h, ic, ac, txt_color, action=None, **kwargs):
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed(3)
        if x + w > mouse[0] > x and y + h > mouse[1] > y:
            pygame.draw.rect(display, ac, (x, y, w, h))
            if click[0] == True:
                print(click)
                if action != None:
                    print(kwargs)
                    if len(kwargs) == 0:
                        action()
                    else:
                        action(kwargs)
        else:
            pygame.draw.rect(display, ic, (x, y, w, h))

        smallText = pygame.font.Font("freesansbold.ttf", 20)
        textSurf, textRect = self.text_objects(msg, smallText, txt_color = txt_color)
        textRect.center = ((x + (w / 2)), (y + (h / 2)))
        display.blit(textSurf, textRect)

    def button_grid(self, display, msg, x, y, w, h, ic, ac, txt_color, box_id, action=None, **kwargs):
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()
        if x + w > mouse[0] > x and y + h > mouse[1] > y:
            pygame.draw.rect(display, ac, (x, y, w, h))
            if click[0] == True:
                self.active_box = box_id
                print(click)
                if action != None:
                    print(kwargs.values())
                    action(kwargs.values())
        else:
            pygame.draw.rect(display, ic, (x, y, w, h))

        smallText = pygame.font.Font("freesansbold.ttf", 20)
        textSurf, textRect = self.text_objects(msg, smallText, txt_color = txt_color)
        textRect.center = ((x + (w / 2)), (y + (h / 2)))
        display.blit(textSurf, textRect)

    def add_number(self, numb):
        if numb != self.numb_pressed:
            self.numb_pressed = numb

    def change_pos_active(self):
        g.edit_pos(g.display_grid_lis, self.active_box, self.numb_pressed)

    def action_press_1(self):
        self.add_number(1)
    def action_press_2(self):
        self.add_number(2)
    def action_press_3(self):
        self.add_number(3)
    def action_press_4(self):
        self.add_number(4)
    def action_press_5(self):
        self.add_number(5)
    def action_press_6(self):
        self.add_number(6)
    def action_press_7(self):
        self.add_number(7)
    def action_press_8(self):
        self.add_number(8)
    def action_press_9(self):
        self.add_number(9)

    def solve_grid(self):
        self.click_solve = True
        self.display_grid_lis = c.deepcopy(g.grid)
        self.active_box = None

    def get_given_coords(self, grid):
        coords = []
        for row in range(9):
            for col in range(9):
                if grid[row][col] != " ":
                    coords.append((col, row))
        return coords


g = gen.Grid()
bad_row = 0
g.add_user_row_to_grid()
while True:
    if g.fill_grid() == 0:
        bad_row = g.reset_last_row(g.grid)
        continue
    else:
        break

print("COMPLETE")
for row in g.grid:
    print(row)

gameDisplay = Window((850, 550), black, "Suduko", g.grid, g.user_grid)
def reset_active():
    gameDisplay.active_box = None

def change_pos_active():
    if gameDisplay.active_box in user_grid_given_coords and gameDisplay.numb_pressed != None:
        gameDisplay.numb_pressed = None
    elif gameDisplay.active_box != None and gameDisplay.numb_pressed != None and gameDisplay.active_box:
        g.edit_pos(gameDisplay.display_grid_lis, gameDisplay.active_box, gameDisplay.numb_pressed)
        print(gameDisplay.active_box)
        gameDisplay.numb_pressed = None
        gameDisplay.active_box = None # TODO Which one reset active_box after enter number or keep active_box
    elif gameDisplay.numb_pressed != None and gameDisplay.active_box == None:
        gameDisplay.numb_pressed = None

def delete_active_box():
    if gameDisplay.active_box != None and gameDisplay.active_box not in user_grid_given_coords:
        gameDisplay.display_grid_lis[gameDisplay.active_box[1]][gameDisplay.active_box[0]] = ""
        gameDisplay.active_box = None

def back_to_user_grid():
    gameDisplay.display_grid_lis = c.deepcopy(gameDisplay.copy_user_grid)
    gameDisplay.active_box = None
    gameDisplay.click_solve = False

def check_grid_solve():
    if gameDisplay.display_grid_lis == g.grid and not gameDisplay.click_solve:
        gameDisplay.message_display("SOLVED!", gameDisplay.window, 675, 350, 50, white)


user_grid_given_coords = gameDisplay.get_given_coords(gameDisplay.copy_user_grid)


def main():
    clock = pygame.time.Clock()
    end = False
    while not end:
        for event in pygame.event.get():  # ANY EVENTS THAT HAPPEN WITHIN WINDOW
            print(event)
            # EVENT TYPES ARE ANY MAJOR EVENT (QUIT, ACTIVEEVENT, KEYDOWN, KEYUP, MOUSEMOTION, MOUSEBUTTONUP,
            # MOUSEBUTTONDOWN, JOYAXISMOTION, JOYBALLMOTION, JOYHATMOTION, JOYBUTTONUP, JOYBUTTONDOWN, VIDEORESIZE,
            # VIDEOEXPOSE, USEREVENT)
            if event.type == pygame.QUIT:
                end = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_w:
                    print('w')

        gameDisplay.window.fill(black)
        # DISPLAY OTHER OBJECTS HERE
        for x in range(3):
            for y in range(3):
                gameDisplay.button(gameDisplay.window, str(gameDisplay.numb_pad[y][x]), 550+x*100, 10+y*100, 90, 90, white, blue, black, gameDisplay.button_numb_press_actions[y][x])
        gameDisplay.button(gameDisplay.window, "Solve", 550, 400, 100, 50, white, blue, black, gameDisplay.solve_grid)
        gameDisplay.button(gameDisplay.window, "Clear Active", 675, 490, 150, 50, white, blue, black, reset_active)
        gameDisplay.button(gameDisplay.window, "Delete", 550, 490, 100, 50, white, blue, black, delete_active_box)
        gameDisplay.button(gameDisplay.window, "Reset Grid", 675, 400, 150, 50, white, blue, black, back_to_user_grid)
        # gameDisplay.button(gameDisplay.window, "9", 600, 200, 20, 20, red, blue)
        check_grid_solve()
        change_pos_active()
        gameDisplay.divide_grid()
        gameDisplay.add_grid()
        # gameDisplay.display_grid(gameDisplay.display_grid_lis)
        pygame.display.update()
        clock.tick(144)  # REFRESH RATE
    pygame.quit()


if __name__ == '__main__':
    main()