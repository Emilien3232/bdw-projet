from controleurs.includes import add_activity
from model.model_pg.py import get_instances

REQUEST_VARS['liste_equipes'] = get_instances(SESSION['CONNEXION'], 'equipe')
if POST :
    nb_tours = POST['nb_tours']
    equipes_selectionnees = POST['equipe_selectionnes[]']       
add_activity(SESSION['HISTORIQUE'], "consultation de la page recherche")


