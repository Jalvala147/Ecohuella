# EcoHuella

Sistema de cálculo y monitoreo de huella de carbono individual mediante el consumo de energía eléctrica. Programa de escritorio en Python con una ventana hecha en Tkinter. Los datos duran solo mientras la ventana está abierta: no se guardan en archivo.

El consumo se captura como el recibo de luz: un bimestre (dos meses) y los kWh totales de ese recibo.

El detalle de atributos, tipos y relaciones está en [MODELO.md](MODELO.md). El diccionario de clases, con responsabilidad, atributos, métodos y relaciones, está en [DICCIONARIO_CLASES.md](DICCIONARIO_CLASES.md).

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
6. Comparar consumos bimestrales
7. Salir

Orden de uso: vivienda, habitantes, datos del recibo (kWh del bimestre y año) y cálculo. Después se pueden ver los resultados de cada recibo y la comparación entre bimestres.

En Consultar resultados individuales las cifras van resaltadas: fondo verde para el consumo individual y las huellas, fondo ámbar para el resultado de cada habitante, y una franja verde con el bimestre del recibo.

## Fórmulas

- Consumo individual del bimestre: `Ci = Ct / N`
- Huella individual del bimestre: `HC = Ci * FE`
- Huella de la vivienda en el bimestre: `Ct * FE`

`Ct` es el consumo del recibo, en kWh, ya sumado los dos meses. `N` es el número de habitantes y `FE` el factor de emisión.

FE por defecto: **0.444 kg CO2e/kWh** (0.444 tCO2e/MWh, factor del Sistema Eléctrico Nacional 2024 publicado por SEMARNAT el 28 de febrero de 2025; sigue siendo el más reciente), en `factor_emision.py`. El método `actualizar` de `FactorEmision` permite cambiarlo.

Si `N` es 0 o los kWh no son válidos (cero, negativos o no numéricos), el programa no divide y muestra el motivo en la barra de estado.

## Recomendaciones

Al calcular y al consultar resultados, el kWh del recibo se compara con **309.71 kWh por bimestre**.

Esa cifra sale del consumo promedio por vivienda en México: **1858.24 kWh al año** (CONUEE, Base de Indicadores de Eficiencia Energética, dato 2019 publicado por SEMARNAT). `1858.24 / 12` da **154.85 kWh/mes** y el recibo cubre dos meses, así que `154.85 * 2 = 309.71`.

También se muestra la **huella promedio por persona**: `(309.71 / 3.6) * 0.444 = 38.20 kg CO2e por bimestre`, con 3.6 ocupantes por vivienda (INEGI, Censo 2020). La huella promedio de una vivienda es `309.71 * 0.444 = 137.51 kg CO2e por bimestre`. La constante mensual está comentada en `calculadora_huella.py` y los meses del bimestre viven en `Bimestre.MESES`.

- Si el recibo supera 309.71 kWh, se recomiendan iluminación LED, menos aire acondicionado, cortar el standby, cuidar los horarios y electrodomésticos eficientes.
- Si está en 309.71 kWh o por debajo, se refuerzan esos hábitos.

## Clases

- **Bimestre.** Periodo de dos meses del recibo (enero-febrero … noviembre-diciembre). Valor propio de cada consumo y de cada resultado.
- **Persona.** Nombre, edad e identificación del habitante.
- **Vivienda.** Dirección. Asociación con sus `Persona` (guarda las mismas instancias y no las destruye) y composición de sus `ConsumoElectrico` (viven dentro de la vivienda y se van con ella).
- **ConsumoElectrico.** kWh, bimestre y año del recibo de luz.
- **FactorEmision.** Factor y año. Valor inicial 0.444.
- **CalculadoraHuella.** Hace las cuentas. Sus métodos reciben la vivienda, el consumo, el factor o el resultado como objetos. No guarda datos.
- **Resultado.** kg CO2e, consumo individual y el contexto para mostrarlo (vivienda, bimestre, año, N y FE usado). Copia esos datos; no queda atado a la persona ni al factor. `partes` reparte el texto en líneas con un rol.
- **LineaInforme.** Una línea de ese informe y su rol (encabezado, contexto, resultado, persona, recomendación, error, aviso).
- **Sesion.** Dueña de la vivienda, de la lista de personas, del factor y de la calculadora mientras la ventana está abierta.
- **Aplicacion y paneles.** La ventana. Cada pantalla del menú es una subclase de `PanelSeccion`. `CajaResultados` hereda de `CajaTexto` y pinta cada rol con su resalte.

`ecohuella.py` lee el formulario y llama a `Sesion`. `Sesion` llama al resto de las clases.

## Herencia

En el dominio no hay subclases. No existe un tipo de habitante con un comportamiento distinto que justifique heredar de `Persona`.

En la ventana sí: `PanelVivienda`, `PanelHabitantes`, `PanelConsumo`, `PanelCalcular`, `PanelResultados` y `PanelComparar` heredan de `PanelSeccion`, que concentra título, campos y botones. `CajaResultados` hereda de `CajaTexto`. `Tabla`, `Encabezado`, `MenuLateral` y `BarraEstado` son componentes propios y, como el resto de la ventana, heredan de los widgets de Tkinter.

## Fuentes

- SEMARNAT. (2025, 28 de febrero). *Aviso: Factor de emisión del Sistema Eléctrico Nacional 2024*. https://www.gob.mx/cms/uploads/attachment/file/981194/aviso_fesen_2024.pdf
- SEMARNAT. (2021). *Compendio de Estadísticas Ambientales 2021: Intensidad y consumo de electricidad (BIEE-CONUEE)*. https://apps1.semarnat.gob.mx:8443/dgeia/compendio_2021/dgeiawf.semarnat.gob.mx_8080/ibi_apps/WFServletc953.html
- INEGI. (2023). *Estadísticas a propósito del Día Nacional de la Vivienda*. https://www.inegi.org.mx/contenidos/saladeprensa/aproposito/2023/EAP_Vivienda.pdf
