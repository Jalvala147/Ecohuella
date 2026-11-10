"""Historial de resultados de la sesión. Solo vive en memoria."""

from resultado import Resultado


class Historial:
    """Guarda Resultado anteriores y permite consultarlos."""

    def __init__(self) -> None:
        self._registros: list[Resultado] = []

    def agregar(self, resultado: Resultado) -> None:
        self._registros.append(resultado)

    def consultar(self) -> tuple[Resultado, ...]:
        return tuple(self._registros)

    def consultar_periodo(self, mes: int, anio: int) -> tuple[Resultado, ...]:
        return tuple(
            registro for registro in self._registros if registro.mes == mes and registro.anio == anio
        )

    def mostrar(self) -> str:
        if not self._registros:
            return "El historial está vacío."
        lineas = [f"Historial de resultados ({len(self._registros)}):"]
        for indice, registro in enumerate(self._registros, start=1):
            lineas.append(f"{indice}. {registro.resumen()}")
        return "\n".join(lineas)
