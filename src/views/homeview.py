import flet as ft
import datetime
from src.views.navigation import navigate
from src.views.albumsview import AlbumsView
from src.views.favoritesview import FavoritesView

class HomeView(ft.Column):
    def __init__(self, page: ft.Page):
        super().__init__(
            expand=True,
            scroll=ft.ScrollMode.ADAPTIVE,
            spacing=25
        )
        self.main_page = page
        
        # 1. SALUDO DINÁMICO
        self.controls.append(self._crear_cabecera())

        # 2. ACCESO RÁPIDO A BIBLIOTECA
        self.controls.append(
            ft.Container(
                content=ft.Column([
                    ft.Text("Ver", size=20, weight=ft.FontWeight.BOLD),
                    ft.ResponsiveRow([
                        self._boton_biblioteca("Álbumes", ft.Icons.ALBUM_ROUNDED, ft.Colors.PURPLE),
                        self._boton_biblioteca("Favoritos", ft.Icons.FAVORITE_ROUNDED, ft.Colors.RED),
                    ], spacing=10)
                ]),
                padding=ft.Padding(20, 0, 20, 0)
            )
        )

        self.controls.append(
            ft.Container(
                content=ft.Column([
                    ft.Text("Descripción", size=20, weight=ft.FontWeight.BOLD),
                    ft.ResponsiveRow([
                        self.texto_boton(f"¡Bienvenid@ a nuestra app de música EmatMusic.\n\nEmatMusic es un reproductor de musica local que te permite escuchar musica que tu descargues en tu dispositivo, aqui podras explorar tus álbumes y guardar tus canciones favoritas para acceder a ellas rápidamente."),
                    ], spacing=10)
                ]),
                padding=15,
            )
        )

    def _crear_cabecera(self):
        hora = datetime.datetime.now().hour
        if 5 <= hora < 12:
            saludo = "¡Buenos días!"
        elif 12 <= hora < 18:
            saludo = "¡Buenas tardes!"
        else:
            saludo = "¡Buenas noches!"

        return ft.Container(
            content=ft.Row([
                ft.Column([
                    ft.Text(saludo, size=28, weight=ft.FontWeight.BOLD),
                    ft.Text("¿Qué vas a escuchar hoy?", color=ft.Colors.GREY_500),
                ]),
            ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
            padding=ft.Padding(20, 8, 20, 0)
        )

    def _boton_biblioteca(self, titulo, icono, color):
        # Asignamos la vista correspondiente
        destino = AlbumsView if titulo == "Álbumes" else FavoritesView
        
        return ft.Container(
            content=ft.Row([
                ft.Icon(icono, color=color, size=30),
                ft.Text(titulo, weight=ft.FontWeight.W_600)
            ], spacing=15),
            bgcolor=ft.Colors.GREY_900 if self.main_page.theme_mode == ft.ThemeMode.DARK else ft.Colors.GREY_100,
            padding=15,
            border_radius=12,
            col={"sm": 6}, 
            on_click=lambda _: navigate(self.main_page, destino),
        )

    def descripcion(self, texto):
        # ¡IMPORTANTE! Agregar el 'return' para que el contenedor se añada a la lista
        return ft.Container(
            content=ft.Text(
                texto, 
                size=16, 
                color=ft.Colors.WHITE,
            ),
            padding=ft.padding.only(top=5)   
        )
    
    def texto_boton(self, texto):
        return ft.Container(
            content=ft.Text(
                texto,
                size=16,
                weight=ft.FontWeight.W_400,
                color=ft.Colors.WHITE if self.main_page.theme_mode == ft.ThemeMode.DARK else ft.Colors.GREY_900,
            ),
            padding=15,
            
            border_radius=12,
            bgcolor=ft.Colors.GREY_900 if self.main_page.theme_mode == ft.ThemeMode.DARK else ft.Colors.GREY_100,
        )
    