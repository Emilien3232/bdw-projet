from controleurs.includes import add_activity
from model.model_pg import get_morpion_par_equipe , get_morpion_par_id , verif_cond_victoire
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
    equipe1_active = True #par défaut l'équipe 1 commence toujours
    tab = SESSION['TAB']
    cmpt = 0
    REQUEST_VARS['equipe1_active'] = equipe1_active
        
    if 'valider_deplacement' in POST :
        #gestion des erreurs de selection de morpion et case cible
        if len(POST['morpion_selectionne[]']) > 1 :
            REQUEST_VARS['message_erreur'] = "Erreur : Vous ne pouvez déplacer qu'un seul morpion à la fois."
        elif len(POST['case_cible[]']) > 1 :
            REQUEST_VARS['message_erreur'] = "Erreur : Vous ne pouvez cibler qu'une seule case à la fois."
        elif len(POST['morpion_selectionne[]']) == 0 :
            REQUEST_VARS['message_erreur'] = "Erreur : Vous devez sélectionner un morpion à déplacer."
        elif len(POST['case_cible[]']) == 0 :
            REQUEST_VARS['message_erreur'] = "Erreur : Vous devez sélectionner une case cible pour le déplacement."



        else : #gestion action
            coord_1= int(POST['case_cible[]'][0].split(',')[0]) #on recupere les coordonnées de la case cible (str -> int)
            coord_2 = int(POST['case_cible[]'][0].split(',')[1])
            morpion_action = get_morpion_par_id(SESSION['CONNEXION'],POST['morpion_selectionne[]'][0])[0] #récupération des infos du morpion sélectionné
            #on ajoute dans le tableau les données recueillies
            tab[coord_1][coord_2] = [ (SESSION['EQUIPE_1'][0] if equipe1_active else SESSION['EQUIPE_2'][0]) , morpion_action ]
            SESSION['TAB'] = tab #on met à jour la grille de jeu affichée
            verif = verif_cond_victoire(SESSION['CONNEXION'],SESSION['CONFIG_PARTIE'][2] ,tab ,get_morpion_par_equipe(SESSION['CONNEXION'],SESSION['EQUIPE_1'][0]) ,  get_morpion_par_equipe(SESSION['CONNEXION'], SESSION['EQUIPE_2'][0]) , cmpt , SESSION['CONFIG_PARTIE'][1]) 
            cmpt = verif[2]
            if verif[0] :
                REQUEST_VARS['message_victoire'] = "Félicitations ! L'équipe {} a gagné la partie en {} tours.".format( "1" if verif[1] == SESSION['EQUIPE_1'][0] else "2" , verif[2] )
            if verif[2] == 0 :
                REQUEST_VARS['message_victoire'] = "Match nul ! La partie se termine sans vainqueur après {} tours.".format( SESSION['CONFIG_PARTIE'][1] )
            if equipe1_active :
                equipe1_active = False
            else :
                equipe1_active = True #on change l'équipe active après un déplacement réussi
            REQUEST_VARS['equipe1_active'] = equipe1_active

















add_activity(SESSION['HISTORIQUE'], "consultation de la page Partie Simple")

