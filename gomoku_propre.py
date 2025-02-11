# %% Imports

import numpy as np
import time
from math import *

# %% Constantes

joueur_humain = input("Voulez-vous jouer avec les noirs (X) ? (O pour les blancs) : ").strip().upper() == 'X'
player = 'X' if joueur_humain else 'O'
CPU = 'O' if joueur_humain else 'X'

dim = 15
N = 60 #est 'X'
B = 60 #est 'O'

# %% Fonctions Gomoku

def Gomoku():
    global N
    global B
    
    s = init_board()
    afficher_plateau(s)
    
    #Deux cas : IA est premier ou le joueur l'est
    if 'X' == CPU:
        #début selon la variante
        s = long_pro(s, CPU)
        
        #Déroulé avec Minimax
        while not(all(Terminal_test(s))):
                
            #Tour du joueur
            print("Pions blancs :", B, "\nPions noirs :", N)
            pos_x, pos_y = interaction_joueur(s)
            s = Result(s,(pos_x, pos_y), player)
            print(player)
            pion_utilise(player)
            
            #Vérification si victoire    
            fin = Terminal_test(s)
            if fin[0] == True :
                afficher_plateau(s)
                print("le joueur a gagné") if fin[1] == player else (print("L'IA a gagné") if fin[1] == CPU else print("Match nul"))
                return
            
            #Tour de l'IA
            print("Tour de l'IA")
            next_act = Minimax_AlphaBeta(s)
            s = Result(s, next_act, CPU)
            pion_utilise(CPU)
            
            #Vérification si victoire    
            fin = Terminal_test(s)
            if fin[0] == True :
                afficher_plateau(s)
                print("le joueur a gagné") if fin[1] == player else (print("L'IA a gagné") if fin[1] == CPU else print("Match nul"))
                return
    
        return 'Match nul'
    
    elif 'X' == player:
        #début selon la variante
        s = long_pro(s, player)
        
        #Déroulé avec Minimax
        while not(all(Terminal_test(s))):
            
            #Tour de l'IA
            print("Tour de l'IA")
            next_act = Minimax_AlphaBeta(s)
            s = Result(s, next_act, CPU)
            pion_utilise(CPU)
            
            #Vérification si victoire    
            fin = Terminal_test(s)
            if fin[0] == True :
                afficher_plateau(s)
                print("le joueur a gagné") if fin[1] == player else (print("L'IA a gagné") if fin[1] == CPU else print("Match nul"))
                return
    
            #Tour du joueur
            print("Pions blancs :", B, "\nPions noirs :", N)
            pos_x, pos_y = interaction_joueur(s)
            s = Result(s,(pos_x, pos_y), player)
            pion_utilise(player)
            
            #Vérification si victoire    
            fin = Terminal_test(s)
            if fin[0] == True :
                afficher_plateau(s)
                print("le joueur a gagné") if fin[1] == player else (print("L'IA a gagné") if fin[1] == CPU else print("Match nul"))
                return
    
        return 'Match nul'

def long_pro(s, play):
    if play == CPU:
        s = Result(s, (7,7), 'X')
        pion_utilise(CPU)

        print("Pions blancs :", B, "\nPions noirs :", N)
        pos_x, pos_y = interaction_joueur(s)
        s = Result(s,(pos_x, pos_y), player)
        pion_utilise(player)
        
        s_debut = s.copy()
        for i in range(1, 8):
            for j in range(1, 8):
                s_debut[3 + i][3 + j] = "1"
        

        print("Tour de l'IA")
        alpha = -inf
        beta = inf
        next_act = Minimax_AlphaBeta(s_debut)
        s = Result(s, next_act, CPU)
    
        pion_utilise(CPU)
        
    elif play == player:
        s = Result(s, (7,7), 'X')
        pion_utilise(player)
        
        print("Tour de l'IA")
        alpha = -inf
        beta = inf
        next_act = Minimax_AlphaBeta(s)
        s = Result(s, next_act, CPU)
        pion_utilise(CPU)
        
        s_debut = s.copy()
        for i in range(1, 8):
            for j in range(1, 8):
                s_debut[3 + i][3 + j] = "1"

        print("Pions blancs :", B, "\nPions noirs :", N)
        pos_x, pos_y = interaction_joueur(s_debut)
        s = Result(s,(pos_x, pos_y), player)
        pion_utilise(player)
        
    return s

# %% Fonctions de plateau

directions = [(0,1), (1,0), (1,1), (1, -1)]

def init_board():
    return np.array([['-'] * 15] * 15)

def valid_move(s, pos):
    return (s[pos[0]][pos[1]] == '-')

def pion_utilise(play):
    global N
    global B
    if play == 'X' :
        N = N - 1
    elif play == "O":
        B = B - 1

# %% Fonctions d'interface

def afficher_plateau(plateau):
    print("  " + " ".join(f"{i :3}" for i in range(15)))  # En-tête des colonnes
    for i, ligne in enumerate(plateau):
        print(f"{chr(65 + i):2} " + " ".join(" . " if case == '-' else (" N " if case == 'X' else " B ") for case in ligne))

def interaction_joueur(s):
    print("Tour du joueur")
    afficher_plateau(s)

    # Demander la position au joueur
    position = input("Veuillez entrer une position pour votre pion (ex: A7) : ").upper()

    # Vérification de la validité de l'entrée
    while not (len(position) <= 3 and position[0] in "ABCDEFGHIJKLMNO" and position[1:].isdigit() and int(position[1:]) >= 0 and int(position[1:]) <= 14):
        print("Entrée invalide. Essayez encore.")
        position = input("Veuillez entrer une position (ex: A7) : ").upper()

    row = ord(position[0]) - ord('A')
    col = int(position[1:])

    if valid_move(s, (row, col)):
        return row, col
    else:
        print("Case déjà occupée. Essayez à nouveau.")
        return interaction_joueur(s)
    
# %% Fonctions de base du MiniMax

def Actions(s):
    list_actions = []
    for i in range(s.shape[0]): #row
        for j in range(s.shape[1]): #column
            #print(i,j)
            if s[i][j] == '-':
                list_actions.append((i,j))
    return list_actions

def Result(s,a,play): #testé
    res_state = s.copy()
    #print(s)
    res_state[a[0]][a[1]] = play
    return res_state

def Terminal_test(s): #np.array ->  (bool, str) (etat, joueur qui gagne ou non)
    if N == 0 and B == 0: #plus de pièces
        return True, 'Nul'
    
    ali = align(s)
    for i in ali:
        if i[0] == 5: #qqn a un alignement de 5
            #print(ali)
            #print(ali.index(i))
            return True, i[1]
        
    return False, False

# %% Fonctions de base du MiniMax - Special Utility

def Utility(board):
    # Score basé sur des alignements partiels
    alignements = align(board)
    player_score = list(filter(lambda x : x[1] == player, alignements))
    player_score = sum(list(map(ali_3_4_5, player_score)))
    
    CPU_score = list(filter(lambda x : x[1] == CPU, alignements))
    CPU_score = sum(list(map(ali_3_4_5, CPU_score)))

    #vérifie si bloque
    block_score = 60 * block_opponent(board, player)
    return CPU_score - player_score + block_score

# %% Alignements

def align(s): 
    #alignements de tout le plateau
    L = []
    
    #print('\nColonnes')
    #Colonnes
    for i in range(dim-5):
        for j in range(dim):
            player = s[i][j]
            if player != '-':
                cpt_temp_c = 1
                
                for k in range(1,5):
                    if s[i][j] == s[i+k][j] and i+k >= 0 and i+k <=14:
                        cpt_temp_c = cpt_temp_c + 1
                    else:
                        break

                L.append((cpt_temp_c, player))
  
                
    #print('\nLignes')
    #Lignes
    for i in range(dim):
        for j in range(dim-5):
            player = s[i][j]
            if player != '-':
                cpt_temp_l = 1
                
                for k in range(1,5):
                    if s[i][j] == s[i][j+k] and j+k >= 0 and j+k <=14:
                        cpt_temp_l = cpt_temp_l + 1
                    else:
                        break

                L.append((cpt_temp_l, player))
                
    
    #print('\nDiag')
    #Diagonale
    for i in range(dim):
        for j in range(dim):
            if s[i][j] != '-':
                player = s[i][j]
                cpt_temp_d = 1

                L_res = [] #liste des résultats d'égalité
                for k in range(1,5):
                    if i+k < 15 and j+k < 15 and s[i][j] == s[i+k][j+k]:
                            cpt_temp_d = cpt_temp_d + 1
                    else:
                        break

                L.append((cpt_temp_d, player))

                

    #print('\nContrediag')
    #Contre Diagonale
    for i in range(dim):
        for j in range(dim):
            if s[i][j] != '-':
                player = s[i][j]
                cpt_temp_cd = 1

                for k in range(1,5):
                    if i+k < 15 and j-k >= 0 and s[i][j] == s[i+k][j-k]:
                            cpt_temp_cd = cpt_temp_cd + 1
                    else:
                        break
                    
                L.append((cpt_temp_cd, player))
                    
    if L == []:
        L.append((0, '_')) #plateau vide
        
    return L


def block_opponent(s, player): #plateau et symbole de l'adversaire
    # Si l'action bloque un alignement de 4 alors Utility ++
    current, opp = ('X', 'O') if player == 'O' else ('O', 'X')
    nb_block = 0
    pattern_4 = [[opp, opp, opp, opp, current],
                 [opp, opp, opp, current, opp],
                 [opp, opp, current, opp, opp],
                 [opp, current, opp, opp, opp],
                 [current, opp, opp, opp, opp]]
    pattern_3 = [[current, opp, opp, opp, '-'], [opp, opp, opp, current, '-']]
    
    for i in range(dim - 5):
        for j in range(dim):
            play = s[i][j]
            if s[i][j] != '-':
                
                #Colonnes
                if [s[i][j], s[i+1][j], s[i+2][j], s[i+3][j], s[i+4][j]] in pattern_4:
                    nb_block += 1
                elif [s[i][j], s[i+1][j], s[i+2][j], s[i+3][j], s[i+4][j]] in pattern_3:
                    nb_block += 0.5
    
    for i in range(dim):
        for j in range(dim - 5):
            play = s[i][j]
            if s[i][j] != '-':
                
                #Lignes
                if [s[i][j], s[i][j+1], s[i][j+2], s[i][j+3], s[i][j+4]] in pattern_4:
                    nb_block += 1
                elif [s[i][j], s[i][j+1], s[i][j+2], s[i][j+3], s[i][j+4]] in pattern_3:
                    nb_block += 0.5

    for i in range(dim):
        for j in range(dim):
            play = s[i][j]
            if s[i][j] != '-':
                
                #Diagonales
                L_res = [] #liste des résultats d'égalité
                L_res.append(s[i][j])
                for k in range(1,5):
                    if i+k < 15 and j+k < 15:
                        L_res.append(s[i+k][j+k])
                #print(L_res)
                #print('Diagonale', L_res)
                if L_res in pattern_4:
                    nb_block += 1
                elif L_res in pattern_3:
                    nb_block += 0.5
                
    for i in range(dim):
        for j in range(dim):
            play = s[i][j]
            if s[i][j] != '-':
                
                #Contre Diagonales
                L_res = [] #liste des résultats d'égalité
                L_res.append(s[i][j])
                for k in range(1,5):
                    if i+k < 15 and j-k >= 0:
                        L_res.append(s[i+k][j-k])
                if L_res in pattern_4:
                    nb_block += 1
                elif L_res in pattern_3:
                    nb_block += 0.5
    return nb_block
        
def ali_3_4_5(alignement):
    score = alignement[0]
    if score == 3:
        score += 10
    elif score == 4:
        score +=20
    elif score == 5:
        score+= 80
    return score

# %% Minimax AlphaBeta

profondeur = 0
limit_prf = -100

def Minimax_AlphaBeta(state):
    global profondeur
    profondeur = 0
    """
    global limit_prf
    empty_cells = np.sum(state == '-')
    limit_prf = max(-25, -int(empty_cells / 4))
    """
    start = time.time()
    play = CPU
    val = -inf
    alpha, beta = -inf, inf
    action = None
    for a in Actions(state):
        val_temp = Min_ValueBeta(Result(state, a, play), alpha, beta) #les infs pour pouvoir mettre les alpha et beta au début
        #print(val_temp)
        if val_temp > val: #on met le max dedans pour éviter plus de parcours de listes
            action = a
            val = val_temp
        #print(Utility(Result(state, action, play)))
    print(time.time() - start)
    #print(Utility(Result(state, action, play)))
    return action

def Max_ValueAlpha(s, alpha, beta):
    play = CPU
    global profondeur
    profondeur = profondeur - 1
    v = -inf
    
    #print(s)
    
    if Terminal_test(s):
        return Utility(s)
    if profondeur < limit_prf:
        return Utility(s)
    
    v = -inf
    for a in Actions(s):
        v = max(v, Min_ValueBeta(Result(s,a, play), alpha, beta)) #arg pour même alpha et beta pour max et min
    return v

def Min_ValueBeta(s, alpha, beta):
    play = player
    global profondeur
    profondeur = profondeur - 1
    v = inf
    
    #print(s)
    
    if Terminal_test(s):
        return Utility(s)
    if profondeur < limit_prf:
        return Utility(s)
    for a in Actions(s):
        v = min(v, Max_ValueAlpha(Result(s,a, play), alpha, beta))
        if v <= alpha:
            return v
        beta = min(beta, v)
    return v

# %% Main de test de Gomoku()

Gomoku()
