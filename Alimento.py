class Alimento:
    def __init__(self, id, nombre, calorias, peso, largo, ancho, profundidad):
        self.id = id
        self.nombre = nombre
        self.calorias = calorias
        self.peso = peso
        self.largo = largo
        self.ancho = ancho
        self.profundidad = profundidad
        self.volumen = 0

    def calular_volumen(self):
        self.volumen = self.largo * self.ancho * self.profundidad

    def __repr__(self):
        return repr((self.id, self.nombre, self.calorias, self.peso, self.largo, self.ancho, self.profundidad, self.volumen))
