"""Resultado de una huella ya calculada para un recibo bimestral."""

from bimestre import Bimestre


class LineaInforme:
    """Una línea del informe y el papel que cumple al mostrarla.

    El módulo de resultados usa el papel para resaltar las cifras.
    """

    ENCABEZADO = "encabezado"
    CONTEXTO = "contexto"
    RESULTADO = "resultado"
    ETIQUETA = "etiqueta"
    PERSONA = "persona"
    TITULO_RECOMENDACION = "titulo_recomendacion"
    RECOMENDACION = "recomendacion"
    ERROR = "error"
    AVISO = "aviso"
    SEPARADOR = "separador"

    def __init__(self, texto: str, rol: str) -> None:
        self._texto = texto
        self._rol = rol

    @property
    def texto(self) -> str:
        return self._texto

    @property
    def rol(self) -> str:
        return self._rol


class Resultado:
    """kg CO2e, consumo individual y el contexto para mostrarlo.

    Guarda copias de los datos usados en el cálculo. No conserva la Persona
    ni el FactorEmision: si después cambian los habitantes, este objeto
    sigue describiendo el cálculo que lo produjo.
    """

    def __init__(
        self,
        kg_co2: float,
        consumo_individual: float,
        consumo_total: float,
        direccion: str,
        bimestre: Bimestre,
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
        self._bimestre = Bimestre(bimestre.numero)
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
    def bimestre(self) -> Bimestre:
        return self._bimestre

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
            f"{self.direccion} | {self.bimestre.describir(self.anio)}"
            f" | N={self.habitantes}"
            f" | Ci={self.consumo_individual:.2f} kWh"
            f" | HC={self.kg_co2:.2f} kg CO2e"
        )

    def partes(self) -> tuple[LineaInforme, ...]:
        """Líneas del resultado. El rol dice cuáles son las cifras a resaltar."""
        huella_vivienda = self.consumo_total * self.factor
        lineas = [
            LineaInforme(f"Vivienda: {self.direccion}", LineaInforme.CONTEXTO),
            LineaInforme(f"Recibo: {self.bimestre.describir(self.anio)}", LineaInforme.CONTEXTO),
            LineaInforme(f"Consumo del recibo (Ct): {self.consumo_total:.2f} kWh", LineaInforme.CONTEXTO),
            LineaInforme(f"Habitantes (N): {self.habitantes}", LineaInforme.CONTEXTO),
            LineaInforme(
                f"Consumo individual (Ci = Ct / N): {self.consumo_individual:.2f} kWh",
                LineaInforme.RESULTADO,
            ),
            LineaInforme(
                f"Factor de emisión (FE): {self.factor:.3f} kg CO2e/kWh ({self.anio_factor})",
                LineaInforme.CONTEXTO,
            ),
            LineaInforme(
                f"Huella individual del bimestre (HC = Ci * FE): {self.kg_co2:.2f} kg CO2e",
                LineaInforme.RESULTADO,
            ),
            LineaInforme(
                f"Huella de la vivienda en el bimestre (Ct * FE): {huella_vivienda:.2f} kg CO2e",
                LineaInforme.RESULTADO,
            ),
            LineaInforme("Resultado por habitante:", LineaInforme.ETIQUETA),
        ]
        if not self.nombres:
            lineas.append(LineaInforme("(sin nombres registrados)", LineaInforme.CONTEXTO))
        else:
            for nombre in self.nombres:
                lineas.append(
                    LineaInforme(
                        f"{nombre}: {self.consumo_individual:.2f} kWh, {self.kg_co2:.2f} kg CO2e",
                        LineaInforme.PERSONA,
                    )
                )
        return tuple(lineas)

    def mostrar(self) -> str:
        return "\n".join(linea.texto for linea in self.partes())
