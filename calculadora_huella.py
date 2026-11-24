"""Cálculo de la huella individual a partir del recibo bimestral."""

import math

from bimestre import Bimestre
from consumo_electrico import ConsumoElectrico
from factor_emision import FactorEmision
from resultado import Resultado
from vivienda import Vivienda

# Promedio residencial de referencia en México: 167 kWh/mes
# (consumo anual típico de aproximadamente 2000 kWh; 2000/12 da cerca de 167).
# El recibo de luz cubre un bimestre, así que la comparación usa 167 * Bimestre.MESES.
PROMEDIO_RESIDENCIAL_MEXICO_KWH = 167.0


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

    def recomendar(self, resultado: Resultado) -> str:
        promedio = self.promedio_bimestral_kwh()
        mensual = self.promedio_residencial_kwh()
        consumo = f"{resultado.consumo_total:.2f}"
        referencia = f"{promedio:.0f}"
        base = f"{mensual:.0f}"
        if resultado.consumo_total > promedio:
            return (
                "Recomendaciones de uso:\n"
                f"El consumo del recibo ({consumo} kWh en el bimestre) supera el promedio "
                f"residencial en México de {referencia} kWh por bimestre "
                f"({base} kWh/mes, unos 2000 kWh al año).\n"
                "- Iluminación LED: cambia focos incandescentes o fluorescentes.\n"
                "- Aire acondicionado: fíjalo cerca de 25 C y apágalo si la habitación queda vacía.\n"
                "- Standby: desconecta equipos que siguen consumiendo apagados.\n"
                "- Horarios: concentra el uso fuerte en menos horas y apaga lo que no se ocupa.\n"
                "- Electrodomésticos eficientes: prefiere equipos de bajo consumo."
            )
        return (
            "Recomendaciones de uso:\n"
            f"El consumo del recibo ({consumo} kWh en el bimestre) está en o por debajo del "
            f"promedio residencial en México de {referencia} kWh por bimestre "
            f"({base} kWh/mes, unos 2000 kWh al año).\n"
            "Mantener estos hábitos conserva la huella baja:\n"
            "- Sigue con iluminación LED.\n"
            "- Mantén moderado el aire acondicionado.\n"
            "- Evita dejar aparatos en standby.\n"
            "- Conserva horarios de uso cortos.\n"
            "- Sigue usando electrodomésticos eficientes."
        )
