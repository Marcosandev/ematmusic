import flet as ft
import os
import time
import pygame
import platform
import asyncio

PYGAME_AVAILABLE = True
try:
    import pygame
except ImportError:
    PYGAME_AVAILABLE = False


class PlaylistController:
    """Controller holding audio and session logic for PlaylistView.

    The controller keeps a reference to the view instance and manipulates
    its attributes when the UI needs to change. This keeps the view file
    focused on widget construction and layout.

    To avoid rescanning the file system on every navigation, a simple cache
    of the discovered songs is stored in a class variable.  """

    # simple in-memory cache shared across controller instances
    _cached_canciones = None

    def __init__(self, view):
        self.view = view
        # recover paused flag from session so switching views doesn't reset it
        pausado = self.view.main_page.session.store.get("musica_en_pausa")
        if pausado is None:
            pausado = False
        setattr(self.view, "en_pausa", pausado)
        # always keep session in sync (in case other code reads it)
        self.view.main_page.session.store.set("musica_en_pausa", pausado)

    def cargar_musica(self, inicial=False):
        """Escaneo profundo y resistente a errores de permisos."""
        # Limpiamos solo la UI, no tocamos la lógica de reproducción
        self.view.lista_canciones.controls.clear()
        self.view.canciones_paths = []

        if PlaylistController._cached_canciones is not None:
            canciones = PlaylistController._cached_canciones
        else:
            canciones = []
            sistema = platform.system()
            
            # Puntos de partida
            if sistema == "Windows":
                rutas_raiz = [os.path.expanduser("~")]
                ignorar = ["AppData", "Local Settings", "Application Data", "Temp", "Cookies"]
            else:
                # Android: Memoria interna completa
                rutas_raiz = ["/storage/emulated/0", "/sdcard"]
                ignorar = ["Android", "data", "obb"]

            for root_dir in rutas_raiz:
                if not os.path.exists(root_dir):
                    continue
                    
                # Usamos un try-except por si el root_dir no es accesible
                try:
                    for raiz, dirs, archivos in os.walk(root_dir, topdown=True):
                        # Modificamos dirs in-place para saltar carpetas prohibidas o del sistema
                        dirs[:] = [d for d in dirs if d not in ignorar and not d.startswith('.')]
                        
                        for f in archivos:
                            try:
                                if f.lower().endswith(".mp3"):
                                    full_path = os.path.join(raiz, f).replace("\\", "/")
                                    # Solo agregamos si el archivo es realmente legible
                                    if os.access(full_path, os.R_OK):
                                        canciones.append({
                                            "path": full_path, 
                                            "titulo": f.replace(".mp3", ""),
                                            "carpeta": os.path.basename(raiz)
                                        })
                            except Exception:
                                continue # Si un archivo da error, seguimos con el siguiente
                except Exception as e:
                    print(f"Error accediendo a {root_dir}: {e}")
                    continue

            # Ordenar y guardar en caché
            canciones.sort(key=lambda x: x["titulo"].lower())
            PlaylistController._cached_canciones = canciones

        # RECONEXIÓN CON LA VISTA:
        # Volvemos a llenar la lista exactamente como la vista lo espera
        for i, c in enumerate(canciones):
            self.view.canciones_paths.append(c)
            es_esta = (i == self.view.indice_actual)
            # Usamos el creador de la vista para mantener el diseño original
            self.view.lista_canciones.controls.append(
                self.view._crear_listtile(c["titulo"], idx=i, activo=es_esta)
            )

        self.view.update()

    def reproducir(self, indice):
        self.view.posicion_salto = 0
        self.view.main_page.session.store.set("musica_pos", 0)
        self.view.indice_actual = indice
        cancion = self.view.canciones_paths[indice]

        # persistir
        self.view.main_page.session.store.set("musica_indice", indice)
        self.view.main_page.session.store.set("musica_titulo", cancion["titulo"])
        self.view.main_page.session.store.set("musica_artista", "Desconocido")
        # al iniciar reproducción nueva, no estamos en pausa
        self.view.en_pausa = False
        self.view.main_page.session.store.set("musica_en_pausa", False)

        # inicializar controles
        self.view.slider_progreso.value = 0
        self.view.lbl_tiempo_actual.value = "0:00"

        if PYGAME_AVAILABLE:
            pygame.mixer.music.load(cancion["path"])
            pygame.mixer.music.play()
            audio_info = pygame.mixer.Sound(cancion["path"])
            duracion = audio_info.get_length()
            self.view.slider_progreso.max = duracion
            self.view.lbl_tiempo_total.value = self.formatear_tiempo(duracion)

        self.view.txt_titulo.value = cancion["titulo"]
        self.view.full_txt_titulo.value = cancion["titulo"]
        self.view.btn_play_pause.icon = ft.Icons.PAUSE_ROUNDED
        self.view.btn_play_pause_full.icon = ft.Icons.PAUSE_CIRCLE_FILLED_ROUNDED
        # nuevo estado, no estamos en pausa
        self.view.en_pausa = False

        # recargar lista para marca activa
        self.cargar_musica()
        # Actualizar el icono de favorito según si la canción está en favoritos
        self._actualizar_icono_favorito()
        self.view.update()

    def toggle_reproduccion(self, e=None):
        # if no song selected, start first one
        if self.view.indice_actual == -1 and self.view.canciones_paths:
            self.reproducir(0)
            self.view.en_pausa = False
        elif PYGAME_AVAILABLE:
            if pygame.mixer.music.get_busy():
                # normal pause path: remember where we were so resuming later
                self.view.posicion_salto = self.view.slider_progreso.value
                self.view.main_page.session.store.set("musica_pos", self.view.posicion_salto)

                self.view.en_pausa = True
                self.view.main_page.session.store.set("musica_en_pausa", True)
                pygame.mixer.music.pause()
                self.view.btn_play_pause.icon = ft.Icons.PLAY_ARROW_ROUNDED
                self.view.btn_play_pause_full.icon = ft.Icons.PLAY_CIRCLE_FILLED_ROUNDED
            else:
                # not busy when user clicked; could mean
                # 1) we were already paused (en_pausa True)
                # 2) playback stopped due to view change/OS
                if getattr(self.view, "en_pausa", False):
                    # resume paused track
                    pygame.mixer.music.unpause()
                    # if mixer forgot, reload (using stored position)
                    if not pygame.mixer.music.get_busy() and self.view.indice_actual != -1:
                        ruta = self.view.canciones_paths[self.view.indice_actual]["path"]
                        pygame.mixer.music.load(ruta)
                        pygame.mixer.music.play(start=self.view.posicion_salto)
                    self.view.en_pausa = False
                    self.view.main_page.session.store.set("musica_en_pausa", False)
                    self.view.btn_play_pause.icon = ft.Icons.PAUSE_ROUNDED
                    self.view.btn_play_pause_full.icon = ft.Icons.PAUSE_CIRCLE_FILLED_ROUNDED
                else:
                    # user wanted to pause but playback already stopped; just
                    # reload and pause at current position without advancing.
                    if self.view.indice_actual != -1:
                        ruta = self.view.canciones_paths[self.view.indice_actual]["path"]
                        pygame.mixer.music.load(ruta)
                        pygame.mixer.music.play(start=self.view.posicion_salto)
                        pygame.mixer.music.pause()
                    self.view.en_pausa = True
                    self.view.main_page.session.store.set("musica_en_pausa", True)
                    self.view.btn_play_pause.icon = ft.Icons.PLAY_ARROW_ROUNDED
                    self.view.btn_play_pause_full.icon = ft.Icons.PLAY_CIRCLE_FILLED_ROUNDED
        self.view.update()

    async def actualizar_progreso_async(self):
        while True:
            try:
                if getattr(self.view, "buscando", False):
                    await asyncio.sleep(0.1)
                    continue

                if hasattr(self.view, "slider_progreso") and PYGAME_AVAILABLE:
                    if pygame.mixer.music.get_busy():
                        t_pygame = pygame.mixer.music.get_pos() / 1000
                        if t_pygame >= 0:
                            pos_real = self.view.posicion_salto + t_pygame
                            if pos_real <= self.view.slider_progreso.max:
                                self.view.slider_progreso.value = pos_real
                                self.view.lbl_tiempo_actual.value = self.formatear_tiempo(pos_real)
                                self.view.slider_progreso.update()
                                self.view.lbl_tiempo_actual.update()
                    elif self.view.indice_actual != -1 and not getattr(self.view, "en_pausa", False):
                        # only advance when song really reached end (not just busy ==
                        # False due to external stop). use slider value as proxy.
                        if self.view.slider_progreso.value >= self.view.slider_progreso.max - 0.1:
                            if self.view.is_loop:
                                self.reproducir(self.view.indice_actual)
                            else:
                                self.cambiar_cancion(1)
                            if self.view.page:
                                self.view.page.update()
                        # otherwise do nothing and let the next toggle/pause handle it
            except:
                pass
            await asyncio.sleep(0.1)

    def formatear_tiempo(self, segundos):
        mins = int(segundos // 60)
        secs = int(segundos % 60)
        return f"{mins}:{secs:02d}"

    def sincronizar_estado_inicial(self):
        # Restore slider/max values and ensure pygame has the current track
        if self.view.indice_actual == -1:
            # Actualizar el icono de favorito cuando se carga la vista sin canción
            self._actualizar_icono_favorito()
            return
        if PYGAME_AVAILABLE:
            try:
                ruta = None
                if self.view.indice_actual < len(self.view.canciones_paths):
                    ruta = self.view.canciones_paths[self.view.indice_actual]["path"]
                if ruta:
                    audio_info = pygame.mixer.Sound(ruta)
                    dur = audio_info.get_length()
                    self.view.slider_progreso.max = dur
                    self.view.lbl_tiempo_total.value = self.formatear_tiempo(dur)

                    # If we were paused when leaving, just load the song and set
                    # the position; don't play it.  That prevents a tiny sound
                    # fragment before we can pause again.  toggle_reproduccion
                    # already knows how to restart a paused-but-not-busy track.
                    if getattr(self.view, "en_pausa", False):
                        pygame.mixer.music.load(ruta)
                        try:
                            pygame.mixer.music.set_pos(self.view.posicion_salto)
                        except Exception:
                            # some formats don't support set_pos; we'll handle
                            # correct start on unpause later
                            pass

                    t_pygame = pygame.mixer.music.get_pos() / 1000
                    if t_pygame < 0:
                        t_pygame = 0
                    self.view.slider_progreso.value = self.view.posicion_salto + t_pygame
                    self.view.lbl_tiempo_actual.value = self.formatear_tiempo(self.view.slider_progreso.value)
                    self.view.btn_play_pause.icon = (
                        ft.Icons.PAUSE_ROUNDED
                        if pygame.mixer.music.get_busy()
                        else ft.Icons.PLAY_ARROW_ROUNDED
                    )
                    self.view.btn_play_pause_full.icon = (
                        ft.Icons.PAUSE_CIRCLE_FILLED_ROUNDED
                        if pygame.mixer.music.get_busy()
                        else ft.Icons.PLAY_CIRCLE_FILLED_ROUNDED
                    )
                    self.view.slider_progreso.update()
                    self.view.lbl_tiempo_actual.update()
                    self.view.lbl_tiempo_total.update()
                    # Actualizar el icono de favorito cuando se sincroniza el estado
                    self._actualizar_icono_favorito()
            except Exception:
                pass

    def on_slider_start(self, e):
        self.view.buscando = True

    def on_slider_change(self, e):
        nuevo_valor = float(e.data)
        self.view.lbl_tiempo_actual.value = self.formatear_tiempo(nuevo_valor)
        self.view.lbl_tiempo_actual.update()

    def seek_music(self, e):
        if PYGAME_AVAILABLE and self.view.indice_actual != -1:
            try:
                nuevo_punto = float(e.data)
                self.view.posicion_salto = nuevo_punto
                self.view.main_page.session.store.set("musica_pos", nuevo_punto)
                pygame.mixer.music.play(start=nuevo_punto)
                self.view.slider_progreso.value = nuevo_punto
                self.view.slider_progreso.update()
            except:
                pass
            time.sleep(0.1)
            self.view.buscando = False

    def toggle_favorito(self, e):
        # Usamos self.view.main_page porque el controlador conoce la vista
        page = self.view.main_page
        
        # 1. Obtenemos el nombre de la canción que está en el texto del reproductor
        nombre_cancion = self.view.full_txt_titulo.value
        
        if nombre_cancion == "Selecciona una canción":
            return

        # 2. Obtener favoritos (Corregido: Flet usa set_data/get_data o simplemente session)
        # Para evitar errores, usamos page.session.get_data
        favoritos = page.session.store.get("mis_favoritos") or []

        # 3. Lógica simple: si está, se va. Si no, entra.
        if nombre_cancion in favoritos:
            favoritos.remove(nombre_cancion)
            self.view.reproductor_full.btn_fav.icon_color = ft.Colors.GREY_400
        else:
            favoritos.append(nombre_cancion)
            self.view.reproductor_full.btn_fav.icon_color = ft.Colors.RED

        # 4. Guardar
        page.session.store.set("mis_favoritos", favoritos)
        page.update()

    def _actualizar_icono_favorito(self):
        """Actualiza el color del icono de favorito según si la canción actual está en favoritos."""
        page = self.view.main_page
        nombre_cancion = self.view.full_txt_titulo.value
        
        if nombre_cancion == "Selecciona una canción":
            return
            
        favoritos = page.session.store.get("mis_favoritos") or []
        
        if nombre_cancion in favoritos:
            self.view.reproductor_full.btn_fav.icon_color = ft.Colors.RED
        else:
            self.view.reproductor_full.btn_fav.icon_color = ft.Colors.GREY_400

    def toggle_loop(self, e):
        self.view.is_loop = not self.view.is_loop
        e.control.icon_color = ft.Colors.BLUE_400 if self.view.is_loop else ft.Colors.GREY_400
        self.view.update()

    def cambiar_cancion(self, delta):
        if not self.view.canciones_paths:
            return
        self.view.indice_actual = (self.view.indice_actual + delta) % len(self.view.canciones_paths)
        self.reproducir(self.view.indice_actual)

    def abrir_reproductor(self, e):
        if self.view.page.navigation_bar:
            self.view.page.navigation_bar.visible = False
        # header previously added by NavigationBar; hide it too so the
        # panel can occupy the full screen without being covered.
        if hasattr(self.view.page, "app_header"):
            self.view.page.app_header.visible = False
        self.view.reproductor_full.bottom = 0
        # Actualizar el icono de favorito cuando se abre el reproductor
        self._actualizar_icono_favorito()
        self.view.page.update()

    def cerrar_reproductor(self, e):
        if self.view.page.navigation_bar:
            self.view.page.navigation_bar.visible = True
        if hasattr(self.view.page, "app_header"):
            self.view.page.app_header.visible = True
        self.view.reproductor_full.bottom = -1000
        self.view.page.update()