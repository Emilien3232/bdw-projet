from model.model_pg import get_instances
from controleurs.includes import add_activity

REQUEST_VARS['equipes'] = get_instances(SESSION['CONNEXION'], 'equipe')

if POST:
    try: 
        equipe_supp = POST['equipe_supp']
        if equipe_supp in 


add_activity(SESSION['HISTORIQUE'], "consultation de la page afficher")





