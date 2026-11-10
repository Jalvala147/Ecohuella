# EcoHuella

Sistema de cálculo y monitoreo de huella de carbono individual mediante el consumo de energía eléctrica. Programa de escritorio en Python con una ventana hecha en Tkinter. Los datos duran solo mientras la ventana está abierta: no se guardan en archivo.

## Requisitos

Python 3, con Tkinter (viene con la biblioteca estándar). En Ubuntu, si falta:

```bash
sudo apt install python3-tk
```

No hace falta instalar nada más.

## Ejecutar

Desde esta carpeta:

```bash
python3 ecohuella.py
```

La ventana tiene el menú a la izquierda:

1. Registrar vivienda
2. Registrar habitantes
3. Registrar consumo eléctrico
4. Calcular huella de carbono
5. Consultar resultados individuales
6. Consultar historial
7. Comparar consumos mensuales
8. Salir

Orden de uso: vivienda, habitantes, consumo mensual en kWh y cálculo. Después se pueden ver los resultados, el historial y la comparación entre meses.

## Fórmulas

- Consumo individual: `Ci = Ct / N`
- Huella individual: `HC = Ci * FE`
- Huella de la vivienda: `Ct * FE`

`Ct` es el consumo mensual de la vivienda en kWh, `N` el número de habitantes y `FE` el factor de emisión.

FE por defecto: **0.444 kg CO2e/kWh** (México, 2024), en `factor_emision.py`. El método `actualizar` de `FactorEmision` permite cambiarlo.

Si `N` es 0 o los kWh no son válidos (cero, negativos o no numéricos), el programa no divide y muestra el motivo en la barra de estado.

## Recomendaciones

Al calcular y al consultar resultados, el consumo mensual de la vivienda se compara con **167 kWh/mes**.

Esa cifra es una referencia aproximada de uso residencial en México: un consumo anual típico de unos **2000 kWh** (`2000 / 12` da cerca de 167). La misma constante está comentada en `calculadora_huella.py`.

- Si el mes supera 167 kWh, se recomiendan iluminación LED, menos aire acondicionado, cortar el standby, cuidar los horarios y electrodomésticos eficientes.
- Si está en 167 kWh o por debajo, se refuerzan esos hábitos.

## Clases

- **Persona.** Nombre, edad e identificación del habitante.
- **Vivienda.** Dirección. Asociación con sus `Persona` (guarda las mismas instancias y no las destruye) y composición de sus `ConsumoElectrico` (viven dentro de la vivienda y se van con ella).
- **ConsumoElectrico.** kWh, mes y año.
- **FactorEmision.** Factor y año. Valor inicial 0.444.
- **CalculadoraHuella.** Hace las cuentas. Sus métodos reciben la vivienda, el consumo, el factor o el resultado como objetos.
- **Resultado.** kg CO2e, consumo individual y el contexto para mostrarlo (vivienda, mes, año, N y FE usado).
- **Historial.** Guarda resultados de la sesión y permite consultarlos, también por mes y año.

`ecohuella.py` es solo la ventana: lee el formulario y llama a esas clases.

## Herencia

No hay herencia. No existe un tipo de habitante con un comportamiento distinto que justifique una subclase. `Persona` basta para registrar a quien vive en la vivienda.
