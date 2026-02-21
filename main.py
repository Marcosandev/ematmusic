import sys
import os

# --- CORRECCIÓN DE IMPORTACIÓN ---
# 1. Obtenemos la ruta absoluta de 'src/main.py'
current_dir = os.path.dirname(os.path.abspath(__file__))

# 2. Subimos un nivel para obtener la ruta de la raíz del proyecto ('eventmatch-eventmatch')
project_root = os.path.dirname(current_dir)

# 3. Agregamos la raíz a la lista de rutas donde Python busca módulos
sys.path.append(project_root)
# ---------------------------------

import flet as ft

from src.controllers.user_controller import UserController
from src.controllers.preferences_controller import PreferencesController

from src.views.homeview import HomeView
from src.views.registerview import RegisterView
from src.views.loginview import LoginView
from src.views.listview import ListView
from src.views.navigationbar import NavigationBar
from src.views.playlistview import PlaylistView
from src.views.profileview import ProfileView

def main(page: ft.Page):
    # Configuración principal de la página
    page.title = "Music App"
    
    page.theme_mode = ft.ThemeMode.LIGHT

    # Configuración de las dimensiones de la ventana (estilo móvil)
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


if __name__ == "__main__":
    ft.run(target=main)
