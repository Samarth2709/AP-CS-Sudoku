import random
import math
import copy as c

class Grid:
    def __init__(self, level: str = 'EASY'):
        self.grid = [
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
        ]
        self.user_grid = [
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
        ]
        if level == 'BASIC':
            self.numb_hints = 50
        elif level == 'EASY':
            self.numb_hints = 30
        elif level == 'MEDIUM':
            self.numb_hints = 27
        elif level == 'HARD':
            self.numb_hints = 22
        elif level == 'IMPOSSIBLE':
            self.numb_hints = 19

    def get_row(self, row: int):
        return c.deepcopy(self.grid[row])

    def get_col(self, col: int):
        column_data = []
        for row_g in self.grid:
            column_data.append(c.deepcopy(row_g[col]))
        return c.deepcopy(column_data)

    def get_box(self, box_coord):
        # Get Y row of coord
        if box_coord[1] == 0:
            box_row = [self.get_row(0), self.get_row(1), self.get_row(2)]
        elif box_coord[1] == 1:
            box_row = [self.get_row(3), self.get_row(4), self.get_row(5)]
        elif box_coord[1] == 2:
            box_row = [self.get_row(6), self.get_row(7), self.get_row(8)]
        else:
            raise ValueError

        # Get x column of y row
        if box_coord[0] == 0:
            box = [box_row[0][:3], box_row[1][:3], box_row[2][:3]]
        elif box_coord[0] == 1:
            box = [box_row[0][3:6], box_row[1][3:6], box_row[2][3:6]]
        elif box_coord[0] == 2:
            box = [box_row[0][6:], box_row[1][6:], box_row[2][6:]]
        else:
            raise ValueError

        return box

    def get_box_id(self, coord):
        x_box = math.floor(coord[0]/3)
        y_box = math.floor(coord[1]/3)
        return (x_box, y_box)

    def get_pos(self, coord):
        return self.get_row(coord[1])[coord[0]]

    def get_box_coord(self, box_numb):
        #box numbs start with 0 and go to 80
        row = math.floor(box_numb/9)
        col = box_numb % 9
        return col, row

    def get_box_w_numb(self, box_numb):
        x, y = self.get_box_coord(box_numb)
        return self.get_pos((x, y))

    def get_possib_solution(self):
        solution = {}
        for col in range(9):
            for row in range(9):
                if self.get_pos((col, row)) == 0:
                    possible = []
                    for numb in range(9):
                        if not self.check_pos((col, row), numb):
                            possible.append(numb)
                    solution[(col, row)] = c.deepcopy(possible)
        return solution

    def check_list(self, data: list):
        # removes all 0s from list
        if 0 in data:
            for i in range(len(data)):
                try:
                    data.remove(0)
                except ValueError:
                    break

        # Checks any duplicates
        for i in range(len(data)):
            for j in range(i + 1, len(data)):
                if data[i] == data[j]:
                    return True  # if duplicate RETURNS TRUE
        return False

    def check_row(self, row: int):
        data = self.get_row(row)
        self.check_list(data)

    def check_col_row(self, col: int):
        data = self.get_col(col)
        self.check_list(data)

    def check_pos(self, coord, numb): #if pos bad ret TRUE
        #check row
        row_c = c.deepcopy(self.get_row(coord[1]))
        row_c[coord[0]] = numb
        if self.check_list(row_c):
            return True

        #check col
        col_c = c.deepcopy(self.get_col(coord[0]))
        col_c[coord[1]] = numb
        if self.check_list(col_c):
            return True

        #check box
        box_c = self.get_box(self.get_box_id(coord))
        flat_list_box = [item for sublist in box_c for item in sublist]
        if numb in flat_list_box:
            return True

        return False

    def edit_pos(self, coord, numb):
        self.grid[coord[1]][coord[0]] = numb

    def fill_grid(self):
        for col in range(len(self.grid[0])):
            for row in range(len(self.grid)):
                if self.get_pos((col, row)) == 0:
                    print("(", str(col), ",", str(row), ")")
                    while True:
                        numb = random.randint(1,9)
                        if self.check_pos((col, row), numb):
                            continue
                        self.edit_pos((col, row), numb)
                        print(True)
                        break
                for row in self.grid:
                    print(row)

g= Grid()
g.fill_grid()