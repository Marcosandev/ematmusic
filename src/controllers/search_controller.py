import flet as ft

class SearchController:
    def __init__(self):
        # Datos de ejemplo (Mock Data) para que puedas probar la interfaz de inmediato.
        # En una app real, aquí inicializarías tu conexión a la base de datos.
        self.canciones_db = [
            {"id": 1, "title": "Como la Flor", "artist": "Selena", "duration": "3:02", "genre": "Tejano"},
            {"id": 2, "title": "Me Porto Bonito", "artist": "Bad Bunny", "duration": "2:58", "genre": "Reggaeton"},
            {"id": 3, "title": "Save Your Tears", "artist": "The Weeknd", "duration": "3:35", "genre": "Pop"},
            {"id": 4, "title": "Blinding Lights", "artist": "The Weeknd", "duration": "3:20", "genre": "Synthwave"},
            {"id": 5, "title": "Thriller", "artist": "Michael Jackson", "duration": "5:57", "genre": "Pop"},
        ]

        self.artistas_db = [
            {"id": 1, "name": "The Weeknd", "image": "https://i.scdn.co/image/ab6761610000e5eb214f3db2420f7851066ed79c"},
            {"id": 2, "name": "Bad Bunny", "image": "https://i.scdn.co/image/ab6761610000e5eb9890157940e53655df02742d"},
            {"id": 3, "name": "Selena", "image": "https://i.scdn.co/image/ab6761610000e5eb0d45b533830852d2f704b2a8"},
        ]

    def search_songs(self, query: str):
        """
        Busca canciones cuyo título o artista coincida con la consulta.
        """
        if not query:
            return []
        
        query = query.lower()
        # Filtramos la lista buscando coincidencias en título o nombre del artista
        results = [
            song for song in self.canciones_db 
            if query in song['title'].lower() or query in song['artist'].lower()
        ]
        return results

    def search_artists(self, query: str):
        """
        Busca artistas cuyo nombre coincida con la consulta.
        """
        if not query:
            return []
        
        query = query.lower()
        results = [
            artist for artist in self.artistas_db 
            if query in artist['name'].lower()
        ]
        return results

    def get_song_details(self, song_id: int):
        """
        Obtiene la información completa de una canción por su ID.
        """
        return next((s for s in self.canciones_db if s['id'] == song_id), None)