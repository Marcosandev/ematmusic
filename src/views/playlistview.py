import flet as ft
# Asegúrate de importar tu función de consultas
from src.models.consultas import obtener_playlist_detallada 

class PlaylistView(ft.Column): # O ft.Container, según uses
    def __init__(self, page: ft.Page):
        super().__init__()
        # CAMBIO CLAVE: Usa self.main_page en lugar de self.page
        self.main_page = page 
        self.expand = True
        
        # Lista visual donde irán las canciones
        self.lista_items = ft.ListView(expand=True, spacing=10)
        
        # El reproductor de audio
        self.audio_player = ft.Audio(src="", autoplay=False)
        if self.audio_player not in self.main_page.overlay:
            self.main_page.overlay.append(self.audio_player)

        self.controls = [
            ft.Text("Mi Playlist", size=30, weight="bold"),
            self.lista_items
        ]
        
        # Cargar los datos de Postgres
        self.cargar_datos()

    def cargar_datos(self):
        canciones = obtener_playlist_detallada()
        self.lista_items.controls.clear()
        
        for c in canciones:
            self.lista_items.controls.append(
                ft.ListTile(
                    title=ft.Text(c["titulo"]),
                    subtitle=ft.Text(f"{c['artista']} - {c['album']}"),
                    on_click=lambda e, r=c["ruta_archivo"]: self.play_song(r)
                )
            )

    def play_song(self, ruta):
        self.audio_player.src = ruta
        self.audio_player.update()
        self.audio_player.play()