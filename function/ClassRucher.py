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
        self.remove_widget(self._gridSuppr)
        self.remove_widget(self._buttonChoixRuche)
        self.remove_widget(self._buttonChoixRuche2)

    # met a jour l'interface pour le futur ajout
    def addRuche(self):

        self.remove_widget(self._blButton)
        self.add_widget(self._buttonChoixRuche)

    def addNewRuche(self):
        numRuche = 1
        # compare dans l'ordre croisant les id de ruche à un itérateur qui débute a 1 pour prendre le premier id disponible
        for i, elt in enumerate(sorted(self.bdd.lectureIdRuche()), 1):
            if i != elt:
                print(elt)
                numRuche = elt
                break
            else:
                numRuche = elt + 1
        self.nbRuches += 1
        date = datetime.datetime.now()
        self.bdd.insertData("T_ruches",
                            {"num": numRuche, "dateInstall": str(date), "nomRucher": self.nom, "nouri": False,
                             "traite": False, "nbHausses": 0, "comment": ""})
        ruche = Ruche(num=numRuche, rucher=self, dateInstall=date, nouri=False, traite=False, nbHausses=0, comment="")
        self.listRuche.append(ruche)
        self.majGridRuche()
        self.remove_widget(self._buttonChoixRuche)
        self.add_widget(self._blButton)

    def addStockRuche(self):
        # a faire
        print("a faire")
        self.remove_widget(self._buttonChoixRuche)
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
        for child in self._gridRuche.children[:]:
            self._gridRuche.remove_widget(child)
        # definir la taille du gridLayout
        # self._gridRuche.cols = 4
        # si on depasse 4 ruchers ajouter une ligne
        if self.nbRuches % 4 != 0:
            self.nbRows = int(self.nbRuches / 4) + 1
        self._gridRuche.rows = self.nbRows
        # ajouter tout les elements contenus dans la liste
        for elt in self.listRuche:
            elt.btn.text = elt.getNum()
            self._gridRuche.add_widget(elt.btn)

    def delRuche(self):
        self.remove_widget(self._blButton)
        self.add_widget(self._buttonChoixRuche2)

    def defDelRuche(self):
        if self.nbRuches > 0:
            self.remove_widget(self._blButton)
            # ici commence l'ajout
            self.remove_widget(self._gridRuche)
            for child in self._gridSuppr.children[:]:
                self._gridSuppr.remove_widget(child)
            self._gridSuppr.rows = self.nbRows
            for elt in self.listRuche:
                self._gridSuppr.add_widget(Button(text=str(elt.num), on_press=self.on_pressDel))
            self.add_widget(self._gridSuppr)
            self.nbRuches -= 1

    def moveToStockRuche(self):
        print("a faire")

    def on_pressDel(self, Parent):

        self.remove_widget(self._gridSuppr)
        i = 0
        j = len(self.listRuche)
        while i < j:
            if self.listRuche[i].num == int(Parent.text):
                del self.listRuche[i]
                break
            i += 1
        self.majGridRuche()
        self.add_widget(self._gridRuche)
        self.add_widget(self._blButton)
        self.remove_widget(self._buttonChoixRuche2)
        # le supprimer aussi dans la base
        self.bdd.delRuche(Parent.text, self.nom)
