"""Cálculo de la huella individual a partir del recibo bimestral."""

import math

from bimestre import Bimestre
from consumo_electrico import ConsumoElectrico
from factor_emision import FactorEmision
from resultado import Resultado
from vivienda import Vivienda

# Consumo promedio de electricidad por vivienda en México: 1,858.24 kWh al año (2019).
# Fuente: CONUEE, Base de Indicadores de Eficiencia Energética (BIEE), publicado por SEMARNAT
# en el Compendio de Estadísticas Ambientales 2021, "Consumo por vivienda" (kWh/vivienda):
# https://apps1.semarnat.gob.mx:8443/dgeia/compendio_2021/dgeiawf.semarnat.gob.mx_8080/ibi_apps/WFServletc953.html
# 1858.24 / 12 da 154.85 kWh/mes. El recibo cubre un bimestre: 154.85 * Bimestre.MESES = 309.71 kWh.
CONSUMO_ANUAL_VIVIENDA_MEXICO_KWH = 1858.24
PROMEDIO_RESIDENCIAL_MEXICO_KWH = CONSUMO_ANUAL_VIVIENDA_MEXICO_KWH / 12

# Promedio de ocupantes por vivienda en México: 3.6 personas.
# Fuente: INEGI, Censo de Población y Vivienda 2020, en "Estadísticas a propósito del Día
# Nacional de la Vivienda" (2023): https://www.inegi.org.mx/contenidos/saladeprensa/aproposito/2023/EAP_Vivienda.pdf
# Se usa para la huella promedio por persona: (309.71 / 3.6) * FE.
OCUPANTES_PROMEDIO_VIVIENDA_MEXICO = 3.6


class CalculadoraHuella:
    """Ci = Ct / N y HC = Ci * FE. Ct es el kWh del recibo bimestral.

    No divide si N es 0 o los kWh no son válidos. No guarda estado:
    cada cálculo recibe la vivienda, el recibo y el factor.
    """

    def calcular(
        self,
        vivienda: Vivienda,
        consumo: ConsumoElectrico,
        factor: FactorEmision,
    ) -> Resultado:
        consumo.validar()
        habitantes = vivienda.numero_habitantes()
        if habitantes == 0:
            raise ValueError(
                "No hay habitantes registrados (N = 0). No se puede calcular el consumo individual."
            )
        if not math.isfinite(factor.valor) or not factor.valor > 0:
            raise ValueError("El factor de emisión no es válido.")

        consumo_individual = consumo.kwh / habitantes
        kg_co2 = consumo_individual * factor.valor
        nombres = [persona.nombre for persona in vivienda.habitantes]
        return Resultado(
            kg_co2,
            consumo_individual,
            consumo.kwh,
            vivienda.direccion,
            consumo.bimestre,
            consumo.anio,
            habitantes,
            factor.valor,
            factor.anio,
            nombres,
        )

    def promedio_residencial_kwh(self) -> float:
        return PROMEDIO_RESIDENCIAL_MEXICO_KWH

    def promedio_bimestral_kwh(self) -> float:
        return self.promedio_residencial_kwh() * Bimestre.MESES

    def huella_promedio_persona_kg(self, factor: float) -> float:
        """Huella promedio por persona en un bimestre: (kWh promedio del recibo / 3.6) * FE."""
        return self.promedio_bimestral_kwh() / OCUPANTES_PROMEDIO_VIVIENDA_MEXICO * factor

    def recomendar(self, resultado: Resultado) -> str:
        promedio = self.promedio_bimestral_kwh()
        mensual = self.promedio_residencial_kwh()
        consumo = f"{resultado.consumo_total:.2f}"
        referencia = f"{promedio:.2f}"
        base = f"{mensual:.2f}"
        huella_promedio = self.huella_promedio_persona_kg(resultado.factor)
        comparacion_huella = (
            f"Tu huella individual es de {resultado.kg_co2:.2f} kg CO2e en el bimestre; "
            f"la huella promedio por persona en México es de {huella_promedio:.2f} kg CO2e "
            f"por bimestre (FE {resultado.factor:.3f}, {OCUPANTES_PROMEDIO_VIVIENDA_MEXICO} "
            "ocupantes por vivienda).\n"
        )
        if resultado.consumo_total > promedio:
            return (
                "Recomendaciones de uso:\n"
                f"El consumo del recibo ({consumo} kWh en el bimestre) supera el promedio "
                f"residencial en México de {referencia} kWh por bimestre "
                f"({base} kWh/mes, 1858.24 kWh al año según CONUEE).\n"
                + comparacion_huella
                + "- Iluminación LED: cambia focos incandescentes o fluorescentes.\n"
                "- Aire acondicionado: fíjalo cerca de 25 C y apágalo si la habitación queda vacía.\n"
                "- Standby: desconecta equipos que siguen consumiendo apagados.\n"
                "- Horarios: concentra el uso fuerte en menos horas y apaga lo que no se ocupa.\n"
                "- Electrodomésticos eficientes: prefiere equipos de bajo consumo."
            )
        return (
            "Recomendaciones de uso:\n"
            f"El consumo del recibo ({consumo} kWh en el bimestre) está en o por debajo del "
            f"promedio residencial en México de {referencia} kWh por bimestre "
            f"({base} kWh/mes, 1858.24 kWh al año según CONUEE).\n"
            + comparacion_huella
            + "Mantener estos hábitos conserva la huella baja:\n"
            "- Sigue con iluminación LED.\n"
            "- Mantén moderado el aire acondicionado.\n"
            "- Evita dejar aparatos en standby.\n"
            "- Conserva horarios de uso cortos.\n"
            "- Sigue usando electrodomésticos eficientes."
        )
