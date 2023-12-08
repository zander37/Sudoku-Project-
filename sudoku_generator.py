import math, random, copy


class SudokuGenerator:

    def __init__(self, row_length, removed_cells):
        self.row_length = row_length
        self.removed_cells = removed_cells
        self.board = [
            [],
            [],
            [],
            [],
            [],
            [],
            [],
            [],
            []
        ]
        self.box_length = int(math.sqrt(row_length))

    def get_board(self):
        return self.board

    def print_board(self):
        for row in self.board:
            for num in row:
                print(num, end=" ")
            print()

    def valid_in_row(self, row, num):
        if num in self.board[row]:
            return False
        else:
            return True

    def valid_in_col(self, col, num):
        column = []
        for row in self.board:
            column.append(row[col])
        if num in column:
            return False
        else:
            return True

    def valid_in_box(self, row_start, col_start, num):
        for i in range(3):
            for j in range(3):
                if self.board[row_start + i][col_start + j] == num:
                    return False
        return True

    def is_valid(self, row, col, num):
        if self.valid_in_row(row, num) and self.valid_in_col(col, num) and self.valid_in_box(row - row % 3, col - col % 3, num):
            return True
        else:
            return False

    def fill_box(self, row_start, col_start):
        box_values = [1, 2, 3, 4, 5, 6, 7, 8, 9]
        random.shuffle(box_values)
        for i in range(3):
            for j in range(3):
                self.board[row_start + i][col_start + j] = box_values.pop()

    def fill_diagonal(self):
        for row in self.board:
            for i in range(9):
                row.append(0)
        for i in range(0, 9, 3):
            self.fill_box(i, i)

    # '''
    # DO NOT CHANGE
    # Provided for students
    # Fills the remaining cells of the board
    # Should be called after the diagonal boxes have been filled
    #
	# Parameters:
	# row, col specify the coordinates of the first empty (0) cell
    #
	# Return:
	# boolean (whether or not we could solve the board)
    # '''

    def fill_remaining(self, row, col):
        if (col >= self.row_length and row < self.row_length - 1):
            row += 1
            col = 0
        if row >= self.row_length and col >= self.row_length:
            return True
        if row < self.box_length:
            if col < self.box_length:
                col = self.box_length
        elif row < self.row_length - self.box_length:
            if col == int(row // self.box_length * self.box_length):
                col += self.box_length
        else:
            if col == self.row_length - self.box_length:
                row += 1
                col = 0
                if row >= self.row_length:
                    return True

        for num in range(1, self.row_length + 1):
            if self.is_valid(row, col, num):
                self.board[row][col] = num
                if self.fill_remaining(row, col + 1):
                    return True
                self.board[row][col] = 0
        return False

    # '''
    # DO NOT CHANGE
    # Provided for students
    # Constructs a solution by calling fill_diagonal and fill_remaining
    #
	# Parameters: None
	# Return: None
    # '''

    def fill_values(self):
        self.fill_diagonal()
        self.fill_remaining(0, self.box_length)

    # '''
    # Removes the appropriate number of cells from the board
    # This is done by setting some values to 0
    # Should be called after the entire solution has been constructed
    # i.e. after fill_values has been called
    #
    # NOTE: Be careful not to 'remove' the same cell multiple times
    # i.e. if a cell is already 0, it cannot be removed again
    #
	# Parameters: None
	# Return: None
    # '''

    def remove_cells(self):
        check = []
        while len(check) != self.removed_cells:
            row = random.randint(0, 8)
            col = random.randint(0, 8)
            coord = (row, col)
            check.append(coord)
            if len(check) != len(set(check)):
                check.pop(-1)
                continue
        for tup in check:
            self.board[tup[0]][tup[1]] = 0




# '''
# DO NOT CHANGE
# Provided for students
# Given a number of rows and number of cells to remove, this function:
# 1. creates a SudokuGenerator
# 2. fills its values and saves this as the solved state
# 3. removes the appropriate number of cells
# 4. returns the representative 2D Python Lists of the board and solution
#
# Parameters:
# size is the number of rows/columns of the board (9 for this project)
# removed is the number of cells to clear (set to 0)
#
# Return: list[list] (a 2D Python list to represent the board)


def generate_sudoku(size, removed):
    sudoku = SudokuGenerator(size, removed)
    sudoku.fill_values()
    board = sudoku.get_board()
    board_sol = copy.deepcopy(board)
    sudoku.remove_cells()
    board = sudoku.get_board()
    return board_sol, board

# Added Methods

def available_square(board, row, col):
    try:
        if board[row][col] == 0:
            return True
    except IndexError:
        pass
    return False

def available_again(board, row, col, check):
    try:
        if board[row][col] == 0 or (row, col) not in check:
            return True
    except IndexError:
        pass
    return False


def mark_square(board, row, col, num):
    board[row][col] = num


def board_is_full(board):
    for row in board:
        for num in row:
            if num == 0:
                return False
    return True


def get_sketchable(board):
    filled = []
    for row in range(9):
        for col in range(9):
            if board[row][col] == 0:
                filled.append((row, col))
    return filled


def get_original(board):
    filled = []
    for row in range(9):
        for col in range(9):
            if board[row][col] != 0:
                filled.append((row, col))
    return filled


def check_if_winner(board, sol_board):
    if board == sol_board:
        return True
    return False
