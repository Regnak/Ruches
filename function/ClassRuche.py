# coding: utf-8

from kivy.uix.widget import Widget
from kivy.uix.button import Button
import datetime

class Ruche(Widget):

    def __init__(self, **kwargs):
        super(Ruche, self).__init__()

        self.rucher = kwargs.get("rucher")
        self.num = kwargs.get("num")
        self.nourri = kwargs.get("nouri")
        self.traite = kwargs.get("traite")
        self.nbHausses = kwargs.get("nbHausses")
        self.dateInstall = kwargs.get("dateInstall")
        self.comment = kwargs.get("comment")

        self.btn = Button(text=str(self.num))
        self.btn.bind(on_press=self.openRuche)
        if self.comment != "":
            self.btn.background_color = [1, 0, 1, 1]


    """widget ou objet representant un ruche avec toute donnee qui la concerne"""


    def openRuche(self, state):
        root = self.rucher.parent
        root.remove_widget(self.rucher)
        root.add_widget(self)
        self._ti1.text = str(self.nbHausses)
        self._text1.text = self.comment
        self._ch1.active = self.nourri
        self._ch2.active = self.traite
        if self._text1.text != "":
            self._btnCom.background_color = [1, 0, 1, 1]  # purple
        self.remove_widget(self._text1)
        self.remove_widget(self._gridRuche)

    def closeRuche(self):
        # - recup les donnée des widget hors commentaires
        self.nourri = self._ch1.active
        self.traite = self._ch2.active
        # verif que l'on a bien un int
        self.nbHausses = int(self._ti1.text)
        # - met a jour la BDD
        self.rucher.bdd.updateRuche(self.num, self.rucher.nom, self.nourri, self.traite, self.nbHausses, self.comment)
        # - met les widget a jour
        self.parent.add_widget(self.rucher)
        self.rucher.parent.remove_widget(self)

    def retourComment(self):
        if self._btnCom.text == "Valider":
            self.comment = self._text1.text
            self.remove_widget(self._text1)
            self._btnCom.text = "Commentaire"
            if self._text1.text != "":
                self._btnCom.background_color = [1, 0, 1, 1] # purple
                self.btn.background_color = [1, 0, 1, 1]
            self._boxButton.add_widget(self._sp1)
            self._boxButton.add_widget(self._btnRetour)
            self.add_widget(self._gridCheck)
            print(self.comment)
        else:
            self.add_widget(self._text1)
            self._btnCom.text = "Valider"
            self._btnCom.background_color = [1, 1, 1, 1]
            self._boxButton.remove_widget(self._btnRetour)
            self._boxButton.remove_widget(self._sp1)
            self.remove_widget(self._gridCheck)

    def changerRucher(self):
        # a finir -> faire un grille un peu comme gridsuppr et GG !
        self.remove_widget(self._gridCheck)
        self.remove_widget(self._boxButton)
        if self.rucher.inter.nbRucher > 0:
            print("blbl")
            i = 0
            for child in self._gridRuche.children[:]:
                self._gridRuche.remove_widget(child)
            for elt in self.rucher.inter.listRucher:
                if elt.nom != self.rucher.nom:
                    self._gridRuche.add_widget(Button(text=elt.nom, on_press=self.on_pressChange))
                    i += 1
            self._gridRuche.rows = int(i / 4) + 1
            self.add_widget(self._gridRuche)

    def on_pressChange(self, parent):
        date = datetime.datetime.now()
        nbRuche = len(self.rucher.bdd.lectureRuche(parent.text))
        self.rucher.bdd.insertData("T_ruches", {"num": (nbRuche + 1), "dateInstall": str(date), "nomRucher": parent.text, "nouri": self.nourri, "traite": self.traite, "nbHausses": self.nbHausses, "comment": self.comment})
        self.rucher.bdd.delRuche(self.num, self.rucher.nom)

        rucherBase = self.rucher
        for elt in self.rucher.inter.listRucher:
            if elt.nom == parent.text:
                self.rucher = elt
        i = 0
        while i < len(rucherBase.listRuche):
            if rucherBase.listRuche[i].num == self.num:
                self.rucher.listRuche.append(rucherBase.listRuche.pop(i))
            i += 1
        self.num = nbRuche + 1
        rucherBase.majGridRuche()
        rucherBase.nbRuches -= 1
        self.rucher.nbRuches += 1
        self.rucher.majGridRuche()

        self.remove_widget(self._gridRuche)
        self.add_widget(self._gridCheck)
        self.add_widget(self._boxButton)



    def getNum(self):
        return str(self.num)
