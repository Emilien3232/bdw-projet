import psycopg
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
	




