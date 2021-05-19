import random
import copy as c
import math
import statistics as s
import time


class Grid:
    def __init__(self):
        # self.row* is template or each row
        self.row = [1, 2, 3, 4, 5, 6, 7, 8, 9]
        # self.grid* is the grid that is edited
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
        # self.repeat_all* is counter for the times while loop is repeated
        self.repeat_all = 0
        # self.hint_grid* is copy of self.grid* that is not solved yet
        self.hint_grid = c.deepcopy(self.grid)

    def get_pos(self, grid, coord):
        return self.get_row(grid, coord[1])[coord[0]]
        # returns the number located at the entered coord* in the entered grid*

    def get_row(self, grid, row: int):
        return c.deepcopy(grid[row])
        # returns a row of numbs from entered grid*
        # parameter row* is an int from 0-8 with 0 at top of grid and 8 at bottom

    def get_col(self, grid, col: int):
        column_data = []
        for row_g in grid:
            column_data.append(c.deepcopy(row_g[col]))
        return c.deepcopy(column_data)
        # returns a column of numbs from grid*
        # parameter col* is an int from 0-8 with 0 as left most col and 8 as right most col

    def get_box(self, grid, box_coord):
        # Get Y row of coord
        if box_coord[1] == 0:
            box_row = [self.get_row(grid, 0), self.get_row(grid, 1), self.get_row(grid, 2)]
        elif box_coord[1] == 1:
            box_row = [self.get_row(grid, 3), self.get_row(grid, 4), self.get_row(grid, 5)]
        elif box_coord[1] == 2:
            box_row = [self.get_row(grid, 6), self.get_row(grid, 7), self.get_row(grid, 8)]
        else:
            raise ValueError
        # sets box_row as one of the three big rows

        # Get x column of y row
        if box_coord[0] == 0:
            box = [box_row[0][:3], box_row[1][:3], box_row[2][:3]]
        elif box_coord[0] == 1:
            box = [box_row[0][3:6], box_row[1][3:6], box_row[2][3:6]]
        elif box_coord[0] == 2:
            box = [box_row[0][6:], box_row[1][6:], box_row[2][6:]]
        else:
            raise ValueError
        # filters box_row to parameter x coord

        return box
        # returns list of 3 lists

    def get_box_id(self, coord):
        x_box = math.floor(coord[0] / 3)
        y_box = math.floor(coord[1] / 3)
        return (x_box, y_box)
        # returns coord of for getting box (0-2, 0-2)

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
        return False  # if list passes check RETURNS FALSE

    def check_row(self, grid, row: int):
        # checks is data of row at parameter row* (int) is valid
        data = self.get_row(grid, row)
        if self.check_list(data):
            return True  # IF duplicate RETURNS TRUE
        return False  # if pass check RETURNS FALSE

    def check_col(self, grid, col: int):
        # checks is data of col at parameter col* (int) is valid
        data = self.get_col(grid, col)
        if self.check_list(data):
            return True  # IF duplicate RETURNS TRUE
        return False  # if pass check RETURNS FALSE

    def check_pos(self, grid, coord, numb):  # if pos bad ret TRUE
        # checks row, col, box of parameter coord* with parameter numb* in grid*
        # check row
        row_c = c.deepcopy(self.get_row(grid, coord[1]))
        row_c[coord[0]] = numb
        if self.check_list(row_c):
            return True  # IF duplicate RETURNS TRUE

        # check col
        col_c = c.deepcopy(self.get_col(grid, coord[0]))
        col_c[coord[1]] = numb
        if self.check_list(col_c):
            return True  # IF duplicate RETURNS TRUE

        # check box
        box_c = self.get_box(grid, self.get_box_id(coord))
        flat_list_box = [item for sublist in box_c for item in sublist]
        if numb in flat_list_box:
            return True  # IF duplicate RETURNS TRUE

        return False  # if pass check RETURNS FALSE

    def edit_row(self, grid, row_numb, row_data):
        # edits row indexed with parameter row_numb* and replaces with parameter row_data*
        grid[row_numb] = c.deepcopy(row_data)
        return grid
        # returns edited grid

    def edit_pos(self, grid, coord, numb):
        # edits param grid* with param numb* at param coord*
        grid[coord[1]][coord[0]] = numb
        return grid
        # returns edited grid

    def flat_list(self, list_of_lists):
        # takes in a list of multiple lists
        return [item for sublist in list_of_lists for item in sublist]
        # returns a single list with all of the same elements

    def find_missing_numb(self, data):
        temp = []
        for i in range(1, 10):
            if i not in data:
                temp.append(i)
        return temp
        # return numbs not in list of data* from 1-9

    def remove_duplicates_zero(self, data):
        temp = []
        for element in data:
            if element in temp or element == 0:
                continue
            else:
                temp.append(element)
        return temp

    def reset_last_row(self, grid):
        for i, row in enumerate(grid):
            if 0 in row:
                last_row = i - 1
                break
        self.edit_row(grid, last_row, [0, 0, 0, 0, 0, 0, 0, 0, 0])
        return last_row
        # resets last row that is full with 0's

    def when_row_is_8(self):
        # change to this when row itter is 7 (one left)
        for col_numb in range(9):
            col_data = self.get_col(self.grid, col_numb)
            missing_ans = self.find_missing_numb(col_data)
            self.edit_pos(self.grid, (col_numb, 8), missing_ans[0])
        # finds the last numb that is not in col and adds to last row

    def ask_first_row(self):
        while True:
            row = []
            for i in range(9):
                numb = int(input("Enter the order of numbers for the first row.\nWhat do you want the "+str(i+1)+" number to be?:\n"))
                row.append(numb)
            if self.check_list(row):
                print("There was a duplicate in tour list of numbers")
                continue
            else:
                print("Good")
                break
        return c.deepcopy(row)

    def when_row_is_7(self):
        #chenge to this when row itter is 6 (two row left)
        def check(possib_dict):
            # checks if combination of 9 cols of 2 numbs works for last 2 rows
            copy_grid = c.deepcopy(self.grid)
            for key, val in possib_dict.items():
                for i, numb in enumerate(val):
                    self.edit_pos(copy_grid, (key, 7 + i), numb)
            if not self.check_row(copy_grid, 8):
                self.grid = c.deepcopy(copy_grid)
                return False
            return True

        def flip(possib_dict, key):
            # flips one of the sets of numbs in possib_dict* at position key*
            possib_dict[key] = [possib_dict[key][-1], possib_dict[key][0]]
            return possib_dict[key], possib_dict


        def func(length):
            # Algorithm that gets all possible combinations for possib_soluction (dict)
            for i in range(2):
                # flips last element in dict
                flip(possib_solution, length)
                if not check(possib_solution):
                    return 1
                    # QUIT **********************
                if length != 0:
                    func(length - 1)

        possib_solution = {}
        for col_numb in range(9):
            possib_solution[col_numb] = self.find_missing_numb(
                self.get_col(self.grid, col_numb))  # create possib_solution with key as col numb
        # returns a good combination of possib_solution
        return func(8)

    def add_user_row_to_grid(self):
        print("DOING")
        self.grid[0] = self.ask_first_row()

    def fill_grid(self, row_ind=1):
        row_index = 1
        repeat = 0
        while True:
            shuffle_row = c.deepcopy(self.row)
            random.shuffle(shuffle_row)
            row_work = True
            past = []
            if shuffle_row in past:
                repeat += 1
                continue
            else:
                past.append(c.deepcopy(shuffle_row))
            for i, element in enumerate(shuffle_row):
                if not self.check_pos(self.grid, (i, row_index), element):
                    continue
                else:
                    row_work = False
                    break
            if row_work:
                self.edit_row(self.grid, row_index, shuffle_row)
                repeat = 0
                row_index += 1

            # if single row is taking more than 50000 loops return 0 to end func then delete prev row
            if repeat > 50000:
                return 0

            repeat += 1
            self.repeat_all += 1
            # stop randomizing row and begin alg for last 2 rows
            if row_index == 7:
                return self.when_row_is_7()
                # return self.grid

    def user_grid(self, hints=20):
        # min hints for 1 solution is 17
        self.hint_grid = c.deepcopy(self.grid)

        if hints < 18:
            hints = 18

        amount_zeros = 81 - hints
        zer_per_box_min, zer_per_box_max = int(amount_zeros/9)-1, int(amount_zeros/9)+1

        for col in range(3):
            for row in range(3):
                zer_box = random.randint(zer_per_box_min, zer_per_box_max)
                for i in range(zer_box):
                    while True:
                        x, y = random.randint(0, 2), random.randint(0, 2)
                        coord_x = col*3 + x
                        coord_y = row*3 + y
                        if self.get_pos(self.hint_grid, (coord_x, coord_y)) == " ":
                            continue
                        else:
                            break
                    self.edit_pos(self.hint_grid, (coord_x, coord_y), " ")
        for col in range(9):
            numb_count = 0
            for numb in self.get_col(self.hint_grid, col):
                if numb != " ":
                    numb_count+=1
            while numb_count<5 or numb_count>6:
                row = random.randint(0, 8)
                if numb_count<5:
                    if self.get_pos(self.hint_grid, (col, row)) == " ":
                        self.edit_pos(self.hint_grid, (col, row), self.get_pos(self.grid, (col, row)))
                        numb_count+=1
                    else:
                        continue
                elif numb_count>6:
                    if self.get_pos(self.hint_grid, (col, row)) != " ":
                        self.edit_pos(self.hint_grid, (col, row), " ")
                        numb_count-=1
                    else:
                        continue

        for row in range(9):
            numb_count = 0
            for numb in self.get_row(self.hint_grid, row):
                if numb != " ":
                    numb_count+=1
            while numb_count<5 or numb_count>6:
                col = random.randint(0, 8)
                if numb_count<5:
                    if self.get_pos(self.hint_grid, (col, row)) == " ":
                        self.edit_pos(self.hint_grid, (col, row), self.get_pos(self.grid, (col, row)))
                        numb_count+=1
                    else:
                        continue
                elif numb_count>6:
                    if self.get_pos(self.hint_grid, (col, row)) != " ":
                        self.edit_pos(self.hint_grid, (col, row), " ")
                        numb_count-=1
                    else:
                        continue

        for box_col in range(3):
            for box_row in range(3):
                numb_count = 0
                for box in self.flat_list(self.get_box(self.hint_grid, (box_col, box_row))):
                    if box != " ":
                        numb_count+=1
                while numb_count < 3 or numb_count > 5:
                    x = random.randint(0, 2)
                    y = random.randint(0, 2)
                    if numb_count < 3:
                        if self.get_pos(self.hint_grid, (box_col*3+x, box_row*3+y)) == " ":
                            self.edit_pos(self.hint_grid, (box_col*3+x, box_row*3+y), self.get_pos(self.grid, (box_col*3+x, box_row*3+y)))
                            numb_count+=1
                        else:
                            continue
                    elif numb_count>5:
                        if self.get_pos(self.hint_grid, (box_col*3+x, box_row*3+y)) != " ":
                            self.edit_pos(self.hint_grid, (box_col*3+x, box_row*3+y), " ")
                            numb_count-=1
                        else:
                            continue


        # for i in range(amount_zeros):
        #     x, y = random.randint(0, 8), random.randint(0, 8)
        #     self.edit_pos(self.hint_grid, (x, y), " ")
        return self.hint_grid


if __name__ == "__main__":
    g = Grid()
    bad_row = 0
    g.add_user_row_to_grid()
    while True:
        if g.fill_grid(bad_row) == 0:
            bad_row = g.reset_last_row(g.grid)
            continue
        else:
            break
    print("COMPLETE")
    for row in g.grid:
        print(row)
