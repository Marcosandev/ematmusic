import flet as ft
from src.views.navigationbar import NavigationBar
from src.controllers.search_controller import SearchController
from src.views.navigation import navigate
# Asumo que crearás una vista para el detalle de la canción o reproductor
# from src.views.PlayerView import PlayerView 

class SearchView(ft.Column):
    def __init__(self, page: ft.Page):
        super().__init__(
            expand=True,
            alignment=ft.MainAxisAlignment.START,
        )
        self.main_page = page
        self.controller = SearchController()
        # Modos adaptados a música
        self.mode = "canciones"

        # Barra de búsqueda
        self.search_field = ft.TextField(
            hint_text="¿Qué quieres escuchar?",
            expand=True, # Mantenemos tu expand
            prefix_icon=ft.Icons.SEARCH,
            border_radius=15,
            filled=True,
            border_color=ft.Colors.TRANSPARENT,
            bgcolor=ft.Colors.GREY_900 if page.theme_mode == ft.ThemeMode.DARK else ft.Colors.GREY_100,
            content_padding=10,
            on_change=self.ejecutar_busqueda,
            on_submit=self.ejecutar_busqueda
        )
        
        # Botones de Filtro
        self.btn_canciones = ft.TextButton(
            content=ft.Text("Canciones"), # Corregido a content=ft.Text para evitar el error de 'text'
            on_click=lambda e: self.cambiar_modo("canciones"),
            style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=10), bgcolor=ft.Colors.BLUE_900 if page.theme_mode == ft.ThemeMode.DARK else ft.Colors.BLUE_50)
        )
        self.btn_artistas = ft.TextButton(
            content=ft.Text("Artistas"),
            on_click=lambda e: self.cambiar_modo("artistas"),
            style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=10))
        )
        
        row_botones = ft.Row(
            controls=[self.btn_canciones, self.btn_artistas],
            alignment=ft.MainAxisAlignment.CENTER,
            spacing=20
        )

        # Contenedor de Resultados
        self.resultados_col = ft.Column(
            controls=[],
            scroll=ft.ScrollMode.ADAPTIVE,
            expand=True
        )
        
        self.controls = [
            ft.Container(
                content=ft.Column([
                    ft.Text("Buscar", size=28, weight=ft.FontWeight.BOLD),
                    
                    ft.Row([self.search_field]), 
                    
                    ft.Divider(height=5, color=ft.Colors.TRANSPARENT),
                    row_botones,
                    ft.Divider(height=20, color="#1E2126"),
                    self.resultados_col
                ], expand=True),
                padding=25,
                expand=True
            )
        ]

    def cambiar_modo(self, mode):
        self.mode = mode

        is_dark = self.main_page.theme_mode == ft.ThemeMode.DARK
        active_color = ft.Colors.BLUE_900 if is_dark else ft.Colors.BLUE_50
        
        if mode == "canciones":
            self.btn_canciones.style.bgcolor = active_color
            self.btn_artistas.style.bgcolor = ft.Colors.TRANSPARENT
            self.search_field.hint_text = "Buscar canciones..."
        else:
            self.btn_canciones.style.bgcolor = ft.Colors.TRANSPARENT
            self.btn_artistas.style.bgcolor = active_color
            self.search_field.hint_text = "Buscar artistas o álbumes..."
            
        self.update()
        self.ejecutar_busqueda(None)

    def ejecutar_busqueda(self, e):
        query = self.search_field.value
        self.resultados_col.controls = []
        
        if not query or len(query) < 1: # Evitar búsquedas vacías o muy cortas
            self.resultados_col.update()
            return
            
        if self.mode == "canciones":
            # Asumiendo que tu controlador tiene este método ahora
            results = self.controller.search_songs(query)
            for song in results:
                self.resultados_col.controls.append(
                    ft.ListTile(
                        leading=ft.Icon(ft.Icons.MUSIC_NOTE, color=ft.Colors.BLUE),
                        title=ft.Text(song['title'], weight=ft.FontWeight.BOLD),
                        subtitle=ft.Text(f"{song.get('artist', 'Artista desconocido')} • {song.get('genero', 'Género desconocido')}"),
                        trailing=ft.IconButton(icon=ft.Icons.PLAY_ARROW_ROUNDED, on_click=lambda e, s=song: self.reproducir(s['url'])),
                        on_click=lambda e, s=song: self.reproducir(s['url'])
                    )
                )
        else:
            results = self.controller.search_artists(query)
            for artist in results:
                self.resultados_col.controls.append(
                    ft.ListTile(
                        leading=ft.CircleAvatar(
                            foreground_image_src=artist.get('image', ""),
                            content=ft.Text(artist['name'][0])
                        ),
                        title=ft.Text(artist['name']),
                        subtitle=ft.Text("Artista"), 
                    )
                )
        
        self.resultados_col.update()

    def reproducir(self, url):
        import webbrowser
        if url:
            webbrowser.open(url)