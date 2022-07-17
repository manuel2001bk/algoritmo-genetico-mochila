class Mochila :
    def __init__(self,largo,ancho,profundo,volumen) :
        self.largo = largo
        self.ancho = ancho
        self.profundo = profundo
        self.volumen = volumen

    def __repr__(self):
        return repr((self.largo, self.ancho, self.profundo, self.volumen)) 
