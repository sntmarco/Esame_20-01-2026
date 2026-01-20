from database.DB_connect import DBConnect
from model.artist import Artist

class DAO:

    @staticmethod
    def get_all_artists():

        conn = DBConnect.get_connection()
        result = []

        if conn is None:
            print("❌ Errore di connessione al database.")
            return None

        cursor = conn.cursor(dictionary=True)
        query = """
                SELECT *
                FROM artist a
                """
        cursor.execute(query)
        for row in cursor:
            artist = Artist(id=row['id'], name=row['name'])
            result.append(artist)
        cursor.close()
        conn.close()
        return result

    @staticmethod
    def get_artisti(n_alb):
        cnx = DBConnect.get_connection()
        result = []

        if cnx is None:
            print("❌ Errore di connessione al database.")
            return None

        cursor = cnx.cursor(dictionary=True)
        query = """
                select count(*) as num_album, al.artist_id, ar.name 
                from album al, artist ar
                where al.artist_id = ar.id 
                group by al.artist_id 
                having num_album >= %s
                """
        try:
            cursor.execute(query, (n_alb,))
            for row in cursor:
                artista = Artist(id=row['artist_id'], name=row['name'], num_album=row['num_album'])
                result.append(artista)

        except Exception as e:
            print(f"Errore durante la query get_artisti: {e}")
            result = None
        finally:
            cursor.close()
            cnx.close()
        return result


    @staticmethod
    def get_peso(artista):
        cnx = DBConnect.get_connection()
        result = []

        if cnx is None:
            print("❌ Errore di connessione al database.")
            return None

        cursor = cnx.cursor(dictionary=True)
        query = """
                select distinct genre_id
                from track 
                where album_id in (select id
                from album
                where artist_id = %s)
                """
        try:
            cursor.execute(query, (artista.id,))
            for row in cursor:
                genere = row['genre_id']
                result.append(genere)

        except Exception as e:
            print(f"Errore durante la query get_peso: {e}")
            result = None
        finally:
            cursor.close()
            cnx.close()
        return result
