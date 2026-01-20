import flet as ft
from UI.view import View
from model.model import Model
from database.DB_connect import DBConnect

class Controller:
    def __init__(self, view: View, model: Model):
        self._view = view
        self._model = model
        self.artisti = []

        self._connessione_db = DBConnect.get_connection()
        if self._connessione_db is None:
            self._view.show_alert("❌ Errore di connessione al database")

    def handle_create_graph(self, e):
        if self._connessione_db is None:
            self._view.show_alert("❌ Errore di connessione al database")

        n_alb = self._view.txtNumAlbumMin.value
        try:
            n_alb = int(n_alb)
        except (ValueError, TypeError):
            self._view.show_alert("Inserire il numero di album in un formato corretto")
            return
        if n_alb <= 0:
            self._view.show_alert("Inserire un numero di album maggiore di zero")
            return
        self.artisti = self._model.load_artists_with_min_albums(n_alb)
        nodi, archi = self._model.build_graph()
        self._view.txt_result.controls.clear()
        self._view.txt_result.controls.append(ft.Text(f"Grafo creato: {nodi} nodi (artisti), {archi} archi"))
        self._view.update_page()
        self.popola_dd()

    def popola_dd(self):
        self._view.ddArtist.options.clear()
        if self.artisti:
            for artista in self.artisti:
                self._view.ddArtist.options.append(ft.dropdown.Option(artista.id, f"{artista.name} ({artista.id})"))
        else:
            self._view.show_alert("Errore nel caricamento degli artisti.")
        self._view.ddArtist.disabled = False
        self._view.btnArtistsConnected.disabled = False
        self._view.txtMaxArtists.disabled = False
        self._view.txtMinDuration.disabled = False
        self._view.btnSearchArtists.disabled = False
        self._view.update_page()

    def handle_connected_artists(self, e):
        if self._connessione_db is None:
            self._view.show_alert("❌ Errore di connessione al database")

        self._view.txt_result.controls.clear()
        self.artista_selezionato = self._view.ddArtist.value
        artisti_collegati = self._model.get_artisti_collegati(self.artista_selezionato)
        self._model.peso_artisti_collegati(self.artista_selezionato, artisti_collegati)
        artisti_collegati = sorted(artisti_collegati, key=lambda x: [0])
        self._view.txt_result.controls.append(ft.Text(f"Artisti direttamente collegati all'artista {self.artista_selezionato}, {self._model.get_nome(self.artista_selezionato)} "))
        for artista in artisti_collegati:
            peso = self._model.G[self.artista_selezionato][artista]['weight']
            self._view.txt_result.controls.append(ft.Text(f"{artista}, {self._model.get_nome(artista)} - Numero di generi in comune {peso}"))

        self._view.update_page()

    def ricorsione(self, e):
        n_art = self._view.txtMaxArtists.value
        d_min = self._view.txtMinDuration.value
        try:
            d_min = float(d_min)
            n_art = int(n_art)
        except (ValueError, TypeError):
            self._view.show_alert("Inserire i valori in un formato corretto")
            return
        if n_art not in range(1, len(self.artisti) + 1):
            self._view.show_alert(f"Inserire un numero di artisti compreso tra 1 e {len(self.artisti)}")
            return
        if d_min <= 0:
            self._view.show_alert(f"Inserire un numero maggiore di zero")
            return

        self._model.calcola_percorso_ottimo(self.artista_selezionato, d_min, n_art)
        self._view.txt_result.controls.clear()


