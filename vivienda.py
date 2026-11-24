"""Vivienda: asocia habitantes y posee sus recibos de luz."""

from consumo_electrico import ConsumoElectrico
from persona import Persona


class Vivienda:
    """Dirección del hogar.

    Asociación: guarda las mismas Persona que crea la sesión; no las crea ni las destruye.
    Composición: los ConsumoElectrico viven en esta lista y desaparecen con la vivienda.
    """

    def __init__(self, direccion: str) -> None:
        direccion = direccion.strip()
        if not direccion:
            raise ValueError("La dirección no puede estar vacía.")
        self._direccion = direccion
        self._habitantes: list[Persona] = []
        self._consumos: list[ConsumoElectrico] = []

    @property
    def direccion(self) -> str:
        return self._direccion

    def agregar_habitante(self, persona: Persona) -> None:
        if not isinstance(persona, Persona):
            raise TypeError("Se esperaba una Persona.")
        self._habitantes.append(persona)

    def quitar_habitante(self, persona: Persona) -> None:
        self._habitantes = [actual for actual in self._habitantes if actual is not persona]

    def desasociar_habitantes(self) -> None:
        """Quita la asociación. Las Persona siguen existiendo fuera de la vivienda."""
        self._habitantes.clear()

    def numero_habitantes(self) -> int:
        return len(self._habitantes)

    @property
    def habitantes(self) -> tuple[Persona, ...]:
        return tuple(self._habitantes)

    def agregar_consumo(self, consumo: ConsumoElectrico) -> None:
        if not isinstance(consumo, ConsumoElectrico):
            raise TypeError("Se esperaba un ConsumoElectrico.")
        consumo.validar()
        for existente in self._consumos:
            if existente.mismo_periodo(consumo):
                raise ValueError("Ya existe un recibo registrado para ese bimestre y año.")
        self._consumos.append(consumo)

    def quitar_consumo(self, indice: int) -> None:
        if indice < 0 or indice >= len(self._consumos):
            raise ValueError("No hay un recibo en esa posición.")
        del self._consumos[indice]

    @property
    def consumos(self) -> tuple[ConsumoElectrico, ...]:
        return tuple(self._consumos)

    def comparar_consumos(self, promedio_kwh: float) -> str:
        if len(self._consumos) < 2:
            return "Se necesitan al menos dos recibos bimestrales para comparar."

        ordenados = sorted(self._consumos, key=lambda consumo: (consumo.anio, consumo.bimestre))
        referencia = f"{promedio_kwh:.0f}"
        lineas = [
            f"Comparación de consumos bimestrales (promedio del recibo: {referencia} kWh/bimestre):"
        ]
        anterior: ConsumoElectrico | None = None
        for actual in ordenados:
            lineas.append(self._describir_contra_promedio(actual, promedio_kwh, anterior))
            anterior = actual
        return "\n".join(lineas)

    def _describir_contra_promedio(
        self,
        actual: ConsumoElectrico,
        promedio_kwh: float,
        anterior: ConsumoElectrico | None,
    ) -> str:
        diferencia = actual.kwh - promedio_kwh
        texto = actual.resumen()
        if anterior is None:
            texto += f" ({diferencia:+.2f} kWh frente al promedio)"
        else:
            delta = actual.kwh - anterior.kwh
            texto += (
                f" ({delta:+.2f} kWh respecto al bimestre anterior; "
                f"{diferencia:+.2f} kWh frente al promedio)"
            )
        if actual.kwh > promedio_kwh:
            texto += " - por encima del promedio"
        else:
            texto += " - en o por debajo del promedio"
        return texto
