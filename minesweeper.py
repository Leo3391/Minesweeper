import random
import logging
import pprint


# Logging
def log(obj: object) -> None:
    logging.info("\n%s", pprint.pformat(obj))

logging.basicConfig(
        level=logging.CRITICAL,
        format="%(levelname)s: %(message)s"
)


def get_input(grid):
    printing(grid)
    print("row col (f)")
    s = input("> ")
    if s[-1] == "f":
        flag = True
        s = s[:-1]
    else:
        flag = False
    x, y = (int(i) for i in s.split())
    return x, y, flag


def printing(grid):
    cols = len(grid[0])
    rows = len(grid)
    cl = len(str(cols))
    rl = len(str(rows))
    print(" "*(cl)+" "+"  ".join("\b"*(len(str(i))-1)+str(i) for i in range(cols)))
    for i in range(rows):
        print(str(i).rjust(rl)+"["+"][".join(grid[i])+"]")


def check(x, y, mines):
    rows = len(mines)
    cols = len(mines[0])
    count = 0

    for dx in (-1, 0, 1):
        for dy in (-1, 0, 1):
            if dx == 0 and dy == 0:
                continue  # don't count the center cell

            nx, ny = x + dx, y + dy

            if 0 <= nx < rows and 0 <= ny < cols:
                if mines[nx][ny] == 1:
                    count += 1

    return count


def open_block(x, y, mines, status):
    rows = len(mines)
    cols = len(mines[0])

    # out of bounds or already revealed / flagged
    if not (0 <= x < rows and 0 <= y < cols):
        return
    if status[x][y] != "x":
        return

    # reveal this cell
    n = check(x, y, mines)  # number of surrounding mines
    status[x][y] = " " if n == 0 else str(n)

    # if no surrounding mines, open neighbors recursively
    if n == 0:
        for dx in (-1, 0, 1):
            for dy in (-1, 0, 1):
                if dx == 0 and dy == 0:
                    continue
                open_block(x + dx, y + dy, mines, status)


def check_win(mines, status):
    rows = len(mines)
    cols = len(mines[0])
    
    for r in range(rows):
        for c in range(cols):
            # if it's not a mine and still hidden, player hasn't won
            if mines[r][c] != 1 and status[r][c] == "x":
                return False
    return True


rows = int(input("Rows: "))
cols = int(input("Cols: "))
mine = int(input(f"Mines (<{rows*cols}): "))
mines = [[0 for _ in range(cols)] for _ in range(rows)]
status = [["x" for _ in range(cols)] for _ in range(rows)]

input_x, input_y, flag = get_input(status)
for i in range(mine):
    while True:
        x, y  = random.randint(0, cols-1), random.randint(0, rows-1)
        if (x, y) != (input_x, input_y) and not mines[x][y]:
            mines[x][y] = 1
            break

log(mines)

while True:

    if flag and status[input_x][input_y] == "x":
        status[input_x][input_y] = "f"
    elif flag and status[input_x][input_y] == "f":
        status[input_x][input_y] = "x"
        input_x, input_y, flag = get_input(status)
        continue

    if mines[input_x][input_y] and status[input_x][input_y] != "f":
        print("You lose!")
        break
    else:
        open_block(input_x, input_y, mines, status)

    if check_win(mines, status):
        print("You win!")
        break
    
    input_x, input_y, flag = get_input(status)

printing(status)
print("\nMines:")
printing([[str(j) for j in i] for i in mines])
