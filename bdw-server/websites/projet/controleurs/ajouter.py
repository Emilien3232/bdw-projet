from controleurs.includes import add_activity
from model.model_pg import get_instances 

REQUEST_VARS['morpions'] = get_instances(SESSION['CONNEXION'],'morpion') # on recupere les instances de morpion disponibles pour le formulaire d'ajout d'équipe
REQUEST_VARS['message_erreur'] = ""
REQUEST_VARS['message_confirmation'] = ""

#afin de eviter les erreur d'ajout à la base de deonnées 
#(couleur unique et nom unique) on doit rajouter une comparaison des variables Post avec les elements 
#deja presents dans la base de données

if POST:
    try:
        nom_equipe = POST['nom']
        couleur_equipe = POST['couleur_equipe']
        morpion_id = POST['morpions_selectionnes[]'] #recupere les morpions selectionnés par l'utilisateur dans le formulaire
        
        if not (6 <= len(morpion_id) <= 8): #si l'utilisateur n'a pas selectionné entre 6 et 8 morpions on renvoie un message d'erreur
            REQUEST_VARS['message_erreur'] = "Veuillez sélectionner entre 6 et 8 morpions pour l'équipe."
        else: #si ce n'esst pas le cas on utilise la fonction ajout_equipe et on renvoie un message de confirmation
            #ajoute_equipe(SESSION['CONNEXION'], nom_equipe, morpion_id, couleur)
            REQUEST_VARS['message_confirmation'] = "L'équipe a été ajoutée avec succès."
    except KeyError:
        REQUEST_VARS['message_erreur'] = "Veuillez séléctionner des morpions."


add_activity(SESSION['HISTORIQUE'], "consultation de la page ajouter")