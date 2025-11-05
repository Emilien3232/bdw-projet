from controleurs.includes import add_activity
from model.model_pg import nombre_equipe, nombre_partie, nombre_morpion ,partie_plus_courte, partie_plus_longue, moyenne_journalisation

#Focntionnalité 1 : accueil et statistiques
REQUEST_VARS['nb_equipe'] = nombre_equipe(SESSION['CONNEXION'])[0][0] #1 . 3 instances au choix
REQUEST_VARS['nb_partie'] = nombre_partie(SESSION['CONNEXION'])[0][0] #1
REQUEST_VARS['nb_morpion'] = nombre_morpion(SESSION['CONNEXION'])[0][0] #1
REQUEST_VARS['partie_courte'] = partie_plus_courte(SESSION['CONNEXION']) #2 . la durée de la partie la plus courte et de la plus longue
REQUEST_VARS['partie_longue'] = partie_plus_longue(SESSION['CONNEXION']) #2
REQUEST_VARS['moyenne_journalisation'] = moyenne_journalisation(SESSION['CONNEXION']) #3 . la moyenne de journalisation par équipe



add_activity(SESSION['HISTORIQUE'], "consultation de la page d'accueil")





