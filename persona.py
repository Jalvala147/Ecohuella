"""Habitante de una vivienda."""


class Persona:
    """Nombre, edad e identificación. No hay subtipos: todos cuentan igual en N."""

    def __init__(self, nombre: str, edad: int, identificacion: str) -> None:
        nombre = nombre.strip()
        identificacion = identificacion.strip()
        if not nombre:
            raise ValueError("El nombre no puede estar vacío.")
        if not isinstance(edad, int) or isinstance(edad, bool) or edad < 0 or edad > 130:
            raise ValueError("Edad inválida. Usa un número entre 0 y 130.")
        if not identificacion:
            raise ValueError("La identificación no puede estar vacía.")
        self._nombre = nombre
        self._edad = edad
        self._identificacion = identificacion

    @property
    def nombre(self) -> str:
        return self._nombre

    @property
    def edad(self) -> int:
        return self._edad

    @property
    def identificacion(self) -> str:
        return self._identificacion

    def mostrar(self) -> str:
        return f"{self.nombre}, {self.edad} años, identificación {self.identificacion}"
