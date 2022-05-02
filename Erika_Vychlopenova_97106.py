# Erika Vychlopenova, ID: 97106
# Clovece, nehnevaj sa!
# Projekt PROG1

import random


def cube():  # vrati nahodne cislo
    randomNumber = random.randint(1, 6)
    return randomNumber


def gensachovnica(n):
    # check ci je zadany spravny rozmer sachovnice, program bude pytat vstup, pokial nebude spravny (t.j. neparny a vacsi ako 5)
    if ((n % 2) == 1 and n >= 5):
        print("Bol zadany vhodny rozmer, pokracujeme... \n")
    else:
        while ((n % 2) == 0 or n < 5):
            print("Bol zadany nevhodny rozmer...")
            n = int(input("Zadaj velkost znova: "))
        print("Bol zadany vhodny rozmer, pokracujeme... \n")

    # prazdny zoznam, teda vypis znaku " "
    board = []
    for i in range(0, n):
        pom = []
        for j in range(0, n):
            pom.append(" ")
        board.append(pom)

    center = int(n / 2)
    plusOne = int(n / 2) + 1
    minusOne = int(n / 2) - 1

    # vypis znaku "*" okolo znaku "D", znak "D" zapisem neskor, pretoze by prepisovalo viac "*"
    for i in range(0, n):
        for j in range(0, n):
            board[i][plusOne] = "*"
            board[plusOne][i] = "*"
            board[i][minusOne] = "*"
            board[minusOne][i] = "*"

    # vypis znaku "D" do kriza
    for i in range(0, n):
        board[i][center] = "D"
        board[center][i] = "D"

    # prepisat krajne, stredne znaky "D" za "*"
    board[0][center] = "*"
    board[center][0] = "*"
    board[n - 1][center] = "*"
    board[center][n - 1] = "*"

    # vypis znaku "X" do stredu sachovnice, musim zapisat po zapisani "D", pretoze ho prepise
    board[center][center] = "X"

    return board


def TlacSachovnicu(board):  # vypis sachovnice v konzole
    for i in range(0, len(board)):
        for j in board[i]:
            print(j, end=" ")
        print()


def game(board, boardSize, rowA, colA, rowB, colB):
    current = "B"
    movepointY = 1
    movepointX = 1

    won = False
    collision = False
    collisionSteps = 0

    row = rowA
    col = colA

    while not won:
        # vymena hracov
        if current == "A":
            current = "B"
            row = rowB
            col = colB
        else:
            current = "A"
            row = rowA
            col = colA

        # "hodi" sa kocka, nahodne cislo sa ulozi do premennej steps
        steps = cube()
        print("Hrac", current, "hodil pocet", steps)

        # hodene cislo sa dekrementuje o 1. Kolko padlo cislo, tolkokrat sa pohyb zopakuje
        # chcela som spravit pohyb po jednom policku a premazavat konzolu, pre viac lively feeling,
        # ale v zadani je, ze takto nemozeme :(
        while (steps > 0):
            won, board, row, col, collision, collisionSteps = move(won, board, boardSize, current, row, col,
                                                                   collision, collisionSteps)
            steps -= 1
            if won:
                break
        # po pohybe si ulozim do premennych poziciu aktualneho hraca, teda updatujem stare udaje
        if current == "A":
            rowA = row
            colA = col
        else:
            rowB = row
            colB = col
        # tlac sachovnice som povodne mala v cykle, teda vypisovalo kazdy krok
        TlacSachovnicu(board)
        print()

    # if won = True, teda az skonci hra, vykona tieto vypisy
    print("Game over")
    print("Player", current, "won!")


def move(won, board, boardSize, player, row, col, collision, collisionSteps):
    # zistim si, ktory hrac je aktualny a ktory je nepriatel, teda ten druhy
    if player == "A":
        other = "B"
    else:
        other = "A"

    # pohyb po x a y osi, teda riadkoch, stlpcoch, znamienko sa meni podla kvadrantu v ktorom figurka je
    if col < boardSize / 2:
        movepointY = -1
    else:
        movepointY = 1

    if row > boardSize / 2:
        movepointX = -1
    else:
        movepointX = 1

    # pohyb som riesila tak, ze hrac najprv zisti, v ktorom kvadrante sa nachadza, zisti si smer ktorym ma ist (hore, dole,
    # doprava, dolava) a posunie sa o jedno dopredu. Kedze som to chcela vypisovat po jednom kroku, tak sa posunie o jedno
    # policko a zistuje si kvadrant a smer znova, tolko krat, kolko "padlo" nahodne cislo z kocky
    # ked sa cislo dekrementuje na 0, znamena to, ze hrac sa posunul o tolko policok kolko mal a ide druhy hrac
    # do row a col sa vo funkcii game zapise pozicia aktualneho(druheho) hraca

    # prvy kvadrant
    if row < boardSize - 1 and (board[row + movepointY][col] == "*" or board[row + movepointY][col] == other):
        if col == int((boardSize / 2) - 1) and row == 0:
            if board[row + movepointY][col] == other:
                board[row + movepointY][col] = player
                collision = True

            else:
                board[row][col + movepointX] = player
                collision = replace_old(col, collision, player, row, board, collisionSteps)
                if collision:
                    collisionSteps += 1
                col += 1
        elif col == int(boardSize / 2) and row == 0:
            if player == "B":  # aby hrac B pokracoval, pretoze tam nie je jeho domcek
                if board[row][col + 1] == other:
                    board[row][col + 1] = player
                    collision = True

                else:
                    board[row][col + 1] = player

                collision = replace_old(col, collision, player, row, board, collisionSteps)
                if collision:
                    collisionSteps += 1
                col += 1
            else:
                board[row + 1][col] = player
                collision = replace_old(col, collision, player, row, board, collisionSteps)
                if collision:
                    collisionSteps += 1
                won = True
        elif col == int((boardSize / 2) + 1) and row == 0:
            if board[row + 1][col] == other:
                board[row + 1][col] = player
                collision = True
            else:
                if board[row + 1][col] == other:
                    board[row + 1][col] = player
                    collision = True

                else:
                    board[row + 1][col] = player

            collision = replace_old(col, collision, player, row, board, collisionSteps)
            if collision:
                collisionSteps += 1
            row += 1
        else:
            if board[row + movepointY][col] == other:
                board[row + movepointY][col] = player
                collision = True

            else:
                board[row + movepointY][col] = player

            collision = replace_old(col, collision, player, row, board, collisionSteps)
            if collision:
                collisionSteps += 1
            row += movepointY

    # stvrty kvadrant
    elif col < boardSize - 1 and board[row][col + movepointX] == "*" or board[row][col + movepointX] == other:
        if col == int((boardSize / 2)) and row == boardSize - 1 and player == "B":  # -1
            board[row - 1][col] = player
            board[row][col] = "*"
            won = True
        else:
            if board[row][col + movepointX] == other:
                board[row][col + movepointX] = player
                collision = True
            else:
                board[row][col + movepointX] = player

            collision = replace_old(col, collision, player, row, board, collisionSteps)
            if collision:
                collisionSteps += 1
            col += movepointX

    # treti kvadrant
    elif col >= 0 and board[row][col + movepointX] == "*" or board[row][col + movepointX] == other:
        if board[row][col + movepointX] == other:
            board[row][col + movepointX] = player
            collision = True

        else:
            board[row][col + movepointX] = player

        collision = replace_old(col, collision, player, row, board, collisionSteps)
        if collision:
            collisionSteps += 1
        col += movepointX

    # druhy kvadrant
    elif row >= 0 and board[row + movepointY][col] == "*" or board[row + movepointY][col] == other:
        if board[row + movepointY][col] == other:
            board[row + movepointY][col] = player
            collision = True

        else:
            board[row + movepointY][col] = player

        collision = replace_old(col, collision, player, row, board, collisionSteps)
        if collision:
            collisionSteps += 1
        row += movepointY

    return won, board, row, col, collision, collisionSteps


# osetrila som situaciu, kedy sa figurky stretnu na jednom policku, figurky sa preskocia(nevyhadzuju sa)
# inspirovala som sa pravidlami ked som clovece hravala
def replace_old(col, collision, player, row, board, collisionSteps):
    if collision:
        if collisionSteps == 1:
            if player == "A":
                board[row][col] = "B"
            else:
                board[row][col] = "A"
            collisionSteps = 0
            return False
        else:
            board[row][col] = "*"
        return True
    else:
        board[row][col] = "*"
        return False


def main():
    # zistime rozmer sachovnice
    boardSize = int(input("Zadaj velkost: "))
    board = gensachovnica(boardSize)
    # vlozenie figurok na sachovnicu
    board[0][int(boardSize / 2) + 1] = "A"
    board[boardSize - 1][int(boardSize / 2) - 1] = "B"
    # print sachovnice
    print("Sachovnica:")
    TlacSachovnicu(board)
    print()
    # zacni hru
    game(board, boardSize, 0, int(boardSize / 2) + 1, boardSize - 1, int(boardSize / 2) - 1)


main()
