import flet as ft

class pageplaylist(ft.View):
    def __init__(self, page):
        super().__init__()
        self.page = page
        self.title = "Playlist"
        self.bgcolor = ft.Colors.BLACK

    def build(self):
        return ft.Text("This is the playlist page")