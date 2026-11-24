"""Recibo de luz bimestral: kWh del periodo que factura la compañía."""

from __future__ import annotations

import math

from bimestre import Bimestre


class ConsumoElectrico:
    """kWh, bimestre y año de un recibo. Lo posee la vivienda por composición.

    El bimestre también es composición: el periodo forma parte del recibo
    y no se comparte con otro consumo.
    """

    def __init__(self, kwh: float, bimestre: Bimestre, anio: int) -> None:
        if isinstance(kwh, bool) or not isinstance(kwh, (int, float)):
            raise ValueError("Consumo inválido: los kWh del recibo deben ser un número mayor que cero.")
        if not isinstance(bimestre, Bimestre):
            raise TypeError("El periodo del recibo debe ser un Bimestre.")
        if isinstance(anio, bool) or not isinstance(anio, int):
            raise ValueError("Año inválido: usa un valor entre 1990 y 2100.")
        self._kwh = float(kwh)
        self._bimestre = bimestre
        self._anio = anio

    @property
    def kwh(self) -> float:
        return self._kwh

    @property
    def bimestre(self) -> Bimestre:
        return self._bimestre

    @property
    def anio(self) -> int:
        return self._anio

    def validar(self) -> None:
        if not math.isfinite(self._kwh) or not self._kwh > 0:
            raise ValueError("Consumo inválido: los kWh del recibo deben ser mayores que cero.")
        if self._anio < 1990 or self._anio > 2100:
            raise ValueError("Año inválido: usa un valor entre 1990 y 2100.")

    def mismo_periodo(self, otro: ConsumoElectrico) -> bool:
        return self._anio == otro.anio and self._bimestre == otro.bimestre

    def periodo(self) -> str:
        return self._bimestre.describir(self._anio)

    def resumen(self) -> str:
        return f"{self.periodo()}: {self._kwh:.2f} kWh"
