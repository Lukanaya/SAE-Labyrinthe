import tkinter as tk
import random
import time
import math

# Dimensions du plateau/cases
WIDTH = 21 # Largeur du plateau
HEIGHT = 21 # Hauteur du plateau
dim_case = 30
labyrinthe = [] # Réel plateau (Attention, vérifier qu'il nest pas vide au changement len(labyrinthe) != 0)
pourcent_mur_a_retirer = 0.02

# Création de la fenêtre Tkinter
affichage = tk.Tk()
affichage.title("Génération d’un plateau")

# Création du widget Canvas pour afficher le plateau
canvas = tk.Canvas(affichage, width=WIDTH * dim_case, height=HEIGHT * dim_case)
canvas.pack()

# Fonction pour dessiner le plateau sur le Canvas
def draw_plateau(plateau):
    canvas.delete("all") # permet d’effacer le contenu affiché sur la canvas
    for y in range(HEIGHT):
        for x in range(WIDTH):
            if plateau[x][y] == 1 :
                canvas.create_rectangle(x * dim_case, y * dim_case, (x + 1) * dim_case, (y + 1) * dim_case, fill="black", outline="gray")
            elif plateau[x][y] == 0:    
                canvas.create_rectangle(x * dim_case, y * dim_case, (x + 1) * dim_case, (y + 1) * dim_case, fill="white", outline="gray")
            elif plateau[x][y] == 2:
                canvas.create_rectangle(x * dim_case, y * dim_case, (x + 1) * dim_case, (y + 1) * dim_case, fill="blue", outline="gray")

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

def generer_labyrinthe():
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

    # Enlever 2% des murs
    nb_mur=0
    for largeur in range(len(labyrinthe)):
        for hauteur in range(len(labyrinthe)):
            if labyrinthe[largeur][hauteur]==1:
                nb_mur+=1
    nbNotMur=math.floor(pourcent_mur_a_retirer*nb_mur)
    while nbNotMur>0:
        x=random.randint(0,WIDTH-1)
        y=random.randint(0,HEIGHT-1)
        if labyrinthe[x][y]==1:
            labyrinthe[x][y]=0
            nbNotMur-=1
            draw_plateau(labyrinthe)
            affichage.update()
            
    resolutionDijkstra(labyrinthe)
    
    
# résolution par l'algorithme de Dijkstra
def resolutionDijkstra(plateau):
    
    result = {}
    Q = []
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
    
    sommetInitial = (0, 0)
    #Trouver le chemin le plus court dans le graphe
    # On ajoute les sommets a Q
    for sommet in nodes.keys():
        if sommet == sommetInitial:
            result[sommet] = [0, None]
        else: 
            result[sommet] = [math.inf, None]
        Q.append(sommet)
    while len(Q) > 0:
        u = Q[0]
        for s in Q:
            if result[s][0] < result[u][0]:
                u = s
        Q.remove(u)
        for v in nodes[u]:
            if result[u][0] + 1 < result[v][0]:
                result[v][0] = result[u][0] + 1
                result[v][1] = u
    
    #parcourir le dictionnaire résultat dans le sens inverse et afficher les valeurs sur le labyrinthe en temps réel
    chemin_final = []

    case = (WIDTH-1, HEIGHT-1) 

    while case is not None:
        chemin_final.append(case)
        case = result[case][1]  # remonter le chemin depuis l'arrivée vers le départ

    chemin_final.reverse()  # retourner le tableau pour partir du départ

    for case in chemin_final:
        x, y = case #récupérer les coordonnées dans le tuple
        plateau[x][y] = 2 # mettre a jour la couleur de la case en cours
        draw_plateau(plateau)
        affichage.update()
            

# Bouton pour lancer la génération et résolution du labyrinthe
start_button = tk.Button(affichage, text="Générer le plateau et résoudre par Dijkstra", command = lambda: generer_labyrinthe())
start_button.pack()

# Lancer la boucle principale de l’application
affichage.mainloop() # permet de garder la fenêtre ouverte en attendant lesinteractions de l’utilisateur