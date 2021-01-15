# -*- coding: utf-8 -*-

import networkx as nx
import matplotlib.pyplot as plt
from bokeh.io import output_file, show
from bokeh.models import (PanTool, SaveTool, BoxZoomTool, WheelZoomTool, Circle, HoverTool, MultiLine, Plot, Range1d, ResetTool)
from bokeh.plotting import from_networkx
from bokeh.models.graphs import NodesAndLinkedEdges, EdgesAndLinkedNodes

import Documents as doc

# Permettra de stocker les différents mot saisit pas l'utilisateur
mots = []

# Fonction qui crée et affiche le graphe en fonction des données
def creation_affichage_graphe():
    nb_mots = len(mots)
    
    # On récupère d'abord toutes les données qu'il nous faut
    liste_de_titres = doc.création_liste_titres(doc.corpus)

    # On va trier les données qu'on récupère    
    noeuds_a_trier = []
    
    # Création d'une liste contenant le titre du noeud, les mots et leur nombre d'apparition dans le texte du titre
    # Format de la liste des données qui seront traités par la suite : [titrePublication, mot1, occurence_mot1, mot2, occurence_mot2, etc.]
    for titre in liste_de_titres:
        noeud = [titre]
        
        for mot in mots:
            occurence = doc.Compter_occurence_via_titre(titre, doc.corpus, mot)
            noeud.append(mot)
            noeud.append(occurence)
        
        noeuds_a_trier.append(noeud)


    # Création du graphe vide
    G = nx.Graph() 
    
    noeuds_principaux = []
    noeuds_secondaires = []
    
    # On définit les données à afficher au survol des noeuds, à savoir les titres, les mots et leur occurence
    liste_data_titres = []
    liste_data_nom_mot1 = []
    liste_data_nombre_mot1 = []
    liste_data_nom_mot2 = []
    liste_data_nombre_mot2 = []
    liste_data_nom_mot3 = []
    liste_data_nombre_mot3 = []
    liste_data_nom_mot4 = []
    liste_data_nombre_mot4 = []
    liste_data_nom_mot5 = []
    liste_data_nombre_mot5 = []
    
    #### Création des noeuds principaux
    # Tri des noeuds à afficher ou non (si les mots ne sont pas dans les textes, il n'est pas pertinent de garder les noeuds)
    for publication in noeuds_a_trier:
        # On regarde l'occurence de chaque mot
        for i in range(2, 1+2*nb_mots, 2):
            # Si au moins un mot est dans le texte, on crée le noeud s'il n'est pas déjà créé (pour éviter d'avoir 2 mêmes mots)
            # Si tous les mots ont une occurence = 0, c'est qu'il ne sont pas dans les textes donc pas besoin de créer un noeud
            if publication[i] != 0 and publication not in noeuds_principaux:
                G.add_node(publication[0]) # publication[0] correspond au titre de la publication, le nom du noeud sera donc le titre
                noeuds_principaux.append(publication)
    
    
    # Remplissage des listes de données à afficher au survol des noeuds principaux
    cpt = -1 # cpt permettra de boucler sur les différentes publications
    for noeuds in noeuds_principaux:
        liste_data_titres.append(noeuds[0]) # On ajoute le titre dans la liste des données des noeuds 
        
        cpt += 1
        # On remplit les listes de données en fonction du nombre de mots qui a été saisit pour éviter d'avoir des listes vides ou des erreurs
        # De cette manière, si on saisit 2 mots, les données du 1er mot sont renseignées précédemment à laquelles on rajoute les données du 2ème mot, etc.
        if nb_mots >= 1: 
            # --> liste de la forme : [["Titre1", "mot1", "nbFois1"], ["Titre2", "mot1", "nbFois1"]]
            liste_data_nom_mot1.append(noeuds_principaux[cpt][1]) # On ajoute le nom
            liste_data_nombre_mot1.append(noeuds_principaux[cpt][2]) # On ajoute le nombre
        if nb_mots >= 2: 
            # --> liste de la forme : [["Titre1", "mot1", "nbFois1", "mot2", "nbFois2"], ["Titre2", "mot1", "nbFois1", "mot2", "nbFois2"]]
            liste_data_nom_mot2.append(noeuds_principaux[cpt][3])
            liste_data_nombre_mot2.append(noeuds_principaux[cpt][4])
        if nb_mots >= 3:
            liste_data_nom_mot3.append(noeuds_principaux[cpt][5])
            liste_data_nombre_mot3.append(noeuds_principaux[cpt][6])
        if nb_mots >= 4:
            liste_data_nom_mot4.append(noeuds_principaux[cpt][7])
            liste_data_nombre_mot4.append(noeuds_principaux[cpt][8])
        if nb_mots >= 5:
            liste_data_nom_mot5.append(noeuds_principaux[cpt][9])
            liste_data_nombre_mot5.append(noeuds_principaux[cpt][10])
     
    
    #### Création des noeuds secondaires à partir des noeuds principaux
    cpt = -1
    num_node = 0 # Numéro de noeud secondaire qui s'incrémentera en fonction du nombre de noeud secondaire
    for publication in noeuds_principaux:
        cpt += 1
        # Permet de récupérer les éléments à cpt+1 sauf pour le dernier (car on ne peut pas le coupler avec l'élément cpt+1 
        # et car ce dernier élément sera déjà couplé avec chaque élément/publication précédent)
        if cpt < len(noeuds_principaux)-1:
            # On cherche tous les autres noeuds principaux pour les relier entre eux s'ils ont un mot en commun
            for j in range(cpt+1, len(noeuds_principaux)):
                if ([noeuds_principaux[cpt], noeuds_principaux[j]] not in noeuds_secondaires) or ([noeuds_principaux[j], noeuds_principaux[cpt]] not in noeuds_secondaires):
                    boolIntersectionVide = False
                    # Si l'occurence minimum de chaque mot est de 0 pour les 2 noeuds, on ne crée pas de lien
                    if nb_mots >= 1:
                    	if min(publication[2], noeuds_principaux[j][2]) == 0:
                    		if nb_mots >= 2:
                    			if min(publication[4], noeuds_principaux[j][4]) == 0:
                    				if nb_mots >= 3:
                    					if min(publication[6], noeuds_principaux[j][6]) == 0:
                    						if nb_mots >= 4:
                    							if min(publication[8], noeuds_principaux[j][8]) == 0:
                    								if nb_mots >= 5:
                    									if min(publication[10], noeuds_principaux[j][10]) == 0:
                    										boolIntersectionVide = True
                    								else:
                    									boolIntersectionVide = True	
                    						else:
                    							boolIntersectionVide = True
                    				else:
                    					boolIntersectionVide = True
                    		else:
                    			boolIntersectionVide = True
                    
                    # Si intersection non vide (donc si un mot est dans les 2 textes)
                    if boolIntersectionVide == False:
                        # On crée le lien entre les deux noeuds
                        noeuds_secondaires.append([noeuds_principaux[cpt], noeuds_principaux[j]])
                        G.add_node(str(num_node))                
                        G.add_edge(str(num_node), publication[0])
                        G.add_edge(str(num_node), noeuds_principaux[j][0])
                                    
                    num_node += 1
    
    #### Remplissage des listes de données à afficher au survol des noeuds secondaires
    cpt = -1
    for noeuds in noeuds_secondaires:
        # On ajoute un titre "---" dans la liste des données des noeuds 
        # car le noeuds secondaires est une intersection et n'a donc pas de titre
        liste_data_titres.append("---") 
        
        cpt += 1
        # On remplit les listes de données en fonction du nombre de mots qui a été saisit pour éviter d'avoir des listes vides ou des erreurs
        if nb_mots >= 1:
            liste_data_nom_mot1.append(noeuds_secondaires[cpt][0][1]) # On ajoute le nom du mot
            liste_data_nombre_mot1.append(str(min(noeuds_secondaires[cpt][0][2], noeuds_secondaires[cpt][1][2])) + " fois en commun") # On ajoute l'occurence du mot en commun
        if nb_mots >= 2:
            # De cette manière, si on saisit 2 mots, les données du 1er mot sont renseignées précédemment à laquelles on rajoute les données du 2ème mot, etc.
            liste_data_nom_mot2.append(noeuds_secondaires[cpt][0][3])
            liste_data_nombre_mot2.append(str(min(noeuds_secondaires[cpt][0][4], noeuds_secondaires[cpt][1][4])) + " fois en commun")
        if nb_mots >= 3:
            liste_data_nom_mot3.append(noeuds_secondaires[cpt][0][5])
            liste_data_nombre_mot3.append(str(min(noeuds_secondaires[cpt][0][6], noeuds_secondaires[cpt][1][6])) + " fois en commun")
        if nb_mots >= 4:
            liste_data_nom_mot4.append(noeuds_secondaires[cpt][0][7])
            liste_data_nombre_mot4.append(str(min(noeuds_secondaires[cpt][0][8], noeuds_secondaires[cpt][1][8])) + " fois en commun")
        if nb_mots >= 5:
            liste_data_nom_mot5.append(noeuds_secondaires[cpt][0][9])
            liste_data_nombre_mot5.append(str(min(noeuds_secondaires[cpt][0][10], noeuds_secondaires[cpt][1][10])) + " fois en commun")
      
    
    ## Partie permettant de colorer les noeuds principaux en bleu et les noeuds secondaires (intersections) en rouge
    ## Elle permet aussi de gérer la taille du noeud (plus gros si c'est un noeud principal)
    SAME_MAIN_NOEUDS_COLOR, DIFFERENT_MAIN_NOEUDS_COLOR = "blue", "red"
    SAME_MAIN_NOEUDS_SIZE, DIFFERENT_MAIN_NOEUDS_SIZE = 25, 12
    node_color_attrs = {}
    node_size_attrs = {}
    
    cpt = -1 # Permettra de limiter les caractéristiques entre celles des noeuds principaux et et celles des noeuds secondaires
    for node in G.nodes(data=False):
        cpt +=1
        # Si noeud principal, la couleur est bleu et la taille 25, sinon (si noeud secondaire), la couleur est rouge et la taille 12
        node_color = SAME_MAIN_NOEUDS_COLOR if cpt < len(noeuds_principaux) else DIFFERENT_MAIN_NOEUDS_COLOR
        node_size = SAME_MAIN_NOEUDS_SIZE if cpt < len(noeuds_principaux) else DIFFERENT_MAIN_NOEUDS_SIZE
        node_color_attrs[node] = node_color
        node_size_attrs[node] = node_size
    
    # Ajout des caractéristiques aux noeuds du graphe 
    nx.set_node_attributes(G, node_color_attrs, "node_color")
    nx.set_node_attributes(G, node_size_attrs, "node_size")
    
    # On affiche le graphe de manière simple
    nx.draw(G, with_labels=True)
    plt.show() # display
    
    
    #### Affichage graphique
    # Création de la fenêtre du graphe
    plot = Plot(plot_width=600, plot_height=600, x_range=Range1d(-1.1, 1.1), y_range=Range1d(-1.1, 1.1))
    plot.title.text = "Graphe intéractif de co-occurences - Projet Python"
    
    # Mise en place et affichage des données dans les différents noeuds lors du survol de ceux-ci avec la souris
    graph_renderer = from_networkx(G, nx.spring_layout, scale=1, center=(0, 0))
    
    TOOLTIPS = [("Titre", "@Titre")]
    graph_renderer.node_renderer.data_source.add(liste_data_titres, 'Titre')
    
    # On affiche autant de ligne dans l'infobulle qu'il y a de mot (une pour chaque mot)
    if nb_mots >= 1:
        TOOLTIPS.append((str(mots[0]), "@Mot1"))
        graph_renderer.node_renderer.data_source.add(liste_data_nombre_mot1, 'Mot1')
    if nb_mots >= 2:
        TOOLTIPS.append((str(mots[1]), "@Mot2"))
        graph_renderer.node_renderer.data_source.add(liste_data_nombre_mot2, 'Mot2')
    if nb_mots >= 3:
        TOOLTIPS.append((str(mots[2]), "@Mot3"))
        graph_renderer.node_renderer.data_source.add(liste_data_nombre_mot3, 'Mot3')
    if nb_mots >= 4:
        TOOLTIPS.append((str(mots[3]), "@Mot4"))
        graph_renderer.node_renderer.data_source.add(liste_data_nombre_mot4, 'Mot4')
    if nb_mots >= 5:
        TOOLTIPS.append((str(mots[4]), "@Mot5"))
        graph_renderer.node_renderer.data_source.add(liste_data_nombre_mot5, 'Mot5')
        
    node_hover_tool = HoverTool(tooltips=TOOLTIPS)
    
    # Ajout des différents outils qui apparaitront à côté du graphe pour interagir avec (se déplacer dessus, le sauvegarder, etc.)
    plot.add_tools(node_hover_tool, PanTool(), WheelZoomTool(), BoxZoomTool(), ResetTool(), SaveTool())
    
    ## Affichage graphique des noeuds et des arêtes
    # Noeuds
    graph_renderer.node_renderer.glyph = Circle(size="node_size", fill_color="node_color")
    graph_renderer.node_renderer.hover_glyph = Circle(size=21, fill_color='yellow')
    
    # Arrête
    graph_renderer.edge_renderer.glyph = MultiLine(line_color='black', line_width=1)
    graph_renderer.edge_renderer.hover_glyph = MultiLine(line_color='green', line_width=5)
    
    # Mise en valeur du noeud et des arêtes associées lors du survol du noeud
    graph_renderer.selection_policy = EdgesAndLinkedNodes()
    graph_renderer.inspection_policy = NodesAndLinkedEdges()
    
    # Ajout de l'aspect graphique au graphe
    plot.renderers.append(graph_renderer)
    
    # Affichage du graphe dans une page HTML
    output_file("interactive_graphs.html")
    show(plot)

# Test
#creation_affichage_graphe()




