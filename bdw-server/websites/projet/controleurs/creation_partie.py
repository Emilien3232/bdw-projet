from controleurs.includes import add_activity
from datetime import datetime
from model.model_pg import get_instances , ajoute_config , supp_config , ajoute_partie , supp_partie , count_instances

REQUEST_VARS['liste_equipes'] = get_instances(SESSION['CONNEXION'], 'equipe')
equipes_par_id = {str(equipe[0]): equipe for equipe in REQUEST_VARS['liste_equipes']} #obliger vu que retour du form sont des strings
print(REQUEST_VARS['liste_equipes'])
if POST :
    nb_tours = POST['nb_tours'][0]
    equipes_id_selectionnees = POST['equipe_selectionnes[]']
    dim_grille = POST['taille_grille'][0]
    if len(equipes_id_selectionnees) != 2 :
        REQUEST_VARS['message_erreur'] = "Veuillez sélectionner exactement deux équipes."
    else :
        equipe_1_complete = equipes_par_id[equipes_id_selectionnees[0]]
        equipe_2_complete = equipes_par_id[equipes_id_selectionnees[1]]
        ajoute_config(SESSION['CONNEXION'],nb_tours, dim_grille) # on ajoute la nouvelle config
        n = count_instances(SESSION['CONNEXION'], 'configuration')[0][0] -1 #on récupère l'id de la dernière config ajoutée
        SESSION['CONFIG_PARTIE'] = get_instances(SESSION['CONNEXION'],'configuration')[n] #on met à jour la config en session
        SESSION['EQUIPE_1'] = equipe_1_complete
        SESSION['EQUIPE_2'] = equipe_2_complete
        REQUEST_VARS['message_confirmation'] = f"""La partie a été créée avec succès et les équipes : {SESSION['EQUIPE_1'][3]} ET {SESSION['EQUIPE_2'][3]} sont prêtes pour la partie ! allez dans JOUER."""
        SESSION['DATE_DEBUT_PARTIE'] = datetime.now().replace(microsecond=0)
        ajoute_partie(SESSION['CONNEXION'], SESSION['EQUIPE_1'][0], SESSION['EQUIPE_2'][0])

add_activity(SESSION['HISTORIQUE'], "consultation de la page de création de partie")


