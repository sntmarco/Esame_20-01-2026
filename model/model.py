import networkx as nx
from database.dao import DAO

class Model:
    def __init__(self):
        self.G = nx.Graph()
        self._artists_list = []
        self.artisti = []
        #self.load_all_artists()

    def load_all_artists(self):
        self._artists_list = DAO.get_all_artists()
        print(f"Artisti: {self._artists_list}")

    def load_artists_with_min_albums(self, min_albums):
        self.artisti = DAO.get_artisti(min_albums)
        return self.artisti

    def build_graph(self):
        self.G.clear()
        for a1 in self.artisti:
            for a2 in self.artisti:
                if a1 != a2:
                    genere1 = set(DAO.get_peso(a1))
                    genere2 = set(DAO.get_peso(a2))
                    intersezione = genere1.intersection(genere2)
                    peso = len(intersezione)
                    if peso != 0:
                        self.G.add_edge(str(a1.id), str(a2.id), weight = peso)
                    print(a1, a2, peso)
        return self.G.number_of_nodes(), self.G.number_of_edges()

    def get_artisti_collegati(self, artista_selezionato):
        artisti_collegati = self.G.neighbors(artista_selezionato)
        return list(artisti_collegati)

    def peso_artisti_collegati(self, artista_selezionato, artisti_collegati):
        artisti_collegati = sorted(artisti_collegati, key=lambda x: [0])
        for artista in artisti_collegati:
            peso = self.G[artista_selezionato][artista]['weight']

    def get_nome(self, id):
        conversione = id
        print(id)
        for artista in self.artisti:
            if int(id) == artista.id:
                conversione = artista.name
        return conversione


    def calcola_percorso_ottimo(self, start, durata_min, L):
            self.best_solution = []
            self.best_value = float("inf")

            for nodo in self.G.nodes():
                self._ricorsione(
                    parziale=[start],
                    visitati={nodo},
                    valore_corrente=0,
                    L= L,
                    durata_min = durata_min,
                )
            return self.best_solution, self.best_value

    def _ricorsione(self, parziale, visitati, valore_corrente, L, durata_min):

        if valore_corrente < self.best_value and len(parziale) == L:
            self.best_value = valore_corrente
            self.best_solution = parziale[:]

        nodo_corrente = parziale[-1]

        for vicino in self.G.neighbors(nodo_corrente):

            if vicino in visitati:
                continue

            peso = self.G[nodo_corrente][vicino]["weight"]

            if durata_min <= peso:
                continue

            parziale.append(vicino)
            visitati.add(vicino)

            self._ricorsione(
                parziale,
                visitati,
                valore_corrente + peso,
                peso,
                durata_min,

            )

            visitati.remove(vicino)
            parziale.pop()
