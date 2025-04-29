import tkinter as tk
import random
import time
import math
import copy

# Dimensions du plateau/cases
WIDTH = 21 # Largeur du plateau
HEIGHT = 21 # Hauteur du plateau
dim_case = 30
proba_mur_retire = 0.05

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
        
def distance(pointDepart: tuple, pointArrivee: tuple) -> float:
    x1, y1 = pointDepart
    x2, y2 = pointArrivee
    resultat = math.sqrt(math.pow(x2-x1, 2) + math.pow(y2-y1, 2))
    return resultat

class Labyrinthe:
    def __init__(self):
        self.labyrinthe = []
        self.affichage = tk.Tk()
        self.affichage.title("Génération d'un labyrinthe")
        self.canvas = tk.Canvas(self.affichage, width=WIDTH * dim_case, height=HEIGHT * dim_case)
        self.canvas.pack()
        self.setup_boutons()
        
    def setup_boutons(self):
        tk.Button(self.affichage, text="Générer le plateau", command = self.fonctionGenererLabyrinthe).pack()
        tk.Button(self.affichage, text="Générer le plateau et résolution par DFS", command = self.fonctionResolutionDFS).pack()
        tk.Button(self.affichage, text="Générer le plateau et résolution par Dijkstra", command = self.fonctionResolutionDijkstra).pack()
        tk.Button(self.affichage, text="Générer le plateau et résolution par Blinky", command = self.fonctionResolutionBlinky).pack()

    def draw_plateau(self, plateau):
        self.canvas.delete("all")
        for y in range(HEIGHT):
            for x in range(WIDTH):
                if plateau[x][y] == 1:
                    self.canvas.create_rectangle(x * dim_case, y * dim_case, (x+1) * dim_case, (y+1) * dim_case, fill="black", outline="gray")
                elif plateau[x][y] == 0:
                    self.canvas.create_rectangle(x * dim_case, y * dim_case, (x+1) * dim_case, (y+1) * dim_case, fill="white", outline="gray")
                elif plateau[x][y] == 2:
                    self.canvas.create_rectangle(x * dim_case, y * dim_case, (x+1) * dim_case, (y+1) * dim_case, fill="blue", outline="gray")
                elif plateau[x][y] == 3:
                    self.canvas.create_rectangle(x * dim_case, y * dim_case, (x+1) * dim_case, (y+1) * dim_case, fill="red", outline="gray") 
                elif plateau[x][y] == 4:
                    self.canvas.create_rectangle(x * dim_case, y * dim_case, (x+1) * dim_case, (y+1) * dim_case, fill="yellow", outline="gray") 
                elif plateau[x][y] == 5:
                    self.canvas.create_rectangle(x * dim_case, y * dim_case, (x+1) * dim_case, (y+1) * dim_case, fill="green", outline="gray")
                    

    #Resolution DFS
    def resolutionDFS(self):
        plateau = copy.deepcopy(self.labyrinthe)
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
            self.draw_plateau(plateau)
            self.affichage.update()
            
    # résolution par l'algorithme de Dijkstra
    def resolutionDijkstra(self):
        plateau = copy.deepcopy(self.labyrinthe)
        result = {}
        Q = []
        #Transformer le plateau en graphe
        nodes = plateau_to_graphe(plateau)
        
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
            self.draw_plateau(plateau)
            self.affichage.update()
            
        plateau[0][0] = 4
        plateau[WIDTH-1][HEIGHT - 1] = 4
        self.draw_plateau(plateau)
        self.affichage.update()

        
    def resolutionBlinky(self):
        plateau = copy.deepcopy(self.labyrinthe)
        nodes = plateau_to_graphe(plateau)
        result = {}
        Q = []
        
        sommetInitial = (0,0)
        sommetFinal = (WIDTH-1, HEIGHT-1)
        
        for sommet in nodes.keys():
            if sommet == sommetInitial:
                result[sommet] = [0, None]
            else: 
                result[sommet] = [math.inf, None]
        Q.append(sommetInitial)
        u = sommetInitial
        while len(Q) > 0 and sommetFinal not in Q:
            distMin = math.inf
            for s in Q:
                if result[s][0] < distMin:
                    distMin = result[s][0]
                    u = s
            Q.remove(u)
            for v in nodes[u]:
                if distance(u, v) + distance(v, sommetFinal) < result[v][0]:
                    result[v][0] = distance(u, v) + distance(v, sommetFinal)
                    result[v][1] = u
                    Q.append(v)
        chemin = []
        if sommetFinal in Q:
            sommetCourant = sommetFinal
            chemin.append(sommetCourant)
            while sommetCourant != sommetInitial:
                sommetCourant = result[sommetCourant][1]
                chemin.append(sommetCourant)
            chemin.reverse()
            for sommet in chemin:
                x, y = sommet
                plateau[x][y] = 5
                self.draw_plateau(plateau)
                self.affichage.update()
            plateau[0][0] = 4
            plateau[WIDTH-1][HEIGHT-1] = 4
            self.draw_plateau(plateau)
            self.affichage.update()
            
    def generer_labyrinthe(self):
        plateau = [[1 for _ in range(WIDTH)] for _ in range(HEIGHT)]
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
                #si la zone trouvé est dans les limites du plateau et qu'il est possible de passer dessus alors
                if 0 <= nx < WIDTH and 0 <= ny < HEIGHT and plateau[ny][nx] != 0:
                    plateau[cy + dy][cx+dx] = 0
                    plateau[ny][nx] = 0
                    pile.append((ny,nx))
                    trouve=True
                    break

            #On sort de la boucle
            #On vérifie si le chemin n'a pas été trouvé
            if not trouve:
                pile.pop() 


            #On vérifie si il n'y a plus de possibilité
            if len(pile)==0: terminer=True

            self.draw_plateau(plateau)
            # permet de faire une pause de 1 seconde entre l’affichage des deux carrés
            self.affichage.update()
            # time.sleep(0.0000001)

        nb_mur=0
        for largeur in range(len(plateau)):
            for hauteur in range(len(plateau)):
                if plateau[largeur][hauteur]==1:
                    nb_mur+=1
        nbNotMur=math.floor(proba_mur_retire*nb_mur)
        while nbNotMur>0:
            x=random.randint(0,WIDTH-1)
            y=random.randint(0,HEIGHT-1)
            if plateau[x][y]==1:
                plateau[x][y]=0
                nbNotMur-=1
            self.draw_plateau(plateau)
            self.affichage.update()
        return plateau

    def fonctionGenererLabyrinthe(self):
        self.labyrinthe = self.generer_labyrinthe()
        
    def fonctionResolutionDFS(self):
        if self.labyrinthe:
            self.resolutionDFS()   
                 
    def fonctionResolutionDijkstra(self):
        if self.labyrinthe:
            self.resolutionDijkstra()    
                
    def fonctionResolutionBlinky(self):
        if self.labyrinthe:
            self.resolutionBlinky()
            
    def run(self):
        self.affichage.mainloop()

app = Labyrinthe()
app.run()