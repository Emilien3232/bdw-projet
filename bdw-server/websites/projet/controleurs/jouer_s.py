from controleurs.includes import add_activity
from model.model_pg import get_morpion_par_equipe
if SESSION['CONFIG_PARTIE'] :
    REQUEST_VARS['morpion_equipe_1'] = get_morpion_par_equipe(SESSION['CONNEXION'], SESSION['EQUIPE_1'][0]) #on recupere les morpions des deux équipes
    REQUEST_VARS['morpion_equipe_2'] = get_morpion_par_equipe(SESSION['CONNEXION'], SESSION['EQUIPE_2'][0])
    REQUEST_VARS['nb_morpion_equipe_1'] = len(REQUEST_VARS['morpion_equipe_1']) #on calcule le nombre de morpions pour chaque équipe pour la longueur des grilles d'affichage des morpions
    REQUEST_VARS['nb_morpion_equipe_2'] = len(REQUEST_VARS['morpion_equipe_2'])
    equipe1_active = True #par défaut l'équipe 1 commence toujours

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
        else :
            equipe1_active = not(equipe1_active) #on change l'équipe active après un déplacement réussi
            REQUEST_VARS['equipe1_active'] = equipe1_active 


















add_activity(SESSION['HISTORIQUE'], "consultation de la page Partie Simple")

