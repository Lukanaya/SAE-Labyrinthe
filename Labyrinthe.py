import tkinter as tk
import random
import time
#Dimensions du plateau/cases
WIDTH = 11
HEIGHT = 11
dim_case = 30

labyrinthe = [[0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0], 
              [0, 1, 1, 1, 0, 1, 0, 1, 0, 1, 0], 
              [0, 0, 0, 0, 0, 1, 0, 1, 0, 1, 0], 
              [1, 1, 1, 1, 1, 1, 0, 1, 0, 1, 0], 
              [0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0], 
              [0, 1, 0, 1, 1, 1, 1, 1, 1, 1, 0], 
              [0, 1, 0, 1, 0, 0, 0, 1, 0, 0, 0], 
              [0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 1], 
              [0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0], 
              [0, 1, 1, 1, 0, 1, 0, 1, 0, 1, 0], 
              [0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0]]

#Création de la fenêtre Tkinter
affichage = tk.Tk()
affichage.title("Génération d'un plateau")

#Création du widget Canvas pour afficher le plateau
canvas = tk.Canvas(affichage, width=WIDTH * dim_case, height=HEIGHT * dim_case)
canvas.pack()

#Génération de deux cases aléatoires sur le plateau
def generer_n_cases_aleatoire(n):
    #Création d'un plateau de taille WIDTH x HEIGHT
    plateau = [[1 for _ in range(WIDTH)] for _ in range(HEIGHT)]
    
    for _ in range(n):
        x = random.randint(0, WIDTH-1); y = random.randint(0, HEIGHT -1)
        while plateau[x][y] == 0:
            x = random.randint(0, WIDTH-1); y = random.randint(0, HEIGHT -1)
        plateau[x][y] = 0
        draw_plateau(plateau)
        #permet de faire une pause de 1s entre l'affichage des deux carrés
        affichage.update()
        time.sleep(1)
        
def direction_aleatoire(direction):
    if len(direction) == 1:
        i = 0
    else:
        i = random.randint(0, len(direction) - 1)
    return direction[i]
      

def deplacementX(direction):
    valeur = 0
    if direction == "gauche":
        valeur = - 1
    elif direction == "droite":
        valeur = + 1
    return valeur
    
def deplacementY(direction):
    valeur = 0
    if direction == "haut":
        valeur = - 1
    elif direction == "bas":
        valeur = + 1
    return valeur 
    

def direction_possible(posX, posY, plateau):
    direction_possible = []
    if posX - 1 >= 0 and plateau[posX - 1][posY] == 0:
        direction_possible.append("gauche")
    if posX + 1 < len(plateau) and plateau[posX + 1][posY] == 0:
        direction_possible.append("droite")
    if posY - 1 >= 0 and plateau[posX][posY - 1] == 0:
        direction_possible.append("haut")
    if posY + 1 < len(plateau[0]) and plateau[posX][posY + 1] == 0:
        direction_possible.append("bas")
    return direction_possible


#Resolution DFS
def resolDFS(plateau):

    posX = 0
    posY = 0
    posFinalX = WIDTH - 1
    posFinalY = HEIGHT - 1
    resol = False
    pile = []
    pile.append([posX,posY])
    plateau[posX][posY] = 2
    while not resol:
        print(posX, posY)
        if direction_possible(posX, posY, plateau) == [] and len(pile) > 0:
            print("a")
            plateau[posX][posY] = 3
            precedent = pile.pop()
            posX = precedent[0]
            posY = precedent[1]
        else:
            print("b")
            direction = direction_aleatoire(direction_possible(posX, posY, plateau))
            posX = posX + deplacementX(direction)
            posY = posY + deplacementY(direction)
            plateau[posX][posY] = 2
            pile.append([posX,posY])
        if posX == posFinalX and posY == posFinalY:
            resol = True
        draw_plateau(plateau)
        affichage.update()
        time.sleep(0.1)
        

    



#Fonction pour dessiner le plateau sur le Canvas
def draw_plateau(plateau):
    canvas.delete("all")
    for y in range(HEIGHT):
        for x in range(WIDTH):
            if plateau[x][y] == 1:
                canvas.create_rectangle(x * dim_case, y * dim_case, (x+1) * dim_case, (y+1) * dim_case, fill="black", outline="gray")
            elif plateau[x][y] == 0:
                canvas.create_rectangle(x * dim_case, y * dim_case, (x+1) * dim_case, (y+1) * dim_case, fill="white", outline="gray")
            elif plateau[x][y] == 2:
                canvas.create_rectangle(x * dim_case, y * dim_case, (x+1) * dim_case, (y+1) * dim_case, fill="blue", outline="gray")
            elif plateau[x][y] == 3:
                canvas.create_rectangle(x * dim_case, y * dim_case, (x+1) * dim_case, (y+1) * dim_case, fill="red", outline="gray")    
                    
#Bouton pour lancer "generer_n_case_aleatoire"
n = 2 #nbr de carrés
start_button = tk.Button(affichage, text = "Générer le plateau")
start_button.pack()
start_button = tk.Button(affichage, text = "Resoudre en DFS", command=lambda: resolDFS(labyrinthe))
start_button.pack()

#Lancer la boucle principale de l'application
affichage.mainloop()