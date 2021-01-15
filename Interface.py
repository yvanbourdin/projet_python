# -*- coding: utf-8 -*-

from tkinter import *

import Graphe as graph
import Documents as doc

# Importation des données Reddit lors du clique sur le bouton "Reddit"
def importer_donnees_reddit():
    doc.corpus = doc.Importation_via_Reddit(doc.reddit)
    bouton_reddit.config(state=DISABLED)
    bouton_arxiv.config(state=NORMAL)
    bouton_valider.config(state=NORMAL)
    label_info_importation.config(text="\n Vous avez importé les données Reddit.")

# Importation des données Arxiv lors du clique sur le bouton "Arxiv"    
def importer_donnees_arxiv():
    doc.corpus = doc.Importation_via_Arxiv(doc.url, doc.data, doc.docs)
    bouton_reddit.config(state=NORMAL)
    bouton_arxiv.config(state=DISABLED)
    bouton_valider.config(state=NORMAL)
    label_info_importation.config(text="\n Vous avez importé les données Arxiv.")
    
# Permet de vider les champs de textes et de vider les données du corpus
def reinitialisation():
    doc.corpus = None
    bouton_reddit.config(state=NORMAL)
    bouton_arxiv.config(state=NORMAL)
    label_info_importation.config(text="\n Vous n'avez pas encore importé de données.")
    nom_mot1.set("")
    nom_mot2.set("")
    nom_mot3.set("")
    nom_mot4.set("")
    nom_mot5.set("")
    bouton_valider.config(state=DISABLED)

# Remplissage du tableau de mots qui apparaitront au survol des noeuds en fonction des mots saisis par l'utilisateur
def tableau_mots():
    # Pour chaque chanmps de texte, on vérifie ce qui a été saisit et on remplit le tableau de mot si le champ n'est pas vide
    graph.mots = []
    if nom_mot1.get() != "":
        graph.mots.append(nom_mot1.get())
    if nom_mot2.get() != "":
        graph.mots.append(nom_mot2.get())
    if nom_mot3.get() != "":
        graph.mots.append(nom_mot3.get())
    if nom_mot4.get() != "":
        graph.mots.append(nom_mot4.get())
    if nom_mot5.get() != "":
        graph.mots.append(nom_mot5.get())
        
# Permet de créer et d'afficher le graphe 
def creation_graphe():    
    # On remplit le tableau des mots saisis
    tableau_mots()
    
    # Puis on exécute la fonction qui va créer et afficher le graphe
    graph.creation_affichage_graphe()
    

#### Création de la fenêtre
fenetre = Tk()
fenetre.title("Interface Programmation Python")
fenetre.config(background='skyblue')

#### Titre
label_titre = Label(fenetre, text="Interface Programmation Python",
                    fg = "darkblue", bg='skyblue', font = ("Helvetica", 20 , "bold"), padx=20).pack()

#### Pied de page
label_sous_titre = Label(fenetre, text="Master 1 Informatique - Année 2020-2021\nBourdin Yvan & Frintz Elisa - Sujet 2 : Extraction de collocations", 
                         borderwidth=1, relief="groove", fg = "darkblue", bg='skyblue', font = ("Arial", 10 , "italic")).pack(fill=BOTH, side=BOTTOM)

#### Partie importation des données
labelframe_importation_donnees = LabelFrame(fenetre, text="Importation des données", padx=20, pady=20, fg = "DodgerBlue4", bg='skyblue', font = ("Arial", 15 , "normal"))
labelframe_importation_donnees.pack(fill=Y)

label_importation = Label(labelframe_importation_donnees, text="Importation via :", fg = "DodgerBlue4", bg='skyblue', font = ("Arial", 12 , "normal"))
label_importation.grid(row=0, column=0, columnspan=2, sticky="W", pady=2)

## Boutons permettant de choisir entre l'importation des données Reddit ou des données Arxiv
# Reddit
bouton_reddit = Button(labelframe_importation_donnees, text="Reddit", command=importer_donnees_reddit, state=NORMAL)
bouton_reddit.grid(row=1, column=0)

#Arxiv
bouton_arxiv = Button(labelframe_importation_donnees, text="Arxiv", command=importer_donnees_arxiv, state=NORMAL)
bouton_arxiv.grid(row=1, column=1)

# Label permettant de savoir quelles données ont été importées si elles l'ont été
label_info_importation = Label(labelframe_importation_donnees, text="\n Vous n'avez pas encore importé de données.", fg = "DodgerBlue4", bg='skyblue', font = ("Arial", 12 , "bold"))
label_info_importation.grid(row=2, column=0, columnspan=2)

#### Section pour la recherche des mots
label_selection_mots = Label(labelframe_importation_donnees, text="\n Sélection des mots : ", fg = "DodgerBlue4", bg='skyblue', font = ("Arial", 12 , "normal"))
label_selection_mots.grid(row=3, column=0, sticky="W")

# Mot 1
nom_mot1 = StringVar()
zone_mot1 = Entry(labelframe_importation_donnees, textvariable=nom_mot1)
zone_mot1.grid(row=4, column=0, sticky="WE", pady=2)

# Mot 2
nom_mot2 = StringVar()
zone_mot2 = Entry(labelframe_importation_donnees, textvariable=nom_mot2)
zone_mot2.grid(row=5, column=0, sticky="WE", pady=2)

# Mot 3
nom_mot3 = StringVar()
zone_mot3 = Entry(labelframe_importation_donnees, textvariable=nom_mot3)
zone_mot3.grid(row=6, column=0, sticky="WE", pady=2)

# Mot4
nom_mot4 = StringVar()
zone_mot4 = Entry(labelframe_importation_donnees, textvariable=nom_mot4)
zone_mot4.grid(row=7, column=0, sticky="WE", pady=2)

# Mot 5
nom_mot5 = StringVar()
zone_mot5 = Entry(labelframe_importation_donnees, textvariable=nom_mot5)
zone_mot5.grid(row=8, column=0, sticky="WE", pady=2)

# Bouton pour tout réinitialiser 
bouton_reinitialiser = Button(labelframe_importation_donnees, text="Réinitialiser", command=reinitialisation)
bouton_reinitialiser.grid(row=10, column=0, pady=10)

# Bouton pour valider la recherche et lancer le graphe
bouton_valider = Button(labelframe_importation_donnees, text="Valider", command=creation_graphe)
bouton_valider.grid(row=10, column=1)
bouton_valider.config(state=DISABLED)
    

fenetre.mainloop()












