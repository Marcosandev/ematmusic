import flet as ft

class HomeView(ft.Column):
    def __init__(self):
        super().__init__()
        self.build()

    def build(self):
        self.controls.append(ft.Text("Bienvenido a la Home View", size=24, weight=ft.FontWeight.BOLD))
        # Aquí puedes agregar más controles para mostrar contenido relevante en la Home View