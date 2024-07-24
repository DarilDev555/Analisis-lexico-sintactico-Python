class Nodo:
    def __init__(self, dato):
        self.dato = dato
        self.siguiente = None

class ListaLigadaCircular:
    def __init__(self):
        self.cabeza = None

    def agregar(self, dato):
        nuevo_nodo = Nodo(dato)
        if not self.cabeza:
            self.cabeza = nuevo_nodo
            self.cabeza.siguiente = self.cabeza
        else:
            temp = self.cabeza
            while temp.siguiente != self.cabeza:
                temp = temp.siguiente
            temp.siguiente = nuevo_nodo
            nuevo_nodo.siguiente = self.cabeza

    def mostrar(self):
        nodos = []
        temp = self.cabeza
        if temp:
            while True:
                nodos.append(temp.dato)
                temp = temp.siguiente
                if temp == self.cabeza:
                    break
        print(" -> ".join(map(str, nodos)))
