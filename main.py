import sys
import os

# --- CORRECCIÓN DE IMPORTACIÓN ---
# 1. Obtenemos la ruta absoluta de 'src/main.py'
current_dir = os.path.dirname(os.path.abspath(__file__))

# 2. Subimos un nivel para obtener la ruta de la raíz del proyecto
project_root = os.path.dirname(current_dir)

# 3. Agregamos la raíz a la lista de rutas donde Python busca módulos
sys.path.append(project_root)
# ---------------------------------

import flet as ft

from src.views.homeview import HomeView
from src.views.navigationbar import NavigationBar
from src.views.playlistview import PlaylistView
from src.views.app_header import AppHeader

def main(page: ft.Page):
    # Configuración principal de la página
    page.title = "EmatMusic"
    
    page.theme_mode = ft.ThemeMode.DARK
    
    # Create and add the app header
    page.app_header = AppHeader(page)
    
    page.window.width = 400
    page.window.height = 750
    page.window.resizable = False

    # Inicialización de bases de datos
    # (Comentado temporalmente o gestionado dentro de los controladores)
    # try:
    #     # Postgres connection is now lazy/handled in controllers
    #     pass
    # except Exception as e:
    #     print(f"Error al inicializar PostgreSQL (Asegúrate de configurar el .env): {e}")

    # init_sqlite_db()
    # print("SQLite Inicializado")

    def route_change(e): # Añade el parámetro 'e'
        page.views.clear()
        
        # Barra de navegación
        nav = NavigationBar(page)

        if page.route == "/":
            page.views.append(
                ft.View(
                    route="/",
                    controls=[page.app_header, HomeView(page)],
                    navigation_bar=nav,
                )
            )
        elif page.route == "/playlist":
            page.views.append(
                ft.View(
                    route="/playlist",
                    controls=[page.app_header, PlaylistView(page)],
                    navigation_bar=nav,
                )
            )
        page.update()

    # 1. Asignar el evento
    page.on_route_change = route_change
    
    # 2. LA CORRECCIÓN: En lugar de push_route o go, haz esto:
    page.route = "/" 
    page.on_route_change(None) # Llamamos a la función manualmente para cargar la Home


if __name__ == "__main__":
    ft.run(main)