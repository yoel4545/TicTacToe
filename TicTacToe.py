#!/usr/bin/env python3
"""
Tic-Tac-Toe (Tres en línea) - versión con nombres de jugadores.
Opciones: jugador vs jugador o jugador vs CPU (IA con Minimax).
"""

import math
import random

WIN_COMBINATIONS = [
    (0,1,2), (3,4,5), (6,7,8),
    (0,3,6), (1,4,7), (2,5,8),
    (0,4,8), (2,4,6)
]

def display_board(board):
    lines = []
    for i in range(0, 9, 3):
        lines.append(' {} | {} | {} '.format(board[i] or str(i+1), board[i+1] or str(i+2), board[i+2] or str(i+3)))
    sep = '\n---+---+---\n'
    print('\n' + sep.join(lines) + '\n')

def available_moves(board):
    return [i for i, val in enumerate(board) if val == '']

def winner(board):
    for a, b, c in WIN_COMBINATIONS:
        if board[a] and board[a] == board[b] == board[c]:
            return board[a]
    return None

def is_full(board):
    return all(cell != '' for cell in board)

def minimax(board, player, maximizing_player, ai_symbol, human_symbol):
    win = winner(board)
    if win == ai_symbol:
        return 1, None
    elif win == human_symbol:
        return -1, None
    elif is_full(board):
        return 0, None

    if maximizing_player:
        best_score = -math.inf
        best_move = None
        for mv in available_moves(board):
            board[mv] = ai_symbol
            score, _ = minimax(board, human_symbol, False, ai_symbol, human_symbol)
            board[mv] = ''
            if score > best_score:
                best_score = score
                best_move = mv
        return best_score, best_move
    else:
        best_score = math.inf
        best_move = None
        for mv in available_moves(board):
            board[mv] = human_symbol
            score, _ = minimax(board, ai_symbol, True, ai_symbol, human_symbol)
            board[mv] = ''
            if score < best_score:
                best_score = score
                best_move = mv
        return best_score, best_move

def cpu_move(board, ai_symbol, human_symbol):
    if len(available_moves(board)) == 9:
        return random.choice([0, 2, 4, 6, 8])
    _, move = minimax(board, ai_symbol, True, ai_symbol, human_symbol)
    return move

def player_move(board, name, symbol):
    while True:
        try:
            choice = input(f"{name} ({symbol}), elige casilla (1-9): ")
            idx = int(choice) - 1
            if idx not in range(9):
                print("Número inválido. Intenta otra vez.")
                continue
            if board[idx] != '':
                print("Casilla ocupada. Elige otra.")
                continue
            return idx
        except ValueError:
            print("Entrada inválida. Escribe un número del 1 al 9.")

def choose_mode():
    print("Modo de juego:\n1) Jugador vs Jugador\n2) Jugador vs CPU")
    while True:
        opt = input("Elige 1 o 2: ")
        if opt in ('1', '2'):
            return int(opt)
        print("Opción inválida.")

def choose_symbol():
    while True:
        s = input("Elige tu símbolo para el jugador 1 (X/O). X empieza primero: ").upper()
        if s in ('X', 'O'):
            return s
        print("Elige X o O.")

def play():
    print("\nBienvenido a Tic-Tac-Toe (Tres en línea).\n")
    mode = choose_mode()
    board = [''] * 9

    if mode == 1:
        # Jugador vs Jugador
        player1 = input("Nombre del Jugador 1: ") or "Jugador 1"
        player2 = input("Nombre del Jugador 2: ") or "Jugador 2"

        current = 'X'
        display_board(board)
        while True:
            name = player1 if current == 'X' else player2
            mv = player_move(board, name, current)
            board[mv] = current
            display_board(board)
            w = winner(board)
            if w:
                ganador = player1 if w == 'X' else player2
                print(f"¡{ganador} ({w}) gana!")
                break
            if is_full(board):
                print("Empate.")
                break
            current = 'O' if current == 'X' else 'X'

    else:
        # Jugador vs CPU
        human_name = input("Tu nombre: ") or "Jugador"
        human_symbol = choose_symbol()
        ai_symbol = 'O' if human_symbol == 'X' else 'X'
        current = 'X'
        display_board(board)
        while True:
            if current == human_symbol:
                mv = player_move(board, human_name, human_symbol)
                board[mv] = human_symbol
            else:
                print("CPU está jugando...")
                mv = cpu_move(board, ai_symbol, human_symbol)
                board[mv] = ai_symbol
                print(f"CPU colocó en la casilla {mv+1}.")
            display_board(board)
            w = winner(board)
            if w:
                if w == human_symbol:
                    print(f"¡Felicidades, {human_name}! Ganaste.")
                else:
                    print("La CPU gana. Mejor suerte la próxima.")
                break
            if is_full(board):
                print("Empate.")
                break
            current = 'O' if current == 'X' else 'X'

    if input("¿Jugar otra vez? (s/n): ").lower().startswith('s'):
        play()

if __name__ == '__main__':
    play()
