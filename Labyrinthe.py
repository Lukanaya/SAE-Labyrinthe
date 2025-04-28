import tkinter as tk
import random
import time
import math

# Dimensions du plateau/cases
WIDTH = 21 # Largeur du plateau
HEIGHT = 21 # Hauteur du plateau
dim_case = 30
labyrinthe = [] # Réel plateau (Attention, vérifier qu'il nest pas vide au changement len(labyrinthe) != 0)

affichage = tk.Tk()
affichage.title("Génération d’un plateau")

# Création du widget Canvas pour afficher le plateau
canvas = tk.Canvas(affichage, width=WIDTH * dim_case, height=HEIGHT * dim_case)
canvas.pack()

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
            elif plateau[x][y] == 4:
                canvas.create_rectangle(x * dim_case, y * dim_case, (x+1) * dim_case, (y+1) * dim_case, fill="yellow", outline="gray") 

# Génération de deux cases aléatoires sur le plateau
def generer_n_case_aleatoire(n):
    # Créer d’un plateau de taille WIDTH x HEIGHT
    plateau = [[1 for _ in range(WIDTH)] for _ in range(HEIGHT)]

    for _ in range(n):
        x = random.randint(0,WIDTH-1) ; y = random.randint(0,HEIGHT-1)
        while plateau[x][y] == 0:
            x = random.randint(0,WIDTH-1) ; y = random.randint(0,HEIGHT-1)
        plateau[x][y] = 0
        draw_plateau(plateau)
        # permet de faire une pause de 1 seconde entre l’affichage des deux carrés
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
    print(plateau)
    #Initialisation de la position de départ
    posX = 0
    posY = 0
    #Initialisation de la position de final cherchée
    posFinalX = WIDTH - 1
    posFinalY = HEIGHT - 1
    resol = False
    #Initialisation de la pile
    pile = []
    pile.append([posX,posY])
    plateau[posX][posY] = 2
    #Tant qu'on est pas a la position final on reste dans la boucle
    while not resol:
        #Si il n'y a pas de direction possible et que la pile n'est pas vide, on revient en arriere
        if len(direction_possible(posX, posY, plateau)) == 0 and len(pile) > 0:
            plateau[posX][posY] = 3
            precedent = pile.pop()
            posX = precedent[0]
            posY = precedent[1]
        #Sinon on prend une position aléatoire et on avance
        else:
            pile.append([posX,posY])
            direction = direction_aleatoire(direction_possible(posX, posY, plateau))
            posX = posX + deplacementX(direction)
            posY = posY + deplacementY(direction)
            plateau[posX][posY] = 2
        #Si la position finale est atteinte on arrete la boucle
        if posX == posFinalX and posY == posFinalY:
            resol = True
            #On affiche le départ et l'arrivée pour montrer la fin de la resolution DFS
            plateau[posX][posY] = 4
            plateau[0][0] = 4
        draw_plateau(plateau)
        affichage.update()
            
def plateau_to_graphe(plateau):
    #Transformer le plateau en graphe
    nodes = {}
    #initier le dictionnaire nodes avec des valeurs vides pour chaque tuple (x,y)
    for x in range(len(plateau)):
        for y in range(len(plateau)):
            if plateau[x][y] == 0:  # uniquement pour les cases libres
                nodes[(x, y)] = []
                
    for x, y in nodes.keys():
        if x < WIDTH - 1 and plateau[x+1][y] == 0:
            nodes[(x, y)].append((x+1, y))
        if y < HEIGHT - 1 and plateau[x][y+1] == 0:
            nodes[(x, y)].append((x, y+1))
        if x > 0 and plateau[x-1][y] == 0:
            nodes[(x, y)].append((x-1, y))
        if y > 0 and plateau[x][y-1] == 0:
            nodes[(x, y)].append((x, y-1))
    return nodes

def generer_labyrinthe(type_resol):
    labyrinthe = [[1 for _ in range(WIDTH)] for _ in range(HEIGHT)]
    dir = [(1,0),(-1,0),(0,1),(0,-1)] #haut bas droite gauche (direction au hasard donc osef)

    pile=[(0,0)]

    #construction
    terminer = False
    while not terminer:
        random.shuffle(dir)
        #sommet de la pile
        cy, cx = pile[-1] 

        #chercher la bonne direction et se déplacer
        trouve=False
        for dy, dx in dir:
            ny = cy + 2*dy
            nx = cx + 2*dx
            #si la zone trouvé est dans les limites du labyrinthe et qu'il est possible de passer dessus alors
            if 0 <= nx < WIDTH and 0 <= ny < HEIGHT and labyrinthe[ny][nx] != 0:
                labyrinthe[cy + dy][cx+dx] = 0
                labyrinthe[ny][nx] = 0
                pile.append((ny,nx))
                trouve=True
                break

        #On sort de la boucle
        #On vérifie si le chemin n'a pas été trouvé
        if not trouve:
            pile.pop() 


        #On vérifie si il n'y a plus de possibilité
        if len(pile)==0: terminer=True

        draw_plateau(labyrinthe)
        # permet de faire une pause de 1 seconde entre l’affichage des deux carrés
        affichage.update()
        # time.sleep(0.0000001)

    nb_mur=0
    for largeur in range(len(labyrinthe)):
        for hauteur in range(len(labyrinthe)):
            if labyrinthe[largeur][hauteur]==1:
                nb_mur+=1
    nbNotMur=math.floor(0.02*nb_mur)
    while nbNotMur>0:
        x=random.randint(0,WIDTH-1)
        y=random.randint(0,HEIGHT-1)
        if labyrinthe[x][y]==1:
            labyrinthe[x][y]=0
            nbNotMur-=1
        draw_plateau(labyrinthe)
        affichage.update()
        
    match type_resol:
        case "DFS":
            resolDFS(labyrinthe)
             
start_button = tk.Button(affichage, text="Générer le plateau et résolution par DFS", command = lambda: generer_labyrinthe("DFS"))
start_button.pack()

# Lancer la boucle principale de l’application
affichage.mainloop() # permet de garder la fenêtre ouverte en attendant lesinteractions de l’utilisateur