# Diccionario de clases

Catálogo de las clases del modelo. Cada ficha dice para qué existe la clase, qué guarda, qué sabe hacer y con qué otras clases se relaciona. Las clases de Tkinter no entran: son la ventana, no el problema.

Visibilidad: `+` público, `-` privado (el nombre empieza con `_`). En Python el guion bajo es una convención: desde fuera se usan las propiedades y los métodos públicos.

Tipos de relación:

| Relación | Significado en este programa |
| --- | --- |
| Herencia | La subclase es un caso de la clase base y reutiliza su comportamiento. |
| Composición | El objeto contiene al otro. Si el dueño desaparece, el contenido también. |
| Asociación | Guarda una referencia al otro objeto, que vive fuera. |
| Dependencia | Lo usa un momento (parámetro o valor de retorno) y no lo guarda. |

## Índice

| Clase | Archivo | Responsabilidad | Relación principal |
| --- | --- | --- | --- |
| Bimestre | bimestre.py | Periodo de dos meses del recibo de luz. | Lo componen ConsumoElectrico y Resultado. |
| Persona | persona.py | Un habitante: nombre, edad e identificación. | Sesion la crea. Vivienda la asocia. |
| Vivienda | vivienda.py | El hogar: dirección, habitantes y recibos. | Compone recibos y asocia personas. |
| ConsumoElectrico | consumo_electrico.py | Un recibo: kWh, bimestre y año. | Composición de Vivienda. Compone un Bimestre. |
| FactorEmision | factor_emision.py | kg CO2e por cada kWh, y el año del factor. | Composición de Sesion. |
| CalculadoraHuella | calculadora_huella.py | Calcula Ci y HC. No guarda datos. | Depende de vivienda, recibo y factor. Crea Resultado. |
| Resultado | resultado.py | Copia del cálculo para mostrarlo. | Compone un Bimestre. Produce LineaInforme. |
| LineaInforme | resultado.py | Una línea del informe y su rol. | La producen Resultado y Sesion. |
| Sesion | sesion.py | Estado en memoria: vivienda, personas, factor y cálculo. | Compone vivienda, personas, factor y calculadora. |

En el modelo no hay herencia. Todos los habitantes cuentan igual en N, así que `Persona` no tiene subclases.

---

## Dominio

### Bimestre

Periodo bimestral del 1 (enero-febrero) al 6 (noviembre-diciembre). Dos bimestres con el mismo número son el mismo periodo.

| Visibilidad | Miembro | Tipo | Descripción |
| --- | --- | --- | --- |
| + | MESES | int | 2. Meses que cubre cualquier recibo. |
| - | _PERIODOS | tuple[tuple[int, int, str], ...] | Catálogo: mes inicial, mes final y nombre. |
| - | _numero | int | Número del 1 al 6. |
| + | numero() | int | Devuelve `_numero`. |
| + | mes_inicio() | int | Primer mes, leído del catálogo. |
| + | mes_fin() | int | Segundo mes, leído del catálogo. |
| + | nombre() | str | Por ejemplo `marzo-abril`. |
| + | describir(anio: int) | str | Nombre del bimestre más el año. |
| + | opcion() | str | Texto del formulario, por ejemplo `2 - marzo-abril`. |
| + | __eq__(otro) | bool | Igual si el número coincide. |
| + | __hash__() | int | Permite usar el bimestre en conjuntos. |
| + | __lt__(otro: Bimestre) | bool | Ordena del bimestre 1 al 6. |
| + | todos() | tuple[Bimestre, ...] | Los seis bimestres. Método de clase. |
| + | opciones() | tuple[str, ...] | Textos para el combo. Método de clase. |
| + | desde_texto(texto: str) | Bimestre o None | Lee la opción del formulario. Método de clase. |

Relación: valor independiente. `ConsumoElectrico` y `Resultado` componen cada uno el suyo.

### Persona

Habitante. No tiene subtipos: todos entran igual en N.

| Visibilidad | Miembro | Tipo | Descripción |
| --- | --- | --- | --- |
| - | _nombre | str | Nombre, sin espacios de más. |
| - | _edad | int | Entero entre 0 y 130. |
| - | _identificacion | str | Identificación, sin espacios de más. |
| + | __init__(nombre, edad, identificacion) | — | Rechaza nombre vacío, edad fuera de rango o identificación vacía. |
| + | nombre() | str | |
| + | edad() | int | |
| + | identificacion() | str | |
| + | mostrar() | str | Texto con nombre, edad e identificación. |

Relación: `Sesion` la crea y la guarda (composición de la lista). `Vivienda` guarda la misma instancia (asociación).

### Vivienda

Dirección del hogar.

| Visibilidad | Miembro | Tipo | Descripción |
| --- | --- | --- | --- |
| - | _direccion | str | Dirección. No puede quedar vacía. |
| - | _habitantes | list[Persona] | Asociación. La vivienda no crea ni destruye a las personas. |
| - | _consumos | list[ConsumoElectrico] | Composición. Los recibos viven aquí. |
| + | __init__(direccion: str) | — | Recorta la dirección y exige que tenga texto. |
| + | direccion() | str | |
| + | agregar_habitante(persona: Persona) | None | Asocia la misma instancia. |
| + | quitar_habitante(persona: Persona) | None | Quita esa instancia de la lista. |
| + | desasociar_habitantes() | None | Vacía la asociación. Las personas siguen fuera. |
| + | numero_habitantes() | int | N. |
| + | habitantes() | tuple[Persona, ...] | Copia de solo lectura de la lista. |
| + | agregar_consumo(consumo: ConsumoElectrico) | None | Valida el recibo y no admite el mismo bimestre y año dos veces. |
| + | quitar_consumo(indice: int) | None | Borra el recibo de esa posición. |
| + | consumos() | tuple[ConsumoElectrico, ...] | Copia de solo lectura. |
| + | comparar_consumos(promedio_kwh: float) | str | Diferencia entre recibos, ordenados por año y bimestre. |
| - | _describir_contra_promedio(actual, promedio_kwh, anterior) | str | Una línea de esa comparación. |

Relaciones: asociación 0..* con `Persona`. Composición 0..* con `ConsumoElectrico`.

### ConsumoElectrico

Datos de un recibo de luz.

| Visibilidad | Miembro | Tipo | Descripción |
| --- | --- | --- | --- |
| - | _kwh | float | Consumo del bimestre. Debe ser mayor que cero. |
| - | _bimestre | Bimestre | Composición. El periodo es parte del recibo. |
| - | _anio | int | Año, entre 1990 y 2100. |
| + | __init__(kwh, bimestre, anio) | — | Exige un número, un Bimestre y un año entero. |
| + | kwh() | float | |
| + | bimestre() | Bimestre | |
| + | anio() | int | |
| + | validar() | None | Lanza error si los kWh o el año no sirven. |
| + | mismo_periodo(otro: ConsumoElectrico) | bool | Mismo bimestre y mismo año. |
| + | periodo() | str | Texto del bimestre con el año. |
| + | resumen() | str | Periodo y kWh. |

Relación: composición de `Vivienda`. Compone un `Bimestre`. `CalculadoraHuella` lo usa y no lo guarda.

### FactorEmision

Kilogramos de CO2e por cada kWh. El valor inicial es 0.444, México 2024.

| Visibilidad | Miembro | Tipo | Descripción |
| --- | --- | --- | --- |
| - | _factor | float | FE. Se lee con `valor`. |
| - | _anio | int | Año de ese factor. |
| + | __init__(factor=0.444, anio=2024) | — | |
| + | valor() | float | |
| + | anio() | int | |
| + | actualizar(factor: float, anio: int) | None | Cambia el factor si es mayor que cero y el año está entre 1990 y 2100. |

Relación: composición de `Sesion`. `CalculadoraHuella` lo recibe y copia el número dentro de `Resultado`; el resultado no guarda este objeto.

### CalculadoraHuella

Hace `Ci = Ct / N` y `HC = Ci * FE`. Ct es el kWh del recibo. No divide si N es 0 o los kWh no son válidos. No tiene atributos: no recuerda la vivienda ni el recibo.

| Visibilidad | Miembro | Tipo | Descripción |
| --- | --- | --- | --- |
| + | calcular(vivienda, consumo, factor) | Resultado | Crea el resultado del recibo. |
| + | promedio_residencial_kwh() | float | 167 kWh/mes. |
| + | promedio_bimestral_kwh() | float | 167 × `Bimestre.MESES`, o sea 334 kWh por recibo. |
| + | recomendar(resultado: Resultado) | str | Hábitos según el recibo esté sobre o bajo 334 kWh. |

Relaciones: depende de `Vivienda`, `ConsumoElectrico`, `FactorEmision` y `Bimestre`. Crea un `Resultado` y no lo almacena.

### Resultado

Copia de un cálculo ya hecho. Si después cambian los habitantes o el factor, este objeto sigue describiendo el cálculo que lo produjo.

| Visibilidad | Miembro | Tipo | Descripción |
| --- | --- | --- | --- |
| - | _kg_co2 | float | HC, huella individual del bimestre. |
| - | _consumo_individual | float | Ci. |
| - | _consumo_total | float | Ct del recibo. |
| - | _direccion | str | Copia de la dirección. |
| - | _bimestre | Bimestre | Copia del periodo. Composición. |
| - | _anio | int | Año del recibo. |
| - | _habitantes | int | N usado al dividir. |
| - | _factor | float | Copia del FE. No es el objeto FactorEmision. |
| - | _anio_factor | int | Año de ese FE. |
| - | _nombres | tuple[str, ...] | Nombres copiados. No hay enlace a Persona. |
| + | __init__(...) | — | Recibe las cifras y el contexto, y copia el bimestre. |
| + | kg_co2(), consumo_individual(), consumo_total(), direccion(), bimestre(), anio(), habitantes(), factor(), anio_factor(), nombres() | el tipo de cada atributo | Lectura de la copia. |
| + | resumen() | str | Una línea: dirección, periodo, N, Ci y HC. |
| + | partes() | tuple[LineaInforme, ...] | Reparte el texto en líneas con rol. |
| + | mostrar() | str | Une esas líneas en un solo texto. |

Relaciones: compone un `Bimestre`. Produce `LineaInforme`. No asocia `Persona` ni `FactorEmision`.

### LineaInforme

Una línea del informe y el papel que cumple al pintarla. El rol decide el resalte en Consultar resultados individuales.

| Visibilidad | Miembro | Tipo | Descripción |
| --- | --- | --- | --- |
| + | ENCABEZADO, CONTEXTO, RESULTADO, ETIQUETA, PERSONA, TITULO_RECOMENDACION, RECOMENDACION, ERROR, AVISO, SEPARADOR | str | Constantes de clase. `RESULTADO` y `PERSONA` son las cifras resaltadas. |
| - | _texto | str | Texto visible. |
| - | _rol | str | Una de esas constantes. |
| + | __init__(texto: str, rol: str) | — | |
| + | texto() | str | |
| + | rol() | str | |

Relación: la crean `Resultado.partes` y `Sesion`. La ventana solo la lee para pintar.

### Sesion

Dueña del estado mientras la ventana está abierta. No escribe archivos.

| Visibilidad | Miembro | Tipo | Descripción |
| --- | --- | --- | --- |
| - | _personas | list[Persona] | Composición. La sesión crea a los habitantes. |
| - | _vivienda | Vivienda o None | Composición. None hasta el primer registro. |
| - | _factor | FactorEmision | Composición. Uno para toda la sesión. |
| - | _calculadora | CalculadoraHuella | Composición. Servicio sin memoria. |
| + | __init__() | — | Crea factor y calculadora. Aún no hay vivienda. |
| + | vivienda() | Vivienda o None | |
| + | factor() | FactorEmision | |
| + | calculadora() | CalculadoraHuella | |
| + | personas() | tuple[Persona, ...] | |
| + | exigir_vivienda() | Vivienda | Error si todavía no hay vivienda. |
| + | registrar_vivienda(direccion: str) | bool | True si reemplazó a otra. Valida la dirección antes de borrar lo ya capturado. |
| + | agregar_habitante(nombre, edad, identificacion) | Persona | Crea la persona y la asocia a la vivienda. |
| + | quitar_habitante(indice: int) | None | La quita de la vivienda y de la lista de la sesión. |
| + | registrar_consumo(kwh, bimestre, anio) | ConsumoElectrico | Crea el recibo y se lo entrega a la vivienda. |
| + | quitar_consumo(indice: int) | None | |
| + | calcular_en(indice: int) | tuple[Resultado, str] | Resultado del recibo y texto de recomendación. |
| + | lineas_resultados() | tuple[LineaInforme, ...] | Informe de cada recibo, con rol por línea. |
| - | _lineas_recomendacion(texto: str) | tuple[LineaInforme, ...] | Parte la recomendación en título y viñetas. |
| + | describir_resultados() | str | El informe en texto plano. |
| + | comparar() | str | Pide a la vivienda la comparación contra 334 kWh. |
| + | resumen_contexto() | str | Vivienda, habitantes y cantidad de recibos. |
| + | descripcion_vivienda_actual() | str | Dirección registrada, o ninguna. |

Relaciones: compone `Vivienda`, `Persona`, `FactorEmision` y `CalculadoraHuella`. Crea `ConsumoElectrico` y lo cede a la vivienda. Produce `LineaInforme`.

La ventana sigue hecha con clases (`Aplicacion`, paneles, tablas y cajas) que heredan de Tkinter. No forman parte de este diccionario: no representan la vivienda, el recibo ni la huella. Solo capturan datos y muestran lo que ya calcula `Sesion`.
