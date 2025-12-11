import psycopg
import random as rd
from psycopg import sql
from logzero import logger
from datetime import datetime

def execute_select_query(connexion, query, params=[]):
    """
    Méthode générique pour exécuter une requête SELECT (qui peut retourner plusieurs instances).
    Utilisée par des fonctions plus spécifiques.
    """
    with connexion.cursor() as cursor:
        try:
            cursor.execute(query, params)
            result = cursor.fetchall()
            return result 
        except psycopg.Error as e:
            logger.error(e)
    return None

def execute_other_query(connexion, query, params=[]):
    """
    Méthode générique pour exécuter une requête INSERT, UPDATE, DELETE.
    Utilisée par des fonctions plus spécifiques.
    """
    with connexion.cursor() as cursor:
        try:
            cursor.execute(query, params)
            result = cursor.rowcount
            return result 
        except psycopg.Error as e:
            logger.error(e)

    return None

def get_instances(connexion, nom_table):
    """
    Retourne les instances de la table nom_table
    String nom_table : nom de la table
    """
    query = sql.SQL('SELECT * FROM {table}').format(table=sql.Identifier(nom_table), )
    return execute_select_query(connexion, query)

def get_listenom(connexion):
    """
    Retourne les noms de la table equipe
    """

    query = sql.SQL('SELECT nom FROM equipe ').format(table=sql.Identifier(equipe), )
    return execute_select_query(connexion, query)

def count_instances(connexion, nom_table):
    """
    Retourne le nombre d'instances de la table nom_table
    String nom_table : nom de la table
    """
    query = sql.SQL('SELECT COUNT(*) AS nb FROM {table}').format(table=sql.Identifier(nom_table))
    return execute_select_query(connexion, query)



def get_table_like(connexion, nom_table, like_pattern):
    """
    Retourne les instances de la table nom_table dont le nom correspond au motif like_pattern
    String nom_table : nom de la table
    String like_pattern : motif pour une requête LIKE
    """
    motif = '%' + like_pattern + '%'
    nom_att = 'nomsérie'  # nom attribut dans séries (à éviter)
    if nom_table == 'actrices':  # à éviter
        nom_att = 'nom'  # nom attribut dans actrices (à éviter)
    query = sql.SQL("SELECT * FROM {} WHERE {} ILIKE {}").format(
        sql.Identifier(nom_table),
        sql.Identifier(nom_att),
        sql.Placeholder())
    #    like_pattern=sql.Placeholder(name=like_pattern))
    return execute_select_query(connexion, query, [motif])

#Fonctionnalités 1 : accueil et statistiques

#1 . 3 instances au choix
def nombre_equipe(connexion):
    """
    Retourne le nombre d'équipes dans la table équipes
    """
    query = 'SELECT COUNT(*) AS nb FROM equipe'
    return execute_select_query(connexion, query)

def nombre_partie(connexion):
    """
    Retourne le nombre de parties dans la table parties
    """
    query = 'SELECT COUNT(*) AS nombre_parties FROM partie'
    return execute_select_query(connexion, query)

def nombre_morpion(connexion):
    """
    Retourne le nombre de parties de morpion dans la table morpion
    """
    query = 'SELECT COUNT(*) AS nombre_morpion FROM morpion'
    return execute_select_query(connexion, query)

#2 . la durée de la partie la plus courte et de la plus longue
def partie_plus_courte(connexion):
    """
    Retourne la partie la plus courte dans la table parties
    """
    query = '''
    SELECT
        ID_Partie,
        date_debut,
        date_fin,
        (date_fin - date_debut) AS duree
    FROM
        partie
    WHERE
        date_fin IS NOT NULL
    ORDER BY
        duree ASC
    LIMIT 1
    '''
    return execute_select_query(connexion, query)

def partie_plus_longue(connexion):
    """
    Retourne la partie la plus longue dans la table parties
    """
    query = '''
    SELECT
        ID_Partie,
        date_debut,
        date_fin,
        (date_fin - date_debut) AS duree
    FROM
        partie
    WHERE
        date_fin IS NOT NULL
    ORDER BY
        duree DESC
    LIMIT 1
    '''
    return execute_select_query(connexion, query)

#3 . la moyenne du nombre de lignes de journalisation par mois et par année
def moyenne_journalisation(connexion):
    """
    Retourne la moyenne du nombre de lignes de journalisation par mois et par année
    """
    query= '''
    SELECT
        EXTRACT(YEAR FROM P.date_debut) AS annee_partie,
        EXTRACT(MONTH FROM P.date_debut) AS mois_partie,
        AVG(T1.nombre_lignes)::numeric(10, 2) AS moyenne_lignes_journalisation
    FROM
        partie P
    JOIN
        (
            SELECT
                ID_Partie,
                COUNT(id_ligne) AS nombre_lignes
            FROM
                ligne_journal
            GROUP BY
                ID_Partie
        ) AS T1 ON P.ID_Partie = T1.ID_Partie
    GROUP BY
        annee_partie,
        mois_partie
    ORDER BY
        annee_partie,
        mois_partie
    '''
    return execute_select_query(connexion, query)

def ajoute_equipe(connexion, string_nom_equipe, liste_morpion_id, string_couleur):
    """
    Ajoute une équipe dans la table équipe avec les morpions sélectionnés
    String string_nom_equipe : nom de l'équipe
    List liste_morpion_id : liste des IDs des morpions sélectionnés
    String string_couleur : couleur de l'équipe
    Retourne le nombre de tuples insérés, ou None
    """
    id_equipe = count_instances(connexion, 'equipe')[0][0] + 1 # récupère nombre d'équipe déja rentrées dans la bdw
    date = datetime.now().replace(microsecond=0)  # date actuelle sans les microsecondes

    query1 = f"""
    INSERT INTO equipe  (id_equipe , couleur , date_creation , nom )
    values ({id_equipe}, '{string_couleur}', '{date}' ,'{string_nom_equipe}' )
    """

    liste_values = 'values'
    
    for i in range (len(liste_morpion_id)-1):
        values = f'({id_equipe},{liste_morpion_id[i]})'
        liste_values = liste_values + values + ',' 
    liste_values = liste_values + f'({id_equipe},{liste_morpion_id[-1]})'

    query2 = f""" INSERT INTO composer (id_equipe, id_morpion) 
    {liste_values} """
    

    execute_other_query(connexion, query1, params=[])
    execute_other_query(connexion, query2, params=[])
    return None

def ajoute_config(connexion,nb_tours, dimension):
    """ 
    Ajoute une configuration d'une nouvelle partie avec une taille de grille ( dimension ) 
    un nombre de tour max, en ajoutant aussi la date de création 
    et un identifiant de config 
    
    """

    id_config = count_instances(connexion, 'configuration')[0][0] + 1 # récupère nombre d'équipe déja rentrées dans la bdw et ajoute 1 pour avoir la nouvelle id_config
    date = datetime.now().replace(microsecond=0)  # date actuelle sans les microsecondes

    query = f"""
    INSERT INTO configuration  (id_configuration , nb_tours_max , dimension , date_creation )
    values ({id_config}, '{nb_tours}', '{dimension}' ,'{date}' )
    """
 
    execute_other_query(connexion, query, params=[])

    return None

def supp_config(connexion):
    """ 
    une fonction qui supprime les configurations existantes dans la bdw
    """
    query = f""" DELETE 
    from configuration 
    """
    execute_other_query(connexion, query, params=[])

    return None


def supp_partie(connexion):
    """ 
    une fonction qui supprime les parties existantes dans la bdw
    """
    query = f""" DELETE 
    from partie 
    """
    execute_other_query(connexion, query, params=[])

    return None

def supp_equipe(connexion,nom):
    """ 
    une fonction qui prend en entrée le nom d'une équipe et qui efface les données de l'équipe 
    et les données de composer sur les morpions utilisés
    
    """
    query1 = f""" DELETE 
    from equipe 
    where nom = '{nom}'
    """
    query2 = f""" DELETE 
    from composer 
    where id_equipe = (SELECT id_equipe 
                      from equipe 
                      where nom = '{nom}' )
    """
    execute_other_query(connexion, query2, params=[])
    execute_other_query(connexion, query1, params=[])

    
    return None
	

def get_morpion_par_equipe(connexion, id_equipe):
    """
    Retourne les morpions associés à une équipe donnée
    Integer id_equipe : identifiant de l'équipe
    """
    query = f"""
    select m.* from morpion m where m.id_morpion in (select c.id_morpion from composer c where c.id_equipe = {id_equipe} )
    """

    return execute_select_query(connexion, query, params=[])

def get_morpion_par_id(connexion, id_morpion):
    """
    Retourne le morpion associé à un id_morpion donné
    Integer id_morpion : identifiant du morpion
    """
    query = f"""
    select m.* from morpion m where m.id_morpion = {id_morpion}
    """

    return execute_select_query(connexion, query, params=[])



def verif_cond_victoire(connexion, dimension, tableau,  morpions_equipe1, morpions_equipe2, nb_tours, nb_tours_max):



    ''' cette fonction vérifie si une des deux équipes à gagné ou pas ( aligné 3/4 morpions )

    renvoie ( TRUE , équipe gagnante 1 ou 2 ) si il y a une condition de victoire

    '''

    nb_tours = nb_tours +1

# test ligne ou colonne ou diagonale pour dimension 3
    if dimension == 3 :
        for i in range (3):

            if tableau[i][0][0] != None and tableau[i][1][0] != None and tableau[i][2][0] != None : #on verifie si les cases de la ligne i sont remplies

                if tableau[i][0][0] == tableau[i][1][0] == tableau[i][2][0] : # on verifie si les cases de la ligne i ont le meme numéro d'équipe

                    return [True , tableau[i][0][0] , nb_tours ] # on retourne vrai et le numéro de l'équipe gagnante

            if tableau[0][i][0] != None and tableau[1][i][0] != None and tableau[2][i][0] != None : #on verifie si les cases de la colonne i sont remplies

                if tableau[0][i][0] == tableau[1][i][0] == tableau[2][i][0] : # on verifie si les cases de la colonne i ont le meme numéro d'équipe

                    return [True , tableau[0][i][0] , nb_tours ] 



        if tableau[0][0][0] != None and tableau[1][1][0] != None and tableau[2][2][0] != None : # on verifie si les cases de la diagonale principale sont remplies (gauche à droite)

            if tableau[0][0][0] == tableau[1][1][0] ==tableau[2][2][0] : # on verifie si les cases de la diagonale principale ont le meme numéro d'équipe

                return [True , tableau[0][0][0] , nb_tours ] 



        if tableau[0][2][0] != None and tableau[1][1][0] != None and tableau[2][0][0] != None : # on verifie si les cases de la diagonale secondaire sont remplies (droite à gauche)

            if tableau[0][2][0] == tableau[1][1][0] ==tableau[2][0][0] :

                return [True , tableau[0][2][0] , nb_tours ]

# de meme maniere pour dimension 4
    if dimension ==4 :

        for i in range (4):

            if tableau[i][0][0] != None and tableau[i][1][0] != None and tableau[i][2][0] != None and tableau[i][3][0] != None :

                if tableau[i][0][0] == tableau[i][1][0] == tableau[i][2][0] == tableau[i][3][0] :

                    return [True , tableau[i][0][0] , nb_tours ] 

            if tableau[0][i][0] != None and tableau[1][i][0] != None and tableau[2][i][0] != None and tableau[3][i][0] != None :

                if tableau[0][i][0] == tableau[1][i][0] == tableau[2][i][0] == tableau[3][i][0] :

                    return [True , tableau[0][i][0] , nb_tours ] 



        if tableau[0][0][0] != None and tableau[1][1][0] != None and tableau[2][2][0] != None and tableau[3][3][0] != None :

            if tableau[0][0][0] == tableau[1][1][0] ==tableau[2][2][0] ==tableau[3][3][0]:

                return [True , tableau[0][0][0] , nb_tours ] 



        if tableau[0][3][0] != None and tableau[1][2][0] != None and tableau[2][1][0] != None and tableau[3][0][0] != None :

            if tableau[0][3][0] == tableau[1][2][0] ==tableau[2][1][0] ==tableau[3][0][0]:

                return [True , tableau[0][3][0] , nb_tours ]

        

# test si tous les morpions d'une équipe sont morts 

    if morpions_equipe1 == []:

        return  [True, 2, nb_tours ]

    if morpions_equipe2 == []:

        return [True , 1, nb_tours ]



# test si le nombre de tours max est atteint

    if nb_tours == nb_tours_max :

        return [True , 0 , nb_tours ] # match nul

    

    return [False , None , nb_tours ]






def morpions_morts(morpions_equipe1,  morpions_equipe2, tableau):



    '''cette fonction enleve les morpions morts de la liste des morpions de chaque équipe et enlève les morpions morts du tableau '''



    for n in range (len(morpions_equipe1)): # on enleve les morpions de l'équipe 1 qui sont morts

        if morpions_equipe1[n][3] == 0 :

             # morpions_equipe[n][0] c'est l'id du morpion qui est mort



            for i in range (len(tableau)) :

                for j in range (len(tableau)):

                    if tableau[i][j][0] != None :

                        if [tableau[i][j][0],tableau[i][j][1][0]] == [1,morpions_equipe1[n][0]] :

                            

                            tableau[i][j][0] = None

                            tableau[i][j][1] = None



            morpions_equipe1.pop(n)





    for i in range (len(morpions_equipe2)):



        if morpions_equipe2[i][3] == 0:



            for i in range (len(tableau)) :

                for j in range (len(tableau)):

                    if tableau[i][j][0] != None :

                        if [tableau[i][j][0],tableau[i][j][1][0]] == [2,morpions_equipe1[n][0]] :

                            

                            tableau[i][j][0] = None

                            tableau[i][j][1] = None



            morpions_equipe2.pop(i)





    return [morpions_equipe2,morpions_equipe1,tableau]




def ajoute_journal(connexion,cord1, cord2, tableau , morpion_choisis, sorts, attaque, boolean_partie ):



    if boolean_partie :

        joueuse = 1

    if not boolean_partie :

        joueuse = 2



    id_partie = count_instances(connexion, 'partie')[0][0]

    id_ligne = count_instances(connexion, 'ligne_journal')[0][0] +1

    date = datetime.now().replace(microsecond=0)





    if sorts == 0 :

        query = f'''

        INSERT INTO ligne_journal (id_ligne,date_action, description, id_partie )

        values ({id_ligne}, '{date}',"la joueuse{joueuse} lance une boule de feu en ({cord1};{cord2})", {id_partie} ) '''

            

    elif sorts == 1 :

       query =  f''' 

        INSERT INTO ligne_journal (id_ligne, date_action, description , id_partie )

        values ({id_ligne},"{date}", "la joueuse{joueuse} soigne {morpion_choisis[1]} avec un sort de soin", {id_partie} )  '''

 

    elif sorts == 2 :

        query =  f''' 

        INSERT INTO ligne_journal (id_ligne,date_action, description , id_partie )

        values ({id_ligne},"{date}", "la joueuse {joueuse} à lancé le sort armagedon sur la case ({cord1};{cord2})", {id_partie} )  '''





    elif attaque != None :

        query =  f''' 

        INSERT INTO ligne_journal (id_ligne,date_action, description , id_partie )

        values ({id_ligne}, '{date}','la joueuse{joueuse} attaque avec {morpion_choisis[1]} la case {cord1};{cord2}', {id_partie} )  '''



    

    else :

        query =  f''' 

        INSERT INTO ligne_journal (id_ligne , date_action , description , id_partie ) 

        values ({id_ligne},'{date}' , 'la joueuse{joueuse} joue {morpion_choisis[1]} en ({cord1};{cord2})' , {id_partie})  '''


    execute_other_query(connexion, query, params=[])
    return None


#la joueuse {joueuse} à joué {morpion_choisis[1]} dans la case ({cord1};{cord2})





def fin_partie(connexion):



    date = datetime.now().replace(microsecond=0)

    id_partie = count_instances(connexion, 'partie')[0][0]/2



    query = f'''UPDATE partie

    SET date_fin = {date}

    WHERE id_partie = {id_partie}'''



    execute_other_query(connexion, query, params=[])



def ajoute_partie(connexion, id_equipe1, id_equipe2):



    date = datetime.now().replace(microsecond=0)

    id_partie = count_instances(connexion, 'partie')[0][0]/2 + 1

    id_config = count_instances(connexion, 'configuration')[0][0] 



    query1 = f''' INSERT INTO partie (id_partie, date_debut, id_configuration, id_equipe)

    values ({id_partie},'{date}',{id_config},{id_equipe1})'''


    execute_other_query(connexion, query1, params=[])


     

def sorts(connexion, morpion_choisis, morpions_equipe1, morpions_equipe2, boolean_partie, sort, tableau , cord1, cord2, 
          cases_inutilisables):
    
    ''' cette fonction va gerer les lancements des sorts et mettre a jour l'action joueur '''

    morpion_attaque = None
    if tableau[cord1][cord2][0] is not None :
        morpion_attaque = tableau[cord1][cord2][1][0] # recupere id du morpion attaquee

    reussite = False 
    mana = [2, 1, 5] # les points de mana que coutent chaque sort (Sort 0, Sort 1, Sort 2)

    numerochoisi2 = None
    numerochoisi1 = None
    numeroattaque1 = None
    numeroattaque2 = None

    for i in range (len(morpions_equipe2)):
        if morpions_equipe2[i][0] == morpion_choisis[0] :
            numerochoisi2 = i
    for i in range (len(morpions_equipe1)):
        if morpions_equipe1[i][0] == morpion_choisis[0] :
            numerochoisi1 = i

    if morpion_attaque is not None:
        for i in range (len(morpions_equipe2)):
            if morpions_equipe2[i][0] == morpion_attaque :
                numeroattaque2 = i
        for i in range (len(morpions_equipe1)):
            if morpions_equipe1[i][0] == morpion_attaque :
                numeroattaque1 = i

    morpion_lanceur = None
    if boolean_partie: # C'est le tour de l'équipe 1
        if numerochoisi1 is not None:
            morpion_lanceur = morpions_equipe1[numerochoisi1]
    else: # C'est le tour de l'équipe 2
        if numerochoisi2 is not None:
            morpion_lanceur = morpions_equipe2[numerochoisi2]
    if sort in [0, 1, 2]:
        cout = mana[sort] 
    else:
        cout = 0
    mana_lanceur_index = 4 
    
    if morpion_lanceur is not None and morpion_lanceur[mana_lanceur_index] >= cout:
        #morpion_lanceur[mana_lanceur_index] -= cout #tuple alors valeur inchageable
        reussite = True # Le sort a été lancé avec succès

        if sort == 0: #boule de feu
            if morpion_attaque is not None:
                degats = 10 
                
                pv_index = 3 
                if boolean_partie and numeroattaque2 is not None: # Attaque l'équipe 2
                    morpions_equipe2[numeroattaque2][pv_index] -= degats
                elif not boolean_partie and numeroattaque1 is not None: # Attaque l'équipe 1
                    morpions_equipe1[numeroattaque1][pv_index] -= degats

        elif sort == 1:
            # Sort de soin (cible le Morpion lanceur)
            soin = 5
            pv_index = 3
            morpion_lanceur[pv_index] += soin
            
        # armageddon
        elif sort == 2:
            if (cord1, cord2) not in cases_inutilisables:
                cases_inutilisables.append((cord1, cord2))
        

    else:
        reussite = False
        
    return reussite


def attaque(connexion, boolean_partie, morpion_choisis, morpions_equipe2, morpions_equipe1, tableau, cord1,cord2):



    ''' cette fonction va gerer les attaques '''



    reussite = False 

    morpion_attaque = tableau[cord1][cord2][1][0]



    numerochoisi2 = None

    numerochoisi1 = None



    numeroattaque1 = None

    numeroattaque2 = None

    

    for i in range (len(morpions_equipe2)):

        if morpions_equipe2[i][0] == morpion_choisis[0] :

            numerochoisi2 = i



    for i in range (len(morpions_equipe1)):

        if morpions_equipe1[i][0] == morpion_choisis[0] :

            numerochoisi1 = i



    

    for i in range (len(morpions_equipe2)):

        if morpions_equipe2[i][0] == morpion_attaque :

            numeroattaque2 = i



    for i in range (len(morpions_equipe1)):

        if morpions_equipe1[i][0] == morpion_attaque :

            numeroattaque1 = i

     

    

    if rd.randint(1,100) < 10 * morpion_choisis[5] : # on regarde si l'attaque réussit



        reussite = not(reussite)



        if boolean_partie == False: 



           # rajoute des points de réussite au morpion qui vient de réussir son attaque

            morpions_equipe2[numerochoisi2][5] = morpions_equipe2[numerochoisi2][5] + 0.5 



            # on déduis l'attaque de l'attaquant aux pv de l'attaqué

            morpions_equipe1[numeroattaque1][3] = morpions_equipe1[numeroattaque1][3] - morpions_equipe2[numerochoisi2][6]



        else :

            morpions_equipe1[numerochoisi1][5] = morpions_equipe1[numerochoisi1][5] + 0.5

            morpions_equipe2[numeroattaque2][3] = morpions_equipe2[numeroattaque2][3] - morpions_equipe1[numerochoisi1][6]





    return [morpions_equipe1, morpions_equipe2]
      