# Diccionario de clases

Catálogo de las clases del modelo. Cada ficha dice para qué existe la clase, qué guarda, qué sabe hacer y con qué otras clases se relaciona. Las clases de Tkinter no entran: son la ventana, no el problema.

Visibilidad: `+` público, `-` privado (el nombre empieza con `_`). En Python el guion bajo es una convención: desde fuera se usan las propiedades y los métodos públicos.

En cada clase, los elementos van en orden alfabético por su nombre, sin tomar en cuenta el guion bajo. Si un atributo y su propiedad se llaman igual, el atributo va primero.

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
| + | describir(anio: int) | str | Nombre del bimestre más el año. |
| + | desde_texto(texto: str) | Bimestre o None | Lee la opción del formulario. Método de clase. |
| + | __eq__(otro) | bool | Igual si el número coincide. |
| + | __hash__() | int | Permite usar el bimestre en conjuntos. |
| + | __lt__(otro: Bimestre) | bool | Ordena del bimestre 1 al 6. |
| + | mes_fin() | int | Segundo mes, leído del catálogo. |
| + | mes_inicio() | int | Primer mes, leído del catálogo. |
| + | MESES | int | 2. Meses que cubre cualquier recibo. |
| + | nombre() | str | Por ejemplo `marzo-abril`. |
| - | _numero | int | Número del 1 al 6. |
| + | numero() | int | Devuelve `_numero`. |
| + | opcion() | str | Texto del formulario, por ejemplo `2 - marzo-abril`. |
| + | opciones() | tuple[str, ...] | Textos para el combo. Método de clase. |
| - | _PERIODOS | tuple[tuple[int, int, str], ...] | Catálogo: mes inicial, mes final y nombre. |
| + | todos() | tuple[Bimestre, ...] | Los seis bimestres. Método de clase. |

Relación: valor independiente. `ConsumoElectrico` y `Resultado` componen cada uno el suyo.

### Persona

Habitante. No tiene subtipos: todos entran igual en N.

| Visibilidad | Miembro | Tipo | Descripción |
| --- | --- | --- | --- |
| - | _edad | int | Entero entre 0 y 130. |
| + | edad() | int | Devuelve `_edad`. |
| - | _identificacion | str | Identificación, sin espacios de más. |
| + | identificacion() | str | Devuelve `_identificacion`. |
| + | __init__(nombre, edad, identificacion) | — | Rechaza nombre vacío, edad fuera de rango o identificación vacía. |
| + | mostrar() | str | Texto con nombre, edad e identificación. |
| - | _nombre | str | Nombre, sin espacios de más. |
| + | nombre() | str | Devuelve `_nombre`. |

Relación: `Sesion` la crea y la guarda (composición de la lista). `Vivienda` guarda la misma instancia (asociación).

### Vivienda

Dirección del hogar.

| Visibilidad | Miembro | Tipo | Descripción |
| --- | --- | --- | --- |
| + | agregar_consumo(consumo: ConsumoElectrico) | None | Valida el recibo y no admite el mismo bimestre y año dos veces. |
| + | agregar_habitante(persona: Persona) | None | Asocia la misma instancia. |
| + | comparar_consumos(promedio_kwh: float) | str | Diferencia entre recibos, ordenados por año y bimestre. |
| - | _consumos | list[ConsumoElectrico] | Composición. Los recibos viven aquí. |
| + | consumos() | tuple[ConsumoElectrico, ...] | Copia de solo lectura. |
| + | desasociar_habitantes() | None | Vacía la asociación. Las personas siguen fuera. |
| - | _describir_contra_promedio(actual, promedio_kwh, anterior) | str | Una línea de esa comparación. |
| - | _direccion | str | Dirección. No puede quedar vacía. |
| + | direccion() | str | Devuelve `_direccion`. |
| - | _habitantes | list[Persona] | Asociación. La vivienda no crea ni destruye a las personas. |
| + | habitantes() | tuple[Persona, ...] | Copia de solo lectura de la lista. |
| + | __init__(direccion: str) | — | Recorta la dirección y exige que tenga texto. |
| + | numero_habitantes() | int | N. |
| + | quitar_consumo(indice: int) | None | Borra el recibo de esa posición. |
| + | quitar_habitante(persona: Persona) | None | Quita esa instancia de la lista. |

Relaciones: asociación 0..* con `Persona`. Composición 0..* con `ConsumoElectrico`.

### ConsumoElectrico

Datos de un recibo de luz.

| Visibilidad | Miembro | Tipo | Descripción |
| --- | --- | --- | --- |
| - | _anio | int | Año, entre 1990 y 2100. |
| + | anio() | int | Devuelve `_anio`. |
| - | _bimestre | Bimestre | Composición. El periodo es parte del recibo. |
| + | bimestre() | Bimestre | Devuelve `_bimestre`. |
| + | __init__(kwh, bimestre, anio) | — | Exige un número, un Bimestre y un año entero. |
| - | _kwh | float | Consumo del bimestre. Debe ser mayor que cero. |
| + | kwh() | float | Devuelve `_kwh`. |
| + | mismo_periodo(otro: ConsumoElectrico) | bool | Mismo bimestre y mismo año. |
| + | periodo() | str | Texto del bimestre con el año. |
| + | resumen() | str | Periodo y kWh. |
| + | validar() | None | Lanza error si los kWh o el año no sirven. |

Relación: composición de `Vivienda`. Compone un `Bimestre`. `CalculadoraHuella` lo usa y no lo guarda.

### FactorEmision

Kilogramos de CO2e por cada kWh. El valor inicial es 0.444, México 2024.

| Visibilidad | Miembro | Tipo | Descripción |
| --- | --- | --- | --- |
| + | actualizar(factor: float, anio: int) | None | Cambia el factor si es mayor que cero y el año está entre 1990 y 2100. |
| - | _anio | int | Año de ese factor. |
| + | anio() | int | Devuelve `_anio`. |
| - | _factor | float | FE. Se lee con `valor`. |
| + | __init__(factor=0.444, anio=2024) | — | Valor inicial 0.444, año 2024. |
| + | valor() | float | Devuelve `_factor`. |

Relación: composición de `Sesion`. `CalculadoraHuella` lo recibe y copia el número dentro de `Resultado`; el resultado no guarda este objeto.

### CalculadoraHuella

Hace `Ci = Ct / N` y `HC = Ci * FE`. Ct es el kWh del recibo. No divide si N es 0 o los kWh no son válidos. No tiene atributos: no recuerda la vivienda ni el recibo.

| Visibilidad | Miembro | Tipo | Descripción |
| --- | --- | --- | --- |
| + | calcular(vivienda, consumo, factor) | Resultado | Crea el resultado del recibo. |
| + | promedio_bimestral_kwh() | float | 167 × `Bimestre.MESES`, o sea 334 kWh por recibo. |
| + | promedio_residencial_kwh() | float | 167 kWh/mes. |
| + | recomendar(resultado: Resultado) | str | Hábitos según el recibo esté sobre o bajo 334 kWh. |

Relaciones: depende de `Vivienda`, `ConsumoElectrico`, `FactorEmision` y `Bimestre`. Crea un `Resultado` y no lo almacena.

### Resultado

Copia de un cálculo ya hecho. Si después cambian los habitantes o el factor, este objeto sigue describiendo el cálculo que lo produjo.

| Visibilidad | Miembro | Tipo | Descripción |
| --- | --- | --- | --- |
| - | _anio | int | Año del recibo. |
| + | anio() | int | Devuelve `_anio`. |
| - | _anio_factor | int | Año de ese FE. |
| + | anio_factor() | int | Devuelve `_anio_factor`. |
| - | _bimestre | Bimestre | Copia del periodo. Composición. |
| + | bimestre() | Bimestre | Devuelve `_bimestre`. |
| - | _consumo_individual | float | Ci. |
| + | consumo_individual() | float | Devuelve `_consumo_individual`. |
| - | _consumo_total | float | Ct del recibo. |
| + | consumo_total() | float | Devuelve `_consumo_total`. |
| - | _direccion | str | Copia de la dirección. |
| + | direccion() | str | Devuelve `_direccion`. |
| - | _factor | float | Copia del FE. No es el objeto FactorEmision. |
| + | factor() | float | Devuelve `_factor`. |
| - | _habitantes | int | N usado al dividir. |
| + | habitantes() | int | Devuelve `_habitantes`. |
| + | __init__(...) | — | Recibe las cifras y el contexto, y copia el bimestre. |
| - | _kg_co2 | float | HC, huella individual del bimestre. |
| + | kg_co2() | float | Devuelve `_kg_co2`. |
| + | mostrar() | str | Une las líneas de `partes` en un solo texto. |
| - | _nombres | tuple[str, ...] | Nombres copiados. No hay enlace a Persona. |
| + | nombres() | tuple[str, ...] | Devuelve `_nombres`. |
| + | partes() | tuple[LineaInforme, ...] | Reparte el texto en líneas con rol. |
| + | resumen() | str | Una línea: dirección, periodo, N, Ci y HC. |

Relaciones: compone un `Bimestre`. Produce `LineaInforme`. No asocia `Persona` ni `FactorEmision`.

### LineaInforme

Una línea del informe y el papel que cumple al pintarla. El rol decide el resalte en Consultar resultados individuales.

| Visibilidad | Miembro | Tipo | Descripción |
| --- | --- | --- | --- |
| + | AVISO | str | Falta la vivienda o faltan recibos. |
| + | CONTEXTO | str | Vivienda, recibo, Ct, N y FE. |
| + | ENCABEZADO | str | Título del recibo. |
| + | ERROR | str | Motivo por el que no se pudo calcular. |
| + | ETIQUETA | str | Rótulo «Resultado por habitante». |
| + | __init__(texto: str, rol: str) | — | Guarda el texto y el rol. |
| + | PERSONA | str | Resultado de cada habitante. |
| + | RECOMENDACION | str | Hábitos sugeridos. |
| + | RESULTADO | str | Ci y las huellas. |
| - | _rol | str | Una de las constantes de rol. |
| + | rol() | str | Devuelve `_rol`. |
| + | SEPARADOR | str | Línea en blanco entre bloques. |
| - | _texto | str | Texto visible. |
| + | texto() | str | Devuelve `_texto`. |
| + | TITULO_RECOMENDACION | str | Título de las recomendaciones. |

Relación: la crean `Resultado.partes` y `Sesion`. La ventana solo la lee para pintar.

### Sesion

Dueña del estado mientras la ventana está abierta. No escribe archivos.

| Visibilidad | Miembro | Tipo | Descripción |
| --- | --- | --- | --- |
| + | agregar_habitante(nombre, edad, identificacion) | Persona | Crea la persona y la asocia a la vivienda. |
| - | _calculadora | CalculadoraHuella | Composición. Servicio sin memoria. |
| + | calculadora() | CalculadoraHuella | Devuelve `_calculadora`. |
| + | calcular_en(indice: int) | tuple[Resultado, str] | Resultado del recibo y texto de recomendación. |
| + | comparar() | str | Pide a la vivienda la comparación contra 334 kWh. |
| + | describir_resultados() | str | El informe en texto plano. |
| + | descripcion_vivienda_actual() | str | Dirección registrada, o ninguna. |
| + | exigir_vivienda() | Vivienda | Error si todavía no hay vivienda. |
| - | _factor | FactorEmision | Composición. Uno para toda la sesión. |
| + | factor() | FactorEmision | Devuelve `_factor`. |
| + | __init__() | — | Crea factor y calculadora. Aún no hay vivienda. |
| - | _lineas_recomendacion(texto: str) | tuple[LineaInforme, ...] | Parte la recomendación en título y viñetas. |
| + | lineas_resultados() | tuple[LineaInforme, ...] | Informe de cada recibo, con rol por línea. |
| - | _personas | list[Persona] | Composición. La sesión crea a los habitantes. |
| + | personas() | tuple[Persona, ...] | Devuelve la lista de habitantes. |
| + | quitar_consumo(indice: int) | None | Quita el recibo de esa posición. |
| + | quitar_habitante(indice: int) | None | La quita de la vivienda y de la lista de la sesión. |
| + | registrar_consumo(kwh, bimestre, anio) | ConsumoElectrico | Crea el recibo y se lo entrega a la vivienda. |
| + | registrar_vivienda(direccion: str) | bool | True si reemplazó a otra. Valida la dirección antes de borrar lo ya capturado. |
| + | resumen_contexto() | str | Vivienda, habitantes y cantidad de recibos. |
| - | _vivienda | Vivienda o None | Composición. None hasta el primer registro. |
| + | vivienda() | Vivienda o None | Devuelve `_vivienda`. |

Relaciones: compone `Vivienda`, `Persona`, `FactorEmision` y `CalculadoraHuella`. Crea `ConsumoElectrico` y lo cede a la vivienda. Produce `LineaInforme`.

La ventana sigue hecha con clases (`Aplicacion`, paneles, tablas y cajas) que heredan de Tkinter. No forman parte de este diccionario: no representan la vivienda, el recibo ni la huella. Solo capturan datos y muestran lo que ya calcula `Sesion`.
