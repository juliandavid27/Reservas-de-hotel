from itertools import combinations
from abc import ABC, abstractmethod
from datetime import datetime

# Clase abstracta para habitaciones
class HabitacionAbstracta(ABC):
    def __init__(self, numero, capacidad, precio, tipo):
        self.numero = numero
        self.capacidad = capacidad
        self.precio = precio
        self.tipo = tipo
        self.disponible = True

    @abstractmethod
    def mostrar_info(self):
        pass

# Subclases de habitaciones
class HabitacionSencilla(HabitacionAbstracta):
    def __init__(self, numero):
        super().__init__(numero, 1, 80000, "Sencilla")

    def mostrar_info(self):
        return f"[Sencilla] Habitacion {self.numero} - Capacidad: {self.capacidad} - Precio: ${self.precio}"

class HabitacionDoble(HabitacionAbstracta):
    def __init__(self, numero):
        super().__init__(numero, 2, 120000, "Doble")

    def mostrar_info(self):
        return f"[Doble] Habitacion {self.numero} - Capacidad: {self.capacidad} - Precio: ${self.precio}"

class HabitacionTriple(HabitacionAbstracta):
    def __init__(self, numero):
        super().__init__(numero, 3, 160000, "Triple")

    def mostrar_info(self):
        return f"[Triple] Habitacion {self.numero} - Capacidad: {self.capacidad} - Precio: ${self.precio}"

class HabitacionFamiliar(HabitacionAbstracta):
    def __init__(self, numero):
        super().__init__(numero, 5, 200000, "Familiar")

    def mostrar_info(self):
        return f"[Familiar] Habitacion {self.numero} - Capacidad: {self.capacidad} - Precio: ${self.precio}"

# Patrón Factory (centralia la creación de habitaciones)
class HabitacionFactory:
    @staticmethod
    def crear_habitacion(tipo, numero):
        if tipo == "Sencilla":
            return HabitacionSencilla(numero)
        elif tipo == "Doble":
            return HabitacionDoble(numero)
        elif tipo == "Triple":
            return HabitacionTriple(numero)
        elif tipo == "Familiar":
            return HabitacionFamiliar(numero)
        else:
            raise ValueError("Tipo de habitación inválido.")

# Clase Singleton para Hotel (solo una instancia)
class Hotel:
    _instancia = None

    def __init__(self, nombre):
        self.nombre = nombre
        self.habitaciones = []

    @classmethod
    def get_instancia(cls, nombre="Hotel Central"):
        if cls._instancia is None:
            cls._instancia = cls(nombre)
        return cls._instancia

    def agregar_habitacion(self, habitacion):
        self.habitaciones.append(habitacion)

    def mostrar_disponibles(self):
        return [h for h in self.habitaciones if h.disponible]

    def buscar_habitaciones(self, cantidad):
        disponibles = self.mostrar_disponibles()
        for r in range(1, len(disponibles) + 1):
            for combo in combinations(disponibles, r):
                if sum(h.capacidad for h in combo) >= cantidad:
                    return combo
        return None

# Clase Observer - para Huesped (reserva notifica a los huespedes)
class Huesped:
    def __init__(self, nombre, documento, email="", telefono=""):
        self.nombre = nombre
        self.documento = documento
        self.email = email
        self.telefono = telefono

    def recibir_notificacion(self, mensaje):
        print(f"Notificación a {self.nombre}: {mensaje}")

# Clase Reserva que notifica a los huéspedes (conectado con Observer)
class Reserva:
    def __init__(self, fecha_inicio, fecha_fin, huesped, habitaciones):
        self.fecha_inicio = fecha_inicio
        self.fecha_fin = fecha_fin
        self.huesped = huesped
        self.habitaciones = habitaciones
        self.observadores = []

    def agregar_observador(self, obs):
        self.observadores.append(obs)

    def notificar_observadores(self, mensaje):
        for obs in self.observadores:
            obs.recibir_notificacion(mensaje)

    def confirmar(self):
        for h in self.habitaciones:
            h.disponible = False
        self.notificar_observadores("Reserva confirmada.")

# Función de reserva con interacción
def reservar():
    hotel = Hotel.get_instancia()
    print("\n--- Registro de huésped ---")
    nombre = input("Nombre del huésped: ")
    doc = input("Documento: ")
    email = input("Email (opcional): ")
    tel = input("Teléfono (opcional): ")
    huesped = Huesped(nombre, doc, email, tel)

    try:
        cantidad = int(input("Cantidad de personas a hospedar: "))
        sugeridas = hotel.buscar_habitaciones(cantidad)
        if sugeridas:
            print("\nHabitaciones sugeridas:")
            total = 0
            for h in sugeridas:
                print(" -", h.mostrar_info())
                total += h.precio
            print(f"Total por noche: ${total}")
            confirmar = input("¿Confirmar reserva? (s/n): ").lower()
            if confirmar == 's':
                reserva = Reserva(datetime.now(), None, huesped, sugeridas)
                reserva.agregar_observador(huesped)
                reserva.confirmar()
                print("Reserva confirmada con éxito.")
            else:
                print("Reserva cancelada.")
        else:
            print("No hay habitaciones suficientes disponibles.")
    except ValueError:
        print("Cantidad inválida.")

def mostrar_habitaciones_disponibles():
    hotel = Hotel.get_instancia()
    disponibles = hotel.mostrar_disponibles()
    print("\nHabitaciones disponibles:")
    for h in disponibles:
        print(" -", h.mostrar_info())

def cargar_habitaciones():
    hotel = Hotel.get_instancia()
    tipos = [("Sencilla", 2), ("Doble", 2), ("Triple", 2), ("Familiar", 2)]
    contador = 1
    for tipo, cantidad in tipos:
        for _ in range(cantidad):
            hab = HabitacionFactory.crear_habitacion(tipo, contador)
            hotel.agregar_habitacion(hab)
            contador += 1

def menu():
    cargar_habitaciones()
    while True:
        print("\n--- MENÚ ---")
        print("1. Ver habitaciones disponibles")
        print("2. Realizar una reserva")
        print("3. Salir")
        opcion = input("Seleccione una opción: ")
        if opcion == "1":
            mostrar_habitaciones_disponibles()
        elif opcion == "2":
            reservar()
        elif opcion == "3":
            print("Gracias por usar el sistema.")
            break
        else:
            print("Opción inválida.")

menu()