# Chess Board
"""
index 1 - vertical movement -  x
index 2 - horizontal movement -  y

. 0 1 2 3 4 5 6 7
0 * * * * * * * *
1 * * * * * * * *
2
3
4
5
6 * * * * * * * *
7 * * * * * * * *
"""

from typing import List, Optional


class Piece:
    def __init__(self, x, y, color, board, name, number):
        self.x = x
        self.y = y
        self.color = color
        self.board = board
        self.eliminated = False
        self.board[self.x][self.y] = self
        self.name = name
        self.number = number

    def get_id(self):
        return self.color + self.name + str(self.number)

    def move(self, pox_x, pox_y):
        self.board[self.x][self.y] = None
        self.x = pox_x
        self.y = pox_y
        eliminated_piece = None
        if self.board[pox_x][pox_y] is not None:
            eliminated_piece = self.board[pox_x][pox_y]
        self.board[pox_x][pox_y] = self

        return eliminated_piece

    def get_vertical_movable_positions(self):

        def move_directionally(direction, to):
            possible_positions = []

            for ver in range(self.x, to, direction):
                if ver == self.x:
                    continue
                if self.board[ver][self.y] is None:
                    possible_positions.append((ver, self.y))
                else:
                    if self.board[ver][self.y].color is self.color:
                        break
                    else:
                        possible_positions.append((ver, self.y))
                        break
            return possible_positions

        return move_directionally(1, 8), move_directionally(-1, -1)

    def get_horizontal_movable_positions(self):

        def move_directionally(direction, to):
            possible_positions = []

            for hor in range(self.y, to, direction):
                if hor == self.y:
                    continue
                if self.board[self.x][hor] is None:
                    possible_positions.append((self.x, hor))
                else:
                    if self.board[self.x][hor].color is self.color:
                        break
                    else:
                        possible_positions.append((self.x, hor))
                        break

            return possible_positions

        return move_directionally(1, 8), move_directionally(-1, -1)

    def get_diagonal_movable_positions(self):

        def move_directionally(direction_x, direction_y):
            possible_positions = []

            hor = self.y
            ver = self.x

            while True:
                hor += direction_y
                ver += direction_x

                if hor > 7 or hor < 0 or ver > 7 or ver < 0:
                    break
                if self.board[ver][hor] is None:
                    possible_positions.append((ver, hor))
                else:
                    if self.board[ver][hor].color is self.color:
                        break
                    else:
                        possible_positions.append((ver, hor))
                        break

            return possible_positions

        return ([*move_directionally(1, 1), *move_directionally(1, -1)],
                [*move_directionally(-1, 1), *move_directionally(-1, -1)])


class Rook(Piece):
    def __init__(self, x, y, color, board, number):
        super().__init__(x, y, color, board, 'r', number)

    def get_possible_moves(self):
        forward, backward = self.get_vertical_movable_positions()
        right, left = self.get_horizontal_movable_positions()

        return [*forward, *right, *left, *backward]


class Bishop(Piece):
    def __init__(self, x, y, color, board, number):
        super().__init__(x, y, color, board, 'b', number)

    def get_possible_moves(self):
        forward, backward = self.get_diagonal_movable_positions()
        return [*forward, *backward]


class Knight(Piece):
    def __init__(self, x, y, color, board, number):
        super().__init__(x, y, color, board, 'n', number)

    def get_possible_moves(self):
        hor_pos = self.y
        ver_pos = self.x

        moves = []

        def can_move(dir_x, dir_y):
            new_y, new_x = hor_pos + dir_x, ver_pos + dir_y
            if new_x > 7 or new_x < 0 or new_y > 7 or new_y < 0:
                return
            if self.board[new_x][new_y] is None:
                moves.append((new_x, new_y))
            else:
                if self.board[new_x][new_y].color != self.color:
                    moves.append((new_x, new_y))

        can_move(1, 2)
        can_move(2, 1)
        can_move(-1, 2)
        can_move(-2, 1)
        can_move(1, -2)
        can_move(2, -1)
        can_move(-1, -2)
        can_move(-2, -1)

        return moves


class Queen(Piece):
    def __init__(self, x, y, color, board, number):
        super().__init__(x, y, color, board, 'q', number)

    def get_possible_moves(self):
        forward, backward = self.get_vertical_movable_positions()
        right, left = self.get_horizontal_movable_positions()
        forward_d, backward_d = self.get_diagonal_movable_positions()

        return [*forward, *backward, *forward_d, *backward_d, *left, *right]


class King(Piece):
    def __init__(self, x, y, color, board, number):
        super().__init__(x, y, color, board, 'k', number)

    def get_possible_moves(self):
        forward, backward = self.get_vertical_movable_positions()
        right, left = self.get_horizontal_movable_positions()
        forward_d, backward_d = self.get_diagonal_movable_positions()
        moves = []
        if forward:
            moves.append(forward[0])
        if backward:
            moves.append(backward[0])
        if right:
            moves.append(right[0])
        if left:
            moves.append(left[0])
        if forward_d:
            moves.append(forward_d[0])
        if backward_d:
            moves.append(backward_d[0])

        return moves


class Pawn(Piece):
    def __init__(self, x, y, color, board, number, direction):
        super().__init__(x, y, color, board, 'p', number)
        self.direction = direction

    def get_possible_moves(self):
        forward, backward = self.get_vertical_movable_positions()
        forward_d, backward_d = self.get_diagonal_movable_positions()

        _moves = []
        if self.direction == 'down':
            if forward:
                if self.board[forward[0][0]][forward[0][1]] is None:
                    _moves.append(forward[0])
            if forward_d:
                if self.board[forward_d[0][0]][forward_d[0][1]] is not None:
                    _moves.append(forward_d[0])
        else:
            if backward:
                if self.board[backward[0][0]][backward[0][1]] is None:
                    _moves.append(backward[0])
            if backward_d:
                if self.board[backward_d[0][0]][backward_d[0][1]] is not None:
                    _moves.append(backward_d[0])

        return _moves


def clear_screen():
    print("\033[H\033[J", end="")


class Board:
    def __init__(self):

        self.name_and_object_map = None
        self.board: List[List[Optional[Piece]]] = [[None for _ in range(0, 9)] for _ in range(0, 9)]
        self.current_player = 'W'

    def print_board(self):

        clear_screen()

        print("       _a_ _b_ _c_ _d_ _e_ _f_ _g_ _h_ ")

        for i in range(0, 8):
            rows = [str(i) + " --> "]
            for j in range(0, 8):
                if self.board[i][j] is None:
                    rows.append("___")
                else:
                    piece = self.board[i][j].get_id()
                    rows.append(piece)
                    self.name_and_object_map[piece] = self.board[i][j]

            print(" ".join(rows))

    def setup(self, primary_player='w'):
        is_white_primary = False

        if primary_player == 'w':
            is_white_primary = True

        black_pawns = [
            Pawn(1 if is_white_primary else 6, 0, 'B', self.board, 1, 'down' if is_white_primary else 'up'),
            Pawn(1 if is_white_primary else 6, 1, 'B', self.board, 2, 'down' if is_white_primary else 'up'),
            Pawn(1 if is_white_primary else 6, 2, 'B', self.board, 3, 'down' if is_white_primary else 'up'),
            Pawn(1 if is_white_primary else 6, 3, 'B', self.board, 4, 'down' if is_white_primary else 'up'),
            Pawn(1 if is_white_primary else 6, 4, 'B', self.board, 5, 'down' if is_white_primary else 'up'),
            Pawn(1 if is_white_primary else 6, 5, 'B', self.board, 6, 'down' if is_white_primary else 'up'),
            Pawn(1 if is_white_primary else 6, 6, 'B', self.board, 7, 'down' if is_white_primary else 'up'),
            Pawn(1 if is_white_primary else 6, 7, 'B', self.board, 8, 'down' if is_white_primary else 'up')
        ]

        black_rooks = [
            Rook(0 if is_white_primary else 7, 0, 'B', self.board, 1),
            Rook(0 if is_white_primary else 7, 7, 'B', self.board, 2),
        ]
        black_bishops = [
            Bishop(0 if is_white_primary else 7, 2, 'B', self.board, 1),
            Bishop(0 if is_white_primary else 7, 5, 'B', self.board, 2),
        ]

        black_knights = [
            Knight(0 if is_white_primary else 7, 1, 'B', self.board, 1),
            Knight(0 if is_white_primary else 7, 6, 'B', self.board, 2),
        ]

        black_queens = Queen(0 if is_white_primary else 7, 3, 'B', self.board, 1)
        black_king = King(0 if is_white_primary else 7, 4, 'B', self.board, 1)

        white_pawns = [
            Pawn(6 if is_white_primary else 1, 0, 'W', self.board, 1, 'up' if is_white_primary else 'down'),
            Pawn(6 if is_white_primary else 1, 1, 'W', self.board, 2, 'up' if is_white_primary else 'down'),
            Pawn(6 if is_white_primary else 1, 2, 'W', self.board, 3, 'up' if is_white_primary else 'down'),
            Pawn(6 if is_white_primary else 1, 3, 'W', self.board, 4, 'up' if is_white_primary else 'down'),
            Pawn(6 if is_white_primary else 1, 4, 'W', self.board, 5, 'up' if is_white_primary else 'down'),
            Pawn(6 if is_white_primary else 1, 5, 'W', self.board, 6, 'up' if is_white_primary else 'down'),
            Pawn(6 if is_white_primary else 1, 6, 'W', self.board, 7, 'up' if is_white_primary else 'down'),
            Pawn(6 if is_white_primary else 1, 7, 'W', self.board, 8, 'up' if is_white_primary else 'down'),
        ]

        white_rooks = [
            Rook(7 if is_white_primary else 0, 0, 'W', self.board, 1),
            Rook(7 if is_white_primary else 0, 7, 'W', self.board, 2),
        ]

        white_bishops = [
            Bishop(7 if is_white_primary else 0, 2, 'W', self.board, 1),
            Bishop(7 if is_white_primary else 0, 5, 'W', self.board, 2),
        ]

        white_knights = [
            Knight(7 if is_white_primary else 0, 1, 'W', self.board, 1),
            Knight(7 if is_white_primary else 0, 6, 'W', self.board, 2),
        ]

        white_queens = Queen(7 if is_white_primary else 0, 3, 'W', self.board, 1)
        white_king = King(7 if is_white_primary else 0, 4, 'W', self.board, 1)

        # print self.board

        self.name_and_object_map = {}

        for i in range(0, 8):
            for j in range(0, 8):
                if self.board[i][j] is not None:
                    piece = self.board[i][j].get_id()
                    self.name_and_object_map[piece] = self.board[i][j]

    def get_possible_moves(self, piece_id: str):
        _moves = self.name_and_object_map[piece_id].get_possible_moves()
        mapped_moves = []
        horizontal_map = {0: 'a', 1: 'b', 2: 'c', 3: 'd', 4: 'e', 5: 'f', 6: 'g', 7: 'h'}
        for _m in _moves:
            ver = _m[0]
            hor = horizontal_map[_m[1]]
            mapped_moves.append((ver, hor))
        return mapped_moves

    def move_piece(self, piece_id: str, movement):

        global piece
        moves = self.get_possible_moves(piece_id)
        try:
            piece = self.name_and_object_map[piece_id]
        except KeyError:
            print('Wrong Key !!')

        horizontal_map = {'a': 0, 'b': 1, 'c': 2, 'd': 3, 'e': 4, 'f': 5, 'g': 6, 'h': 7}
        x = int(movement[0])
        y = int(horizontal_map[movement[1]])

        valid_move = False
        for move in moves:
            if move[0] is movement[0] and move[1] is movement[1]:
                valid_move = True

        if valid_move:
            self.current_player = 'B' if self.current_player == 'W' else 'W'
            return piece.move(x, y)
        else:
            print("Invalid move")
            return None

    def start(self):

        while True:
            self.print_board()
            print(f"Current Player: {"White" if self.current_player == 'W' else "Black"}")
            input_piece_id = input("Chance: Enter piece name to move")

            if input_piece_id[0] != self.current_player:
                print('Wrong Player !!')
                continue

            moves = self.get_possible_moves(input_piece_id)
            print(moves)

            input_move = input("Enter place e.g(1h,2a)")
            move_x = int(input_move[0])
            move_y = input_move[1]

            print(f"Enter move: {move_x},{move_y}")

            eliminated_piece = self.move_piece(input_piece_id, movement=(move_x, move_y))
            if eliminated_piece:
                if eliminated_piece.get_id() == "Bk1":
                    print("*************")
                    print("White player won")
                    break
                if eliminated_piece.get_id() == "Wk1":
                    print("*************")
                    print("Black player won")
                    break
                print("Eliminated piece ", eliminated_piece.get_id())


if __name__ == '__main__':
    chess_board = Board()
    chess_board.setup(primary_player='w')
    chess_board.start()
