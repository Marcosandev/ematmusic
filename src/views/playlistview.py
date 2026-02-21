import flet as ft

class PlaylistView(ft.Column):
    def __init__(self, items):
        super().__init__()
        self.items = items

    def build(self):
        return ft.ListView(
            controls=[ft.Text(item) for item in self.items],
            spacing=10,
            padding=10,
            width=300,
            height=400,
            auto_scroll=True
        )

