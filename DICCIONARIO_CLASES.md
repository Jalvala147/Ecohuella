# Diccionario de clases

Catálogo de las 24 clases de EcoHuella. Cada ficha dice para qué existe la clase, qué guarda, qué sabe hacer y con qué otras clases se relaciona.

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
| LineaInforme | resultado.py | Una línea del informe y su rol visual. | La producen Resultado y Sesion. La lee CajaResultados. |
| Sesion | sesion.py | Estado de la ventana: vivienda, personas, factor y cálculo. | Compone vivienda, personas, factor y calculadora. |
| Tabla | ecohuella.py | Lista con encabezados. | Hereda de tk.Frame. |
| CajaTexto | ecohuella.py | Texto de solo lectura. | Hereda de tk.Frame. |
| CajaResultados | ecohuella.py | La misma caja, con las cifras resaltadas. | Hereda de CajaTexto. |
| ValidadorEntrada | ecohuella.py | Convierte el texto del formulario en números y bimestre. | Depende de Bimestre. |
| Encabezado | ecohuella.py | Título y barra de contexto. | Hereda de tk.Frame. |
| BarraEstado | ecohuella.py | Aviso de la última acción. | Hereda de tk.Label. |
| MenuLateral | ecohuella.py | Botones que cambian de pantalla. | Hereda de tk.Frame. Asocia la acción de Aplicacion. |
| PanelSeccion | ecohuella.py | Base de las pantallas del menú. | Hereda de tk.Frame. Asocia Aplicacion. |
| PanelVivienda | ecohuella.py | Formulario de la dirección. | Hereda de PanelSeccion. |
| PanelHabitantes | ecohuella.py | Alta y baja de habitantes. | Hereda de PanelSeccion. |
| PanelConsumo | ecohuella.py | Alta y baja del recibo bimestral. | Hereda de PanelSeccion. |
| PanelCalcular | ecohuella.py | Cálculo de un recibo elegido. | Hereda de PanelSeccion. |
| PanelResultados | ecohuella.py | Huella de todos los recibos, resaltada. | Hereda de PanelSeccion. Compone CajaResultados. |
| PanelComparar | ecohuella.py | Diferencia entre recibos y el promedio. | Hereda de PanelSeccion. |
| Aplicacion | ecohuella.py | Ventana principal. | Hereda de tk.Tk. Compone Sesion y los paneles. |

En el dominio no hay herencia. Todos los habitantes cuentan igual en N, así que `Persona` no tiene subclases. La herencia está en la ventana.

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

Relación: la crean `Resultado.partes` y `Sesion`. `CajaResultados` la lee y no la posee.

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

---

## Ventana

Estas clases heredan de Tkinter. Su trabajo es leer el formulario y llamar a `Sesion`.

### Tabla

Lista con encabezados. La fila `i` es el elemento `i` de habitantes o de recibos.

| Visibilidad | Miembro | Tipo | Descripción |
| --- | --- | --- | --- |
| + | arbol | ttk.Treeview | La tabla visible. |
| + | __init__(parent, columnas, encabezados, altura) | — | Hereda de tk.Frame. |
| + | vaciar() | None | Borra las filas. |
| + | llenar(filas) | None | Vuelve a cargar las filas. |
| + | indice_seleccionado() | int o None | Fila marcada. |

Herencia: `tk.Frame`. Dependencia: muestra colecciones de `Vivienda`.

### CajaTexto

Texto de solo lectura para el cálculo y la comparación.

| Visibilidad | Miembro | Tipo | Descripción |
| --- | --- | --- | --- |
| + | texto | tk.Text | Widget de texto. |
| + | __init__(parent, altura: int) | — | Hereda de tk.Frame. |
| + | poner(texto: str) | None | Sustituye el contenido. |
| + | contenido() | str | Texto actual, sin espacios sobrantes. |

Herencia: `tk.Frame`. `CajaResultados` hereda de esta clase.

### CajaResultados

La caja del módulo Consultar resultados individuales. Pinta cada rol de `LineaInforme`.

| Visibilidad | Miembro | Tipo | Descripción |
| --- | --- | --- | --- |
| + | __init__(parent, altura: int) | — | Configura los estilos al crearse. |
| - | _configurar_estilos() | None | Verde para las huellas, ámbar para cada habitante, franja verde para el recibo. |
| + | mostrar_informe(lineas) | None | Escribe cada línea con el estilo de su rol. |

Herencia: `CajaTexto`. Dependencia: lee `LineaInforme` y no la guarda.

### ValidadorEntrada

Convierte lo escrito en el formulario. No pinta nada y no guarda estado. Sus métodos son de clase, porque no necesitan un objeto propio.

| Visibilidad | Miembro | Tipo | Descripción |
| --- | --- | --- | --- |
| + | entero(texto, etiqueta) | int | Error si el campo está vacío o no es entero. |
| + | kwh(texto) | float | Acepta coma o punto. |
| + | bimestre(texto) | Bimestre | Error si no hay un bimestre elegido. |

Dependencia: crea un `Bimestre` a partir del texto.

### Encabezado

Título de la ventana y resumen de la sesión.

| Visibilidad | Miembro | Tipo | Descripción |
| --- | --- | --- | --- |
| - | _lbl_contexto | tk.Label | Vivienda, habitantes y recibos. |
| + | __init__(master, texto_factor: str) | — | Hereda de tk.Frame. Muestra FE y el promedio de 334 kWh. |
| + | actualizar_contexto(texto: str) | None | Cambia la barra de contexto. |

Herencia: `tk.Frame`. El texto le llega de `Sesion.resumen_contexto`.

### BarraEstado

Mensaje de la última acción.

| Visibilidad | Miembro | Tipo | Descripción |
| --- | --- | --- | --- |
| + | __init__(master) | — | Hereda de tk.Label. Empieza en «Listo.» |
| + | avisar(texto: str, error=False) | None | Verde si salió bien, rojo si hubo error. |

Herencia: `tk.Label`.

### MenuLateral

Botones del menú.

| Visibilidad | Miembro | Tipo | Descripción |
| --- | --- | --- | --- |
| - | _al_elegir | función | Al pulsar, llama a `Aplicacion.mostrar`. |
| - | _botones | dict[str, tk.Button] | Un botón por pantalla. |
| + | __init__(master, entradas, al_elegir, al_salir) | — | Hereda de tk.Frame. Incluye Salir. |
| + | marcar(clave: str) | None | Deja activa la pantalla elegida. |
| + | etiquetas() | tuple[str, ...] | Textos de los botones. |

Herencia: `tk.Frame`. Asociación: la acción pertenece a `Aplicacion`.

### PanelSeccion

Base de las seis pantallas. Concentra título, campos y botones.

| Visibilidad | Miembro | Tipo | Descripción |
| --- | --- | --- | --- |
| + | clave | str | Identificador: vivienda, habitantes, consumo, calcular, resultados o comparar. |
| + | etiqueta_menu | str | Texto del botón. Cada subclase pone el suyo. |
| + | app | Aplicacion | Asociación. El panel llama a la sesión a través de la ventana. |
| + | __init__(master, app) | — | Hereda de tk.Frame y llama a `construir`. |
| + | construir() | None | La subclase arma su formulario. |
| + | refrescar() | None | La subclase vuelve a leer la sesión. |
| + | titulo(titulo, subtitulo) | None | |
| + | fila(parent, fila, etiqueta, variable, ancho=36) | tk.Entry | Campo de texto. |
| + | boton(parent, texto, comando, primario=True) | tk.Button | |

Herencia: `tk.Frame`. Asociación 1 con `Aplicacion`.

### PanelVivienda

Registrar la dirección. Hereda de `PanelSeccion`. Clave `vivienda`.

| Visibilidad | Miembro | Tipo | Descripción |
| --- | --- | --- | --- |
| + | var_direccion | tk.StringVar | Texto que se convertirá en `Vivienda.direccion`. |
| + | lbl_actual | tk.Label | Dirección ya registrada. |
| + | construir() | None | Arma el formulario. |
| + | refrescar() | None | Muestra la vivienda actual. |
| - | _registrar() | None | Llama a `Sesion.registrar_vivienda`. |

### PanelHabitantes

Alta y baja de habitantes. Hereda de `PanelSeccion`. Clave `habitantes`.

| Visibilidad | Miembro | Tipo | Descripción |
| --- | --- | --- | --- |
| + | var_nombre, var_edad, var_identificacion | tk.StringVar | Datos de la nueva `Persona`. |
| + | lbl_total | tk.Label | Muestra N. |
| + | tabla | Tabla | Lista de habitantes. |
| + | construir() | None | |
| + | refrescar() | None | Vuelve a llenar la tabla desde la vivienda. |
| - | _agregar() | None | Crea la persona en la sesión. |
| - | _quitar() | None | Quita la fila seleccionada. |

### PanelConsumo

Captura del recibo bimestral. Hereda de `PanelSeccion`. Clave `consumo`.

| Visibilidad | Miembro | Tipo | Descripción |
| --- | --- | --- | --- |
| + | var_kwh, var_bimestre, var_anio | tk.StringVar | kWh, bimestre y año del recibo. |
| + | combo | ttk.Combobox | Los seis bimestres. |
| + | tabla | Tabla | Recibos ya registrados. |
| + | construir() | None | |
| + | refrescar() | None | |
| - | _registrar() | None | Valida y llama a `Sesion.registrar_consumo`. |
| - | _quitar() | None | Quita el recibo seleccionado. |

### PanelCalcular

Calcula un recibo elegido. Hereda de `PanelSeccion`. Clave `calcular`. El texto sale plano, sin el resalte del otro módulo.

| Visibilidad | Miembro | Tipo | Descripción |
| --- | --- | --- | --- |
| + | tabla | Tabla | Recibos disponibles. |
| + | caja | CajaTexto | Resultado y recomendación. |
| + | construir() | None | |
| + | refrescar() | None | Actualiza la lista, no el texto ya calculado. |
| + | limpiar() | None | Vuelve al mensaje de seleccionar un recibo. |
| - | _calcular() | None | Llama a `Sesion.calcular_en`. |

### PanelResultados

Huella de cada recibo. Hereda de `PanelSeccion`. Clave `resultados`.

| Visibilidad | Miembro | Tipo | Descripción |
| --- | --- | --- | --- |
| + | caja | CajaResultados | Composición. Aquí se resaltan las cifras. |
| + | construir() | None | |
| + | refrescar() | None | Pide `Sesion.lineas_resultados` y las manda a la caja. |

### PanelComparar

Diferencia entre recibos y el promedio de 334 kWh. Hereda de `PanelSeccion`. Clave `comparar`.

| Visibilidad | Miembro | Tipo | Descripción |
| --- | --- | --- | --- |
| + | caja | CajaTexto | Texto de la comparación. |
| + | construir() | None | |
| + | refrescar() | None | Pide `Sesion.comparar`. |

### Aplicacion

Ventana principal. Hereda de `tk.Tk`. No calcula: delega en `Sesion`.

| Visibilidad | Miembro | Tipo | Descripción |
| --- | --- | --- | --- |
| + | PANELES | tuple de clases | Las seis pantallas, en el orden del menú. |
| + | sesion | Sesion | Composición. Estado del programa. |
| - | _paneles | dict[str, PanelSeccion] | Composición. Una instancia de cada pantalla. |
| + | encabezado | Encabezado | Composición. |
| + | menu | MenuLateral | Composición. |
| + | contenido | tk.Frame | Zona donde se apilan los paneles. |
| + | estado | BarraEstado | Composición. |
| + | __init__() | — | Crea la sesión, el menú y las pantallas. |
| - | _configurar_estilo() | None | Fuentes y colores de las tablas. |
| - | _construir_interfaz() | None | Arma encabezado, menú, paneles y barra. |
| + | panel(clave: str) | PanelSeccion | Devuelve una pantalla. |
| + | mostrar(clave: str) | None | Trae la pantalla al frente y la refresca. |
| + | avisar(texto, error=False) | None | Escribe en la barra de estado. |
| + | sincronizar(limpiar_calculo=False) | None | Actualiza contexto y listas. |

La función `main()`, en `ecohuella.py`, solo crea una `Aplicacion` y abre el ciclo de la ventana. Es el único código que no está dentro de una clase.
