from controleurs.includes import add_activity
from model.model_pg import get_morpion_par_equipe
if SESSION['CONFIG_PARTIE'] :
    REQUEST_VARS['morpion_equipe_1'] = get_morpion_par_equipe(SESSION['CONNEXION'], SESSION['EQUIPE_1'][0])
    REQUEST_VARS['morpion_equipe_2'] = get_morpion_par_equipe(SESSION['CONNEXION'], SESSION['EQUIPE_2'][0])
    REQUEST_VARS['nb_morpion_equipe_1'] = len(REQUEST_VARS['morpion_equipe_1'])
    REQUEST_VARS['nb_morpion_equipe_2'] = len(REQUEST_VARS['morpion_equipe_2'])
    id_equipe_active = None
    REQUEST_VARS['lancement_partie'] = False
    if POST :
        REQUEST_VARS['lancement_partie'] = True
        if POST['equipe_commence'][0] == '1' :
            id_equipe_active = SESSION['EQUIPE_1'][0]
        elif POST['equipe_commence'][0] == '2' :
            id_equipe_active = SESSION['EQUIPE_2'][0]
        else :
            id_equipe_active = SESSION['EQUIPE_1'][0] # par défaut équipe 1 commence, implementer systeme aléatoire plus tard


















add_activity(SESSION['HISTORIQUE'], "consultation de la page Partie Simple")

