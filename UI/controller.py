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
        anno = self._model.anno
        for a in anno:
            self._view.ddyear.options.append(ft.dropdown.Option(data=a,
                                                                text=a,
                                                                on_click=self.choiceAnno))
        shape = self._model.shape
        for s in shape:
            self._view.ddshape.options.append(ft.dropdown.Option(data=s,
                                                                 text=s,
                                                                 on_click=self.choiceShape))
        self._view.update_page()
    def choiceAnno(self, e):
        if e.control.data is None:
            self.anno = None
        else:
            self.anno = e.control.data

    def choiceShape(self,e ):
        if e.control.data is None:
            self.shape = None
        else:
            self.shape = e.control.data


    def handle_graph(self, e):
        self._model.buildGraph(self.anno, self.shape)
        nodi, archi = self._model.graph_details()

        self._view.txt_result.controls.append(ft.Text(f"Numero di vertici: {nodi}, Numero di archi: {archi}"))
        peso = self._model.sumPeso(self.anno, self.shape)
        for p in peso:
            self._view.txt_result.controls.append(ft.Text(f"Nodo: {p[0]} somma pesi su archi: {p[1]}"))

        self._view.update_page()



    def handle_path(self, e):
        self._model.computePath()

        self._view.txtOut2.controls.append(ft.Text(
            f"Peso cammino massimo: {str(self._model.solBest)}"))

        for ii in self._model.path_edge:
            self._view.txtOut2.controls.append(ft.Text(
                f"{ii[0].id} --> {ii[1].id}: weight {ii[2]} distance {str(self._model.get_distance_weight(ii))}"))  # ii[2]

        self._view.update_page()