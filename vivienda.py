"""Vivienda: asocia habitantes y posee sus consumos eléctricos."""

from consumo_electrico import ConsumoElectrico
from persona import Persona


class Vivienda:
    """Dirección del hogar.

    Asociación: guarda las mismas Persona que registra la aplicación; no las crea ni las destruye.
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
        if persona is None:
            return
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
        ok, motivo = consumo.es_valido()
        if not ok:
            raise ValueError(motivo)
        for existente in self._consumos:
            if existente.mes == consumo.mes and existente.anio == consumo.anio:
                raise ValueError("Ya existe un consumo registrado para ese mes y año.")
        self._consumos.append(consumo)

    def quitar_consumo(self, indice: int) -> None:
        if indice < 0 or indice >= len(self._consumos):
            raise ValueError("No hay un consumo en esa posición.")
        del self._consumos[indice]

    @property
    def consumos(self) -> tuple[ConsumoElectrico, ...]:
        return tuple(self._consumos)

    def comparar_consumos(self, promedio_kwh: float) -> str:
        if len(self._consumos) < 2:
            return "Se necesitan al menos dos consumos mensuales para comparar."

        ordenados = sorted(self._consumos, key=lambda consumo: (consumo.anio, consumo.mes))
        referencia = f"{promedio_kwh:.0f}"
        lineas = [
            f"Comparación de consumos mensuales (promedio residencial: {referencia} kWh/mes):"
        ]
        for indice, actual in enumerate(ordenados):
            diferencia_promedio = actual.kwh - promedio_kwh
            texto = actual.resumen()
            if indice > 0:
                delta = actual.kwh - ordenados[indice - 1].kwh
                texto += (
                    f" ({delta:+.2f} kWh respecto al mes anterior; "
                    f"{diferencia_promedio:+.2f} kWh frente al promedio)"
                )
            else:
                texto += f" ({diferencia_promedio:+.2f} kWh frente al promedio)"
            if actual.kwh > promedio_kwh:
                texto += " - por encima del promedio"
            else:
                texto += " - en o por debajo del promedio"
            lineas.append(texto)
        return "\n".join(lineas)
