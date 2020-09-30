# coding: utf-8

import kivy
from kivy.app import App
from function import ClassMainWindow
from kivy.lang import Builder


kivy.require('1.9.1')

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


    # des couleur ou autre pour indiquer l'état des ruches et rucher