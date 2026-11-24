"""Bimestre de un recibo de luz: dos meses consecutivos."""

from __future__ import annotations


class Bimestre:
    """Periodo bimestral del 1 (enero-febrero) al 6 (noviembre-diciembre).

    Es un valor: dos bimestres con el mismo número representan el mismo periodo.
    ConsumoElectrico y Resultado guardan cada uno su propia instancia.
    """

    MESES = 2
    _PERIODOS: tuple[tuple[int, int, str], ...] = (
        (1, 2, "enero-febrero"),
        (3, 4, "marzo-abril"),
        (5, 6, "mayo-junio"),
        (7, 8, "julio-agosto"),
        (9, 10, "septiembre-octubre"),
        (11, 12, "noviembre-diciembre"),
    )

    def __init__(self, numero: int) -> None:
        if isinstance(numero, bool) or not isinstance(numero, int) or not 1 <= numero <= 6:
            raise ValueError("Bimestre inválido: usa un número del 1 al 6.")
        self._numero = numero

    @property
    def numero(self) -> int:
        return self._numero

    @property
    def mes_inicio(self) -> int:
        return self._PERIODOS[self._numero - 1][0]

    @property
    def mes_fin(self) -> int:
        return self._PERIODOS[self._numero - 1][1]

    @property
    def nombre(self) -> str:
        return self._PERIODOS[self._numero - 1][2]

    def describir(self, anio: int) -> str:
        """Texto del periodo tal como se lee en el recibo, con el año."""
        return f"{self.nombre} {anio}"

    def opcion(self) -> str:
        return f"{self._numero} - {self.nombre}"

    def __eq__(self, otro: object) -> bool:
        return isinstance(otro, Bimestre) and self._numero == otro._numero

    def __hash__(self) -> int:
        return hash(self._numero)

    def __lt__(self, otro: Bimestre) -> bool:
        if not isinstance(otro, Bimestre):
            return NotImplemented
        return self._numero < otro._numero

    @classmethod
    def todos(cls) -> tuple[Bimestre, ...]:
        return tuple(cls(numero) for numero in range(1, len(cls._PERIODOS) + 1))

    @classmethod
    def opciones(cls) -> tuple[str, ...]:
        return tuple(bimestre.opcion() for bimestre in cls.todos())

    @classmethod
    def desde_texto(cls, texto: str) -> Bimestre | None:
        """Lee la opción del formulario, por ejemplo '2 - marzo-abril'."""
        limpio = texto.strip().lower()
        if not limpio:
            return None
        pieza = limpio.split("-", 1)[0].strip()
        try:
            numero = int(pieza)
        except ValueError:
            return None
        try:
            return cls(numero)
        except ValueError:
            return None
