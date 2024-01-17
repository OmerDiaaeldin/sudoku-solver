def solve_board(board):
    pos = find_empty(board)
    if not pos:
        return True
    for i in range(1,10):
        if(valid(board,i,pos)):
            board[pos[0]][pos[1]] = i
            if(solve_board(board)):
                return True
            board[pos[0]][pos[1]] = 0

    return False

def find_empty(board):
    for i in range(len(board)):
        for j in range(len(board[0])):
            if(board[i][j] == 0):
                return (i, j)
    return None

def valid(board, num, pos):
    row, col = pos
    for i in range(len(board[0])):
        if(board[row][i].value == num and i != col):
            return False
    for i in range(len(board)):
        if(board[i][col].value == num and i != row):
            return False
    mini_grid_row = row//3
    mini_grid_col = col//3

    for i in range(3*mini_grid_row, 3*mini_grid_row+3):
        for j in range(3*mini_grid_col, 3*mini_grid_col+3):
            if(board[i][j].value == num and not (i == row and j == col)):
                return False
    return True

def print_board(board):
    for row in range(len(board)):
        if (row % 3 == 0 and row != 0):
            print("----------------------")
        for column in range(len(board[0])):
            if(column%3 == 0 and column != 0):
                print("|", end=" ")
            print(board[row][column], end=" ")
            if(column == 8):
                print()