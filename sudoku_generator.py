import math, random, copy, sys, pygame


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


def draw_game_start():  # Draws Start Menu

    button_font = pygame.font.Font(None, 100)
    backround = pygame.image.load("Sudoku-RIddles-Game-Quiz-Shutterstock.webp")
    backround_new = pygame.transform.scale(backround, (1200, 900))

    screen.fill((255, 255, 255))
    screen.blit(backround_new, (0, 0))


    # Title
    title_text = "WELCOME TO SUDOKU!"
    title_surf = game_over_font.render(title_text, 0, (0, 0, 0))
    title_rect = title_surf.get_rect(center=(1200 // 2, 900 // 2 - 150))
    screen.blit(title_surf, title_rect)

    # Buttons
    easy_text = button_font.render("Easy", 0, (255, 255, 255))
    med_text = button_font.render("Medium", 0, (255, 255, 255))
    hard_text = button_font.render("Hard", 0, (255, 255, 255))

    easy_surface = pygame.Surface((easy_text.get_size()[0] + 20, easy_text.get_size()[1] + 20))
    easy_surface.fill((255, 165, 0))
    easy_surface.blit(easy_text, (10, 10))
    med_surface = pygame.Surface((med_text.get_size()[0] + 20, med_text.get_size()[1] + 20))
    med_surface.fill((255, 165, 0))
    med_surface.blit(med_text, (10, 10))
    hard_surface = pygame.Surface((hard_text.get_size()[0] + 20, hard_text.get_size()[1] + 20))
    hard_surface.fill((255, 165, 0))
    hard_surface.blit(hard_text, (10, 10))

    easy_rectangle = easy_surface.get_rect(center=(300, 600))
    med_rectangle = med_surface.get_rect(center=(600, 600))
    hard_rectangle = hard_surface.get_rect(center=(900, 600))

    screen.blit(easy_surface, easy_rectangle)
    screen.blit(med_surface, med_rectangle)
    screen.blit(hard_surface, hard_rectangle)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if easy_rectangle.collidepoint(event.pos):
                    sol_board, board = sudoku_generator.generate_sudoku(9, 30)
                    screen.fill((255, 255, 255))
                    return sol_board, board
                elif med_rectangle.collidepoint(event.pos):
                    sol_board, board = sudoku_generator.generate_sudoku(9, 40)
                    screen.fill((255, 255, 255))
                    return sol_board, board
                elif hard_rectangle.collidepoint(event.pos):
                    sol_board, board = sudoku_generator.generate_sudoku(9, 50)
                    screen.fill((255, 255, 255))
                    return sol_board, board
        pygame.display.update()


def display_grid():  # Draws Game Grid
    # Standard Lines
    for i in range(1, 10):
        pygame.draw.line(
            screen,
            (0, 0, 0),
            (0, i * 100),
            (900, i * 100),
            1
        )
    for i in range(1, 9):
        pygame.draw.line(
            screen,
            (0, 0, 0),
            (i * 100, 0),
            (i * 100, 900),
            1
        )
    # Box Lines
    for i in range(1, 3):
        pygame.draw.line(
            screen,
            (0, 0, 0),
            (0, i * 300),
            (900, i * 300),
            5
        )
    for i in range(1, 4):
        pygame.draw.line(
            screen,
            (0, 0, 0),
            (i * 300, 0),
            (i * 300, 900),
            5
        )


def display_selected(row, col):  # Creates a Box To Show Selected
    pygame.draw.line(
        screen,
        (255, 0, 0),
        (col * 100, row * 100),
        (col * 100 + 100, row * 100),
        7
    )
    pygame.draw.line(
        screen,
        (255, 0, 0),
        (col * 100, row * 100),
        (col * 100, row * 100 + 100),
        7
    )
    pygame.draw.line(
        screen,
        (255, 0, 0),
        (col * 100 + 100, row * 100),
        (col * 100 + 100, row * 100 + 100),
        7
    )
    pygame.draw.line(
        screen,
        (255, 0, 0),
        (col * 100, row * 100 + 100),
        (col * 100 + 100, row * 100 + 100),
        7
    )


def draw_num():  # Draws Numbers on Board
    # num_zero_surf = number_font.render(' ', 0, (0, 0, 0))
    num_one_surf = number_font.render('1', 0, (0, 0, 0))
    num_two_surf = number_font.render('2', 0, (0, 0, 0))
    num_three_surf = number_font.render('3', 0, (0, 0, 0))
    num_four_surf = number_font.render('4', 0, (0, 0, 0))
    num_five_surf = number_font.render('5', 0, (0, 0, 0))
    num_six_surf = number_font.render('6', 0, (0, 0, 0))
    num_seven_surf = number_font.render('7', 0, (0, 0, 0))
    num_eight_surf = number_font.render('8', 0, (0, 0, 0))
    num_nine_surf = number_font.render('9', 0, (0, 0, 0))

    for row in range(9):
        for col in range(9):
            # if board[row][col] == 0:
            #     num_zero_rect = num_zero_surf.get_rect(center=(col * 100 + 100 // 2, row * 100 + 100 // 2))
            #     screen.blit(num_zero_surf, num_zero_rect)
            if board[row][col] == 1:
                num_one_rect = num_one_surf.get_rect(center=(col * 100 + 100 // 2, row * 100 + 100 // 2))
                screen.blit(num_one_surf, num_one_rect)
            elif board[row][col] == 2:
                num_two_rect = num_two_surf.get_rect(center=(col * 100 + 100 // 2, row * 100 + 100 // 2))
                screen.blit(num_two_surf, num_two_rect)
            elif board[row][col] == 3:
                num_three_rect = num_three_surf.get_rect(center=(col * 100 + 100 // 2, row * 100 + 100 // 2))
                screen.blit(num_three_surf, num_three_rect)
            elif board[row][col] == 4:
                num_four_rect = num_four_surf.get_rect(center=(col * 100 + 100 // 2, row * 100 + 100 // 2))
                screen.blit(num_four_surf, num_four_rect)
            elif board[row][col] == 5:
                num_five_rect = num_five_surf.get_rect(center=(col * 100 + 100 // 2, row * 100 + 100 // 2))
                screen.blit(num_five_surf, num_five_rect)
            elif board[row][col] == 6:
                num_six_rect = num_six_surf.get_rect(center=(col * 100 + 100 // 2, row * 100 + 100 // 2))
                screen.blit(num_six_surf, num_six_rect)
            elif board[row][col] == 7:
                num_seven_rect = num_one_surf.get_rect(center=(col * 100 + 100 // 2, row * 100 + 100 // 2))
                screen.blit(num_seven_surf, num_seven_rect)
            elif board[row][col] == 8:
                num_eight_rect = num_eight_surf.get_rect(center=(col * 100 + 100 // 2, row * 100 + 100 // 2))
                screen.blit(num_eight_surf, num_eight_rect)
            elif board[row][col] == 9:
                num_nine_rect = num_nine_surf.get_rect(center=(col * 100 + 100 // 2, row * 100 + 100 // 2))
                screen.blit(num_nine_surf, num_nine_rect)


def draw_original_values(): # Draws Original Game Values
    num_one_surf = number_font.render('1', 0, (0, 0, 0))
    num_two_surf = number_font.render('2', 0, (0, 0, 0))
    num_three_surf = number_font.render('3', 0, (0, 0, 0))
    num_four_surf = number_font.render('4', 0, (0, 0, 0))
    num_five_surf = number_font.render('5', 0, (0, 0, 0))
    num_six_surf = number_font.render('6', 0, (0, 0, 0))
    num_seven_surf = number_font.render('7', 0, (0, 0, 0))
    num_eight_surf = number_font.render('8', 0, (0, 0, 0))
    num_nine_surf = number_font.render('9', 0, (0, 0, 0))

    for row in range(9):
        for col in range(9):
            # if board[row][col] == 0:
            #     num_zero_rect = num_zero_surf.get_rect(center=(col * 100 + 100 // 2, row * 100 + 100 // 2))
            #     screen.blit(num_zero_surf, num_zero_rect)
            if board[row][col] == 1:
                num_one_rect = num_one_surf.get_rect(center=(col * 100 + 100 // 2, row * 100 + 100 // 2))
                screen.blit(num_one_surf, num_one_rect)
            elif board[row][col] == 2:
                num_two_rect = num_two_surf.get_rect(center=(col * 100 + 100 // 2, row * 100 + 100 // 2))
                screen.blit(num_two_surf, num_two_rect)
            elif board[row][col] == 3:
                num_three_rect = num_three_surf.get_rect(center=(col * 100 + 100 // 2, row * 100 + 100 // 2))
                screen.blit(num_three_surf, num_three_rect)
            elif board[row][col] == 4:
                num_four_rect = num_four_surf.get_rect(center=(col * 100 + 100 // 2, row * 100 + 100 // 2))
                screen.blit(num_four_surf, num_four_rect)
            elif board[row][col] == 5:
                num_five_rect = num_five_surf.get_rect(center=(col * 100 + 100 // 2, row * 100 + 100 // 2))
                screen.blit(num_five_surf, num_five_rect)
            elif board[row][col] == 6:
                num_six_rect = num_six_surf.get_rect(center=(col * 100 + 100 // 2, row * 100 + 100 // 2))
                screen.blit(num_six_surf, num_six_rect)
            elif board[row][col] == 7:
                num_seven_rect = num_one_surf.get_rect(center=(col * 100 + 100 // 2, row * 100 + 100 // 2))
                screen.blit(num_seven_surf, num_seven_rect)
            elif board[row][col] == 8:
                num_eight_rect = num_eight_surf.get_rect(center=(col * 100 + 100 // 2, row * 100 + 100 // 2))
                screen.blit(num_eight_surf, num_eight_rect)
            elif board[row][col] == 9:
                num_nine_rect = num_nine_surf.get_rect(center=(col * 100 + 100 // 2, row * 100 + 100 // 2))
                screen.blit(num_nine_surf, num_nine_rect)


def make_sketch(row, col):  #  Creates a Sketch
    num_zero_surf = number_font.render(' ', 0, (0, 0, 0))
    num_one_surf = number_font.render('1', 0, (128, 128, 128))
    num_two_surf = number_font.render('2', 0, (128, 128, 128))
    num_three_surf = number_font.render('3', 0, (128, 128, 128))
    num_four_surf = number_font.render('4', 0, (128, 128, 128))
    num_five_surf = number_font.render('5', 0, (128, 128, 128))
    num_six_surf = number_font.render('6', 0, (128, 128, 128))
    num_seven_surf = number_font.render('7', 0, (128, 128, 128))
    num_eight_surf = number_font.render('8', 0, (128, 128, 128))
    num_nine_surf = number_font.render('9', 0, (128, 128, 128))

    if board_copy[row][col] == 0:
        pass
    elif board_copy[row][col] == 1:
        num_one_rect = num_one_surf.get_rect(center=(col * 100 + 100 // 2, row * 100 + 100 // 2))
        screen.blit(num_one_surf, num_one_rect)
    elif board_copy[row][col] == 2:
        num_two_rect = num_two_surf.get_rect(center=(col * 100 + 100 // 2, row * 100 + 100 // 2))
        screen.blit(num_two_surf, num_two_rect)
    elif board_copy[row][col] == 3:
        num_three_rect = num_three_surf.get_rect(center=(col * 100 + 100 // 2, row * 100 + 100 // 2))
        screen.blit(num_three_surf, num_three_rect)
    elif board_copy[row][col] == 4:
        num_four_rect = num_four_surf.get_rect(center=(col * 100 + 100 // 2, row * 100 + 100 // 2))
        screen.blit(num_four_surf, num_four_rect)
    elif board_copy[row][col] == 5:
        num_five_rect = num_five_surf.get_rect(center=(col * 100 + 100 // 2, row * 100 + 100 // 2))
        screen.blit(num_five_surf, num_five_rect)
    elif board_copy[row][col] == 6:
        num_six_rect = num_six_surf.get_rect(center=(col * 100 + 100 // 2, row * 100 + 100 // 2))
        screen.blit(num_six_surf, num_six_rect)
    elif board_copy[row][col] == 7:
        num_seven_rect = num_one_surf.get_rect(center=(col * 100 + 100 // 2, row * 100 + 100 // 2))
        screen.blit(num_seven_surf, num_seven_rect)
    elif board_copy[row][col] == 8:
        num_eight_rect = num_eight_surf.get_rect(center=(col * 100 + 100 // 2, row * 100 + 100 // 2))
        screen.blit(num_eight_surf, num_eight_rect)
    elif board_copy[row][col] == 9:
        num_nine_rect = num_nine_surf.get_rect(center=(col * 100 + 100 // 2, row * 100 + 100 // 2))
        screen.blit(num_nine_surf, num_nine_rect)
    return True


def draw_sketches():
    num_one_surf = number_font.render('1', 0, (128, 128, 128))
    num_two_surf = number_font.render('2', 0, (128, 128, 128))
    num_three_surf = number_font.render('3', 0, (128, 128, 128))
    num_four_surf = number_font.render('4', 0, (128, 128, 128))
    num_five_surf = number_font.render('5', 0, (128, 128, 128))
    num_six_surf = number_font.render('6', 0, (128, 128, 128))
    num_seven_surf = number_font.render('7', 0, (128, 128, 128))
    num_eight_surf = number_font.render('8', 0, (128, 128, 128))
    num_nine_surf = number_font.render('9', 0, (128, 128, 128))

    for tup in sketchable:
        if board_copy[tup[0]][tup[1]] == 0:
            pass
        elif board_copy[tup[0]][tup[1]] == 1:
            num_one_rect = num_one_surf.get_rect(center=(tup[1] * 100 + 100 // 2, tup[0] * 100 + 100 // 2))
            screen.blit(num_one_surf, num_one_rect)
        elif board_copy[tup[0]][tup[1]] == 2:
            num_two_rect = num_two_surf.get_rect(center=(tup[1] * 100 + 100 // 2, tup[0] * 100 + 100 // 2))
            screen.blit(num_two_surf, num_two_rect)
        elif board_copy[tup[0]][tup[1]] == 3:
            num_three_rect = num_three_surf.get_rect(center=(tup[1] * 100 + 100 // 2, tup[0] * 100 + 100 // 2))
            screen.blit(num_three_surf, num_three_rect)
        elif board_copy[tup[0]][tup[1]] == 4:
            num_four_rect = num_four_surf.get_rect(center=(tup[1] * 100 + 100 // 2, tup[0] * 100 + 100 // 2))
            screen.blit(num_four_surf, num_four_rect)
        elif board_copy[tup[0]][tup[1]] == 5:
            num_five_rect = num_five_surf.get_rect(center=(tup[1] * 100 + 100 // 2, tup[0] * 100 + 100 // 2))
            screen.blit(num_five_surf, num_five_rect)
        elif board_copy[tup[0]][tup[1]] == 6:
            num_six_rect = num_six_surf.get_rect(center=(tup[1] * 100 + 100 // 2, tup[0] * 100 + 100 // 2))
            screen.blit(num_six_surf, num_six_rect)
        elif board_copy[tup[0]][tup[1]] == 7:
            num_seven_rect = num_one_surf.get_rect(center=(tup[1] * 100 + 100 // 2, tup[0] * 100 + 100 // 2))
            screen.blit(num_seven_surf, num_seven_rect)
        elif board_copy[tup[0]][tup[1]] == 8:
            num_eight_rect = num_eight_surf.get_rect(center=(tup[1] * 100 + 100 // 2, tup[0] * 100 + 100 // 2))
            screen.blit(num_eight_surf, num_eight_rect)
        elif board_copy[tup[0]][tup[1]] == 9:
            num_nine_rect = num_nine_surf.get_rect(center=(tup[1] * 100 + 100 // 2, tup[0] * 100 + 100 // 2))
            screen.blit(num_nine_surf, num_nine_rect)


def draw_game():

    # Initialize Board
    display_grid()
    draw_num()

    # Buttons


def draw_game_over(winner):

    button_font = pygame.font.Font(None, 100)
    cont = True
    backround = pygame.image.load("Sudoku-RIddles-Game-Quiz-Shutterstock.webp")
    backround_new = pygame.transform.scale(backround, (1200, 900))

    if winner:
        screen.fill((255, 255, 255))
        screen.blit(backround_new, (0, 0))
        end_text = "YOU WIN! :D"
        end_surf = game_over_font.render(end_text, 0, (0, 0, 0))
        end_rect = end_surf.get_rect(center=(1200 // 2, 900 // 2 - 50))
        screen.blit(end_surf, end_rect)

        exit_text = button_font.render("Exit", 0, (255, 255, 255))
        exit_surface = pygame.Surface((exit_text.get_size()[0] + 20, exit_text.get_size()[1] + 20))
        exit_surface.fill((255, 165, 0))
        exit_surface.blit(exit_text, (10, 10))

        exit_rectangle = exit_surface.get_rect(center=(1200 // 2, 900 // 2 + 200))
        screen.blit(exit_surface, exit_rectangle)

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if exit_rectangle.collidepoint(event.pos):
                        pygame.quit()
                        sys.exit()
            pygame.display.update()

    else:
        screen.fill((255, 255, 255))
        screen.blit(backround_new, (0, 0))
        end_text = "YOU LOSE! :("
        end_surf = game_over_font.render(end_text, 0, (0, 0, 0))
        end_rect = end_surf.get_rect(center=(1200 // 2, 900 // 2 - 50))
        screen.blit(end_surf, end_rect)

        restart_text = button_font.render("Restart", 0, (255, 255, 255))
        restart_surface = pygame.Surface((restart_text.get_size()[0] + 20, restart_text.get_size()[1] + 20))
        restart_surface.fill((255, 165, 0))
        restart_surface.blit(restart_text, (10, 10))

        restart_rectangle = restart_surface.get_rect(center=(1200 // 2, 900 // 2 + 200))
        screen.blit(restart_surface, restart_rectangle)

        while cont:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if restart_rectangle.collidepoint(event.pos):
                        screen.fill((255, 255, 255))
                        cont = False
            pygame.display.update()


if __name__ == "__main__":
    pygame.init()
    screen = pygame.display.set_mode((1200, 900))
    pygame.display.set_caption("Sudoku")
    number_font = pygame.font.Font(None, 100)
    button_font = pygame.font.Font(None, 100)
    backround = pygame.image.load("Cumulus_clouds_seen_from_10,000_meters_above_the_ground,_2010.jpg")
    backround_new = pygame.transform.scale(backround, (300, 900))

    # Initialize the game state
    removed = 0
    inserted = []
    filled = []
    player = 1
    game_over = False
    winner = False
    game_over_font = pygame.font.Font(None, 100)

    while True:

        game_running = True
        game_over = False
        sol_board, board = draw_game_start()
        board_copy = copy.deepcopy(board)
        board_copy_2 = copy.deepcopy(board)
        sketchable = sudoku_generator.get_sketchable(board)
        filled.extend(sudoku_generator.get_original(board))
        screen.blit(backround_new, (900, 0))
        draw_game()

        reset_text = button_font.render("Reset", 0, (255, 255, 255))
        restart_text = button_font.render("Restart", 0, (255, 255, 255))
        exit_text = button_font.render("Exit", 0, (255, 255, 255))

        reset_surface = pygame.Surface((reset_text.get_size()[0] + 20, reset_text.get_size()[1] + 20))
        reset_surface.fill((255, 165, 0))
        reset_surface.blit(reset_text, (10, 10))
        restart_surface = pygame.Surface((restart_text.get_size()[0] + 20, restart_text.get_size()[1] + 20))
        restart_surface.fill((255, 165, 0))
        restart_surface.blit(restart_text, (10, 10))
        exit_surface = pygame.Surface((exit_text.get_size()[0] + 20, exit_text.get_size()[1] + 20))
        exit_surface.fill((255, 165, 0))
        exit_surface.blit(exit_text, (10, 10))

        reset_rectangle = reset_surface.get_rect(center=(1050, 150))
        restart_rectangle = restart_surface.get_rect(center=(1050, 450))
        exit_rectangle = exit_surface.get_rect(center=(1050, 750))

        screen.blit(reset_surface, reset_rectangle)
        screen.blit(restart_surface, restart_rectangle)
        screen.blit(exit_surface, exit_rectangle)

        while game_running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN and not game_over:
                    x, y = event.pos
                    row = y // 100
                    col = x // 100
                    if sudoku_generator.available_square(board, row, col):
                        screen.fill((255, 255, 255))
                        display_grid()
                        draw_original_values()
                        draw_sketches()
                        screen.blit(backround_new, (900, 0))
                        screen.blit(reset_surface, reset_rectangle)
                        screen.blit(restart_surface, restart_rectangle)
                        screen.blit(exit_surface, exit_rectangle)
                        display_selected(row, col)
                    elif reset_rectangle.collidepoint(event.pos):
                        board_copy = board_copy_2
			board = board_copy_2
                        inserted.clear()
                        filled.clear()
                        filled.extend(sudoku_generator.get_original(board))
                        screen.fill((255, 255, 255))
                        draw_game()
                        screen.blit(backround_new, (900, 0))
                        screen.blit(reset_surface, reset_rectangle)
                        screen.blit(restart_surface, restart_rectangle)
                        screen.blit(exit_surface, exit_rectangle)
                    elif restart_rectangle.collidepoint(event.pos):
                        pygame.display.update()
                        screen.fill((255, 255, 255))
                        inserted.clear()
                        filled.clear()
                        game_running = False
                    elif exit_rectangle.collidepoint(event.pos):
                        pygame.quit()
                        sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP and (row - 1 >= 0):
                        screen.fill((255, 255, 255))
                        display_grid()
                        draw_original_values()
                        draw_sketches()
                        screen.blit(backround_new, (900, 0))
                        screen.blit(reset_surface, reset_rectangle)
                        screen.blit(restart_surface, restart_rectangle)
                        screen.blit(exit_surface, exit_rectangle)
                        display_selected(row - 1, col)
                        row = row - 1
                    elif event.key == pygame.K_DOWN and (row + 1 <= 8):
                        screen.fill((255, 255, 255))
                        display_grid()
                        draw_original_values()
                        draw_sketches()
                        screen.blit(backround_new, (900, 0))
                        screen.blit(reset_surface, reset_rectangle)
                        screen.blit(restart_surface, restart_rectangle)
                        screen.blit(exit_surface, exit_rectangle)
                        display_selected(row + 1, col)
                        row = row + 1
                    elif event.key == pygame.K_RIGHT and (col + 1 <= 8):
                        screen.fill((255, 255, 255))
                        display_grid()
                        draw_original_values()
                        draw_sketches()
                        screen.blit(backround_new, (900, 0))
                        screen.blit(reset_surface, reset_rectangle)
                        screen.blit(restart_surface, restart_rectangle)
                        screen.blit(exit_surface, exit_rectangle)
                        display_selected(row, col + 1)
                        col = col + 1
                    elif event.key == pygame.K_LEFT and (col - 1 >= 0):
                        screen.fill((255, 255, 255))
                        display_grid()
                        draw_original_values()
                        draw_sketches()
                        screen.blit(backround_new, (900, 0))
                        screen.blit(reset_surface, reset_rectangle)
                        screen.blit(restart_surface, restart_rectangle)
                        screen.blit(exit_surface, exit_rectangle)
                        display_selected(row, col - 1)
                        col = col - 1
                if event.type == pygame.KEYDOWN and sudoku_generator.available_again(board, row, col, filled):
                    if event.key == pygame.K_1:
                        if (row, col) not in inserted:
                            board_copy[row][col] = 1
                            inserted.append((row, col))
                            make_sketch(row, col)
                    elif event.key == pygame.K_2:
                        if (row, col) not in inserted:
                            board_copy[row][col] = 2
                            inserted.append((row, col))
                            make_sketch(row, col)
                    elif event.key == pygame.K_3:
                        if (row, col) not in inserted:
                            board_copy[row][col] = 3
                            inserted.append((row, col))
                            make_sketch(row, col)
                    elif event.key == pygame.K_4:
                        if (row, col) not in inserted:
                            board_copy[row][col] = 4
                            inserted.append((row, col))
                            make_sketch(row, col)
                    elif event.key == pygame.K_5:
                        if (row, col) not in inserted:
                            board_copy[row][col] = 5
                            inserted.append((row, col))
                            make_sketch(row, col)
                    elif event.key == pygame.K_6:
                        if (row, col) not in inserted:
                            board_copy[row][col] = 6
                            inserted.append((row, col))
                            make_sketch(row, col)
                    elif event.key == pygame.K_7:
                        if (row, col) not in inserted:
                            board_copy[row][col] = 7
                            inserted.append((row, col))
                            make_sketch(row, col)
                    elif event.key == pygame.K_8:
                        if (row, col) not in inserted:
                            board_copy[row][col] = 8
                            inserted.append((row, col))
                            make_sketch(row, col)
                    elif event.key == pygame.K_9:
                        if (row, col) not in inserted:
                            board_copy[row][col] = 9
                            inserted.append((row, col))
                            make_sketch(row, col)
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_BACKSPACE:
                            board_copy[row][col] = 0
                            inserted.remove((row, col))
                            screen.fill((255, 255, 255))
                            screen.blit(backround_new, (900, 0))
                            screen.blit(reset_surface, reset_rectangle)
                            screen.blit(restart_surface, restart_rectangle)
                            screen.blit(exit_surface, exit_rectangle)
                            draw_game()
                            draw_sketches()
                            display_selected(row, col)
                        if event.key == pygame.K_RETURN:
                            board[row][col] = board_copy[row][col]
                            draw_num()
                            sketchable.remove((row, col))
                            filled.append((row, col))
                            if sudoku_generator.board_is_full(board):
                                if sudoku_generator.check_if_winner(board, sol_board):
                                    game_over = True
                                    winner = True
                                    if game_over:
                                        pygame.display.update()
                                        pygame.time.delay(1500)
                                        draw_game_over(winner)
                                else:
                                    game_over = True
                                    if game_over:
                                        pygame.display.update()
                                        pygame.time.delay(1500)
                                        draw_game_over(winner)
                                        inserted = []
                                        game_running = False
            pygame.display.update()
