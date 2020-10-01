# coding: utf-8

# from kivy.app import App
from function import ClassBdd

from kivy.uix.widget import Widget
from kivy.uix.button import Button
from function.ClassRuche import Ruche
from function import ClassBdd
import datetime

class Rucher(Widget):
    """widget representant un rucher et affichant les ruches qu'il contient"""
    def __init__(self, **kwargs):

        super(Rucher, self).__init__()

        self.bdd = kwargs.get("bdd")
        self.nom = kwargs.get("name")
        self.inter = kwargs.get("inter")
        self.nbRows = 0
        # definit le bouton pour linterface principale
        self.btn = Button(text=self.nom)
        self.btn.bind(on_press=self.openRucher)
        self.nbRuches = 0
        self.listRuche = []
        for elt in self.bdd.lectureRuche(self.nom):
            ruche = Ruche(num=elt[0], rucher=self, dateInstall=elt[1], nouri=elt[2], traite=elt[3], nbHausses=elt[4], comment=elt[5])
            self.listRuche.append(ruche)
            self.nbRuches += 1
        self.majGridRuche()
        self.remove_widget(self._text1)
        self.remove_widget(self.gridSuppr)

    def addRuche(self):
        self.remove_widget(self._blButton)
        self.remove_widget(self.gridRuche)

        self._text1.hint_text = "rentrer le numéro de la ruche ( unique )"
        self._text1.bind(on_text_validate=self.textInputOn_enterAjout)
        self.add_widget(self._text1)

    def textInputOn_enterAjout(self, Parent):

        print("ajoute un widget dans la fenetre au-dessus pour la ruche")
        self.nbRuches += 1
        date = datetime.datetime.now()
        self.bdd.insertData("T_ruches", {"num": int(Parent.text), "dateInstall": str(date), "nomRucher": self.nom, "nouri": False, "traite": False, "nbHausses": 0, "comment": ""})
        ruche = Ruche(num=int(Parent.text), rucher=self, dateInstall=date, nouri=False, traite=False, nbHausses=0, comment="")
        self.listRuche.append(ruche)
        self.majGridRuche()

        self._text1.unbind(on_text_validate=self.textInputOn_enterAjout)

        self.remove_widget(self._text1)
        self.add_widget(self.gridRuche)
        self.add_widget(self._blButton)

    def openRucher(self, state):
        self.inter.parent.add_widget(self)
        self.parent.remove_widget(self.inter)
        print("le rucher est bien ouvert")


    def closeRucher(self):
        self.parent.add_widget(self.inter)
        self.inter.parent.remove_widget(self)

    def majGridRuche(self):
        # clear tout les elements de la grille
        for child in self.gridRuche.children[:]:
            self.gridRuche.remove_widget(child)
        # definir la taille du gridLayout
        # self.gridRuche.cols = 4
        # si on depasse 4 ruchers ajouter une ligne
        if self.nbRuches % 4 != 0:
            self.nbRows = int(self.nbRuches / 4) + 1
        self.gridRuche.rows = self.nbRows
        # ajouter tout les elements contenus dans la liste
        for elt in self.listRuche:
            elt.btn.text = elt.getNum()
            self.gridRuche.add_widget(elt.btn)

    def delRuche(self):
        if self.nbRuches > 0:
            self.remove_widget(self._blButton)
            # ici commence l'ajout
            self.remove_widget(self.gridRuche)
            for child in self.gridSuppr.children[:]:
                self.gridSuppr.remove_widget(child)
            self.gridSuppr.rows = self.nbRows
            for elt in self.listRuche:
                self.gridSuppr.add_widget(Button(text=str(elt.num), on_press=self.on_pressDel))
            self.add_widget(self.gridSuppr)
            self.nbRuches -= 1

    def on_pressDel(self, Parent):

        self.remove_widget(self.gridSuppr)
        i = 0
        j = len(self.listRuche)
        while i < j:
            if self.listRuche[i].num == int(Parent.text):
                del self.listRuche[i]
                break
            i += 1
        self.majGridRuche()
        self.add_widget(self.gridRuche)
        self.add_widget(self._blButton)
        # le supprimer aussi dans la base
        self.bdd.delRuche(Parent.text, self.nom)
