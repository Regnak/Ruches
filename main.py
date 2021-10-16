# coding: utf-8

import kivy
from kivy.app import App
from function import ClassMainWindow
from kivy.lang import Builder


kivy.require('2.0.0')

# load les designs des deux classes concernées
Builder.load_file('function/rucher.kv')
Builder.load_file('function/ruche.kv')

class MainApp(App):

    def build(self):
        # exécute le widget principal et load son design
        return ClassMainWindow.MainWindow()


if __name__ == '__main__':
    MainApp().run()

# reste a faire

    # créer fonction qui récup tous les id des ruches existante
    # a la suppression d'un rucher mettre toute les ruche dans le stock si il y en a
        # une ruche en stock a nomRucher à NULL en base
    # choisir le lieu de suppression d'un ruche
    # exeption a chaque ajout / modif en base -> numérotation des ruches
    # des couleur ou autre pour indiquer l'état des ruches et rucher
    # point de design