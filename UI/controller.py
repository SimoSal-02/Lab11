import flet as ft


class Controller:
    def __init__(self, view, model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model
        self._listYear = [2015,2016,2017,2018]
        self._listColor = self._model.getColor()
        self._color = None
        self._year = None
        self._p = None

    def fillDD(self):
        myOptYear=list(map(lambda x: ft.dropdown.Option(x), self._listYear))
        self._view._ddyear.options=myOptYear
        myOptColor = list(map(lambda x: ft.dropdown.Option(x),self._model.getColor()))
        self._view._ddcolor.options = myOptColor

    def handle_graph(self, e):
        self._view.txtOut.controls.clear()
        nNodi,lista=self._model.creaGrafo(self._color,self._year)
        self._view.txtOut.controls.append(ft.Text(f"Numero di nodi: {nNodi} Numero archi: {len(lista)}"))
        if len(lista) > 3:
            self._view.txtOut.controls.append(
                ft.Text(f"Arco da {lista[0][0]} a {lista[0][1]}, peso= {lista[0][2]['weight']}"))
            self._view.txtOut.controls.append(
                ft.Text(f"Arco da {lista[1][0]} a {lista[1][1]}, peso= {lista[1][2]['weight']}"))
            self._view.txtOut.controls.append(
                ft.Text(f"Arco da {lista[2][0]} a {lista[2][1]}, peso= {lista[2][2]['weight']}"))
            mappaRip={}
            for i in lista[:3]:
                if i[0].Product_number in mappaRip:
                    mappaRip[i[0].Product_number]+=1
                else:
                    mappaRip[i[0].Product_number] = 1
                if i[1].Product_number in mappaRip:
                    mappaRip[i[1].Product_number]+=1
                else:
                    mappaRip[i[1].Product_number] = 1
            result=[]
            for k,v in mappaRip.items():
                if v >1:
                    result.append(k)
            self._view.txtOut.controls.append(
                ft.Text(f"I nodi ripetuti sono {result}"))
            self.fillDDProduct()

        self._view.update_page()


    def fillDDProduct(self):
        myOptNodes = list(map(lambda x: ft.dropdown.Option(x),self._model.getNodes()))
        self._view._ddnode.options = myOptNodes
        self._view.update_page()


    def handle_search(self, e):
        self._view.txtOut2.controls.append(
            ft.Text(f"Numero archi percorso più lungo: {self._model.bestPath(self._p)}"))
        self._view.update_page()

    def readY(self,e):
        self._year = self._view._ddyear.value
        print(self._year)
    def readC(self,e):
        self._color = self._view._ddcolor.value
        print(self._color)

    def readP(self,e):
        self._p= self._view._ddnode.value
        print(self._p)

