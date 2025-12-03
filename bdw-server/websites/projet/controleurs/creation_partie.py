from controleurs.includes import add_activity
from model.model_pg import get_instances , ajoute_config

REQUEST_VARS['liste_equipes'] = get_instances(SESSION['CONNEXION'], 'equipe')
print(REQUEST_VARS['liste_equipes'])
if POST :
    nb_tours = POST['nb_tours'][0]
    equipes_selectionnees = POST['equipe_selectionnes[]']
    if POST['taille_grille'] == '3' : 
        dim_grille = 3
    else : 
        dim_grille = 4
    if len(equipes_selectionnees) != 2 :
        REQUEST_VARS['message_erreur'] = "Veuillez sélectionner exactement deux équipes."
    else :
        ajoute_config(SESSION['CONNEXION'],nb_tours, dim_grille)
        SESSION['EQUIPE_1'] = equipes_selectionnees[0]
        SESSION['EQUIPE_2'] = equipes_selectionnees[1]
        REQUEST_VARS['message_confirmation'] = "La partie a été créée avec succès et les équipes sont prêtes pour la partie ! allez dans JOUER."

add_activity(SESSION['HISTORIQUE'], "consultation de la page recherche")


