# sistema_hotel.py

from abc import ABC, abstractmethod
import sqlite3
from datetime import datetime

# =======================
# BASE DE DATOS (SQLite)
# =======================
class ConexionBD:
    _conexion = None

    @staticmethod
    def obtener_conexion():
        if ConexionBD._conexion is None:
            ConexionBD._conexion = sqlite3.connect("hotel.db")
            ConexionBD._conexion.execute('''
                CREATE TABLE IF NOT EXISTS reservas (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    huesped TEXT,
                    tipo_habitacion TEXT,
                    numero INTEGER,
                    fecha_inicio TEXT,
                    fecha_fin TEXT
                )
            ''')
        return ConexionBD._conexion

# =======================
# OBSERVER
# =======================
class ObservadorReserva:
    def __init__(self, fecha_inicio, fecha_fin, huesped, habitacion):
        self.fecha_inicio = fecha_inicio
        self.fecha_fin = fecha_fin
        self.huesped = huesped
        self.habitacion = habitacion
        self.observadores = []

    def agregar_observador(self, obs):
        self.observadores.append(obs)

    def notificar_observadores(self):
        for obs in self.observadores:
            obs.recibe_notificacion(f"Reserva confirmada: {self.habitacion.numero} para {self.huesped.nombre}")

    def confirmar(self):
        conn = ConexionBD.obtener_conexion()
        conn.execute('''
            INSERT INTO reservas(huesped, tipo_habitacion, numero, fecha_inicio, fecha_fin)
            VALUES (?, ?, ?, ?, ?)
        ''', (
            self.huesped.nombre,
            self.habitacion.__class__.__name__,
            self.habitacion.numero,
            self.fecha_inicio,
            self.fecha_fin
        ))
        conn.commit()
        self.notificar_observadores()

class Huesped:
    def __init__(self, nombre, documento):
        self.nombre = nombre
        self.documento = documento

    def recibe_notificacion(self, msg):
        print(f"Notificación para {self.nombre}: {msg}")

# =======================
# FACTORY METHOD
# =======================
class HabitacionFactory:
    @staticmethod
    def crear_habitacion(tipo, numero):
        if tipo == "sencilla":
            return HabitacionSencilla(numero)
        elif tipo == "doble":
            return HabitacionDoble(numero)
        elif tipo == "triple":
            return HabitacionTriple(numero)
        elif tipo == "familiar":
            return HabitacionFamiliar(numero)
        else:
            raise ValueError("Tipo de habitación no válido")

# =======================
# CLASE ABSTRACTA Y HERENCIA
# =======================
class HabitacionAbstracta(ABC):
    def __init__(self, numero, capacidad, precio):
        self.numero = numero
        self.capacidad = capacidad
        self.precio = precio

    @abstractmethod
    def mostrar_info(self):
        pass

class HabitacionSencilla(HabitacionAbstracta):
    def __init__(self, numero):
        super().__init__(numero, 1, 100.0)

    def mostrar_info(self):
        return f"Sencilla #{self.numero} - Capacidad: {self.capacidad} - Precio: ${self.precio}"

class HabitacionDoble(HabitacionAbstracta):
    def __init__(self, numero):
        super().__init__(numero, 2, 180.0)

    def mostrar_info(self):
        return f"Doble #{self.numero} - Capacidad: {self.capacidad} - Precio: ${self.precio}"

class HabitacionTriple(HabitacionAbstracta):
    def __init__(self, numero):
        super().__init__(numero, 3, 250.0)

    def mostrar_info(self):
        return f"Triple #{self.numero} - Capacidad: {self.capacidad} - Precio: ${self.precio}"

class HabitacionFamiliar(HabitacionAbstracta):
    def __init__(self, numero):
        super().__init__(numero, 4, 320.0)

    def mostrar_info(self):
        return f"Familiar #{self.numero} - Capacidad: {self.capacidad} - Precio: ${self.precio}"

# =======================
# SINGLETON - HOTEL
# =======================
class Hotel:
    _instancia = None

    def __init__(self, nombre):
        self.nombre = nombre
        self.habitaciones = []

    @classmethod
    def get_instancia(cls, nombre="Mi Hotel"):
        if cls._instancia is None:
            cls._instancia = cls(nombre)
        return cls._instancia

    def agregar_habitacion(self, habitacion):
        self.habitaciones.append(habitacion)

    def mostrar_disponibles(self):
        for h in self.habitaciones:
            print(h.mostrar_info())

    def buscar_combinacion_habitaciones(self, cantidad_personas):
        return [h for h in self.habitaciones if h.capacidad >= cantidad_personas]

    def mostrar_info(self):
        print(f"Hotel: {self.nombre}")
        print(f"Total habitaciones: {len(self.habitaciones)}")

# =======================
# EJEMPLO DE USO
# =======================
if __name__ == "__main__":
    # Crear instancia única del hotel
    hotel = Hotel.get_instancia("Hotel Central")

    # Crear habitaciones con factory
    for i in range(1, 3):
        hotel.agregar_habitacion(HabitacionFactory.crear_habitacion("sencilla", i))
    hotel.agregar_habitacion(HabitacionFactory.crear_habitacion("doble", 3))
    hotel.agregar_habitacion(HabitacionFactory.crear_habitacion("familiar", 4))

    hotel.mostrar_info()
    hotel.mostrar_disponibles()

    # Crear huesped
    huesped = Huesped("Laura Moreno", "123456")

    # Hacer una reserva
    habitacion_reservada = hotel.habitaciones[0]
    reserva = ObservadorReserva("2025-08-01", "2025-08-05", huesped, habitacion_reservada)
    reserva.agregar_observador(huesped)
    reserva.confirmar()