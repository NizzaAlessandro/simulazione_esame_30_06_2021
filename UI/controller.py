import warnings

import flet as ft

from database.DAO import DAO


class Controller:
    def __init__(self, view, model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model


    def buildGraph(self):
        self.loc = DAO.getLocalizzazioni()
        self._model.buildGraph(self.loc)
        n, e = self._model.graphDetails()
        #self._view.txtResult.clean()
        self._view.txtResult.controls.append(ft.Text(f"Grafo creato con {n} nodi e {e} archi"))
        self.fillDD()
        self._view.btnStatistiche.disabled = False
        self._view.btnCammino.disabled = False
        self._view.update_page()


    def fillDD(self):
        locDD = list(map(lambda x: ft.dropdown.Option(key=x), self.loc))
        self._view.ddLocalizzazione.options = locDD
        self._view.update_page()

    def handleStatistiche(self, e):
        self.localizzazione = self._view.ddLocalizzazione.value
        if self.localizzazione is None:
            self._view.create_alert("Localizzazione non inserita")
            self._view.txtResult.clean()
            self._view.update_page()
            return
        result = self._model.statistiche(self.localizzazione)
        self._view.txtResult.clean()
        self._view.txtResult.controls.append(ft.Text(f"\nAdiacenti a {self.localizzazione}"))
        for i in result:
            self._view.txtResult.controls.append(ft.Text(f"{i}-->{result[i]}"))
        self._view.update_page()


    def handleCammino(self,e):
        self.localizzazione = self._view.ddLocalizzazione.value
        if self.localizzazione is None:
            self._view.create_alert("Localizzazione non inserita")
            self._view.txtResult.clean()
            self._view.update_page()
            return

        solBest, lunghezza = self._model.calcolaCammino(self.localizzazione)
        self._view.txtResult.controls.append(ft.Text(f"\nIl cammino massimo ha lunghezza {lunghezza}"))
        for i in range(len(solBest)-1):
            self._view.txtResult.controls.append(ft.Text(f"{solBest[i]} --> {solBest[i+1]}"))
        self._view.update_page()
