"""
Ficher initialisation (eg, constantes chargées au démarrage dans la session)
"""

from datetime import datetime
from os import path

SESSION['APP'] = ""
SESSION['BASELINE'] = ""
SESSION['DIR_HISTORIQUE'] = path.join(SESSION['DIRECTORY'], "historiques")
SESSION['HISTORIQUE'] = dict()
SESSION['CURRENT_YEAR'] = datetime.now().year


SESSION['EQUIPE_1'] = None
SESSION['EQUIPE_2'] = None
SESSION['CONFIG_PARTIE'] = None
SESSION['DATE_DEBUT_PARTIE'] = None
SESSION['TAB'] = [] #initialisation de la grille de jeu , chaque case contient l'id de l'equipe et l'id du morpion qui s'y trouve
SESSION['CASES_INUTILISABLES'] = [] #initialisation de la liste des cases inutilisables (pour les sorts)

if SESSION['CONFIG_PARTIE'] is not None :
    for i in range(SESSION['CONFIG_PARTIE'][2]) : #on crée une grille vide selon la dimension choisie dans la config de partie
        ligne = []
        for j in range(SESSION['CONFIG_PARTIE'][2]) :
            ligne.append( None ) #chaque case est initialisée à None ( pas d'équipe , pas de morpion )
        SESSION['CASES_INUTILISABLES'].append(ligne)
    for i in range(SESSION['CONFIG_PARTIE'][2]) : #on crée une grille vide selon la dimension choisie dans la config de partie
        ligne = []
        for j in range(SESSION['CONFIG_PARTIE'][2]) :
            ligne.append( [ None , None] ) #chaque case est initialisée à None ( pas d'équipe , pas de morpion )
        SESSION['TAB'].append(ligne)
SESSION['NB_TOURS_JOUES'] = 0
SESSION['EQUIPE_1_ACTIVE'] = False #par défaut l'équipe 1 commence toujours
