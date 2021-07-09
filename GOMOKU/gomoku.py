### general data
# import packages
import collections
import math
import random

import pisqpipe as pp
from pisqpipe import DEBUG_EVAL, DEBUG

# project version
pp.infotext = 'name="pbrain-16307110232", author="Deng Qisheng", version="5.0", country="China", www="https://github.com/DengQisheng"'

# board setting
MAX_BOARD = 20
board = [[0 for y in range(MAX_BOARD)] for x in range(MAX_BOARD)]    # (x, y): (row, column)


### evaluators
class Evaluator():

    def __init__(self):
        
        # the size of board
        self.HEIGHT = pp.height
        self.WIDTH = pp.width

    # functions for self.is_terminal()
    def check_horz_win(self, turn: int) -> bool:

        '''
        Check whether there is a win pattern in horizontal direction.
        '''

        # traverse all horizontal patterns in the current board
        for x in range(self.HEIGHT):

            # store the pattern in given row
            row = [self.grid[x][i] for i in range(5)]
            if self.is_win_pattern(turn, row): return True

            for y in range(5, self.WIDTH):

                # traverse the pattern in given row
                row.pop(0); row.append(self.grid[x][y])
                if self.is_win_pattern(turn, row): return True

        return False

    def check_vert_win(self, turn: int) -> bool:

        '''
        Check whether there is a win pattern in vertical direction.
        '''

        # traverse all vertical patterns in the current board
        for y in range(self.WIDTH):

            # store the pattern in given column
            column = [self.grid[i][y] for i in range(5)]
            if self.is_win_pattern(turn, column): return True

            for x in range(5, self.HEIGHT):

                # traverse the pattern in given column
                column.pop(0); column.append(self.grid[x][y])
                if self.is_win_pattern(turn, column): return True

        return False

    def check_left_diag_win(self, turn: int) -> bool:

        '''
        Check whether there is a win pattern in left diagonal direction.
        '''
        
        # traverse all left diagonal patterns in lower-left half of the current board
        for x in range(0, self.HEIGHT - 4):    # including principal left diagonal

            # store the pattern in given left diagonal
            left_diag = [self.grid[x + i][i] for i in range(5)]
            if self.is_win_pattern(turn, left_diag): return True

            for y in range(5, self.WIDTH - x):

                # traverse the pattern in given left diagonal
                left_diag.pop(0); left_diag.append(self.grid[x + y][y])
                if self.is_win_pattern(turn, left_diag): return True
                
        # traverse all left diagonal patterns in upper-right half of the current board
        for y in range(1, self.WIDTH - 4):

            # store the pattern in given left diagonal
            left_diag = [self.grid[i][y + i] for i in range(5)]
            if self.is_win_pattern(turn, left_diag): return True

            for x in range(5, self.HEIGHT - y):
                
                # traverse the pattern in given left diagonal
                left_diag.pop(0); left_diag.append(self.grid[x][x + y])
                if self.is_win_pattern(turn, left_diag): return True

        return False

    def check_right_diag_win(self, turn: int) -> bool:

        '''
        Check whether there is a win pattern in right diagonal direction.
        '''

        # traverse all right diagonal patterns in upper-left half of the current board
        for y in range(4, self.WIDTH):    # including principal right diagonal
            
            # store the pattern in given right diagonal
            right_diag = [self.grid[i][y - i] for i in range(5)]
            if self.is_win_pattern(turn, right_diag): return True

            for x in range(5, y + 1):
                
                # traverse the pattern in given right diagonal
                right_diag.pop(0); right_diag.append(self.grid[x][x - y])
                if self.is_win_pattern(turn, right_diag): return True

        # traverse all right diagonal patterns in lower-right half of the current board
        for x in range(self.HEIGHT - 5, 0, -1):
            
            # store the pattern in given right diagonal
            right_diag = [self.grid[x + i][self.WIDTH - 1 - i] for i in range(5)]
            if self.is_win_pattern(turn, right_diag): return True

            for y in range(self.WIDTH - 6, x - 1, -1):

                # traverse the pattern in given right diagonal
                right_diag.pop(0); right_diag.append(self.grid[self.HEIGHT - 1 + x - y][y])
                if self.is_win_pattern(turn, right_diag): return True

        return False

    def is_win_pattern(self, turn: int, pattern: list) -> bool:

        '''
        Check whether the pattern is winning.
        '''
        return [turn] * 5  == pattern    # turn: 1 -> pattern: [1, 1, 1, 1, 1], turn: 2 -> pattern: [2, 2, 2, 2, 2]

    def is_win(self, turn: int) -> bool:

        '''
        Check whether the current board is in the WIN state.
        '''
        return self.check_horz_win(turn) or self.check_vert_win(turn) or \
               self.check_left_diag_win(turn) or self.check_right_diag_win(turn)

    def is_draw(self) -> bool:

        '''
        Check whether the current board is in the DRAW state.
        '''
        for x in range(self.HEIGHT):
            for y in range(self.WIDTH):
                if self.grid[x][y] == 0: return False    # still have a next move
        return True    # full of pieces

    def is_terminal(self, grid: list, turn: int) -> int:
        
        '''
        Check whether the board is in the WIN (1) or DRAW (-1) state.
        '''
        self.grid = grid    # update the current grid
        if self.is_win(turn): return 1    # the board is in the WIN state
        elif self.is_draw(): return -1    # the board is in the DRAW state
        else: return 0    # the board is not the terminal

    # functions for self.get_next_moves()
    def is_free_move(self, x: int, y: int) -> bool:
        
        '''
        Check whether position (x, y) is available and free (with value 0).
        '''
        return 0 <= x < self.HEIGHT and 0 <= y < self.WIDTH and self.grid[x][y] == 0
    
    def is_legal_move(self, pos: tuple) -> bool:
        
        '''
        Check whether the position = (x, y) is legal.
        '''
        return 0 <= pos[0] < self.HEIGHT and 0 <= pos[1] < self.WIDTH
    
    def get_horz_pattern(self, x: int, y: int) -> tuple:

        '''
        Return the nearby positions with their kinds in horizontal direction.
        '''

        # positions
        l1_p, l2_p, l3_p, l4_p, l5_p = (x, y - 1), (x, y - 2), (x, y - 3), (x, y - 4), (x, y - 5)
        r1_p, r2_p, r3_p, r4_p, r5_p = (x, y + 1), (x, y + 2), (x, y + 3), (x, y + 4), (x, y + 5)

        # kinds
        l1_v = self.grid[x][y - 1] if self.is_legal_move(l1_p) else -1
        l2_v = self.grid[x][y - 2] if self.is_legal_move(l2_p) else -1
        l3_v = self.grid[x][y - 3] if self.is_legal_move(l3_p) else -1
        l4_v = self.grid[x][y - 4] if self.is_legal_move(l4_p) else -1
        l5_v = self.grid[x][y - 5] if self.is_legal_move(l5_p) else -1
        r1_v = self.grid[x][y + 1] if self.is_legal_move(r1_p) else -1
        r2_v = self.grid[x][y + 2] if self.is_legal_move(r2_p) else -1
        r3_v = self.grid[x][y + 3] if self.is_legal_move(r3_p) else -1
        r4_v = self.grid[x][y + 4] if self.is_legal_move(r4_p) else -1
        r5_v = self.grid[x][y + 5] if self.is_legal_move(r5_p) else -1

        return l1_v, l2_v, l3_v, l4_v, l5_v, r1_v, r2_v, r3_v, r4_v, r5_v

    def get_vert_pattern(self, x: int, y: int) -> tuple:

        '''
        Return the nearby positions with their kinds in vertical direction.
        '''

        # positions
        l1_p, l2_p, l3_p, l4_p, l5_p = (x - 1, y), (x - 2, y), (x - 3, y), (x - 4, y), (x - 5, y)
        r1_p, r2_p, r3_p, r4_p, r5_p = (x + 1, y), (x + 2, y), (x + 3, y), (x + 4, y), (x + 5, y)

        # kinds
        l1_v = self.grid[x - 1][y] if self.is_legal_move(l1_p) else -1
        l2_v = self.grid[x - 2][y] if self.is_legal_move(l2_p) else -1
        l3_v = self.grid[x - 3][y] if self.is_legal_move(l3_p) else -1
        l4_v = self.grid[x - 4][y] if self.is_legal_move(l4_p) else -1
        l5_v = self.grid[x - 5][y] if self.is_legal_move(l5_p) else -1
        r1_v = self.grid[x + 1][y] if self.is_legal_move(r1_p) else -1
        r2_v = self.grid[x + 2][y] if self.is_legal_move(r2_p) else -1
        r3_v = self.grid[x + 3][y] if self.is_legal_move(r3_p) else -1
        r4_v = self.grid[x + 4][y] if self.is_legal_move(r4_p) else -1
        r5_v = self.grid[x + 5][y] if self.is_legal_move(r5_p) else -1

        return l1_v, l2_v, l3_v, l4_v, l5_v, r1_v, r2_v, r3_v, r4_v, r5_v

    def get_left_diag_pattern(self, x: int, y: int) -> tuple:
        
        '''
        Return the nearby positions with their kinds in left diagonal direction.
        '''

        # positions
        l1_p, l2_p, l3_p, l4_p, l5_p = (x - 1, y - 1), (x - 2, y - 2), (x - 3, y - 3), (x - 4, y - 4), (x - 5, y - 5)
        r1_p, r2_p, r3_p, r4_p, r5_p = (x + 1, y + 1), (x + 2, y + 2), (x + 3, y + 3), (x + 4, y + 4), (x + 5, y + 5)

        # kinds
        l1_v = self.grid[x - 1][y - 1] if self.is_legal_move(l1_p) else -1
        l2_v = self.grid[x - 2][y - 2] if self.is_legal_move(l2_p) else -1
        l3_v = self.grid[x - 3][y - 3] if self.is_legal_move(l3_p) else -1
        l4_v = self.grid[x - 4][y - 4] if self.is_legal_move(l4_p) else -1
        l5_v = self.grid[x - 5][y - 5] if self.is_legal_move(l5_p) else -1
        r1_v = self.grid[x + 1][y + 1] if self.is_legal_move(r1_p) else -1
        r2_v = self.grid[x + 2][y + 2] if self.is_legal_move(r2_p) else -1
        r3_v = self.grid[x + 3][y + 3] if self.is_legal_move(r3_p) else -1
        r4_v = self.grid[x + 4][y + 4] if self.is_legal_move(r4_p) else -1
        r5_v = self.grid[x + 5][y + 5] if self.is_legal_move(r5_p) else -1

        return l1_v, l2_v, l3_v, l4_v, l5_v, r1_v, r2_v, r3_v, r4_v, r5_v

    def get_right_diag_pattern(self, x: int, y: int) -> tuple:

        '''
        Return the nearby positions with their kinds in right diagonal direction.
        '''

        # positions
        l1_p, l2_p, l3_p, l4_p, l5_p = (x + 1, y - 1), (x + 2, y - 2), (x + 3, y - 3), (x + 4, y - 4), (x + 5, y - 5)
        r1_p, r2_p, r3_p, r4_p, r5_p = (x - 1, y + 1), (x - 2, y + 2), (x - 3, y + 3), (x - 4, y + 4), (x - 5, y + 5)

        # kinds
        l1_v = self.grid[x + 1][y - 1] if self.is_legal_move(l1_p) else -1
        l2_v = self.grid[x + 2][y - 2] if self.is_legal_move(l2_p) else -1
        l3_v = self.grid[x + 3][y - 3] if self.is_legal_move(l3_p) else -1
        l4_v = self.grid[x + 4][y - 4] if self.is_legal_move(l4_p) else -1
        l5_v = self.grid[x + 5][y - 5] if self.is_legal_move(l5_p) else -1
        r1_v = self.grid[x - 1][y + 1] if self.is_legal_move(r1_p) else -1
        r2_v = self.grid[x - 2][y + 2] if self.is_legal_move(r2_p) else -1
        r3_v = self.grid[x - 3][y + 3] if self.is_legal_move(r3_p) else -1
        r4_v = self.grid[x - 4][y + 4] if self.is_legal_move(r4_p) else -1
        r5_v = self.grid[x - 5][y + 5] if self.is_legal_move(r5_p) else -1

        return l1_v, l2_v, l3_v, l4_v, l5_v, r1_v, r2_v, r3_v, r4_v, r5_v

    def search_forced_moves(self, move: tuple):

        '''
        Calculate the evaluation value of the specific move in AI's turn.
        '''

        # initialize basic data
        value = 0    # heuristic value
        ILLEGAL, NULL, AI, OPP = -1, 0, self.turn, 3 - self.turn    # value -1: illegal, value 0: null, value 1: myself, value 2: opponent
        x, y = move[0], move[1]    # move: (x, y)

        # special shapes
        four_win_shape = 0    # double-four win
        four_lost_shape = 0    # double-four lost
        three_win_shape = 0    # double-three win
        three_lost_shape = 0    # double-three lost
        
        # get pattern data
        pattern_data = [
            self.get_horz_pattern(x, y),
            self.get_vert_pattern(x, y),
            self.get_left_diag_pattern(x, y),
            self.get_right_diag_pattern(x, y)
        ]

        # search in four directions
        for l1, l2, l3, l4, l5, r1, r2, r3, r4, r5 in pattern_data:

            # the threat level of patterns
            threat = 1

            # 5-in-line (shape of 4)
            if threat <= 5:

                # 5-in-line to win (shape of 4)
                if l4 == l3 == l2 == l1 == AI: value += 750000000; threat = 5
                if l3 == l2 == l1 == r1 == AI: value += 750000000; threat = 5
                if l2 == l1 == r1 == r2 == AI: value += 750000000; threat = 5
                if l1 == r1 == r2 == r3 == AI: value += 750000000; threat = 5
                if r1 == r2 == r3 == r4 == AI: value += 750000000; threat = 5

                # 5-in-line to block (shape of 4)
                if l4 == l3 == l2 == l1 == OPP: value += 150000000; threat = 5
                if l3 == l2 == l1 == r1 == OPP: value += 150000000; threat = 5
                if l2 == l1 == r1 == r2 == OPP: value += 150000000; threat = 5
                if l1 == r1 == r2 == r3 == OPP: value += 150000000; threat = 5
                if r1 == r2 == r3 == r4 == OPP: value += 150000000; threat = 5

            # 4-in-line (shape of 3)
            if threat <= 4:

                # 4-in-line to win (shape of 3)
                if l3 == l2 == l1 == AI:
                    if l4 == NULL and r1 == NULL: value += 5000000; four_win_shape += 1; threat = 4
                    elif l4 == OPP and r1 == NULL: value += 300
                    elif l4 == ILLEGAL and r1 == NULL: value += 250
                    elif l4 == NULL and r1 == OPP: value += 100
                    elif l4 == NULL and r1 == ILLEGAL: value += 80
                    elif l4 == OPP and r1 == OPP: value += -100
                    elif l4 == ILLEGAL and r1 == OPP: value += -200
                    elif l4 == OPP and r1 == ILLEGAL: value += -300
                if l2 == l1 == r1 == AI:
                    if l3 == NULL and r2 == NULL: value += 2500000; four_win_shape += 1; threat = 4
                    elif l3 == OPP and r2 == NULL: value += 250
                    elif l3 == ILLEGAL and r2 == NULL: value += 200
                    elif l3 == NULL and r2 == OPP: value += 150
                    elif l3 == NULL and r2 == ILLEGAL: value += 100
                    elif l3 == OPP and r2 == OPP: value += -100
                    elif l3 == ILLEGAL and r2 == OPP: value += -200
                    elif l3 == OPP and r2 == ILLEGAL: value += -300
                if l1 == r1 == r2 == AI:
                    if r3 == NULL and l2 == NULL: value += 2500000; four_win_shape += 1; threat = 4
                    elif r3 == OPP and l2 == NULL: value += 250
                    elif r3 == ILLEGAL and l2 == NULL: value += 200
                    elif r3 == NULL and l2 == OPP: value += 150
                    elif r3 == NULL and l2 == ILLEGAL: value += 100
                    elif r3 == OPP and l2 == OPP: value += -100
                    elif r3 == ILLEGAL and l2 == OPP: value += -200
                    elif r3 == OPP and l2 == ILLEGAL: value += -300
                if r1 == r2 == r3 == AI:
                    if r4 == NULL and l1 == NULL: value += 5000000; four_win_shape += 1; threat = 4
                    elif r4 == OPP and l1 == NULL: value += 300
                    elif r4 == ILLEGAL and l1 == NULL: value += 250
                    elif r4 == NULL and l1 == OPP: value += 100
                    elif r4 == NULL and l1 == ILLEGAL: value += 80
                    elif r4 == OPP and l1 == OPP: value += -100
                    elif r4 == ILLEGAL and l1 == OPP: value += -200
                    elif r4 == OPP and l1 == ILLEGAL: value += -300
                if l4 == l2 == l1 == AI and l3 == NULL: 
                    if l5 == NULL: value += 25000; four_win_shape += 1; threat = 4
                    elif l5 == OPP: value += 400
                    elif l5 == ILLEGAL: value += 300
                if l4 == l3 == l1 == AI and l2 == NULL: 
                    if l5 == NULL: value += 20000; four_win_shape += 1; threat = 4
                    elif l5 == OPP: value += 350
                    elif l5 == ILLEGAL: value += 250
                if l4 == l3 == l2 == AI and l1 == NULL: 
                    if l5 == NULL: value += 10000; four_win_shape += 1; threat = 4
                    elif l5 == OPP: value += 450
                    elif l5 == ILLEGAL: value += 350
                if r2 == r3 == r4 == AI and r1 == NULL: 
                    if r5 == NULL: value += 10000; four_win_shape += 1; threat = 4
                    elif r5 == OPP: value += 450
                    elif r5 == ILLEGAL: value += 350
                if r1 == r3 == r4 == AI and r2 == NULL: 
                    if r5 == NULL: value += 20000; four_win_shape += 1; threat = 4
                    elif r5 == OPP: value += 350
                    elif r5 == ILLEGAL: value += 250
                if r1 == r2 == r4 == AI and r3 == NULL:
                    if r5 == NULL: value += 25000; four_win_shape += 1; threat = 4
                    elif r5 == OPP: value += 400
                    elif r5 == ILLEGAL: value += 300

                # 4-in-line to block (shape of 3)
                if l3 == l2 == l1 == OPP:
                    if l4 == NULL and r1 == NULL: value += 1000000; four_lost_shape += 1; threat = 4
                    elif l4 == AI and r1 == NULL: value += 300
                    elif l4 == ILLEGAL and r1 == NULL: value += 250
                    elif l4 == NULL and r1 == AI: value += 100
                    elif l4 == NULL and r1 == ILLEGAL: value += 80
                    elif l4 == AI and r1 == AI: value += -100
                    elif l4 == ILLEGAL and r1 == AI: value += -200
                    elif l4 == AI and r1 == ILLEGAL: value += -300
                if l2 == l1 == r1 == OPP:
                    if l3 == NULL and r2 == NULL: value += 2000000; four_lost_shape += 1; threat = 4
                    elif l3 == AI and r2 == NULL: value += 250
                    elif l3 == ILLEGAL and r2 == NULL: value += 200
                    elif l3 == NULL and r2 == AI: value += 150
                    elif l3 == NULL and r2 == ILLEGAL: value += 100
                    elif l3 == AI and r2 == AI: value += -100
                    elif l3 == ILLEGAL and r2 == AI: value += -200
                    elif l3 == AI and r2 == ILLEGAL: value += -300
                if l1 == r1 == r2 == OPP:
                    if r3 == NULL and l2 == NULL: value += 2000000; four_lost_shape += 1; threat = 4
                    elif r3 == AI and l2 == NULL: value += 250
                    elif r3 == ILLEGAL and l2 == NULL: value += 200
                    elif r3 == NULL and l2 == AI: value += 150
                    elif r3 == NULL and l2 == ILLEGAL: value += 100
                    elif r3 == AI and l2 == AI: value += -100
                    elif r3 == ILLEGAL and l2 == AI: value += -200
                    elif r3 == AI and l2 == ILLEGAL: value += -300
                if r1 == r2 == r3 == OPP:
                    if r4 == NULL and l1 == NULL: value += 1000000; four_lost_shape += 1; threat = 4
                    elif r4 == AI and l1 == NULL: value += 300
                    elif r4 == ILLEGAL and l1 == NULL: value += 250
                    elif r4 == NULL and l1 == AI: value += 100
                    elif r4 == NULL and l1 == ILLEGAL: value += 80
                    elif r4 == AI and l1 == AI: value += -100
                    elif r4 == ILLEGAL and l1 == AI: value += -200
                    elif r4 == AI and l1 == ILLEGAL: value += -300
                if l4 == l2 == l1 == OPP and l3 == NULL: 
                    if l5 == NULL: value += 10000; four_lost_shape += 1; threat = 4
                    elif l5 == AI: value += 400
                    elif l5 == ILLEGAL: value += 300
                if l4 == l3 == l1 == OPP and l2 == NULL: 
                    if l5 == NULL: value += 8000; four_lost_shape += 1; threat = 4
                    elif l5 == AI: value += 350
                    elif l5 == ILLEGAL: value += 250
                if l4 == l3 == l2 == OPP and l1 == NULL: 
                    if l5 == NULL: value += 4000; four_lost_shape += 1; threat = 4
                    elif l5 == AI: value += 450
                    elif l5 == ILLEGAL: value += 350
                if r2 == r3 == r4 == OPP and r1 == NULL: 
                    if l5 == NULL: value += 4000; four_lost_shape += 1; threat = 4
                    elif l5 == AI: value += 450
                    elif l5 == ILLEGAL: value += 350
                if r1 == r3 == r4 == OPP and r2 == NULL: 
                    if l5 == NULL: value += 8000; four_lost_shape += 1; threat = 4
                    elif l5 == AI: value += 350
                    elif l5 == ILLEGAL: value += 250
                if r1 == r2 == r4 == OPP and r3 == NULL:
                    if r5 == NULL: value += 10000; four_lost_shape += 1; threat = 4
                    elif r5 == AI: value += 400
                    elif r5 == ILLEGAL: value += 300

            # 3-in-line (shape of 2)
            if threat <= 3:

                # 3-in-line to attack (shape of 2)
                if l3 == l2 == AI and l1 == NULL:
                    if l4 == NULL and r1 == NULL: value += 1000; three_win_shape += 1; threat = 3
                    elif l4 == OPP and r1 == NULL: value += 50
                    elif l4 == NULL and r1 == OPP: value += 45
                    elif l4 == NULL and r1 == ILLEGAL: value += 40
                    elif l4 == ILLEGAL and r1 == NULL: value += 30
                    elif l4 == OPP and r1 == OPP: value += -20
                    elif l4 == OPP and r1 == ILLEGAL: value += -25
                    elif l4 == ILLEGAL and r1 == OPP: value += -30
                if l3 == l1 == AI and l2 == NULL:
                    if l4 == NULL and r1 == NULL: value += 1500; three_win_shape += 1; threat = 3
                    elif l4 == OPP and r1 == NULL: value += 80
                    elif l4 == NULL and r1 == OPP: value += 65
                    elif l4 == ILLEGAL and r1 == NULL: value += 50
                    elif l4 == NULL and r1 == ILLEGAL: value += 40
                    elif l4 == OPP and r1 == OPP: value += -20
                    elif l4 == OPP and r1 == ILLEGAL: value += -25
                    elif l4 == ILLEGAL and r1 == OPP: value += -30
                if l2 == l1 == AI and l3 == NULL:
                    if l4 == NULL and r1 == NULL: value += 3000; three_win_shape += 1; threat = 3
                    elif l4 == OPP and r1 == NULL: value += 1000
                    elif l4 == ILLEGAL and r1 == NULL: value += 500
                    elif l4 == NULL and r1 == OPP: value += 60
                    elif l4 == NULL and r1 == ILLEGAL: value += 50
                    elif l4 == OPP and r1 == OPP: value += -20
                    elif l4 == OPP and r1 == ILLEGAL: value += -25
                    elif l4 == ILLEGAL and r1 == OPP: value += -30
                if l2 == r1 == AI and l1 == NULL:
                    if l3 == NULL and r2 == NULL: value += 1500; three_win_shape += 1; threat = 3
                    elif l3 == OPP and r2 == NULL: value += 80
                    elif l3 == NULL and r2 == OPP: value += 65
                    elif l3 == ILLEGAL and r2 == NULL: value += 50
                    elif l3 == NULL and r2 == ILLEGAL: value += 40
                    elif l3 == OPP and r2 == OPP: value += -20
                    elif l3 == OPP and r2 == ILLEGAL: value += -25
                    elif l3 == ILLEGAL and r2 == OPP: value += -30
                if l1 == r1 == AI:
                    if l2 == NULL and r2 == NULL: value += 2000; three_win_shape += 1; threat = 3
                    elif l2 == OPP and r2 == NULL: value += 60
                    elif l2 == NULL and r2 == OPP: value += 60
                    elif l2 == ILLEGAL and r2 == NULL: value += 50
                    elif l2 == NULL and r2 == ILLEGAL: value += 50
                    elif l2 == OPP and r2 == OPP: value += -20
                    elif l2 == OPP and r2 == ILLEGAL: value += -25
                    elif l2 == ILLEGAL and r2 == OPP: value += -30
                if l2 == r2 == AI:
                    if l1 == NULL and r1 == NULL: value += 800; three_win_shape += 1; threat = 3
                    elif l1 == OPP and r1 == NULL: value += 20
                    elif l1 == NULL and r1 == OPP: value += 20
                    elif l1 == OPP and r1 == OPP: value += -10
                if r2 == l1 == AI and l1 == NULL:
                    if r3 == NULL and l2 == NULL: value += 1500; three_win_shape += 1; threat = 3
                    elif r3 == OPP and l2 == NULL: value += 80
                    elif r3 == NULL and l2 == OPP: value += 65
                    elif r3 == ILLEGAL and l2 == NULL: value += 50
                    elif r3 == NULL and l2 == ILLEGAL: value += 40
                    elif r3 == OPP and l2 == OPP: value += -20
                    elif r3 == OPP and l2 == ILLEGAL: value += -25
                    elif r3 == ILLEGAL and l2 == OPP: value += -30
                if r2 == r1 == AI and r3 == NULL:
                    if r4 == NULL and l1 == NULL: value += 3000; three_win_shape += 1; threat = 3
                    elif r4 == OPP and l1 == NULL: value += 1000
                    elif r4 == ILLEGAL and l1 == NULL: value += 500
                    elif r4 == NULL and l1 == OPP: value += 60
                    elif r4 == NULL and l1 == ILLEGAL: value += 50
                    elif r4 == OPP and l1 == OPP: value += -20
                    elif r4 == OPP and l1 == ILLEGAL: value += -25
                    elif r4 == ILLEGAL and l1 == OPP: value += -30
                if r3 == r1 == AI and r2 == NULL:
                    if r4 == NULL and l1 == NULL: value += 1500; three_win_shape += 1; threat = 3
                    elif r4 == OPP and l1 == NULL: value += 80
                    elif r4 == NULL and l1 == OPP: value += 65
                    elif r4 == ILLEGAL and l1 == NULL: value += 50
                    elif r4 == NULL and l1 == ILLEGAL: value += 40
                    elif r4 == OPP and l1 == OPP: value += -20
                    elif r4 == OPP and l1 == ILLEGAL: value += -25
                    elif r4 == ILLEGAL and l1 == OPP: value += -30
                if r3 == r2 == AI and r1 == NULL:
                    if r4 == NULL and l1 == NULL: value += 1000; three_win_shape += 1; threat = 3
                    elif r4 == OPP and l1 == NULL: value += 50
                    elif r4 == NULL and l1 == OPP: value += 45
                    elif r4 == NULL and l1 == ILLEGAL: value += 40
                    elif r4 == ILLEGAL and l1 == NULL: value += 30
                    elif r4 == OPP and l1 == OPP: value += -20
                    elif r4 == OPP and l1 == ILLEGAL: value += -25
                    elif r4 == ILLEGAL and l1 == OPP: value += -30

                # 3-in-line to defend (shape of 2)
                if l3 == l2 == OPP and l1 == NULL:
                    if l4 == NULL and r1 == NULL: value += 800; three_lost_shape += 1; threat = 3
                    elif l4 == AI and r1 == NULL: value += 30
                    elif l4 == NULL and r1 == AI: value += 25
                    elif l4 == NULL and r1 == ILLEGAL: value += 20
                    elif l4 == ILLEGAL and r1 == NULL: value += 15
                    elif l4 == AI and r1 == AI: value += -20
                    elif l4 == AI and r1 == ILLEGAL: value += -25
                    elif l4 == ILLEGAL and r1 == AI: value += -30
                if l3 == l1 == OPP and l2 == NULL:
                    if l4 == NULL and r1 == NULL: value += 1200; three_lost_shape += 1; threat = 3
                    elif l4 == AI and r1 == NULL: value += 50
                    elif l4 == NULL and r1 == AI: value += 45
                    elif l4 == ILLEGAL and r1 == NULL: value += 40
                    elif l4 == NULL and r1 == ILLEGAL: value += 30
                    elif l4 == AI and r1 == AI: value += -20
                    elif l4 == AI and r1 == ILLEGAL: value += -25
                    elif l4 == ILLEGAL and r1 == AI: value += -30
                if l2 == l1 == OPP and l3 == NULL:
                    if l4 == NULL and r1 == NULL: value += 2400; three_lost_shape += 1; threat = 3
                    elif l4 == AI and r1 == NULL: value += 800
                    elif l4 == ILLEGAL and r1 == NULL: value += 400
                    elif l4 == NULL and r1 == AI: value += 40
                    elif l4 == NULL and r1 == ILLEGAL: value += 30
                    elif l4 == AI and r1 == AI: value += -20
                    elif l4 == AI and r1 == ILLEGAL: value += -25
                    elif l4 == ILLEGAL and r1 == AI: value += -30
                if l2 == r1 == OPP and l1 == NULL:
                    if l3 == NULL and r2 == NULL: value += 1200; three_lost_shape += 1; threat = 3
                    elif l3 == AI and r2 == NULL: value += 50
                    elif l3 == NULL and r2 == AI: value += 45
                    elif l3 == ILLEGAL and r2 == NULL: value += 40
                    elif l3 == NULL and r2 == ILLEGAL: value += 30
                    elif l3 == AI and r2 == AI: value += -20
                    elif l3 == AI and r2 == ILLEGAL: value += -25
                    elif l3 == ILLEGAL and r2 == AI: value += -30
                if l1 == r1 == OPP:
                    if l2 == NULL and r2 == NULL: value += 1600; three_lost_shape += 1; threat = 3
                    elif l2 == AI and r2 == NULL: value += 40
                    elif l2 == NULL and r2 == AI: value += 40
                    elif l2 == ILLEGAL and r2 == NULL: value += 30
                    elif l2 == NULL and r2 == ILLEGAL: value += 30
                    elif l2 == AI and r2 == AI: value += -20
                    elif l2 == AI and r2 == ILLEGAL: value += -25
                    elif l2 == ILLEGAL and r2 == AI: value += -30
                if l2 == r2 == OPP:
                    if l1 == NULL and r1 == NULL: value += 640; three_lost_shape += 1; threat = 3
                    elif l1 == AI and r1 == NULL: value += 15
                    elif l1 == NULL and r1 == AI: value += 15
                    elif l1 == AI and r1 == AI: value += -10
                if r2 == l1 == OPP and r1 == NULL:
                    if r3 == NULL and l2 == NULL: value += 1200; three_win_shape += 1; threat = 3
                    elif r3 == AI and l2 == NULL: value += 50
                    elif r3 == NULL and l2 == AI: value += 45
                    elif r3 == ILLEGAL and l2 == NULL: value += 40
                    elif r3 == NULL and l2 == ILLEGAL: value += 30
                    elif r3 == AI and l2 == AI: value += -20
                    elif r3 == AI and l2 == ILLEGAL: value += -25
                    elif r3 == ILLEGAL and l2 == AI: value += -30
                if r2 == r1 == OPP and r3 == NULL:
                    if r4 == NULL and l1 == NULL: value += 2400; three_win_shape += 1; threat = 3
                    elif r4 == AI and l1 == NULL: value += 800
                    elif r4 == ILLEGAL and l1 == NULL: value += 400
                    elif r4 == NULL and l1 == AI: value += 40
                    elif r4 == NULL and l1 == ILLEGAL: value += 30
                    elif r4 == AI and l1 == AI: value += -20
                    elif r4 == AI and l1 == ILLEGAL: value += -25
                    elif r4 == ILLEGAL and l1 == AI: value += -30
                if r3 == r1 == OPP and r2 == NULL:
                    if r4 == NULL and l1 == NULL: value += 1200; three_lost_shape += 1; threat = 3
                    elif r4 == AI and l1 == NULL: value += 50
                    elif r4 == NULL and l1 == AI: value += 45
                    elif r4 == ILLEGAL and l1 == NULL: value += 40
                    elif r4 == NULL and l1 == ILLEGAL: value += 30
                    elif r4 == AI and l1 == AI: value += -20
                    elif r4 == AI and l1 == ILLEGAL: value += -25
                    elif r4 == ILLEGAL and l1 == AI: value += -30
                if r3 == r2 == OPP and r1 == NULL:
                    if r4 == NULL and l1 == NULL: value += 800; three_lost_shape += 1; threat = 3
                    elif r4 == AI and l1 == NULL: value += 30
                    elif r4 == NULL and l1 == AI: value += 25
                    elif r4 == NULL and l1 == ILLEGAL: value += 20
                    elif r4 == ILLEGAL and l1 == NULL: value += 15
                    elif r4 == AI and l1 == AI: value += -20
                    elif r4 == AI and l1 == ILLEGAL: value += -25
                    elif r4 == ILLEGAL and l1 == AI: value += -30

            # 2-in-position (shape of 1)
            if threat <= 2:
                if l3 == AI: value += 2
                if l2 == AI: value += 6
                if l1 == AI: value += 10
                if r1 == AI: value += 10
                if r2 == AI: value += 6
                if r3 == AI: value += 2
                if l3 == OPP: value += 1
                if l2 == OPP: value += 3
                if l1 == OPP: value += 5
                if r1 == OPP: value += 5
                if r2 == OPP: value += 3
                if r3 == OPP: value += 1

        # special shapes: double-four, double-three, four-three

        # win shapes
        win_value = value
        if four_win_shape + three_win_shape == 2:
            if four_win_shape == 2: win_value *= 400    # double-four
            elif four_win_shape == three_win_shape == 1: win_value *= 200    # four-three
            elif three_win_shape == 2: win_value *= 100    # double-three
        elif four_win_shape + three_win_shape > 2:
            win_value *= 800

        # lost shapes
        lost_value = value
        if four_lost_shape + three_lost_shape == 2:
            if four_lost_shape == 2: lost_value *= 400    # double-four
            elif four_lost_shape == three_lost_shape == 1: lost_value *= 200    # four-three
            elif three_lost_shape == 2: lost_value *= 100    # double-three
        elif four_lost_shape + three_lost_shape > 2:
            lost_value *= 800

        self.heuristic_moves[move] += win_value if win_value >= lost_value else lost_value

    def get_surrounding_moves(self) -> list:

        '''
        Return surrounding moves of pieces on the current board.
        '''
        next_moves = []
        for x in range(self.HEIGHT):
            for y in range(self.WIDTH):
                if self.grid[x][y] != 0:
                    next_moves.extend([
                        (x - 3, y), (x - 2, y), (x - 1, y), (x + 1, y), (x + 2, y), (x + 3, y),    # horizontal
                        (x, y - 3), (x, y - 2), (x, y - 1), (x, y + 1), (x, y + 2), (x, y + 3),    # vertical
                        (x - 3, y - 3), (x - 2, y - 2), (x - 1, y - 1), (x + 1, y + 1), (x + 2, y + 2), (x + 3, y + 3),    # left diagonal
                        (x + 3, y - 3), (x + 2, y - 2), (x + 1, y - 1), (x - 1, y + 1), (x - 2, y + 2), (x - 3, y + 3)    # right diagonal
                    ])
        if next_moves == []: return []
        else: return [(x, y) for x, y in list(set(next_moves)) if self.is_free_move(x, y)]    # delete illegal nodes    # a list of next moves

    def get_heuristic_moves(self) -> tuple:
        
        '''
        Return forced moves searched by heuristic knowledge.
        '''
        
        # get available moves of the current board
        available_moves = self.get_surrounding_moves()    # surrounding positions in the range of three: [(x, y)]
        if available_moves == []: return True, ((self.HEIGHT - 1) // 2, (self.WIDTH - 1) // 2)    # choice for first round: center position of the board

        ### search for forced moves with heuristic knowledge: self.search_forced_moves()
        self.heuristic_moves = collections.defaultdict(int)
        for move in available_moves: self.search_forced_moves(move)
        forced_moves = list(self.heuristic_moves.keys())
        if len(forced_moves) != 0: return True, max(forced_moves, key = lambda x: self.heuristic_moves[x])    # get best move
        else: return False, None

    def get_next_moves(self, board, use_heuristic: bool = True) -> list:

        '''
        Return a best forced move or a list of next moves as children of the root in Monte Carlo Tree.
        '''
        
        # initialize the board data
        self.board = board    # an instance of class Board
        self.grid = board.grid    # a 2-dimension list
        self.turn = board.turn    # 1: turn to AI, 2: turn to opponent

        #####################################################
        ### First strategy: Search for FORCED moves       ###
        ### Second strategy: Search for SURROUNDING moves ###
        #####################################################

        ### First strategy: Use heuristic knowledge to search the best FORCED move
        if use_heuristic:
            is_forced, best_forced_move = self.get_heuristic_moves()
            if is_forced: return [best_forced_move]    # a list with only one move (best forced move)

        ### Second strategy: Expand SURROUNDING positions in the range of three
        return self.get_surrounding_moves()

    # functions for self.get_board_with_move()
    def get_board_with_move(self, board, move: tuple):

        '''
        Return a new instance of class Board with a move inherited by the current board. 
        '''
        self.grid = [[i for i in board.grid[row]] for row in range(self.HEIGHT)]    # self.grid: a deep copy of board.grid
        self.grid[move[0]][move[1]] = board.turn
        return Board(grid = self.grid, turn = 3 - board.turn)    # next turn to opponent


class Old_Evaluator():
    
    def __init__(self):

        # BOARD data
        self.WIDTH = pp.width
        self.HEIGHT = pp.height
        self.round = 0

        # PATTERN data
        self.AI_PATTERN = {
            (1, 1, 1, 1, 1): 10000000, (1, 1, 0, 1, 1): 2000000, 
            (1, 1, 1, 1, 0): 5000000, (0, 1, 1, 1, 1): 5000000,
            (1, 1, 1, 0, 1): 200000, (1, 0, 1, 1, 1): 200000,
            (1, 1, 1, 0, 0): 10000, (0, 0, 1, 1, 1): 10000, 
            (1, 1, 0, 1, 0): 10000, (0, 1, 0, 1, 1): 10000, 
            (1, 1, 0, 0, 1): 1000, (1, 0, 0, 1, 1): 1000, 
            (1, 0, 1, 0, 1): 1000, (0, 1, 1, 1, 0): 10000, 
            (0, 1, 1, 0, 1): 1000, (1, 0, 1, 1, 0): 1000, 
            (1, 1, 0, 0, 0): 500, (0, 0, 0, 1, 1): 500,
            (0, 1, 1, 0, 0): 500, (0, 0, 1, 1, 0): 500, 
            (1, 0, 1, 0, 0): 500, (0, 0, 1, 0, 1): 500,
            (1, 0, 0, 1, 0): 100, (0, 1, 0, 0, 1): 100, 
            (1, 0, 0, 0, 1): 50, (0, 1, 0, 1, 0): 200,
            (1, 0, 0, 0, 0): 10, (0, 0, 0, 0, 1): 10, 
            (0, 0, 0, 1, 0): 10, (0, 1, 0, 0 ,0): 10, 
            (0, 0, 1, 0, 0): 10, (0, 0, 0, 0, 0): 0
        }
        self.OPP_PATTERN = {
            (2, 2, 2, 2, 2): -1000000000, (2, 2, 0, 2, 2): -20000000,
            (2, 2, 2, 2, 0): -50000000, (0, 2, 2, 2, 2): -50000000, 
            (2, 2, 2, 0, 2): -20000000, (2, 0, 2, 2, 2): -20000000, 
            (2, 2, 2, 0, 0): -100000, (0, 0, 2, 2, 2): -100000, 
            (2, 2, 0, 2, 0): -100000, (0, 2, 0, 2, 2): -100000, 
            (2, 2, 0, 0, 2): -10000, (2, 0, 0, 2, 2): -10000, 
            (2, 0, 2, 0, 2): -10000, (0, 2, 2, 2, 0): -50000, 
            (0, 2, 2, 0, 2): -10000, (2, 0, 2, 2, 0): -10000, 
            (2, 2, 0, 0, 0): -500, (0, 0, 0, 2, 2): -500, 
            (0, 2, 2, 0, 0): -500, (0, 0, 2, 2, 0): -500, 
            (2, 0, 2, 0, 0): -500, (0, 0, 2, 0, 2): -500,
            (2, 0, 0, 2, 0): -100, (0, 2, 0, 0, 2): -100, 
            (2, 0, 0, 0, 2): -50, (0, 2, 0, 2, 0): -200, 
            (2, 0, 0, 0, 0): -10, (0, 0, 0, 0, 2): -10, 
            (0, 0, 0, 2, 0): -10, (0, 2, 0, 0, 0): -10, 
            (0, 0, 2, 0, 0): -10, (0, 0, 0, 0, 0): 0
        }
        self.BLOCK_PATTERN = {
            (1, 2, 2, 2, 2): 50000000, (2, 2, 2, 2, 1): 50000000, 
            (2, 1, 2, 2, 2): 50000000, (2, 2, 2, 1, 2): 50000000,
            (2, 2, 1, 2, 2): 30000000, 
            (0, 2, 2, 2, 1): 5000000, (1, 2, 2, 2, 0): 5000000,
            (2, 2, 2, 1, 0): 500000, (0, 1, 2, 2, 2): 500000,
            (2, 2, 1, 2, 0): 400000, (0, 2, 1, 2, 2): 400000, 
            (0, 2, 2, 1, 2): 300000, (2, 1, 2, 2, 0): 300000, 
            (1, 2, 2, 0, 2): 200000, (2, 0, 2, 2, 1): 200000,
            (2, 2, 0, 1, 2): 10000, (2, 1, 0, 2, 2): 10000, 
            (2, 1, 2, 0, 2): 10000, (2, 0, 2, 1, 2): 10000,  
            (2, 2, 1, 0, 2): 10000, (2, 0, 1, 2, 2): 10000, 
            (2, 2, 2, 0, 1): 5000, (1, 0, 2, 2, 2): 5000
        }

        # SCORE data
        self.score = 0

    # functions for self.get_board_value()
    def get_round(self) -> int:

        '''
        Return the total rounds of the current board.
        '''
        return sum(self.board[x].count(1) for x in range(self.HEIGHT))    # round: the number of AI pieces

    def calc_horz_score(self):
        
        '''
        Calculate the total score of patterns in horizontal direction.
        '''

        # traverse all horizontal patterns in the current board
        for x in range(self.HEIGHT):

            # store the pattern in given row
            row = [self.board[x][i] for i in range(5)]
            self.calc_pattern_score(row)

            for y in range(5, self.WIDTH):

                # traverse the pattern in given row
                row.pop(0); row.append(self.board[x][y])
                self.calc_pattern_score(row)

    def calc_vert_score(self):

        '''
        Calculate the total score of patterns in vertical direction.
        '''

        # traverse all vertical patterns in the current board
        for y in range(self.WIDTH):

            # store the pattern in given column
            column = [self.board[i][y] for i in range(5)]
            self.calc_pattern_score(column)

            for x in range(5, self.HEIGHT):

                # traverse the pattern in given column
                column.pop(0); column.append(self.board[x][y])
                self.calc_pattern_score(column)

    def calc_left_diag_score(self):

        '''
        Calculate the total score of patterns in left diagonal direction.
        '''

        # traverse all left diagonal patterns in lower-left half of the current board
        for x in range(0, self.HEIGHT - 4):    # including principal left diagonal

            # store the pattern in given left diagonal
            left_diag = [self.board[x + i][i] for i in range(5)]
            self.calc_pattern_score(left_diag)

            for y in range(5, self.WIDTH - x):

                # traverse the pattern in given left diagonal
                left_diag.pop(0); left_diag.append(self.board[x + y][y])
                self.calc_pattern_score(left_diag)
                
        # traverse all left diagonal patterns in upper-right half of the current board
        for y in range(1, self.WIDTH - 4):

            # store the pattern in given left diagonal
            left_diag = [self.board[i][y + i] for i in range(5)]
            self.calc_pattern_score(left_diag)

            for x in range(5, self.HEIGHT - y):
                
                # traverse the pattern in given left diagonal
                left_diag.pop(0); left_diag.append(self.board[x][x + y])
                self.calc_pattern_score(left_diag)

    def calc_right_diag_score(self):

        '''
        Calculate the total score of patterns in right diagonal direction.
        '''

        # traverse all right diagonal patterns in upper-left half of the current board
        for y in range(4, self.WIDTH):    # including principal right diagonal
            
            # store the pattern in given right diagonal
            right_diag = [self.board[i][y - i] for i in range(5)]
            self.calc_pattern_score(right_diag)

            for x in range(5, y + 1):
                
                # traverse the pattern in given right diagonal
                right_diag.pop(0); right_diag.append(self.board[x][x - y])
                self.calc_pattern_score(right_diag)

        # traverse all right diagonal patterns in lower-right half of the current board
        for x in range(self.HEIGHT - 5, 0, -1):
            
            # store the pattern in given right diagonal
            right_diag = [self.board[x + i][self.WIDTH - 1 - i] for i in range(5)]
            self.calc_pattern_score(right_diag)

            for y in range(self.WIDTH - 6, x - 1, -1):

                # traverse the pattern in given right diagonal
                right_diag.pop(0); right_diag.append(self.board[self.HEIGHT - 1 + x - y][y])
                self.calc_pattern_score(right_diag)

    def calc_loc_score(self):

        '''
        Calculate the total score of the current board in location.
        '''

        # location of the center of the board
        x_center, y_center = (self.HEIGHT - 1) / 2, (self.WIDTH - 1) / 2

        # calculate the score of each position
        location_score = [
            [
                100 * min(
                    math.floor(x_center - abs(x - x_center)), 
                    math.floor(y_center - abs(y - y_center))
                ) 
                for x in range(self.HEIGHT)
            ] 
            for y in range(self.WIDTH)
        ]

        # sum the score
        for x in range(self.HEIGHT):
            for y in range(self.WIDTH):
                if self.board[x][y] == 1: self.score += location_score[x][y]
                elif self.board[x][y] == 2: self.score -= location_score[x][y]

    def calc_dir_score(self):

        '''
        Calculate the total score of the current board in four directions.
        '''
        self.calc_horz_score()
        self.calc_vert_score()
        self.calc_left_diag_score()
        self.calc_right_diag_score()
    
    def calc_pattern_score(self, pattern: list):

        '''
        Calculate the total score of patterns.
        '''
        pattern = tuple(pattern)
        self.score += self.AI_PATTERN.get(pattern, 0) + \
                      self.OPP_PATTERN.get(pattern, 0) + \
                      self.BLOCK_PATTERN.get(pattern, 0)

    def update_pattern_score(self):

        '''
        Update the score of specific patterns on the current round.
        '''

        # patterns for AI
        self.AI_PATTERN[(1, 1, 1, 1, 1)] = 10000000 + 5000000 * self.round
        self.AI_PATTERN[(1, 1, 0, 1, 1)] = 2000000 + 100000 * self.round
        self.AI_PATTERN[(1, 1, 1, 1, 0)] = 5000000 + 100000 * self.round
        self.AI_PATTERN[(0, 1, 1, 1, 1)] = 5000000 + 100000 * self.round
        self.AI_PATTERN[(1, 1, 1, 0, 1)] = 200000 + 10000 * self.round
        self.AI_PATTERN[(1, 0, 1, 1, 1)] = 200000 + 10000 * self.round

        # patterns for opponent
        self.OPP_PATTERN[(2, 2, 2, 2, 2)] = -1000000000 - 50000000 * self.round
        self.OPP_PATTERN[(2, 2, 0, 2, 2)] = -20000000 - 100000 * self.round
        self.OPP_PATTERN[(2, 2, 2, 2, 0)] = -50000000 - 100000 * self.round
        self.OPP_PATTERN[(0, 2, 2, 2, 2)] = -50000000 - 100000 * self.round
        self.OPP_PATTERN[(2, 2, 2, 0, 2)] = -20000000 - 100000 * self.round
        self.OPP_PATTERN[(2, 0, 2, 2, 2)] = -20000000 - 100000 * self.round

        # patterns for block
        self.BLOCK_PATTERN[(1, 2, 2, 2, 2)] = 50000000 + 100000 * self.round
        self.BLOCK_PATTERN[(2, 2, 2, 2, 1)] = 50000000 + 100000 * self.round
        self.BLOCK_PATTERN[(2, 1, 2, 2, 2)] = 50000000 + 100000 * self.round
        self.BLOCK_PATTERN[(2, 2, 2, 1, 2)] = 50000000 + 100000 * self.round
        self.BLOCK_PATTERN[(2, 2, 1, 2, 2)] = 30000000 + 10000 * self.round
        self.BLOCK_PATTERN[(0, 2, 2, 2, 1)] = 5000000 + 10000 * self.round
        self.BLOCK_PATTERN[(1, 2, 2, 2, 0)] = 5000000 + 10000 * self.round

    def get_board_value(self, board: list) -> int:

        '''
        Return the evaluation value of the current board.
        '''

        # initialize the board data
        self.board = board    # update the current board
        self.round = self.get_round()
        self.update_pattern_score()
        self.score = 0

        # evaluate the score in two ways: LOCATION and DIRECTION
        self.calc_loc_score()
        self.calc_dir_score()

        return self.score


### structures
class Board():

    def __init__(self, grid: list, turn: int):
        
        self.grid = grid    # a 2-dimension list: [[x, ..., x], ..., [x, ..., x]]
        self.turn = turn    # 1: turn to AI, 2: turn to opponent
        evaluator = Evaluator()    # evaluator for the current board
        self.is_terminal = evaluator.is_terminal(grid, turn)    # terminal board: board in the state of WIN (1) or DRAW (-1)


class Node():

    def __init__(self, board, parent):

        self.board = board    # an instance of class Board
        self.turn = board.turn    # 1: turn to AI, 2: turn to opponent
        self.is_leaf = board.is_terminal    # leaf node: board in the state of WIN (1) or DRAW (-1)
        self.is_fully_expanded = self.is_leaf    # no node to expand if it is a leaf node

        self.visit_times = 0    # total times of being visited
        self.win_times = 0    # total times of winning if this node is visited

        self.parent = parent    # the parent of the given node: Node
        self.children = {}    # the children of the given node: {(x, y): Node}


### algorithms
class Minimax_with_Alpha_Beta_Pruning():


    def __init__(self):

        # board data
        self.WIDTH = pp.width
        self.HEIGHT = pp.height

        # evaluator for score
        self.old_evaluator = Old_Evaluator()
        self.evaluator = Evaluator()

        # store the result
        self.best_move = None

        # constant data
        self.INF = float('inf')

    def DFS(self, depth, turn, alpha, beta) -> int:

        '''
        Use Depth First Search to search the Minimax Tree.
        '''

        # score of leaf node 
        if depth == 1: return self.old_evaluator.get_board_value(self.board)
        
        # traverse all child nodes with alpha-beta pruning
        for x, y in self.get_next_moves(turn):

            # recursion by DFS
            self.board[x][y] = turn    # 1: turn to AI, 2: turn to opponent
            value = self.DFS(depth = depth - 1, turn = 3 - turn, alpha = alpha, beta = beta)
            self.board[x][y] = 0

            # MAX node    
            if turn == 1:
                self.best_move = (x, y) if alpha < value else self.best_move
                alpha = max(alpha, value)

            # MIN node
            else:
                self.best_move = (x, y) if beta > value else self.best_move
                beta = min(beta, value)
            
            # pruning
            if alpha >= beta:
                break

        return alpha

    def is_free_move(self, x, y) -> bool:

        '''
        Check whether position (x, y) is available and free (with value 0).
        '''
        return 0 <= x < self.HEIGHT and 0 <= y < self.WIDTH and self.board[x][y] == 0

    def get_next_moves(self, turn, use_heuristic = True) -> list:
        
        '''
        Return a list of next moves as children of the root in Minimax Tree.
        '''

        #####################################################
        ### First strategy: Search for FORCED moves       ###
        ### Second strategy: Search for SURROUNDING moves ###
        #####################################################

        ### First strategy: Use heuristic knowledge to search FORCED moves
        if use_heuristic:
            best_forced_move = self.evaluator.get_next_moves(Board(self.board, turn), use_heuristic = True)    # 1: turn to AI, 2: turn to opponent
            return best_forced_move

        ### Second strategy: Expand SURROUNDING positions in the range of three
        next_moves = []
        for x in range(self.HEIGHT):
            for y in range(self.WIDTH):
                if self.board[x][y] != 0:
                    next_moves.extend([
                        (x - 3, y), (x - 2, y), (x - 1, y), (x + 1, y), (x + 2, y), (x + 3, y),    # horizontal
                        (x, y - 3), (x, y - 2), (x, y - 1), (x, y + 1), (x, y + 2), (x, y + 3),    # vertical
                        (x - 3, y - 3), (x - 2, y - 2), (x - 1, y - 1), (x + 1, y + 1), (x + 2, y + 2), (x + 3, y + 3),    # left diagonal
                        (x + 3, y - 3), (x + 2, y - 2), (x + 1, y - 1), (x - 1, y + 1), (x - 2, y + 2), (x - 3, y + 3)    # right diagonal
                    ])
        return [(x, y) for x, y in list(set(next_moves)) if self.is_free_move(x, y)]    # delete illegal nodes

    def get_best_move(self, board, depth = 5) -> tuple:

        '''
        Return the best move (x, y) with Minimax.
        '''
        self.board = board
        self.DFS(depth = depth, turn = 1, alpha = -self.INF, beta = self.INF)
        return self.best_move


class MCTS():

    def __init__(self, sample_size: int):

        self.evaluator = Evaluator()    # evaluator for the current board
        self.sample_size = sample_size    # total times to run MCTS
        self.confidence_level = 1.96    # confidence level of the UCT

    def search(self, board) -> tuple:

        '''
        Use MCTS to search the best move for the given board.
        '''

        # search forced move
        # forced_move = self.evaluator.get_next_moves(board = board, use_heuristic = True)
        # if len(forced_move) == 1: return forced_move[0]

        # construct the root of Monte Carlo Tree
        self.root = Node(board, None)    # no parent

        # play the game for sample_size times
        for i in range(self.sample_size):

            # First Step: Selection & Second Step: Expansion
            node = self.selection(self.root)    # select the node with higher possibility

            # Third Step: Simulation
            result = self.simulation(node.board)    # only need the result: 0 or 1

            # Fourth step: Backpropagation
            self.backpropogation(node, result)    # update each node on the path

        # get the best move from the root node
        return self.get_best_move(self.root)

    def selection(self, node):

        '''
        Return the node selected by MCTS policy.
        '''
        while not node.is_leaf:
            if node.is_fully_expanded: node = self.get_best_child(node)    # search in depth
            else: return self.expansion(node)    # search in breadth
        return node    # get the leaf node

    def expansion(self, node):

        '''
        Return a new node for expansion in the Monte Carlo Tree.
        '''

        # get next moves from the current board
        next_moves = self.evaluator.get_next_moves(node.board)

        # traverse all next moves
        for move in next_moves:

            # a move hasn't been visited
            if move not in node.children.keys():
                
                # generate a new node with this move
                child = Node(self.evaluator.get_board_with_move(node.board, move), node)
                node.children[move] = child

                # the node is fully expanded
                if len(next_moves) == len(node.children): node.is_fully_expanded = True

                # get the selected child node
                return child

    def simulation(self, board) -> bool:

        '''
        Return the result of simulation which uses the simple policy.
        '''
        while not board.is_terminal:
            opponent_move = random.choice(self.evaluator.get_next_moves(board))    # use simple policy to find next move
            board = self.evaluator.get_board_with_move(board, opponent_move)    # a new Board with next move
        if board.is_terminal == -1: return 0    # 0: root draws
        else: return self.root.turn == board.turn    # 1: root wins, 0: root loses (opponent wins)

    def backpropogation(self, node, result: bool):

        '''
        Backpropogate to the root node to update the state of each node on the path.
        '''
        while node is not None:    # the parent of the root is None
            node.visit_times += 1
            node.win_times += result    # 1: win, 0: lost or draw
            node = node.parent    # backpropogation

    def get_best_child(self, node):

        '''
        Return the best child with maximum UCT of the given node.
        '''

        # traverse all chidren of the node
        best_value = -float('inf'); best_children = []
        for child in node.children.values():

            # compute the value of UCT
            exploitation = child.win_times / child.visit_times    # exploitation: chance of winning
            exploration = math.sqrt(math.log(node.visit_times) / child.visit_times)    # exploration: search more nodes
            value = exploitation + self.confidence_level * exploration    # UCT: Upper Confidence Bound applied to Trees

            # record the children with maximum UCT
            if value > best_value: best_value = value; best_children = [child]    # only one child with maximum value
            elif value == best_value: best_children.append(child)    # more than one child with maximum value

        # choose one of the best children
        return random.choice(best_children)

    def get_best_move(self, node) -> tuple:

        '''
        Return the best move of the given node.
        '''

        # get the best child of the given node
        best_child = self.get_best_child(node)

        # get the move between the node and its best child
        for move, child in node.children.items():
            if child is best_child: return move


### functions in pisqpipe module
def brain_init():
	if pp.width < 5 or pp.height < 5:
		pp.pipeOut('ERROR size of the board')
		return
	if pp.width > MAX_BOARD or pp.height > MAX_BOARD:
		pp.pipeOut('ERROR Maximal board size is {}'.format(MAX_BOARD))
		return
	pp.pipeOut('OK')

def brain_restart():
	for x in range(pp.height):
		for y in range(pp.width):
			board[x][y] = 0
	pp.pipeOut('OK')

def isFree(x, y):
	return 0 <= x < pp.height and 0 <= y < pp.width and board[x][y] == 0

def brain_my(x, y):
	if isFree(x, y):
		board[x][y] = 1
	else:
		pp.pipeOut('ERROR my move [{},{}]'.format(x, y))

def brain_opponents(x, y):
	if isFree(x, y):
		board[x][y] = 2
	else:
		pp.pipeOut("ERROR opponents's move [{},{}]".format(x, y))

def brain_block(x, y):
	if isFree(x,y):
		board[x][y] = 3
	else:
		pp.pipeOut('ERROR winning move [{},{}]'.format(x, y))

def brain_takeback(x, y):
	if 0 <= x < pp.height and 0 <= y < pp.width and board[x][y] != 0:
		board[x][y] = 0
		return 0
	return 2

def brain_turn():
    if pp.terminateAI:
        return
    i = 0
    while True:

        ################## API for searching best move ##################
        
        ### use Minimax with Alpha-Beta Pruning
        # searcher = Minimax_with_Alpha_Beta_Pruning()
        # x, y = searcher.get_best_move(board = board, depth = 2)

        ### use MCTS
        searcher = MCTS(sample_size = 1000)
        x, y = searcher.search(Board(grid = board, turn = 1))

        ### use heuristic knowledge only
        # evaluator = Evaluator()
        # x, y = evaluator.get_next_moves(Board(grid = board, turn = 1))[0]

        #################################################################

        i += 1
        if pp.terminateAI:
            return
        if isFree(x, y):
            break
    if i > 1:
        pp.pipeOut("DEBUG {} coordinates didn't hit an empty field".format(i))
    pp.do_mymove(x, y)

def brain_end():
	pass

def brain_about():
	pp.pipeOut(pp.infotext)

if DEBUG_EVAL:
	from win32 import win32gui
	def brain_eval(x, y):
		wnd = win32gui.GetForegroundWindow()
		dc = win32gui.GetDC(wnd)
		rc = win32gui.GetClientRect(wnd)
		c = str(board[x][y])
		win32gui.ExtTextOut(dc, rc[2] - 15, 3, 0, None, c, ())
		win32gui.ReleaseDC(wnd, dc)


### overwrite functions in pisqpipe module
pp.brain_init = brain_init
pp.brain_restart = brain_restart
pp.brain_my = brain_my
pp.brain_opponents = brain_opponents
pp.brain_block = brain_block
pp.brain_takeback = brain_takeback
pp.brain_turn = brain_turn
pp.brain_end = brain_end
pp.brain_about = brain_about
if DEBUG_EVAL:
	pp.brain_eval = brain_eval


### main
def main():
	pp.main()

if __name__ == '__main__':
	main()
