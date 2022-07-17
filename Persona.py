class Persona :
    def __init__(self,edad, peso, altura, calorias) :
        self.edad = edad
        self.peso = peso
        self.altura = altura
        self.calorias = calorias

    def __repr__(self):
        return repr((self.edad, self.peso, self.altura, self.calorias)) 
