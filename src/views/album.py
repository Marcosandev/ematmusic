import flet as ft
from src.controllers.albums_controller import AlbumController

class AlbumView(ft.Column):
    def __init__(self, page: ft.Page, album_id, album_nombre):
        super().__init__(expand=True, scroll=ft.ScrollMode.ADAPTIVE)
        self.main_page = page
        self.album_id = album_id
        self.album_nombre = album_nombre
        self.controller = AlbumController()
        
        # Cabecera con botón de volver
        self.controls.append(
            ft.Container(
                content=ft.Row([
                    ft.IconButton(
                        icon=ft.Icon(ft.Icons.ARROW_BACK_IOS_NEW_ROUNDED, size=18),
                        on_click=lambda _: self.volver()
                    ),
                    ft.Text(self.album_nombre, size=24, weight="bold"),
                ]),
                padding=20
            )
        )
        
        # Contenedor de la lista de canciones
        self.lista_canciones = ft.Column(spacing=10)
        self.controls.append(ft.Container(content=self.lista_canciones, padding=20))

    def did_mount(self):
        self.cargar_canciones()

    def cargar_canciones(self):
        canciones = self.controller.get_songs_by_album(self.album_id)
        self.lista_canciones.controls.clear()
        
        if not canciones:
            self.lista_canciones.controls.append(ft.Text("No hay canciones en este álbum aún."))
        else:
            for can in canciones:
                self.lista_canciones.controls.append(
                    ft.Container(
                        # El ListTile termina AQUÍ (nota el cierre de paréntesis después del IconButton)
                        content=ft.ListTile(
                            leading=ft.Icon(ft.Icons.MUSIC_NOTE, color=ft.Colors.BLUE),
                            title=ft.Text(can['title'], weight="bold"),
                            subtitle=ft.Text(can['artist']),
                            trailing=ft.IconButton(
                                icon=ft.Icons.PLAY_ARROW_ROUNDED,
                                on_click=lambda e, url=can['url']: self.reproducir(url)
                            ),
                        ),
                        # Estas propiedades pertenecen al CONTAINER
                        bgcolor=ft.Colors.GREY_900 if self.main_page.theme_mode == ft.ThemeMode.DARK else ft.Colors.GREY_100,
                        border_radius=12,
                        padding=15,
                    )
                )

        self.update()

    def reproducir(self, url):
        import webbrowser
        if url:
            webbrowser.open(url)

    def volver(self):
        # Aquí usamos tu lógica de navegación para regresar
        from src.views.navigation import go_back
        go_back(self.main_page)