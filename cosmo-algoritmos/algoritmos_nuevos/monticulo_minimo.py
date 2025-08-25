class Nodo:
    def __init__(self, caracter=None, frecuencia=0):
        self.caracter = caracter
        self.frecuencia = frecuencia
        self.izquierda = None
        self.derecha = None

    def __lt__(self, otro):
        return self.frecuencia < otro.frecuencia

# Esta el algoritmo en pág 187 libro
class MonticuloMinimo:
    def __init__(self):
        self.datos = []

    def insertar(self, elemento):
        self.datos.append(elemento)
        self._subir(len(self.datos) - 1)

    def extraer_minimo(self):
        if len(self.datos) == 1:
            return self.datos.pop()
        raiz = self.datos[0]
        self.datos[0] = self.datos.pop()
        self._bajar(0)
        return raiz

    def __len__(self):
        return len(self.datos)

    def _subir(self, indice):
        padre = (indice - 1) // 2
        if indice > 0 and self.datos[indice] < self.datos[padre]:
            self.datos[indice], self.datos[padre] = self.datos[padre], self.datos[indice]
            self._subir(padre)

    def _bajar(self, indice):
        menor = indice
        izquierda = 2 * indice + 1
        derecha = 2 * indice + 2
        if izquierda < len(self.datos) and self.datos[izquierda] < self.datos[menor]:
            menor = izquierda
        if derecha < len(self.datos) and self.datos[derecha] < self.datos[menor]:
            menor = derecha
        if menor != indice:
            self.datos[indice], self.datos[menor] = self.datos[menor], self.datos[indice]
            self._bajar(menor)

a = MonticuloMinimo()

for i in range(11):
    a.insertar(i)

b = a.extraer_minimo()

print(a)