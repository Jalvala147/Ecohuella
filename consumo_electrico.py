"""Registro mensual de consumo eléctrico, en kWh."""

import math

NOMBRES_MES = (
    "",
    "enero",
    "febrero",
    "marzo",
    "abril",
    "mayo",
    "junio",
    "julio",
    "agosto",
    "septiembre",
    "octubre",
    "noviembre",
    "diciembre",
)


def describir_periodo(mes: int, anio: int) -> str:
    if mes < 1 or mes > 12:
        return f"periodo inválido {anio}"
    return f"{NOMBRES_MES[mes]} {anio}"


class ConsumoElectrico:
    """kWh, mes y año de un recibo. Lo posee la vivienda por composición."""

    def __init__(self, kwh: float, mes: int, anio: int) -> None:
        self._kwh = float(kwh)
        self._mes = int(mes)
        self._anio = int(anio)

    @property
    def kwh(self) -> float:
        return self._kwh

    @property
    def mes(self) -> int:
        return self._mes

    @property
    def anio(self) -> int:
        return self._anio

    def es_valido(self) -> tuple[bool, str]:
        if not math.isfinite(self._kwh) or not self._kwh > 0:
            return False, "Consumo inválido: los kWh deben ser mayores que cero."
        if self._mes < 1 or self._mes > 12:
            return False, "Mes inválido: usa un número del 1 al 12."
        if self._anio < 1990 or self._anio > 2100:
            return False, "Año inválido: usa un valor entre 1990 y 2100."
        return True, ""

    def periodo(self) -> str:
        return describir_periodo(self._mes, self._anio)

    def resumen(self) -> str:
        return f"{self.periodo()}: {self._kwh:.2f} kWh"
