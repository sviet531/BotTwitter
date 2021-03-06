# Bibliothèques standard
import sqlite3
import datetime

def CreateTables(user):
    # On crée data.db ou on l'ouvre juste si elle existe
    connexion = sqlite3.connect('data.db')
    c = connexion.cursor()
    # On fait une table si elle n'existe pas
    # On fait une table pour chaque compte
    c.execute('''CREATE TABLE IF NOT EXISTS {tab}
    (id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE, compte text, date DATE);'''.format(tab=user.screen_name))
    c.close()
    connexion.commit()


def UpdateTable(follower, user):
    connexion = sqlite3.connect('data.db')
    c = connexion.cursor()
    # On regarde si on a déjà un follower avec cet id
    c.execute('''SELECT * FROM {tab} WHERE compte = ?;'''.format(tab=user.screen_name), (str(follower),))
    data = c.fetchall()
    # Si cet id existe pas :
    if len(data) == 0:
        # On rentre la date du jour et le compte follow
        c.execute('''INSERT INTO {tab}(compte,date) VALUES (:compte, :date);'''.format(tab=user.screen_name), (follower, datetime.datetime.now()))
        c.close()
        connexion.commit()
    # Si cet id existe
    else:
        # On change la date
        c.execute('''UPDATE {tab} SET date = ? WHERE compte = ?'''.format(tab=user.screen_name), (datetime.datetime.now(), str(follower),))
        c.close()
        connexion.commit()


def Unfollow(user, api):
    print("Vérification des comptes à unfollow.")
    # On crée data.db ou on l'ouvre juste si elle existe
    connexion = sqlite3.connect('data.db')
    c = connexion.cursor()
    # On selectionne toute la table
    c.execute('''SELECT * FROM {tab};'''.format(tab=user.screen_name))
    data = c.fetchall()
    for i in data:
        try:
            date = datetime.datetime.strptime(i[2], "%Y-%m-%d %H:%M:%S.%f")
            if date.month == 11:
                newmonth = 1
                date = date.replace(year=date.year + 1)
            elif date.month == 12:
                newmonth = 2
                date = date.replace(year=date.year + 1)
            else:
                newmonth = date.month+2
            # On ne veut pas une date plus grande que 28 pour fevrier au risque de generer une erreur.
            if newmonth == 2 and date.day > 28:
                date = date.replace(day=28)
            date = date.replace(month=newmonth)
            # Si la date actuel est plus grande aue la date de fin de follow alors :
            if datetime.datetime.now() > date:
                # On unfollow
                c.execute('''DELETE FROM {tab} WHERE compte = ?;'''.format(tab=user.screen_name), (str(i[1]),))
                api.destroy_friendship(i[1])
        except Exception:
            pass
    c.close()
    connexion.commit()
