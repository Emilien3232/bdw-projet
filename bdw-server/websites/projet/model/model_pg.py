import psycopg
from psycopg import sql
from logzero import logger

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

def count_instances(connexion, nom_table):
    """
    Retourne le nombre d'instances de la table nom_table
    String nom_table : nom de la table
    """
    query = sql.SQL('SELECT COUNT(*) AS nb FROM {table}').format(table=sql.Identifier(nom_table))
    return execute_select_query(connexion, query)


"""
ces fonctions ne seront plus utiles car elles sont relatives à un autre schema de BD

def get_episodes_for_num(connexion, numero):

    Retourne le titre des épisodes numérotés numero
    Integer numero : numéro des épisodes

    query = 'SELECT titre FROM episodes where numéro=%s'
    return execute_select_query(connexion, query, [numero])

def get_serie_by_name(connexion, nom_serie):

    Retourne les informations sur la série nom_serie (utilisé pour vérifier qu'une série existe)
    String nom_serie : nom de la série

    query = 'SELECT * FROM series where nomsérie=%s'
    return execute_select_query(connexion, query, [nom_serie])

def insert_serie(connexion, nom_serie):

    Insère une nouvelle série dans la BD
    String nom_serie : nom de la série
    Retourne le nombre de tuples insérés, ou None

    query = 'INSERT INTO series VALUES(%s)'
    return execute_other_query(connexion, query, [nom_serie])
"""


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





