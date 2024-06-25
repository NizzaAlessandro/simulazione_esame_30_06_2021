import flet as ft


class View(ft.UserControl):
    def __init__(self, page: ft.Page):
        super().__init__()
        # page stuff
        self._page = page
        self._page.title = "Template application using MVC and DAO"
        self._page.horizontal_alignment = 'CENTER'
        self._page.theme_mode = ft.ThemeMode.LIGHT
        # controller (it is not initialized. Must be initialized in the main, after the controller is created)
        self._controller = None
        # graphical elements
        self._title = None



    def load_interface(self):
        # title
        self._title = ft.Text("simulazione esame 30/06/2021", color="blue", size=24)
        self._page.controls.append(self._title)


        #row1
        self.ddLocalizzazione = ft.Dropdown(label="Localizzazione")
        self.btnStatistiche = ft.ElevatedButton(text="Statistiche", on_click=self._controller.handleStatistiche, disabled=True)

        row1 = ft.Row([ft.Container(self.ddLocalizzazione, width=300),
                       ft.Container(self.btnStatistiche, width=200)],
                      alignment=ft.MainAxisAlignment.CENTER)
        self._page.controls.append(row1)



        #row2
        self.btnCammino = ft.ElevatedButton(text="Ricerca cammino", on_click=self._controller.handleCammino, disabled=True)
        row2 = ft.Row([ft.Container(self.btnCammino, width=200)], alignment=ft.MainAxisAlignment.CENTER)
        self._page.controls.append(row2)

        #row3
        self.txtResult = ft.ListView(auto_scroll=True)
        self._page.controls.append(self.txtResult)
        self._controller.buildGraph()

        self._page.update()
    @property
    def controller(self):
        return self._controller

    @controller.setter
    def controller(self, controller):
        self._controller = controller

    def set_controller(self, controller):
        self._controller = controller

    def create_alert(self, message):
        dlg = ft.AlertDialog(title=ft.Text(message))
        self._page.dialog = dlg
        dlg.open = True
        self._page.update()

    def update_page(self):
        self._page.update()
