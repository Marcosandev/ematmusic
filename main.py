import flet as ft
import play_playlist

class MusicApp(ft.Container):
    def __init__(self):
        super().__init__()
        self.page = None

    def build(self):
        self.page = ft.Page()
        self.page.title = "Music App"
        self.page.bgcolor = ft.Colors.BLACK
        self.page.views.append(play_playlist.PagePlaylist(self.page))
        self.page.go(play_playlist.PagePlaylist(self.page))
        return self.page