import flet as ft
from src.views.navigation import go_back
from src.controllers.albums_controller import AlbumController # Importamos el controlador
from src.views.album import AlbumView # Importamos la vista de detalle del álbum
from src.views.navigation import navigate # Importamos la función de navegación para ir a la vista de detalle

class AlbumsView(ft.Column):
    def __init__(self, page: ft.Page):
        super().__init__(expand=True, scroll=ft.ScrollMode.ADAPTIVE)
        self.main_page = page
        self.controller = AlbumController()
        
        # Contenedor donde se dibujarán los álbumes cuando lleguen de la DB
        self.grid = ft.ResponsiveRow(spacing=20, run_spacing=20)
        
        # Cabecera
        self.controls.append(
            ft.Container(
                content=ft.Row([
                    ft.IconButton(
                        icon=ft.Icon(ft.Icons.ARROW_BACK_IOS_NEW_ROUNDED, size=18), 
                        on_click=lambda _: go_back(self.main_page)
                    ),
                    ft.Text("Álbumes famosos", size=24, weight="bold"),
                ]),
                padding=ft.Padding(10, 10, 10, 10)
            )
        )

        self.controls.append(ft.Container(content=self.grid, padding=20))
        
        # Llamamos a la función para cargar datos al iniciar
        self.cargar_albumes_db()

    def cargar_albumes_db(self):
        # 1. Obtenemos los datos del controlador
        # Nota: Asegúrate de tener el método get_all_albums en tu controlador
        albums = self.controller.get_all_albums()
        
        self.grid.controls.clear()
        
        for alb in albums:
            # Usamos los nombres de columna de tu tabla: nombre, artista, color_hex
            nombre = alb.get('nombre', 'Sin título')
            artista = alb.get('artista', 'Desconocido')
            color = alb.get('color_hex', '#333333') # Color por defecto si está vacío

            self.grid.controls.append(
                ft.Container(
                    content=ft.Column([
                        ft.Container(
                            width=150, 
                            height=150, 
                            bgcolor=color, 
                            border_radius=15,
                            content=ft.Icon(ft.Icons.ALBUM, size=50, color=ft.Colors.WHITE),
                            alignment=ft.Alignment.CENTER
                        ),
                        ft.Text(nombre, weight="bold", size=14, max_lines=1, overflow=ft.TextOverflow.ELLIPSIS),
                        ft.Text(artista, size=12, color=ft.Colors.GREY_500)
                    ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                    col={"xs": 6, "sm": 4, "md": 3},
                    on_click=lambda e, a_id=alb['id'], a_nom=alb['nombre']: self.ir_a_detalle_album(a_id, a_nom)
                )
            )

    def ir_a_detalle_album(self, album_id, album_nombre):
        # Navegamos a la vista de detalle pasando los parámetros necesarios
        navigate(self.main_page, AlbumView, album_id=album_id, album_nombre=album_nombre)