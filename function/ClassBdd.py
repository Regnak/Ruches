# coding: utf-8

import sqlite3


''' Base de donnée des rucher et fonction liée pour travailler dessus'''


class MaBdd:

    def __init__(self):

        self.conn = sqlite3.connect('resources/ruches.db')
        self.cursor = self.conn.cursor()
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS T_rucher(
                nom TEXT,
                dateInstall DATE,
                lieu TEXT,
                PRIMARY KEY (nom)
            )
            """)
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS T_ruches(
                num INT,
                dateInstall DATE,
                nomRucher TEXT,
                nouri BOOL,
                traite BOOL,
                nbHausses INT,
                comment TEXT,
                FOREIGN KEY (nomRucher) REFERENCES T_rucher(nom)
                PRIMARY KEY (num)
            )
            """)

        self.cursor.execute("""
            REPLACE INTO T_rucher(nom, dateInstall, lieu)
            VALUES('__Stock', '2020-10-04', 'here');
            """)

        self.conn.commit()


    def closeConn(self):
        self.conn.close() 

    # faire une seule fonction insert qui prend en param la table
    def insertData(self, table, data):
        # a voir l'utilité de elt
        if table == "T_ruches":
            self.cursor.execute("""
                INSERT INTO T_ruches(num, dateInstall, nomRucher, nouri, traite, nbHausses, comment) 
                    VALUES(:num, :dateInstall, :nomRucher, :nouri, :traite, :nbHausses, :comment)""", data)
            self.conn.commit()
        elif table == "T_rucher":
            self.cursor.execute("""
                INSERT INTO T_rucher(nom, dateInstall, lieu) 
                    VALUES(:nom, :dateInstall, :lieu)""", data)
            self.conn.commit()
        # controler que le composant n'est pas déjà présent dans la base

    def lectureRucher(self):
        listRucher = list()
        self.cursor.execute("""SELECT nom 
            FROM T_rucher""")
        # row est un pointeur sur le debut de retour de la requete
        for row in self.cursor:
            listRucher.append(row[0])
            print(row[0])
        return listRucher

    def lectureIdRuche(self):
        listRuche = list()
        self.cursor.execute("""SELECT num 
            FROM T_ruches""")
        # row est un pointeur sur le debut de retour de la requete
        for row in self.cursor:
            listRuche.append(row[0])
            print(row[0])
        return listRuche

    def lectureRuche(self, rucher):
        listRuche = list()
        self.cursor.execute("""SELECT * 
            FROM T_ruches
            WHERE nomRucher = ?
            """, [rucher])
        # row est un pointeur sur le debut de retour de la requete
        for row in self.cursor:
            listRuche.append((row[0], row[1], row[3], row[4], row[5], row[6]))
            print(row[0], row[1], row[3], row[4], row[5], row[6])
        return listRuche

    def updateRuche(self, num, rucher, nouri, traite, nbHausses, comment):
        self.cursor.execute("""UPDATE T_ruches
            SET nouri = ?,
                traite = ?,
                nbHausses = ?,
                comment = ?
            WHERE nomRucher = ? AND num = ?""", (nouri, traite, nbHausses, comment, rucher, num))
        self.conn.commit()
        print(num, rucher, nouri, traite, nbHausses, comment)

    def delRucher(self, rucher):
        self.cursor.execute("""DELETE
            FROM T_rucher
            WHERE nom = ?
            """, [rucher])
        self.conn.commit()

    def delRuche(self, num, rucher):
        self.cursor.execute("""DELETE
                    FROM T_ruches
                    WHERE num = ? AND nomRucher = ?
                    """, (num, rucher))
        self.conn.commit()


