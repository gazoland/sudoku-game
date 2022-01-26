import pygame
from pprint import pprint
from random import randrange
import time
import itertools


def board_definitions():
    """Makes all board calculations."""
    # DEFINITIONS
    grid_width = 3  # Always odd
    minigrid_width = 1
    outside_width = 3  # Always odd
    micro_space = 27
    macro_space = 3 * micro_space + 2 * minigrid_width
    upper_left = (20, 100)
    inside_upper_left = [x + outside_width // 2 for x in upper_left]
    inner_length = 8 * ((3 * micro_space + 2 * minigrid_width) + 3) + 3 * micro_space + 2 * minigrid_width  # 771
    size = inner_length + 2 * outside_width // 2
    board_color = (0, 255, 0)
    main_grid_color1 = (0, 0, 0)
    main_grid_color2 = (180, 180, 180)
    mini_grid_color = (255, 0, 0)

    # PARAMETERS
    board = dict()

    board["grid_width"] = grid_width
    board["minigrid_width"] = minigrid_width
    board["outside_width"] = outside_width
    board["micro_space"] = micro_space
    board["macro_space"] = macro_space
    board["upper_left"] = upper_left
    board["inside_upper_left"] = inside_upper_left
    board["inner_length"] = inner_length
    board["size"] = size
    board["board_color"] = board_color

    board["main_grid"] = dict()
    board["main_grid"]["color1"] = main_grid_color1
    board["main_grid"]["color2"] = main_grid_color2

    board["mini_grid"] = dict()
    board["mini_grid"]["color"] = mini_grid_color

    # MAINGRID

    # Vertical
    x_macrogrid = upper_left[0]
    board["main_grid"]["v_lines_coords"] = list()
    for _ in range(8):
        x_macrogrid += macro_space + 3
        board["main_grid"]["v_lines_coords"].append(x_macrogrid)

    # Horizontal
    y_macrogrid = upper_left[1]
    board["main_grid"]["h_lines_coords"] = list()
    for _ in range(8):
        y_macrogrid += macro_space + 3
        board["main_grid"]["h_lines_coords"].append(y_macrogrid)

    # MINIGRID

    # Vertical
    x_minigrid = inside_upper_left[0]
    v_minilines = 0
    c_centers = []
    board["mini_grid"]["v_lines_coords"] = list()
    for _ in range(26):
        cspace_center = x_minigrid + 14
        c_centers.append(cspace_center)
        v_minilines += 1
        x_minigrid += micro_space + 1

        if v_minilines % 3 == 0:
            x_minigrid += grid_width - 1

        else:
            board["mini_grid"]["v_lines_coords"].append(x_minigrid)

    c_centers.append(x_minigrid + 14)

    # Horizontal
    y_minigrid = inside_upper_left[1]
    h_minilines = 0
    l_centers = []
    board["mini_grid"]["h_lines_coords"] = list()
    for _ in range(26):
        lspace_center = y_minigrid + 14
        l_centers.append(lspace_center)
        h_minilines += 1
        y_minigrid += micro_space + 1

        if h_minilines % 3 == 0:
            y_minigrid += grid_width - 1

        else:
            board["mini_grid"]["h_lines_coords"].append(y_minigrid)

    l_centers.append(y_minigrid + 14)

    return board, c_centers, l_centers


def board_drawing(window, board):
    """Draws the board used in the game."""

    # OUTSIDE BOARD

    pygame.draw.rect(window, board["board_color"], (board["upper_left"][0], board["upper_left"][1],
                                                    board["size"], board["size"]), board["outside_width"])

    # MAINGRID

    # Vertical
    v_macrolines = 0
    for x in board["main_grid"]["v_lines_coords"]:

        v_macrolines += 1
        if v_macrolines % 3 == 0:
            color = board["main_grid"]["color1"]
        else:
            color = board["main_grid"]["color2"]

        pygame.draw.line(window, color, start_pos=(x, board["inside_upper_left"][1]),
                         end_pos=(x, board["inside_upper_left"][1] + board["inner_length"]), width=board["grid_width"])

    # Horizontal
    h_macrolines = 0
    for y in board["main_grid"]["h_lines_coords"]:

        h_macrolines += 1
        if h_macrolines % 3 == 0:
            color = board["main_grid"]["color1"]
        else:
            color = board["main_grid"]["color2"]

        pygame.draw.line(window, color, start_pos=(board["inside_upper_left"][0], y),
                         end_pos=(board["inside_upper_left"][0] + board["inner_length"], y), width=board["grid_width"])

    # MINIGRID

    """
    # Vertical
    for x in board["mini_grid"]["v_lines_coords"]:
        pygame.draw.line(window, board["mini_grid"]["color"], start_pos=(x, board["inside_upper_left"][1]),
                         end_pos=(x, board["inside_upper_left"][1] + board["inner_length"]))

    # Horizontal
    for y in board["mini_grid"]["h_lines_coords"]:
        pygame.draw.line(window, board["mini_grid"]["color"], start_pos=(board["inside_upper_left"][0], y),
                         end_pos=(board["inside_upper_left"][0] + board["inner_length"], y))
    """


def grid_systems(c_centers, l_centers):
    """Defines all cells within the board grids, its values and its centers."""
    # cell_size = 85
    half_cell = 42

    minigrid = dict()  # System for note numbers
    maingrid = dict()  # System for guesses and clues
    cells_system = dict()  # System for each single major cell
    quads = {"q1": {"cells": list()}, "q2": {"cells": list()}, "q3": {"cells": list()},
             "q4": {"cells": list()}, "q5": {"cells": list()}, "q6": {"cells": list()},
             "q7": {"cells": list()}, "q8": {"cells": list()}, "q9": {"cells": list()}}
    # System for cells of the 9 quadrants (blocks)

    maingrid_centers = (2, 5, 8, 11, 14, 17, 20, 23, 26)

    line_counter = 1
    cell = 1
    for y_coord in l_centers:

        if line_counter in [1, 4, 7, 10, 13, 16, 19, 22, 25]:
            working_numbers = (1, 2, 3)
        elif line_counter in [2, 5, 8, 11, 14, 17, 20, 23, 26]:
            working_numbers = (4, 5, 6)
        else:
            working_numbers = (7, 8, 9)

        minigrid[f"l{str(line_counter)}"] = dict()

        num_counter = 0
        column_counter = 1

        if line_counter in maingrid_centers:
            maingrid[f"l{str(line_counter)}"] = dict()

        for x_coord in c_centers:
            center = (x_coord, y_coord)
            value = working_numbers[num_counter]

            minigrid[f"l{str(line_counter)}"][f"c{str(column_counter)}"] = {"value": str(value), "center": center,
                                                                            "show": False}

            num_counter += 1
            if num_counter == 3:
                num_counter = 0

            if column_counter in maingrid_centers and line_counter in maingrid_centers:
                x_interval = (x_coord - half_cell, x_coord + half_cell)
                y_interval = (y_coord - half_cell, y_coord + half_cell)
                maingrid[f"l{str(line_counter)}"][f"c{str(column_counter)}"] = {"center": center, "value": None,
                                                                                "clue": False, "show": False,
                                                                                "correct": None,
                                                                                "x_interval": x_interval,
                                                                                "y_interval": y_interval}

                cells_system[cell] = {"center": center, "x_interval": x_interval, "y_interval": y_interval,
                                      "lines": [f"l{str(line_counter - 1)}",
                                                f"l{str(line_counter)}",
                                                f"l{str(line_counter + 1)}"],
                                      "columns": [f"c{str(column_counter - 1)}",
                                                  f"c{str(column_counter)}",
                                                  f"c{str(column_counter + 1)}"]}

                # Top Quads
                if line_counter in [2, 5, 8]:
                    if column_counter in [2, 5, 8]:
                        quads["q1"]["cells"].append(cell)
                        if line_counter == 5 and column_counter == 5:
                            quads["q1"]["center"] = center
                    elif column_counter in [11, 14, 17]:
                        quads["q2"]["cells"].append(cell)
                        if line_counter == 5 and column_counter == 14:
                            quads["q2"]["center"] = center
                    elif column_counter in [20, 23, 26]:
                        quads["q3"]["cells"].append(cell)
                        if line_counter == 5 and column_counter == 23:
                            quads["q3"]["center"] = center

                # Mid Quads
                elif line_counter in [11, 14, 17]:
                    if column_counter in [2, 5, 8]:
                        quads["q4"]["cells"].append(cell)
                        if line_counter == 14 and column_counter == 5:
                            quads["q4"]["center"] = center
                    elif column_counter in [11, 14, 17]:
                        quads["q5"]["cells"].append(cell)
                        if line_counter == 14 and column_counter == 14:
                            quads["q5"]["center"] = center
                    elif column_counter in [20, 23, 26]:
                        quads["q6"]["cells"].append(cell)
                        if line_counter == 14 and column_counter == 23:
                            quads["q6"]["center"] = center

                # Bottom Quads
                elif line_counter in [20, 23, 26]:
                    if column_counter in [2, 5, 8]:
                        quads["q7"]["cells"].append(cell)
                        if line_counter == 23 and column_counter == 5:
                            quads["q7"]["center"] = center
                    elif column_counter in [11, 14, 17]:
                        quads["q8"]["cells"].append(cell)
                        if line_counter == 23 and column_counter == 14:
                            quads["q8"]["center"] = center
                    elif column_counter in [20, 23, 26]:
                        quads["q9"]["cells"].append(cell)
                        if line_counter == 23 and column_counter == 23:
                            quads["q9"]["center"] = center

                cell += 1

            column_counter += 1

        line_counter += 1

    # pprint(minigrid)
    # pprint(maingrid)
    # pprint(cells_system)
    # pprint(quads)

    return maingrid, minigrid, cells_system, quads


def board_writing(*grids):
    """Writes the numbers on each square of the maingrid and minigrid."""

    class ScreenNum:
        def __init__(self, number, grid_type, center, clue, hit):
            self.number = str(number)
            self.center = center

            if grid_type == "main":
                self.font = pygame.font.Font("freesansbold.ttf", 60)
                if clue is True:
                    self.color = (0, 0, 0)
                else:
                    self.color = (52, 97, 246) if hit is True else (250, 40, 40)

            elif grid_type == "mini":
                self.font = pygame.font.Font("freesansbold.ttf", 22)
                self.color = (120, 120, 120)

    # WRITE GRID NUMBERS

    for grid in grids:
        if len(grid.keys()) == 9:
            grid_size = "main"
        else:
            grid_size = "mini"

        num_writes = []
        for grid_line, columns in grid.items():
            for grid_column, attr in columns.items():
                if attr['show'] is True:
                    try:
                        is_given = attr["clue"]
                    except KeyError:  # Minigrid
                        is_given = False
                    try:
                        right_ans = str(attr["correct"])
                        correct = True if right_ans == attr["value"] else False
                    except KeyError:  # Minigrid
                        correct = None

                    num_writes.append(ScreenNum(attr["value"], grid_size, attr["center"], is_given, correct))

        for scr_num in num_writes:
            w_num = scr_num.font.render(scr_num.number, True, scr_num.color)
            screen.blit(w_num, w_num.get_rect(center=scr_num.center))


def cell_selector(x_cursor, y_cursor, cells_system):
    """Identifies if a click is made within a cell."""
    class Coordinates(tuple):
        def contains(self, coord):
            return min(self) <= coord <= max(self)

    # cell_size = 85 x 85

    for cell, attr in cells_system.items():
        x_interval = Coordinates(attr["x_interval"])
        y_interval = Coordinates(attr["y_interval"])

        if x_interval.contains(x_cursor) and y_interval.contains(y_cursor):  # If click is within cell
            return [attr["center"], attr["lines"], attr["columns"], cell]

    return [None, None, None, None]


def cell_highlighting(cell_params, quadrants):
    """Highlights the cell, its whole column, line and block (quadrant) when selected."""
    quad_center = None
    # center: (407, 487)
    for quad, attr in quadrants.items():
        if cell_params[3] in attr["cells"]:
            quad_center = attr["center"]

    cell_rect = pygame.Rect(200, 100, 81, 81)
    fill_rect = pygame.Rect(200, 100, 79, 79)
    fill_column = pygame.Rect(200, 100, 83, 777)
    fill_line = pygame.Rect(200, 100, 777, 83)
    fill_quad = pygame.Rect(200, 100, 263, 263)
    cell_rect.center = cell_params[0]
    fill_rect.center = cell_params[0]
    fill_column.center = (cell_params[0][0], 487)
    fill_line.center = (407, cell_params[0][1])
    fill_quad.center = quad_center

    screen.fill((235, 235, 235), rect=fill_quad)
    screen.fill((235, 235, 235), rect=fill_column)
    screen.fill((235, 235, 235), rect=fill_line)
    pygame.draw.rect(screen, (0, 100, 255), cell_rect, 5)
    screen.fill((175, 175, 175), rect=fill_rect)


def button_selector(x_cursor, y_cursor, button_interval, current_state):
    """Identifies if a click is made within a button."""
    class Coordinates(tuple):
        def contains(self, coord):
            return min(self) <= coord <= max(self)

    x_interval = Coordinates(button_interval["x_interval"])
    y_interval = Coordinates(button_interval["y_interval"])

    return not current_state if x_interval.contains(x_cursor) and y_interval.contains(y_cursor) else current_state


def num_writing_engine(num, cell_params):
    """Erases notes where there would be a conflict of numbers within a cell's line, column or block (quadrant)."""
    # Write guess
    main_grid[cell_params[1][1]][cell_params[2][1]]["value"] = num
    main_grid[cell_params[1][1]][cell_params[2][1]]["show"] = True

    # ERASING CONFLICTING NOTES
    for cell_line in cell_params[1]:

        # Erase notes of that cell
        for cell_column in cell_params[2]:
            mini_grid[cell_line][cell_column]["show"] = False

        # Erase equal notes on that line
        for mini_col, attr in mini_grid[cell_line].items():
            if attr["value"] == num:
                attr["show"] = False

    # Erase equal notes on that column
    for mini_line, col_attr in mini_grid.items():
        for mini_col, attr in col_attr.items():
            if mini_col in cell_params[2] and num == attr["value"]:
                attr["show"] = False  # Changes dict "mini_grid" globally

    # Erase notes on that quadrant
    for quad, content in board_quads.items():
        if cell_params[3] in content["cells"]:
            cells_to_erase = [x for x in content["cells"]]
            cells_to_erase.remove(cell_params[3])

            for cell in cells_to_erase:
                cell_lines = main_cells[cell]["lines"]
                cell_columns = main_cells[cell]["columns"]
                for cell_line in cell_lines:
                    for cell_column in cell_columns:
                        if mini_grid[cell_line][cell_column]["value"] == num:
                            mini_grid[cell_line][cell_column]["show"] = False  # Changes dict "mini_grid" globally

    # pprint(main_grid)


def game_generator_engine():
    """Creates random sudoku board and validates the board as a valid sudoku game."""

    def num_generator(*args):
        """Generates a random number between 1 and 10."""
        n = randrange(1, 10)
        els = []
        for arg in args:
            els += arg

        els = list(filter((0).__ne__, els))
        if len(set(els)) == 9:
            return 0
        else:
            while n in els:
                n = randrange(1, 10)
            return n

    def board_generator():
        """Using random numbers from 1 to 10, iterates through 9 lines of 9 digits and makes sure the digits don't
        repeat themselves within a line, column or block. Usually takes less than 0.1 seconds."""
        iterate = True
        its = 1
        start = time.time()
        g_lines = None
        while iterate:
            nn = 10

            g_lines = [[0 for _ in range(9)] for _ in range(9)]
            g_columns = [[0 for _ in range(9)] for _ in range(9)]
            g_blocks = [[0 for _ in range(9)] for _ in range(9)]

            line_counter = 0
            block_line = 0
            for g_line in g_lines:
                col_counter = 0

                for _ in g_line:
                    block_counter = 0
                    block_pos = 0

                    if line_counter in [0, 1, 2]:
                        if col_counter in [0, 1, 2]:
                            block_counter = 0
                        elif col_counter in [3, 4, 5]:
                            block_counter = 1
                        elif col_counter in [6, 7, 8]:
                            block_counter = 2
                    elif line_counter in [3, 4, 5]:
                        if col_counter in [0, 1, 2]:
                            block_counter = 3
                        elif col_counter in [3, 4, 5]:
                            block_counter = 4
                        elif col_counter in [6, 7, 8]:
                            block_counter = 5
                    elif line_counter in [6, 7, 8]:
                        if col_counter in [0, 1, 2]:
                            block_counter = 6
                        elif col_counter in [3, 4, 5]:
                            block_counter = 7
                        elif col_counter in [6, 7, 8]:
                            block_counter = 8

                    if block_line == 0:
                        if col_counter in [0, 3, 6]:
                            block_pos = 0
                        elif col_counter in [1, 4, 7]:
                            block_pos = 1
                        elif col_counter in [2, 5, 8]:
                            block_pos = 2
                    elif block_line == 1:
                        if col_counter in [0, 3, 6]:
                            block_pos = 3
                        elif col_counter in [1, 4, 7]:
                            block_pos = 4
                        elif col_counter in [2, 5, 8]:
                            block_pos = 5
                    elif block_line == 2:
                        if col_counter in [0, 3, 6]:
                            block_pos = 6
                        elif col_counter in [1, 4, 7]:
                            block_pos = 7
                        elif col_counter in [2, 5, 8]:
                            block_pos = 8

                    nn = num_generator(g_lines[line_counter], g_columns[col_counter], g_blocks[block_counter])
                    if nn == 0:
                        break
                    g_lines[line_counter][col_counter] = nn
                    g_columns[col_counter][line_counter] = nn
                    g_blocks[block_counter][block_pos] = nn

                    col_counter += 1

                if nn == 0:
                    its += 1
                    break
                line_counter += 1
                block_line += 1
                if block_line > 2:
                    block_line = 0

            if g_lines[8][8] != 0:
                iterate = False

        end = time.time()
        print(end - start)
        print(f"iterations: {str(its)}")
        pprint(g_lines)
        return g_lines

    def validate_board(board):
        """Takes on a possible sudoku board and checks if it is a valid sudoku game."""
        valid = False

        while not valid:
            # Check lines
            for el in board:
                if len(set(el)) != 9 or 0 in el or max(el) > 9 or min(el) < 1:
                    valid = False
                    break
                else:
                    valid = True
            if not valid:
                continue

            # Check columns
            board_columns = zip(*board)
            for c in board_columns:
                if len(set(c)) != 9 or 0 in c or max(c) > 9 or min(c) < 1:
                    valid = False
                    break
                else:
                    valid = True
            if not valid:
                continue

            # Check blocks
            blocks = [[board[x + a][y + b] for a in (0, 1, 2) for b in (0, 1, 2)] for x in (0, 3, 6) for y in (0, 3, 6)]
            for b in blocks:
                if len(set(b)) != 9 or 0 in b or max(b) > 9 or min(b) < 1:
                    valid = False
                    break
                else:
                    valid = True

        return valid

    is_valid = False
    game_board = None
    while not is_valid:
        game_board = board_generator()
        is_valid = validate_board(game_board)

    return game_board


def starting_board_generator(game_board, maingrid, cells_system, to_leave):
    """Generates the initial board for the game with clues and empty cells."""
    # Putting every number in its cell
    l_index = 2  # Miniline index for main cells
    for board_line in game_board:
        c_index = 2  # Minicolumn index for main cells
        for col_num in board_line:
            maingrid[f"l{str(l_index)}"][f"c{str(c_index)}"]["value"] = col_num
            maingrid[f"l{str(l_index)}"][f"c{str(c_index)}"]["clue"] = True
            maingrid[f"l{str(l_index)}"][f"c{str(c_index)}"]["show"] = True
            maingrid[f"l{str(l_index)}"][f"c{str(c_index)}"]["correct"] = col_num
            c_index += 3
        l_index += 3

    # Leaving only [to_leave] numbers as clue
    retry = True
    board_list = []
    while retry:
        board_list = list(itertools.chain.from_iterable(game_board))  # Makes a list out of all board numbers
        left = 81
        while left > to_leave:
            idx = 100  # arbitrary
            gen_idx = True
            while gen_idx:
                idx = randrange(0, 81)
                gen_idx = board_list[idx] is None

            board_list[idx] = None
            left -= 1

        if len(set(board_list)) >= 9:  # Prevents total absence of two different numbers on the board
            retry = False

    for i in range(len(board_list)):
        if board_list[i] is None:
            main_line = cells_system[i+1]["lines"][1]
            main_column = cells_system[i+1]["columns"][1]
            maingrid[main_line][main_column]["show"] = False
            maingrid[main_line][main_column]["clue"] = False
            maingrid[main_line][main_column]["value"] = None

    return maingrid


def key_pressing(key, cell):
    """Response to the respective key when pressed."""
    # Numbers
    number_keys = [str(x) for x in range(1, 10)]
    if key in number_keys:
        number = key
        return number, cell

    elif cell[0] is not None:  # If a cell is selected
        if key == "backspace":  # Erase cell with backspace
            main_grid[cell[1][1]][cell[2][1]]["value"] = None
            main_grid[cell[1][1]][cell[2][1]]["show"] = False
            for mini_l in cell[1]:
                for mini_c in cell[2]:
                    mini_grid[mini_l][mini_c]["show"] = False
            return None, cell

        elif key in ["up", "down", "left", "right"]:  # Arrow cell navigation
            if key == "up" and cell[1][1] != "l2":
                new_line = int(cell[1][1].replace("l", "")) - 3
                center = main_grid[f"l{str(new_line)}"][cell[2][1]]["center"]
                cell_idx = reversed_cells[center]
                return None, [main_cells[cell_idx]["center"], main_cells[cell_idx]["lines"],
                              main_cells[cell_idx]["columns"], cell_idx]

            elif key == "down" and cell[1][1] != "l26":
                new_line = int(cell[1][1].replace("l", "")) + 3
                center = main_grid[f"l{str(new_line)}"][cell[2][1]]["center"]
                cell_idx = reversed_cells[center]
                return None, [main_cells[cell_idx]["center"], main_cells[cell_idx]["lines"],
                              main_cells[cell_idx]["columns"], cell_idx]

            elif key == "left" and cell[2][1] != "c2":
                new_column = int(cell[2][1].replace("c", "")) - 3
                center = main_grid[cell[1][1]][f"c{str(new_column)}"]["center"]
                cell_idx = reversed_cells[center]
                return None, [main_cells[cell_idx]["center"], main_cells[cell_idx]["lines"],
                              main_cells[cell_idx]["columns"], cell_idx]

            elif key == "right" and cell[2][1] != "c26":
                new_column = int(cell[2][1].replace("c", "")) + 3
                center = main_grid[cell[1][1]][f"c{str(new_column)}"]["center"]
                cell_idx = reversed_cells[center]
                return None, [main_cells[cell_idx]["center"], main_cells[cell_idx]["lines"],
                              main_cells[cell_idx]["columns"], cell_idx]

    return None, cell


def win_verification():
    """Checks for game-winning conditions."""
    win = False
    for main_line, main_columns in main_grid.items():
        for main_column, props in main_columns.items():
            if str(props["value"]) == str(props["correct"]) and props["show"] is True:
                win = True
            else:
                win = False
                break
        if win is False:
            break
    return win


def wrong_moves(lives):
    """Looks for a wrong number put in by the player and decreases its lives by 1 for each mistake made."""
    global wrong_move
    wrong_counter = 0
    to_remove = []
    for main_line, main_columns in main_grid.items():
        for main_column, props in main_columns.items():
            if str(props["value"]) != str(props["correct"]) and props["show"] is True:
                for w in wrong_move:
                    if w[:-2] == f"{main_line}{main_column}" and w[-1] != str(props["value"]):
                        to_remove.append(w)
                if len(to_remove) > 0:
                    wrong_move = [x for x in wrong_move if x not in to_remove]
                wrong_counter += 1
                wrong_string = f"{main_line}{main_column}v{str(props['value'])}"
                if wrong_string not in wrong_move:
                    wrong_move.append(wrong_string)
                    lives -= 1

    if wrong_counter == 0:
        wrong_move = []

    return lives


class Buttons:
    def __init__(self, outer, outer_color, inner_color, center, interval, font, text, text_color):
        pass


if __name__ == '__main__':
    full_game_board = game_generator_engine()

    # Initialize window for game
    pygame.init()

    # Create screen
    screen = pygame.display.set_mode([1200, 900])

    # Board
    board_metrics, columns_centers, lines_centers = board_definitions()
    main_grid, mini_grid, main_cells, board_quads = grid_systems(columns_centers, lines_centers)
    main_grid = starting_board_generator(full_game_board, main_grid, main_cells, to_leave=35)
    reversed_cells = {v["center"]: k for k, v in main_cells.items()}

    # Note button
    note_button_center = (1000, 200)
    note_button_out = pygame.Rect(200, 100, 120, 50)
    note_button_in = pygame.Rect(200, 100, 117, 47)
    note_button_interval = {"x_interval": (940, 1060), "y_interval": (175, 225)}
    note_button_out.center = note_button_center
    note_button_in.center = note_button_center
    note_button_font = pygame.font.Font("freesansbold.ttf", 22)
    note_text = note_button_font.render("Notes", True, (50, 50, 50))

    selected_cell = [None, None, None, None]
    note_button = False
    lives_left = 3
    wrong_move = []

    # Run window

    run = True

    while run:
        write_num = None
        note_button_color = (230, 230, 230)
        if note_button:
            note_button_color = (120, 120, 120)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # Check if quit button was clicked
                run = False
            elif event.type == pygame.MOUSEBUTTONDOWN:  # Check for cell highlighting
                mouse_pos = pygame.mouse.get_pos()
                selected_cell = cell_selector(mouse_pos[0], mouse_pos[1], main_cells)
                if selected_cell[0] is None:
                    note_button = button_selector(mouse_pos[0], mouse_pos[1], note_button_interval, note_button)

            elif event.type == pygame.KEYDOWN:  # Check for keyboard number entry
                pressed_key = pygame.key.name(event.key).replace("[", "").replace("]", "")
                write_num, selected_cell = key_pressing(pressed_key, selected_cell)

        # Fill board with white colour
        screen.fill((255, 255, 255))

        # Notes button

        pygame.draw.rect(screen, (20, 20, 20), note_button_out, 4)
        screen.fill(note_button_color, rect=note_button_in)
        screen.blit(note_text, note_text.get_rect(center=note_button_center))

        # Cell selection
        if selected_cell[0] is not None:
            cell_highlighting(selected_cell, board_quads)

            # Writing guesses on cell if it's not a clue
            if write_num is not None and not note_button and \
                    main_grid[selected_cell[1][1]][selected_cell[2][1]]["clue"] is False:
                num_writing_engine(write_num, selected_cell)

            # Writing note numbers
            elif write_num is not None and note_button and \
                    main_grid[selected_cell[1][1]][selected_cell[2][1]]["show"] is False:

                for line in selected_cell[1]:
                    for column in selected_cell[2]:
                        if mini_grid[line][column]["value"] == write_num:
                            mini_grid[line][column]["show"] = not mini_grid[line][column]["show"]

        # Writing all guesses, notes and clues
        board_writing(main_grid, mini_grid)

        # Create board
        board_drawing(screen, board_metrics)

        # Verify win
        win_condition = win_verification()
        if win_condition:
            run = False

        # Verify mistakes
        lives_left = wrong_moves(lives_left)
        if lives_left == 0:
            run = False

        # Flip the display
        pygame.display.flip()

    # Quit
    pygame.quit()
