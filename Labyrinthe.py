import tkinter as tk
import random
import time
#Dimensions du plateau/cases
WIDTH = 11
HEIGHT = 11
dim_case = 30

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
    i = random.randint(1,len(direction))
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
    if posX - 1 < 0 and plateau[posX - 1][posY] == 0:
        direction_possible += "gauche"
    if posX + 1 < 0 and plateau[posX + 1][posY] == 0:
        direction_possible += "droite"
    if posY - 1 < 0 and plateau[posX][posY - 1] == 0:
        direction_possible += "haut"
    if posY - 1 < 0 and plateau[posX][posY + 1] == 0:
        direction_possible += "bas"
    return direction_possible

def inverser_direction(direction):
    if direction == "gauche":
        retour = "droite"
    if direction == "droite":
        retour = "gauche"
    if direction == "haut":
        retour = "bas"
    if direction == "bas":
        retour = "haut"
    return retour
    

#Resolution DFS
def resolDFS(plateau):
    posX = 0
    posY = 0
    posFinalX = WIDTH - 1
    posFinalY = HEIGHT - 1
    resol = False
    pile = []
    pile.append([posX,posY])
    while not resol:
        if direction_possible(posX, posY) == []:
            prescedant = pile.pop()
            posX = prescedant[0]
            posY = prescedant[1]
        else:
            direction = direction_aleatoire(direction_possible(posX, posY))
            plateau[posX][posY] = -1
            posX = posX + deplacementX(direction)
            posY = posY + deplacementY(direction)
            pile.append([posX,posY])
        if plateau[posX][posY] == plateau[posFinalX][posFinalY]:
            resol = True

    



#Fonction pour dessiner le plateau sur le Canvas
def draw_plateau(plateau):
    canvas.delete("all")
    for y in range(HEIGHT):
        for x in range(WIDTH):
            if plateau[x][y] == 1:
                canvas.create_rectangle(x * dim_case, y * dim_case, (x+1) * dim_case, (y+1) * dim_case, fill="white", outline="gray")
            else :
                if plateau[x][y] == 0:
                    canvas.create_rectangle(x * dim_case, y * dim_case, (x+1) * dim_case, (y+1) * dim_case, fill="red", outline="gray")
                    
#Bouton pour lancer "generer_n_case_aleatoire"
n = 2 #nbr de carrés
start_button = tk.Button(affichage, text = "Générer le plateau")
start_button.pack()
start_button = tk.Button(affichage, text = "Resoudre en DFS", command=lambda: resolDFS())
start_button.pack()

#Lancer la boucle principale de l'application
affichage.mainloop()