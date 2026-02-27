import flet as ft
from src.views.navigation import go_back

class FavoritesView(ft.Column):
    def __init__(self, page: ft.Page):
        super().__init__(expand=True, scroll=ft.ScrollMode.ADAPTIVE)
        self.main_page = page

        self.controls.append(
            ft.Container( # Agregamos el Container para que el padding funcione
                content=ft.Row([
                    ft.IconButton(
                        icon=ft.Icons.ARROW_BACK_IOS_NEW_ROUNDED, 
                        icon_size=18,  
                        on_click=lambda _: go_back(self.main_page)
                    ),
                    ft.Text("Mis Favoritos", size=25, weight="bold"),
                ]),
                padding=ft.padding.all(10) # Manera más limpia de poner 10 en todos los lados
            )
        )

        # Contenedor para los nombres de las canciones
        self.lista_favs = ft.Column()
        
        # Cargar nombres reales desde la sesión
        nombres = self.main_page.session.store.get("mis_favoritos") or []
        
        if not nombres:
            self.lista_favs.controls.append(
                ft.Container(
                    content=ft.Text("No hay canciones favoritas", color="grey"),
                    padding=ft.padding.only(left=30) # Padding para el texto de aviso
                )
            )
        else:
            for nombre in nombres:
                self.lista_favs.controls.append(
                    ft.ListTile(
                        leading=ft.Icon(ft.Icons.MUSIC_NOTE, color="red"),
                        title=ft.Text(nombre)
                    )
                )
        
        self.controls.append(self.lista_favs)