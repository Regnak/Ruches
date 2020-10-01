# coding: utf-8

# import json
from function import ClassBdd
# import os.path
from kivy.uix.widget import Widget
from function.ClassRucher import Rucher
from kivy.uix.button import Button
import datetime


class MainWindow(Widget):
    """widget principale de l'application"""

    def __init__(self, **kwargs):

        super(MainWindow, self).__init__(**kwargs)

        self.nbRucher = 0
        # self.nbList = 0
        self.nbRows = 0
        self.listRucher = []
        self.bdd = ClassBdd.MaBdd()
        # charger mes donnees depuis la base si présente
        for elt in self.bdd.lectureRucher():
            rucher = Rucher(name=str(elt), bdd=self.bdd, inter=self)
            self.listRucher.append(rucher)
        self.majGridRucher()
        # self.textInput = TextInput()
        self.remove_widget(self.text1)
        self.remove_widget(self.gridSuppr)
        print(">>>>>>>>>>>>>Je suis ici<<<<<<<<<<<<<<<<<<")

    def addRucher(self):
        print("ajoute un widget dans la fenetre au-dessus pour le rucher")

        self.remove_widget(self._blButton)
        self.remove_widget(self.gridRucher)

        self.text1.hint_text = "rentrer le nom du rucher ( unique )"
        self.text1.bind(on_text_validate=self.textInputOn_enterAjout)
        self.add_widget(self.text1)

        # self.text1.focus=True

    def majGridRucher(self):
        # clear tout les elements de la grille
        # self.gridRucher.clear_widget()
        for child in self.gridRucher.children[:]:
            self.gridRucher.remove_widget(child)
        # definir la taille du gridLayout
        self.nbRucher = len(self.listRucher)
        # self.gridRucher.cols = 4
        # si on depasse 4 ruchers ajouter une ligne
        if self.nbRucher % 4 != 0:
            self.nbRows = int(self.nbRucher / 4) + 1
        self.gridRucher.rows = self.nbRows
        # ajouter tout les elements contenus dans la liste
        for elt in self.listRucher:
            self.gridRucher.add_widget(elt.btn)
        # l'affiche dans le widget principal
        # self.add_widget(self.gridRucher)

    def textInputOn_enterAjout(self, Parent):

        rucher = Rucher(name=Parent.text, bdd=self.bdd, inter=self)
        date = datetime.datetime.now()
        self.listRucher.append(rucher)
        # enregistre mes donnees dans la base
        self.bdd.insertData("T_rucher", {"nom": Parent.text, "dateInstall": str(date), "lieu": "ici"})
        self.majGridRucher()

        self.text1.unbind(on_text_validate=self.textInputOn_enterAjout)

        self.remove_widget(self.text1)
        self.add_widget(self.gridRucher)
        self.add_widget(self._blButton)

    def delRucher(self):
        if self.nbRucher > 0:
            self.remove_widget(self._blButton)
            # ici commence l'ajout
            self.remove_widget(self.gridRucher)
            for child in self.gridSuppr.children[:]:
                self.gridSuppr.remove_widget(child)

            self.gridSuppr.rows = self.nbRows
            for elt in self.listRucher:
                self.gridSuppr.add_widget(Button(text=elt.nom, on_press=self.on_pressDel))
            self.add_widget(self.gridSuppr)

    def on_pressDel(self, Parent):

        self.remove_widget(self.gridSuppr)
        i = 0
        j = len(self.listRucher)
        while i < j:
            if self.listRucher[i].nom == Parent.text:
                # suppr les ruches du rucher dans la bdd en même temps
                for elt in self.listRucher[i].listRuche:
                    self.bdd.delRuche(str(elt.num), Parent.text)
                del self.listRucher[i]
                break
            i += 1
        self.majGridRucher()
        self.add_widget(self.gridRucher)
        self.add_widget(self._blButton)
        # le supprimer aussi dans la base
        self.bdd.delRucher(Parent.text)

    # a voir pour avoir le rucher depuis ici seulement
    # mon objet rucher former grace a mon textinput
