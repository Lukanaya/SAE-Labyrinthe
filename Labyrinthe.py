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
start_button = tk.Button(affichage, text = "Générer le plateau", command= lambda: generer_n_cases_aleatoire(n))
start_button.pack()

#Lancer la boucle principale de l'application
affichage.mainloop()