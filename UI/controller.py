import flet as ft


class Controller:
    def __init__(self, view, model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model
        self._listYear = []
        self._listShape = []

    def fillDD(self):
        #StatesList = self._model.listStates
        SightingList = self._model.listSighting
        self._listShape = self._model.listShapes

        for n in SightingList:
            if n.datetime.year not in self._listYear:
                self._listYear.append(n.datetime.year)

        for a in self._listShape:
            self._view.ddshape.options.append(ft.dropdown.Option(a))
        for a in self._listYear:
            self._view.ddyear.options.append(ft.dropdown.Option(a))


        self._view.update_page()

    def handle_graph(self, e):
        a = self._view.ddyear.value
        s = self._view.ddshape.value

        self._model.buildGraph(s, a)
        self._view.txt_result.controls.append(ft.Text(f"Numero di vertici: {self._model.get_num_of_nodes()} Numero di archi: {self._model.get_num_of_edges()}"))


        for p in self._model.get_sum_weight_per_node():
             self._view.txt_result.controls.append(ft.Text(f"Nodo {p[0]}, somma pesi su archi ={p[1]}"))

        self._view.update_page()
    def handle_path(self, e):

        self._model.computePath()

        self._view.txtOut2.controls.append(ft.Text(
            f"Peso cammino massimo: {str(self._model.solBest)}"))

        for ii in self._model.path_edge:
            self._view.txtOut2.controls.append(ft.Text(
                f"{ii[0].id} --> {ii[1].id}: weight {ii[2]} distance {str(self._model.get_distance_weight(ii))}")) #ii[2]

        self._view.update_page()