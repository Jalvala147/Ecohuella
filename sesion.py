"""Sesión de trabajo: vivienda, habitantes, recibos y cálculos en memoria."""

from bimestre import Bimestre
from calculadora_huella import CalculadoraHuella
from consumo_electrico import ConsumoElectrico
from factor_emision import FactorEmision
from persona import Persona
from resultado import LineaInforme, Resultado
from vivienda import Vivienda


class Sesion:
    """Dueña del estado mientras la ventana está abierta. No escribe archivos.

    Composición: crea la Vivienda, el FactorEmision y la CalculadoraHuella.
    Composición de la lista de Persona: la sesión las crea.
    Asociación: la vivienda guarda esas mismas Persona, sin copiarlas.
    Los ConsumoElectrico se crean aquí y pasan a ser parte de la vivienda.
    """

    def __init__(self) -> None:
        self._personas: list[Persona] = []
        self._vivienda: Vivienda | None = None
        self._factor = FactorEmision()
        self._calculadora = CalculadoraHuella()

    @property
    def vivienda(self) -> Vivienda | None:
        return self._vivienda

    @property
    def factor(self) -> FactorEmision:
        return self._factor

    @property
    def calculadora(self) -> CalculadoraHuella:
        return self._calculadora

    @property
    def personas(self) -> tuple[Persona, ...]:
        return tuple(self._personas)

    def exigir_vivienda(self) -> Vivienda:
        if self._vivienda is None:
            raise ValueError("Primero registra una vivienda.")
        return self._vivienda

    def registrar_vivienda(self, direccion: str) -> bool:
        """Crea la vivienda. Devuelve True si reemplazó a una anterior.

        La dirección se valida antes de tocar los datos ya capturados.
        """
        nueva = Vivienda(direccion)
        habia = self._vivienda is not None
        if self._vivienda is not None:
            self._vivienda.desasociar_habitantes()
        self._personas.clear()
        self._vivienda = nueva
        return habia

    def agregar_habitante(self, nombre: str, edad: int, identificacion: str) -> Persona:
        vivienda = self.exigir_vivienda()
        persona = Persona(nombre, edad, identificacion)
        self._personas.append(persona)
        vivienda.agregar_habitante(persona)
        return persona

    def quitar_habitante(self, indice: int) -> None:
        vivienda = self.exigir_vivienda()
        habitantes = vivienda.habitantes
        if indice < 0 or indice >= len(habitantes):
            raise ValueError("Selecciona un habitante.")
        persona = habitantes[indice]
        vivienda.quitar_habitante(persona)
        self._personas = [actual for actual in self._personas if actual is not persona]

    def registrar_consumo(self, kwh: float, bimestre: Bimestre, anio: int) -> ConsumoElectrico:
        vivienda = self.exigir_vivienda()
        consumo = ConsumoElectrico(kwh, bimestre, anio)
        vivienda.agregar_consumo(consumo)
        return consumo

    def quitar_consumo(self, indice: int) -> None:
        vivienda = self.exigir_vivienda()
        vivienda.quitar_consumo(indice)

    def calcular_en(self, indice: int) -> tuple[Resultado, str]:
        vivienda = self.exigir_vivienda()
        consumos = vivienda.consumos
        if not consumos:
            raise ValueError("No hay recibos registrados.")
        if indice < 0 or indice >= len(consumos):
            raise ValueError("Selecciona un recibo.")
        resultado = self._calculadora.calcular(vivienda, consumos[indice], self._factor)
        return resultado, self._calculadora.recomendar(resultado)

    def lineas_resultados(self) -> tuple[LineaInforme, ...]:
        """Informe de cada recibo. El rol de cada línea permite resaltar las cifras."""
        if self._vivienda is None:
            return (LineaInforme("Primero registra una vivienda.", LineaInforme.AVISO),)
        consumos = self._vivienda.consumos
        if not consumos:
            return (
                LineaInforme(
                    "No hay recibos registrados. Usa Registrar consumo eléctrico.",
                    LineaInforme.AVISO,
                ),
            )
        lineas: list[LineaInforme] = []
        for indice, consumo in enumerate(consumos, start=1):
            if lineas:
                lineas.append(LineaInforme("", LineaInforme.SEPARADOR))
            lineas.append(LineaInforme(f"Recibo {indice}: {consumo.periodo()}", LineaInforme.ENCABEZADO))
            try:
                resultado = self._calculadora.calcular(self._vivienda, consumo, self._factor)
            except ValueError as exc:
                lineas.append(LineaInforme(str(exc), LineaInforme.ERROR))
                continue
            lineas.extend(resultado.partes())
            lineas.append(LineaInforme("", LineaInforme.SEPARADOR))
            lineas.extend(self._lineas_recomendacion(self._calculadora.recomendar(resultado)))
        return tuple(lineas)

    def _lineas_recomendacion(self, texto: str) -> tuple[LineaInforme, ...]:
        lineas: list[LineaInforme] = []
        for indice, linea in enumerate(texto.splitlines()):
            rol = LineaInforme.TITULO_RECOMENDACION if indice == 0 else LineaInforme.RECOMENDACION
            lineas.append(LineaInforme(linea, rol))
        return tuple(lineas)

    def describir_resultados(self) -> str:
        return "\n".join(linea.texto for linea in self.lineas_resultados() if linea.rol != LineaInforme.SEPARADOR)

    def comparar(self) -> str:
        if self._vivienda is None:
            return "Primero registra una vivienda."
        return self._vivienda.comparar_consumos(self._calculadora.promedio_bimestral_kwh())

    def resumen_contexto(self) -> str:
        if self._vivienda is None:
            return "Vivienda: ninguna    ·    Habitantes: 0    ·    Recibos: 0"
        return (
            f"Vivienda: {self._vivienda.direccion}"
            f"    ·    Habitantes: {self._vivienda.numero_habitantes()}"
            f"    ·    Recibos: {len(self._vivienda.consumos)}"
        )

    def descripcion_vivienda_actual(self) -> str:
        if self._vivienda is None:
            return "Vivienda actual: ninguna"
        return f"Vivienda actual: {self._vivienda.direccion}"
