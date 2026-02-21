from src.models.postgres import PostgresConnector

def obtener_playlist_detallada():
    db = PostgresConnector()
    # Usamos JOIN para traer el nombre del artista desde su tabla
    query = """
        SELECT 
            c.id, 
            c.titulo, 
            a.nombre AS artista, 
            al.nombre AS album,
            c.duracion_segundos, 
            c.ruta_archivo 
        FROM canciones c
        LEFT JOIN artistas a ON c.artista_id = a.id
        LEFT JOIN albumes al ON c.album_id = al.id
        ORDER BY c.fecha_agregada DESC;
    """
    
    resultados = db.execute_query(query)
    return resultados if resultados else []