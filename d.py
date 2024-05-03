from tkinter import *

user = "X"
buttons = [[0, 0, 0],
           [0, 0, 0],
           [0, 0, 0]]
state = [['', '', ''],
         ['', '', ''],
         ['', '', '']]

window = Tk()
window.title("Toe Tic Tac")
board = Frame(window).grid(row=0, column=0)

def check(s):
    terminal = False
    winner = ''

    # Check rows, columns, and diagonals for a win or draw
    for row in s:
        if all(e != '' and e == row[0] for e in row):
            terminal = True
            winner = row[0]

    for c in range(3):
        col = []
        for r in range(3):
            col.append(s[r][c])
        if all(e != '' and e == col[0] for e in col):
            terminal = True
            winner = col[0]

    diagonal = [s[0][0], s[1][1], s[2][2]]
    if all(e != '' and e == diagonal[0] for e in diagonal):
        terminal = True
        winner = diagonal[0]

    diagonal = [s[0][2], s[1][1], s[2][0]]
    if all(e != '' and e == diagonal[0] for e in diagonal):
        terminal = True
        winner = diagonal[0]

    # Check if it's a draw
    hasSpace = any('' in row for row in s)
    if winner == '' and not hasSpace:
        terminal = True

    return terminal, winner

def getTurn(s):
    numX = 0
    numO = 0

    for row in s:
        for e in row:
            if e == 'X':
                numX += 1
            elif e == 'O':
                numO += 1

    if numX == numO:
        return 'X'
    elif numX > numO:
        return 'O'
    else:
        print(f"{numX},{numO}")

def getSuccessors(s, play):
    actions = []
    successors = []

    # Determine possible actions
    for r in range(3):
        for c in range(3):
            if s[r][c] == '':
                actions.append([r, c])

    # Append resulting state of action into successors list
    for a in actions:
        successor = [['', '', ''], ['', '', ''], ['', '', '']]
        for r in range(3):
            for c in range(3):
                successor[r][c] = s[r][c]
        successor[a[0]][a[1]] = play
        successors.append(successor)

    return actions, successors

def max_value(s):
    m = float('-inf')
    move = []
    actions, successors = getSuccessors(s, 'X')
    for i in range(len(successors)):
        v = value(successors[i])
        if v > m:
            m = v
            move = actions[i]
    return m

def min_value(s):
    m = float('inf')
    move = []
    actions, successors = getSuccessors(s, 'O')
    for i in range(len(successors)):
        v = value(successors[i])
        if v < m:
            m = v
            move = actions[i]
    return m

def value(s):
    terminal, winner = check(s)
    turn = getTurn(s)

    if terminal:
        if winner == 'X':  # If AI wins
            return 1
        elif winner == 'O':  # If User wins
            return -1
        else:  # If it's a draw
            return 0
    elif turn == 'X':
        return max_value(s)
    elif turn == 'O':
        return min_value(s)

def update(r, c):
    buttons[r][c].config(text=user, fg='blue')
    buttons[r][c].grid(row=r, column=c)
    state[r][c] = user

    terminal, winner = check(state)
    if terminal:
        if winner == 'X':
            print("X Loses")
        elif winner == 'O':
            print("X Wins")
        else:
            print("DRAW")
    else:
        values = []
        actions, successors = getSuccessors(state, 'O')
        for s in successors:
            values.append(value(s))

        print(f"THE VALUES: {values}")
        print(f"THE ACTIONS: {actions}")
        move = actions[values.index(max(values))]
        print(f"MOVE: {move}")
        buttons[move[0]][move[1]].config(text='O', fg='red')
        buttons[move[0]][move[1]].grid(row=move[0], column=move[1])
        state[move[0]][move[1]] = 'O'

for r in range(3):
    for c in range(3):
        buttons[r][c] = Button(board, text=state[r][c], font=('Cocogoose', 60), width=3, height=1,
                               command=lambda row=r, col=c: update(row, col))
        buttons[r][c].grid(row=r, column=c)

window.mainloop()