"""Factor de emisión eléctrico: kg CO2e por cada kWh."""

import math

# Factor de emisión de referencia: 0.444 kg CO2e/kWh (México, 2024).
FACTOR_MEXICO_2024 = 0.444
ANIO_FACTOR_MEXICO = 2024


class FactorEmision:
    """Guarda el factor y el año. El valor inicial es el de México 2024."""

    def __init__(self, factor: float = FACTOR_MEXICO_2024, anio: int = ANIO_FACTOR_MEXICO) -> None:
        self._factor = float(factor)
        self._anio = int(anio)

    @property
    def valor(self) -> float:
        return self._factor

    @property
    def anio(self) -> int:
        return self._anio

    def actualizar(self, factor: float, anio: int) -> None:
        if not math.isfinite(factor) or not factor > 0:
            raise ValueError("El factor de emisión debe ser mayor que cero.")
        if anio < 1990 or anio > 2100:
            raise ValueError("Año del factor inválido: usa un valor entre 1990 y 2100.")
        self._factor = float(factor)
        self._anio = int(anio)
