from cProfile import label
import math
import random
from random import randint, random as random_2

import matplotlib.pyplot as plt

from ventana_ui import *

from Persona import Persona
from Alimento import Alimento
from Mochila import Mochila
from Individuo import Individuo


class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self, *args, **kwargs):
        QtWidgets.QMainWindow.__init__(self, *args, **kwargs)
        self.setupUi(self)
        self.persona = 0
        self.mochila = 0
        self.lista_alimentos = []
        self.poblacion_max = 8
        self.poblacion_min = 4
        self.lista_individuos = []
        self.num_div = 0

        # botones calorias
        self.calorias_hombre_calcular.clicked.connect(
            self.obtener_calorias_hombre)
        self.calorias_mujer_calcular.clicked.connect(
            self.obtener_calorias_mujer)
        # botones alimentos
        self.registrar_alimento.clicked.connect(self.registrar_alimentos)
        # botones mochila
        self.mochila_buscar_opciones.clicked.connect(self.buscar_opciones)

    def generar_individuos(self):
        print("Lista de Alimentos: ", self.lista_alimentos)
        for i in range(self.poblacion_min):
            lista = self.lista_alimentos.copy()
            random.shuffle(lista)
            self.lista_individuos.append(Individuo(lista))
        print("Lista de individuos generados: ", self.lista_individuos)

    def calcular_volumen_calorias(self, lista):
        for i in lista:
            suma_calorias = 0
            suma_volumen = 0
            contador = 0
            for y in i.lista_alimentos:
                suma_calorias += y.calorias
                suma_volumen += y.volumen
                if suma_volumen < self.mochila.volumen and suma_calorias < self.persona.calorias:
                    i.cantidad_calorias = suma_calorias
                    i.volumen = suma_volumen
                    i.posicion_valido = contador
                contador += 1
        return lista

    def cal_div(self):
        self.num_div = len(self.lista_individuos)
        self.num_div = math.ceil(self.num_div/2)
        print("Numero de division 50% mejores: ", self.num_div)

    def crear_parejas(self):
        parejas = []
        for i in range(self.num_div):
            for y in range(i+1, len(self.lista_individuos)):
                print("PAREJAS: i = ", i, " : y = ", y)
                parejas.append(
                    [self.lista_individuos[i], self.lista_individuos[y]])
        print("Lista parejas: ", parejas)
        return parejas

    def get_hijo(self, puntos_cruza, padre1, padre2):
        hijo = []
        for i in range(puntos_cruza[0]):
            hijo.append(padre1.lista_alimentos[i])

        for i in range(puntos_cruza[0], puntos_cruza[1]):
            hijo.append(padre2.lista_alimentos[i])

        for i in range(puntos_cruza[1], len(padre1.lista_alimentos)):
            hijo.append(padre1.lista_alimentos[i])
        return Individuo(hijo)

    def comprobar_repetidos(self, hijo, padre):
        mylist = hijo.lista_alimentos
        resultant_list = []

        for element in mylist:
            if element not in resultant_list:
                resultant_list.append(element)
        mylist = resultant_list
        for element in padre.lista_alimentos:
            if element not in mylist:
                mylist.append(element)
        return mylist

    def generar_cruza(self, parejas):
        hijos = []
        for i in parejas:
            puntos_cruza = random.sample(
                range(1, len(self.lista_alimentos)-2), k=2)
            puntos_cruza = sorted(puntos_cruza)
            print("Puntos de cruza: ", puntos_cruza)
            padre1 = i[0]
            padre2 = i[1]

            hijo = self.get_hijo(puntos_cruza, padre1, padre2)
            print("Hijo 1: ", hijo)

            hijos.append(Individuo(self.comprobar_repetidos(hijo, padre2)))
            hijo = self.get_hijo(puntos_cruza, padre2, padre1)
            print("Hijo 1: ", hijo)
            hijos.append(Individuo(self.comprobar_repetidos(hijo, padre1)))
        return hijos

    def cal_prob(self, pors):
        probabilidad = random_2()
        if probabilidad < pors:
            return True
        else:
            return False

    def mutacion_genetica(self, hijo):
        for i in range(len(hijo.lista_alimentos)):
            if self.cal_prob(0.25):
                posicion = randint(i, len(hijo.lista_alimentos)-1)
                aux = hijo.lista_alimentos[i]
                hijo.lista_alimentos[i] = hijo.lista_alimentos[posicion]
                hijo.lista_alimentos[posicion] = aux
        return hijo

    def mutacion_ind(self, hijos):
        for i in hijos:
            if self.cal_prob(0.40):
                i = self.mutacion_genetica(i)
        return hijos

    def juntar_poblacion(self, hijos):
        print("Lista de hijos: ", len(hijos))
        for y in hijos:
            self.lista_individuos.append(y)

    def obtener_validos(self, lista):
        for i in lista:
            i.lista_validos = i.lista_alimentos[:i.posicion_valido]
        return lista

    def imprimir_tabla(self):
        data_tabla = []
        lista = []
        for i in self.lista_individuos:
            for y in i.lista_validos:
                lista.append(y.nombre)
            lista = sorted(lista)
            i.lista_validos = lista
            print("Lista validos: ", i.lista_validos)
            lista = []
        for i in range(3):
            data_tabla.append([self.lista_individuos[i].lista_validos, str(
                self.lista_individuos[i].cantidad_calorias), str(self.lista_individuos[i].volumen)])
        column_labels = ["Lista de alimentos", "Calorias", "Volumen"]
        plt.axis('tight')
        plt.axis('off')
        plt.table(cellText=data_tabla, colLabels=column_labels,loc="center" ,colColours=["yellow"] * 3).auto_set_font_size(False)
        plt.show()

    def algoritmo_genetico(self):
        self.generar_individuos()
        self.lista_individuos = self.calcular_volumen_calorias(
            self.lista_individuos)
        self.lista_individuos = sorted(
            self.lista_individuos, key=lambda genoma: genoma.cantidad_calorias, reverse=True)
        self.cal_div()
        for i in range(20):
            print("Generacion : ", i)
            parejas = self.crear_parejas()
            hijos = self.generar_cruza(parejas)
            hijos = self.mutacion_ind(hijos)
            print("Lista de hijos: ", hijos)
            hijos = self.calcular_volumen_calorias(hijos)
            self.juntar_poblacion(hijos)
            self.lista_individuos = sorted(
                self.lista_individuos, key=lambda genoma: genoma.cantidad_calorias, reverse=True)
            print("Lista de poblacion antes de poda:")
            print(self.lista_individuos)
            self.lista_individuos = self.lista_individuos[:self.poblacion_max]
            print("Lista de poblacion despues de poda:")
            print(self.lista_individuos)
            print("----------------------------------------------------")
        self.obtener_validos(self.lista_individuos)
        print("Lista de validos: ", self.lista_individuos)
        self.imprimir_tabla()

    def buscar_opciones(self):
        print("Buscando opciones")
        self.obtener_mochila()
        self.algoritmo_genetico()

    def obtener_mochila(self):
        self.texto_error_3.setText("")
        try:
            largo = float(self.mochila_largo.text())
            ancho = float(self.mochila_ancho.text())
            profundo = float(self.mochila_profundo.text())
            volumen = largo * ancho * profundo
            self.mochila = Mochila(largo, ancho, profundo, volumen)
        except ValueError:
            self.texto_error_3.setText("Error")
        print(self.mochila)

    def registrar_alimentos(self):
        print("Registrando Alimento")
        self.texto_error_2.setText("")
        try:
            cantidad = int(self.alimento_cantidad.text())
            nombre = self.alimento_nombre.text()
            calorias = float(self.alimento_calorias.text())
            peso = float(self.alimento_peso.text())
            largo = float(self.alimento_largo.text())
            ancho = float(self.alimento_ancho.text())
            profundidad = float(self.alimento_profundidad.text())

            for i in range(cantidad):
                alimento = Alimento(nombre + str(i), nombre,
                                    calorias, peso, largo, ancho, profundidad)
                alimento.calular_volumen()
                self.lista_alimentos.append(alimento)
            self.alimento_nombre.setText("")
            self.alimento_calorias.setText("")
            self.alimento_peso.setText("")
            self.alimento_largo.setText("")
            self.alimento_ancho.setText("")
            self.alimento_profundidad.setText("")
            print(self.lista_alimentos)
            auxtext = str(len(self.lista_alimentos))
            self.alimento_cant_registrados.setText(auxtext)
        except ValueError:
            self.texto_error.setText("Error")

    def obtener_calorias_hombre(self):
        print("Obteniendo calorias Hombre")
        # [66 + (13,7 × peso en kg) ] + [ (5 × altura en cm) – (6,8 × edad)] × Factor actividad.
        self.texto_error.setText("")
        try:
            peso = float(self.calorias_peso.text())
            altura = float(self.calorias_altura.text())
            edad = int(self.calorias_edad.text())
            calorias = 66 + (13.7 * peso) + (5 * altura) - (6.8 * edad) * 1.55
            self.persona = Persona(edad, peso, altura, calorias)
            auxtext = "\nCalorias Requeridas Hombre: " + \
                str(calorias) + "\n\npase a la pestaña Ingresar alimentos"
            self.calorias_label_calorias.setText(auxtext)
            self.calorias_hombre_calcular.setEnabled(False)
            self.calorias_mujer_calcular.setEnabled(False)
        except ValueError:
            self.texto_error.setText("Error")

    def obtener_calorias_mujer(self):
        print("Obteniendo calorias Mujer")
        self.texto_error.setText("")
        # [655 + (9,6 × peso en kg) ] + [ (1,8 × altura en cm) – (4,7 × edad)] × Factor actividad.
        try:
            peso = float(self.calorias_peso.text())
            altura = float(self.calorias_altura.text())
            edad = int(self.calorias_edad.text())
            calorias = 655 + (9.6 * peso) + (1.8 * altura) - \
                (4.7 * edad) * 1.55
            self.persona = Persona(edad, peso, altura, calorias)
            auxtext = "\nCalorias Requeridas Mujer: " + \
                str(calorias)+"\n\npase a la pestaña Ingresar alimentos"
            self.calorias_label_calorias.setText(auxtext)
            self.calorias_hombre_calcular.setEnabled(False)
            self.calorias_mujer_calcular.setEnabled(False)
        except ValueError:
            self.texto_error.setText("Error")


if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    window = MainWindow()
    window.show()
    app.exec_()
