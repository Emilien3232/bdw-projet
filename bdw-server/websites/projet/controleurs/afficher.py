from model.model_pg import get_instances , supp_equipe
from controleurs.includes import add_activity
REQUEST_VARS['equipes'] = get_instances(SESSION['CONNEXION'], 'equipe')

if POST:
 
    equipe_supp = POST['supp'][0]
    print("equipe a supp " , equipe_supp)
    
    supp_equipe(SESSION['CONNEXION'], equipe_supp)
    REQUEST_VARS['message_confirmation'] = f"L'équipe {equipe_supp} a été supprimée avec succès."



add_activity(SESSION['HISTORIQUE'], "consultation de la page afficher")




