from model.model_pg import get_instances
from controleurs.includes import add_activity

REQUEST_VARS['equipes'] = get_instances(SESSION['connexion'], 'equipe')


add_activity(SESSION['HISTORIQUE'], "consultation de la page afficher")





