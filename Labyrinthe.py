import tkinter as tk
import random
import time
import math
import copy

# Dimensions du plateau/cases
WIDTH = 31 # Largeur du plateau
HEIGHT = 31 # Hauteur du plateau
dim_case = 15
proba_mur_retire = 0.02


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

def coordoneesTeleporteurs(plateau):
    # récupérer les positions des téléporteurs
    tp1 = None
    tp2 = None
    for x in range(len(plateau)):
        for y in range(len(plateau)):
            if plateau[x][y] == 6:
                if tp1 is None:
                    tp1 = (x,y)
                else:
                    tp2 = (x,y)
    return (tp1,tp2)
    

def caseOK(plateau, x, y):
    valeursOK = [0,6,5] # Les cases que l'on peut parcourir
    return (plateau[x][y] in valeursOK)

def direction_possible(posX, posY, plateau):
    direction_possible = []
    if posX - 1 >= 0 and caseOK(plateau, posX-1, posY):
        direction_possible.append("gauche")
    if posX + 1 < len(plateau) and caseOK(plateau, posX+1, posY):
        direction_possible.append("droite")
    if posY - 1 >= 0 and caseOK(plateau, posX, posY-1):
        direction_possible.append("haut")
    if posY + 1 < len(plateau[0]) and caseOK(plateau, posX, posY+1):
        direction_possible.append("bas")
    return direction_possible

def plateau_to_graphe_avec_teleporteur(plateau):
    #Transformer le plateau en graphe
    nodes = plateau_to_graphe(plateau)
    tp1, tp2 = coordoneesTeleporteurs(plateau)

    # ajouter les coordonnées d'un téléporteur au suivants de l'autre téléporteur
    for x, y in nodes.keys():
        if (x,y) == tp1:
            nodes[(x, y)].append(tp2)
        if (x,y) == tp2:
            nodes[(x, y)].append(tp1)
    return nodes

def plateau_to_graphe(plateau):
    #Transformer le plateau en graphe
    nodes = {}
    #initier le dictionnaire nodes avec des valeurs vides pour chaque tuple (x,y)
    for x in range(len(plateau)):
        for y in range(len(plateau)):
            if caseOK(plateau, x, y):  # uniquement pour les cases libres
                nodes[(x, y)] = []

    for x, y in nodes.keys():
        if x < WIDTH - 1 and caseOK(plateau, x+1, y):
            nodes[(x, y)].append((x+1, y))
        if y < HEIGHT - 1 and caseOK(plateau, x, y+1):
            nodes[(x, y)].append((x, y+1))
        if x > 0 and caseOK(plateau, x-1, y):
            nodes[(x, y)].append((x-1, y))
        if y > 0 and caseOK(plateau, x, y-1):
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
        self.boutons = []
        self.setup_boutons()
        self.posY = 0
        self.posX = 0
        self.deplacement = 0
        
    def setup_boutons(self):
        bouton = tk.Button(self.affichage, text="Générer le plateau", command = self.fonctionGenererLabyrinthe)
        bouton.pack()
        self.boutons.append(bouton)
        bouton1 = tk.Button(self.affichage, text="Résolution par DFS", command = self.fonctionResolutionDFS, state=tk.DISABLED)
        bouton1.pack()
        self.boutons.append(bouton1)
        bouton2 = tk.Button(self.affichage, text="Résolution par Dijkstra", command = self.fonctionResolutionDijkstra, state=tk.DISABLED)
        bouton2.pack()
        self.boutons.append(bouton2)
        bouton3 = tk.Button(self.affichage, text="Résolution par Blinky", command = self.fonctionResolutionBlinky, state=tk.DISABLED)
        bouton3.pack()
        self.boutons.append(bouton3)
        bouton4 = tk.Button(self.affichage, text="Résolution manuelle", command = self.fonctionResolutionManuelle, state= tk.DISABLED)
        bouton4.pack()

    def activerBoutons(self):
        for i in range(1, len(self.boutons)):
            self.boutons[i].config(state=tk.NORMAL)
            
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
                elif plateau[x][y] == 6:
                    self.canvas.create_rectangle(x * dim_case, y * dim_case, (x+1) * dim_case, (y+1) * dim_case, fill="purple", outline="gray")
                    

    #Resolution DFS
    def resolutionDFS(self):
        plateau = copy.deepcopy(self.labyrinthe)
        tp1, tp2 = coordoneesTeleporteurs(plateau)
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
            #self.draw_plateau(plateau)
            #self.affichage.update()
        #On affiche le départ et l'arrivée pour montrer la fin de la resolution DFS
        plateau[posX][posY] = 4
        plateau[0][0] = 4
        plateau[tp1[0]][tp1[1]] = 6
        plateau[tp2[0]][tp2[1]] = 6
        self.draw_plateau(plateau)
        self.affichage.update()
            
    # résolution par l'algorithme de Dijkstra
    def resolutionDijkstra(self):
        plateau = copy.deepcopy(self.labyrinthe)
        tp1, tp2 = coordoneesTeleporteurs(plateau)
        result = {}
        Q = []
        #Transformer le plateau en graphe
        nodes = plateau_to_graphe_avec_teleporteur(plateau)
        
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
            plateau[x][y] = 3 # mettre a jour la couleur de la case en cours
            #self.draw_plateau(plateau)
            #self.affichage.update()
            
        plateau[0][0] = 4
        plateau[WIDTH-1][HEIGHT - 1] = 4
        plateau[tp1[0]][tp1[1]] = 6
        plateau[tp2[0]][tp2[1]] = 6
        self.draw_plateau(plateau)
        self.affichage.update()

        
    def resolutionBlinky(self):
        plateau = copy.deepcopy(self.labyrinthe)
        tp1, tp2 = coordoneesTeleporteurs(plateau)
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
                #self.draw_plateau(plateau)
                #self.affichage.update()
            plateau[0][0] = 4
            plateau[WIDTH-1][HEIGHT-1] = 4
            plateau[tp1[0]][tp1[1]] = 6
            plateau[tp2[0]][tp2[1]] = 6
            self.draw_plateau(plateau)
            self.affichage.update()

    
    def move(self, event):
        plateau = copy.deepcopy(self.labyrinthe)
        tp1, tp2 = coordoneesTeleporteurs(plateau)
        self.draw_plateau(plateau)
        touche = event.keysym
        if touche == 'Up':
            if(self.posY-1 >= 0 and caseOK(plateau,self.posX,self.posY-1)):
                self.posY-=1
                self.deplacement += 1
        elif touche == 'Down':
            if(self.posY+1 < HEIGHT and caseOK(plateau,self.posX,self.posY+1)):
                self.posY+=1
                self.deplacement += 1
        elif touche == 'Right':
            if(self.posX+1 < WIDTH and caseOK(plateau,self.posX+1,self.posY)):
                self.posX+=1
                self.deplacement += 1
        elif touche == 'Left':
            if(self.posX-1 >= 0 and caseOK(plateau,self.posX-1,self.posY)):
                self.posX-=1
                self.deplacement += 1
        if (self.posX, self.posY) == tp1:
            self.posX, self.posY = tp2
        elif (self.posX, self.posY) == tp2:
            self.posX, self.posY = tp1
        plateau[self.posX][self.posY] = 5
        if self.posX == WIDTH-1 and self.posY == HEIGHT-1:
            self.draw_plateau(plateau)
            print("Il a fallu" , self.deplacement , "deplacements")
            self.affichage.unbind("<Key>")
            self.posX = 0
            self.posY = 0
            self.deplacement = 0
            return
            
        self.draw_plateau(plateau)
        self.affichage.update()
        #print(self.posX, self.posY)
        


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

            #self.draw_plateau(plateau)
            #self.affichage.update()

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
            #self.draw_plateau(plateau)
            #self.affichage.update()
        teleport = 0
        while teleport < 2:
            x=random.randint(0,WIDTH-1)
            y=random.randint(0,HEIGHT-1)
            if plateau[x][y]==0:
                plateau[x][y]=6
                teleport += 1
       
        self.draw_plateau(plateau)
        self.affichage.update()
        return plateau

    def fonctionGenererLabyrinthe(self):
        self.labyrinthe = self.generer_labyrinthe()
        self.activerBoutons()
        
    def fonctionResolutionDFS(self):
        if self.labyrinthe:
            self.resolutionDFS()
                 
    def fonctionResolutionDijkstra(self):
        if self.labyrinthe:
            self.resolutionDijkstra()
                
    def fonctionResolutionBlinky(self):
        if self.labyrinthe:
            self.resolutionBlinky()
    
    def fonctionResolutionManuelle(self):
        if self.labyrinthe:
            self.affichage.bind("<Key>", self.move)

    def run(self):
        self.affichage.mainloop()

app = Labyrinthe()
app.run()