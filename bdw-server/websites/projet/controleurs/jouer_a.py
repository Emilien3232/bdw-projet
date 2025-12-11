from controleurs.includes import add_activity
from model.model_pg import get_morpion_par_equipe , get_morpion_par_id , verif_cond_victoire , sorts
#on verifie si les variables sont bine initialisées notamment CONFIG_PARTE etant donné que on ne peut pas commencé de partie sans configuration
if 'EQUIPE_1_ACTIVE' not in SESSION:
    SESSION['EQUIPE_1_ACTIVE'] = True
if 'NB_TOURS_JOUES' not in SESSION:
    SESSION['NB_TOURS_JOUES'] = 0
if 'CONFIG_PARTIE' not in SESSION:
    SESSION['CONFIG_PARTIE'] = None
if SESSION['CONFIG_PARTIE'] is not None :
    if 'TAB' not in SESSION or not SESSION['TAB']:
        SESSION['TAB'] = []
        dimension = SESSION['CONFIG_PARTIE'][2] 
        
        for i in range(dimension) : 
            ligne = []
            for j in range(dimension) :
                ligne.append( [ None , None] ) 
            SESSION['TAB'].append(ligne)

    REQUEST_VARS['morpion_equipe_1'] = get_morpion_par_equipe(SESSION['CONNEXION'], SESSION['EQUIPE_1'][0]) #on recupere les morpions des deux équipes
    REQUEST_VARS['morpion_equipe_2'] = get_morpion_par_equipe(SESSION['CONNEXION'], SESSION['EQUIPE_2'][0])
    REQUEST_VARS['nb_morpion_equipe_1'] = len(REQUEST_VARS['morpion_equipe_1']) #on calcule le nombre de morpions pour chaque équipe pour la longueur des grilles d'affichage des morpions
    REQUEST_VARS['nb_morpion_equipe_2'] = len(REQUEST_VARS['morpion_equipe_2'])
    equipe1_active = SESSION['EQUIPE_1_ACTIVE'] #par défaut l'équipe 1 commence toujours
    tab = SESSION['TAB']
    tabcaseinutilisables = SESSION['CASES_INUTILISABLES'] #liste des cases inutilisables pour les sorts
    tabinit_caseinutilisables = [] #en fin de partie on réinitialise la grille des cases inutilisables alors on reprend le code d'initialisation du init.py
    for i in range(SESSION['CONFIG_PARTIE'][2]) :
        ligne = []
        for j in range(SESSION['CONFIG_PARTIE'][2]) :
            ligne.append( None ) 
        tabinit_caseinutilisables.append(ligne)
    tabinit = [] #en fin de partie on réinitialise la grille alors on reprend le code d'initialisation du init.py
    for i in range(SESSION['CONFIG_PARTIE'][2]) :
        ligne = []
        for j in range(SESSION['CONFIG_PARTIE'][2]) :
            ligne.append( [ None , None] ) 
        tabinit.append(ligne)
    cmpt = SESSION['NB_TOURS_JOUES']
    REQUEST_VARS['equipe1_active'] = equipe1_active
    REQUEST_VARS['nb_tours_restant'] = SESSION['CONFIG_PARTIE'][1] - cmpt -1
        
    if 'valider_deplacement' in POST :

        #gestion des erreurs de selection de morpion et case cible
        if not 'morpion_selectionne[]' in POST or not 'case_cible[]' in POST :
            REQUEST_VARS['message_erreur'] = "Erreur : Vous devez sélectionner un morpion à déplacer et une case cible pour le déplacement."
        elif len(POST['morpion_selectionne[]']) > 1 :
            REQUEST_VARS['message_erreur'] = "Erreur : Vous ne pouvez déplacer qu'un seul morpion à la fois."
        elif len(POST['case_cible[]']) > 1 :
            REQUEST_VARS['message_erreur'] = "Erreur : Vous ne pouvez cibler qu'une seule case à la fois."

        else : #gestion action
            if POST['sorts_equipe'] == "Non" : #si aucun sort n'est selectionné on fait un déplacement classique
                coord_1= int(POST['case_cible[]'][0].split(',')[0]) #on recupere les coordonnées de la case cible (str -> int)
                coord_2 = int(POST['case_cible[]'][0].split(',')[1])
                morpion_action = get_morpion_par_id(SESSION['CONNEXION'],POST['morpion_selectionne[]'][0])[0] #récupération des infos du morpion sélectionné
                #on ajoute dans le tableau les données recueillies
                tab[coord_1][coord_2] = [ (SESSION['EQUIPE_1'][0] if equipe1_active else SESSION['EQUIPE_2'][0]) , morpion_action ]
                SESSION['TAB'] = tab #on met à jour la grille de jeu affichée

                #vérification condition de victoire après le déplacement
                connexion = SESSION['CONNEXION']
                config = SESSION['CONFIG_PARTIE']
                morpion_equipe1 = get_morpion_par_equipe(connexion,SESSION['EQUIPE_1'][0])
                morpion_equipe2 = get_morpion_par_equipe(connexion,SESSION['EQUIPE_2'][0]) 

                verif = verif_cond_victoire(connexion, config[2] ,tab ,morpion_equipe1 , morpion_equipe2 , cmpt , config[1])
                cmpt = verif[2] #incremetnations du compteurs
                SESSION['NB_TOURS_JOUES'] = cmpt
                if verif[0] :
                    REQUEST_VARS['message_victoire'] = "Félicitations ! L'équipe {} a gagné la partie en {} tours.".format( "1" if verif[1] == SESSION['EQUIPE_1'][0] else "2" , verif[2] )
                    SESSION['TAB'] = tabinit #on réinitialise la grille de jeu pour éviter les déplacements après victoire
                    SESSION['NB_TOURS_JOUES'] = 0
                if (verif[1] == 0) and verif[0] :
                    REQUEST_VARS['message_victoire'] = "Match nul ! La partie se termine sans vainqueur après {} tours.".format( SESSION['CONFIG_PARTIE'][1] )
                    SESSION['TAB'] = tabinit
                    SESSION['NB_TOURS_JOUES'] = 0
                #fonction journalisation

                if equipe1_active :
                    equipe1_active = False
                    SESSION['EQUIPE_1_ACTIVE'] = False
                else :
                    equipe1_active = True #on change l'équipe active 
                    SESSION['EQUIPE_1_ACTIVE'] = True
                
            if POST['sorts_equipe'] != "Non" : #gestion des sorts
                coord_1= int(POST['case_cible[]'][0].split(',')[0]) #on recupere les coordonnées de la case cible (str -> int)
                coord_2 = int(POST['case_cible[]'][0].split(',')[1])
                sort_selec = POST['sorts_equipe']
                morpion_action = get_morpion_par_id(SESSION['CONNEXION'],POST['morpion_selectionne[]'][0])[0] #récupération des infos du morpion selectionné
                SESSION['TAB'] = tab #on met à jour la grille de jeu affichée
                sorts(SESSION['CONNEXION'], morpion_action, get_morpion_par_equipe(SESSION['CONNEXION'], SESSION['EQUIPE_1'][0]) , get_morpion_par_equipe(SESSION['CONNEXION'], SESSION['EQUIPE_2'][0]) , equipe1_active , sort_selec , tab , coord_1 , coord_2,tabcaseinutilisables)


                if equipe1_active :
                    equipe1_active = False
                    SESSION['EQUIPE_1_ACTIVE'] = False
                else :
                    equipe1_active = True #on change l'équipe active 
                    SESSION['EQUIPE_1_ACTIVE'] = True















add_activity(SESSION['HISTORIQUE'], "consultation de la page Partie Simple")

