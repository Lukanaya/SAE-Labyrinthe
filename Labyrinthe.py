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
        
def direction_aleatoire():
    direction = ""
    dir = random.randint(1,4)
    match dir:
        case 1:
            direction = "haut"
        case 2:
            direction = "bas"
        case 3:
            direction = "gauche"
        case 4:
            direction = "droite"
    return direction      

def decalageX(direction):
    valeur = 0
    if direction == "gauche":
        valeur = - 2
    elif direction == "droite":
        valeur = + 2
    return valeur
    
def decalageY(direction):
    valeur = 0
    if direction == "haut":
        valeur = - 2
    elif direction == "bas":
        valeur = + 2
    return valeur 
    
# Génération du labyrinthe en partant de la case en haut a gauche pour arriver a la case en bas a droite    
def generer_labyrinthe():
    plateau = [[1 for _ in range(WIDTH)] for _ in range(HEIGHT)]
    
    #Position actuelle du curseur
    posX = 0
    posY = 0
    plateau[posX][posY] = 0
    
    while posX != WIDTH-1 or posY != HEIGHT-1:
        print(posX, posY)
        direction = direction_aleatoire()
        print(direction)
        decalageEnX = decalageX(direction)
        decalageEnY = decalageY(direction)
        posInvalide = (posX + decalageEnX < 0 or posX + decalageEnX > WIDTH-1 or posY + decalageEnY < 0 or posY + decalageEnY > HEIGHT-1) and plateau[posX + decalageEnX][posY + decalageEnY] !=1
        while(posInvalide):
            print(posInvalide)
            posInvalide = (posX + decalageEnX < 0 or posX + decalageEnX > WIDTH-1 or posY + decalageEnY < 0 or posY + decalageEnY > HEIGHT-1) and plateau[posX + decalageEnX][posY + decalageEnY] !=1
            direction = direction_aleatoire()
            print("nouvelle direction :", direction)
            decalageEnX = decalageX(direction)
            decalageEnY = decalageY(direction)
        
        # Nouvelle position du curseur
        nouvellePosX = posX + decalageEnX
        nouvellePosY = posY + decalageEnY
        posIntermediaireX = posX + int(decalageEnX/2)
        posIntermediaireY = posY + int(decalageEnY/2)
        
        plateau[nouvellePosX][nouvellePosY] = 0
        plateau[posIntermediaireX][posIntermediaireY] = 0
        
        posX = nouvellePosX
        posY = nouvellePosY
    
    print(plateau)
    print(posX, posY)
    



#Resolution DFS
def resolDFS(plateau):
    posX = 0
    posY = 0
    posFinalX = WIDTH - 1
    posFinalY = HEIGHT - 1
    resol = False
    pile = []
    while not resol:
        direction = direction_aleatoire()
        while (((decalageX(direction) + posX < 0 
                or decalageX(direction) + posX > WIDTH 
                or decalageY(direction) + posY < 0 
                or decalageY(direction) + posY > WIDTH)
                and plateau[posX + decalageX(direction)][posY + decalageY(direction)] == 0) or (plateau[posX +2][posY] == 0)):
            direction = direction_aleatoire()
        pile.append(direction)
        posX = posX + decalageX(direction)
        posY = posY + decalageY(direction)
        if plateau[posX][posY] == plateau[posFinalX][posFinalY]:
            resol = True

    
generer_labyrinthe()


#Fonction pour dessiner le plateau sur le Canvas
def draw_plateau(plateau):
    canvas.delete("all")
    for y in range(HEIGHT):
        for x in range(WIDTH):
            if plateau[x][y] == 1:
                canvas.create_rectangle(x * dim_case, y * dim_case, (x+1) * dim_case, (y+1) * dim_case, fill="black", outline="gray")
            else :
                if plateau[x][y] == 0:
                    canvas.create_rectangle(x * dim_case, y * dim_case, (x+1) * dim_case, (y+1) * dim_case, fill="white", outline="gray")
                    
#Bouton pour lancer "generer_n_case_aleatoire"
n = 2 #nbr de carrés
start_button = tk.Button(affichage, text = "Générer le plateau", command= lambda: generer_labyrinthe())
start_button.pack()
start_button = tk.Button(affichage, text = "Resoudre en DFS", command=lambda: resolDFS())
start_button.pack()

#Lancer la boucle principale de l'application
affichage.mainloop()