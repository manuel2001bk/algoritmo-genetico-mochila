class Individuo:
    def __init__(self, lista_alimentos):
        self.lista_alimentos = lista_alimentos
        self.posicion_valido = 0
        self.lista_validos = []
        self.volumen = 0
        self.cantidad_calorias = 0
        self.peso = 0

    def calcular_volumen(self):
        for i in self.lista_validos:
            self.volumen += i.volumen
        return self.volumen

    def calcular_peso(self):
        for i in self.lista_validos:
            self.peso += i.peso
        return self.peso

    def calcular_cantidad_calorias(self):
        for i in self.lista_validos:
            self.cantidad_calorias += i.cantidad_calorias
        return self.cantidad_calorias

    def __repr__(self):
        return repr((self.lista_alimentos, self.volumen, self.posicion_valido, self.lista_validos,  self.cantidad_calorias , self.peso))
