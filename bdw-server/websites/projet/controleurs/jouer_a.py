from controleurs.includes import add_activity
from model.model_pg import get_morpion_par_equipe , get_morpion_par_id
if SESSION['CONFIG_PARTIE'] :
    REQUEST_VARS['morpion_equipe_1'] = get_morpion_par_equipe(SESSION['CONNEXION'], SESSION['EQUIPE_1'][0])
    REQUEST_VARS['morpion_equipe_2'] = get_morpion_par_equipe(SESSION['CONNEXION'], SESSION['EQUIPE_2'][0])
    REQUEST_VARS['nb_morpion_equipe_1'] = len(REQUEST_VARS['morpion_equipe_1']) 
    REQUEST_VARS['nb_morpion_equipe_2'] = len(REQUEST_VARS['morpion_equipe_2'])
    cases_inutilisables = []
    equipe1_active = True 
    tab = SESSION['TAB']
    REQUEST_VARS['equipe1_active'] = equipe1_active
        
    if 'valider_deplacement' in POST :
        if len(POST['morpion_selectionne[]']) > 1 :
            REQUEST_VARS['message_erreur'] = "Erreur : Vous ne pouvez déplacer qu'un seul morpion à la fois."
        elif len(POST['case_cible[]']) > 1 :
            REQUEST_VARS['message_erreur'] = "Erreur : Vous ne pouvez cibler qu'une seule case à la fois."
        elif len(POST['morpion_selectionne[]']) == 0 :
            REQUEST_VARS['message_erreur'] = "Erreur : Vous devez sélectionner un morpion à déplacer."
        elif len(POST['case_cible[]']) == 0 :
            REQUEST_VARS['message_erreur'] = "Erreur : Vous devez sélectionner une case cible pour le déplacement."
        else : #gestion action
            if equipe1_active :
                sort = POST['sorts_equipe1']
            else :
                sort = POST['sorts_equipe2']
            #gestion des sorts à implémenter ici
            if sort :   
                #on recupere les coord de la cases cibles 
                coord_1= int(POST['case_cible[]'][0].split(',')[0]) 
                coord_2 = int(POST['case_cible[]'][0].split(',')[1])
                morpion_action = get_morpion_par_id(SESSION['CONNEXION'],POST['morpion_selectionne[]'][0])[0] 
                #verifier si la cases cibles possedes un morpion adverse (tab[coord_1][coord_2][0] est diferent de id equipe active )
                #appeller fonction sort
            else :
                coord_1= int(POST['case_cible[]'][0].split(',')[0]) 
                coord_2 = int(POST['case_cible[]'][0].split(',')[1])
                morpion_action = get_morpion_par_id(SESSION['CONNEXION'],POST['morpion_selectionne[]'][0])[0] 
                tab[coord_1][coord_2] = [ (SESSION['EQUIPE_1'][0] if equipe1_active else SESSION['EQUIPE_2'][0]) , morpion_action ]
                SESSION['TAB'] = tab
            #verif_cond_victoire(SESSION['CONNEXION'], SESSION['EQUIPE_1'][0] , SESSION['EQUIPE_2'][0], SESSION['CONFIG_PARTIE'][2], tab)
            if equipe1_active :
                equipe1_active = False
            else :
                equipe1_active = True 
            REQUEST_VARS['equipe1_active'] = equipe1_active

add_activity(SESSION['HISTORIQUE'], "consultation de la page Partie Simple")

