"""Resultado guardado de una huella ya calculada."""

from consumo_electrico import describir_periodo


class Resultado:
    """kg CO2e, consumo individual y el contexto para mostrarlo."""

    def __init__(
        self,
        kg_co2: float,
        consumo_individual: float,
        consumo_total: float,
        direccion: str,
        mes: int,
        anio: int,
        habitantes: int,
        factor: float,
        anio_factor: int,
        nombres: list[str],
    ) -> None:
        self._kg_co2 = float(kg_co2)
        self._consumo_individual = float(consumo_individual)
        self._consumo_total = float(consumo_total)
        self._direccion = direccion
        self._mes = int(mes)
        self._anio = int(anio)
        self._habitantes = int(habitantes)
        self._factor = float(factor)
        self._anio_factor = int(anio_factor)
        self._nombres = tuple(nombres)

    @property
    def kg_co2(self) -> float:
        return self._kg_co2

    @property
    def consumo_individual(self) -> float:
        return self._consumo_individual

    @property
    def consumo_total(self) -> float:
        return self._consumo_total

    @property
    def direccion(self) -> str:
        return self._direccion

    @property
    def mes(self) -> int:
        return self._mes

    @property
    def anio(self) -> int:
        return self._anio

    @property
    def habitantes(self) -> int:
        return self._habitantes

    @property
    def factor(self) -> float:
        return self._factor

    @property
    def anio_factor(self) -> int:
        return self._anio_factor

    @property
    def nombres(self) -> tuple[str, ...]:
        return self._nombres

    def resumen(self) -> str:
        return (
            f"{self.direccion} | {describir_periodo(self.mes, self.anio)}"
            f" | N={self.habitantes}"
            f" | Ci={self.consumo_individual:.2f} kWh"
            f" | HC={self.kg_co2:.2f} kg CO2e"
        )

    def mostrar(self) -> str:
        huella_vivienda = self.consumo_total * self.factor
        lineas = [
            f"Vivienda: {self.direccion}",
            f"Periodo: {describir_periodo(self.mes, self.anio)}",
            f"Consumo total (Ct): {self.consumo_total:.2f} kWh",
            f"Habitantes (N): {self.habitantes}",
            f"Consumo individual (Ci = Ct / N): {self.consumo_individual:.2f} kWh",
            f"Factor de emisión (FE): {self.factor:.3f} kg CO2e/kWh ({self.anio_factor})",
            f"Huella individual (HC = Ci * FE): {self.kg_co2:.2f} kg CO2e",
            f"Huella de la vivienda (Ct * FE): {huella_vivienda:.2f} kg CO2e",
            "Resultado por habitante:",
        ]
        if not self.nombres:
            lineas.append("- (sin nombres registrados)")
        else:
            for nombre in self.nombres:
                lineas.append(f"- {nombre}: {self.consumo_individual:.2f} kWh, {self.kg_co2:.2f} kg CO2e")
        return "\n".join(lineas)
