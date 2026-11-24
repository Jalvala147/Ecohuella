# Modelo de EcoHuella

Variables, tipos y relaciones del programa. Los datos viven en memoria mientras la ventana está abierta: no hay archivo ni base de datos.

`Ct` es el kWh del recibo bimestral, `N` el número de habitantes y `FE` el factor de emisión.

- `Ci = Ct / N`
- `HC = Ci * FE`
- Huella de la vivienda en el bimestre: `Ct * FE`

## Relaciones entre clases

| Origen | Relación | Destino | Cardinalidad | Qué significa |
| --- | --- | --- | --- | --- |
| Sesion | composición | Vivienda | 0..1 | La sesión crea la vivienda y la reemplaza. Al registrar otra, la anterior deja de usarse. |
| Sesion | composición | Persona | 0..* | La sesión crea a los habitantes y los conserva en su lista. |
| Sesion | composición | FactorEmision | 1 | Un factor para toda la sesión. Valor inicial 0.444, año 2024 (SEMARNAT, factor del SEN 2024). |
| Sesion | composición | CalculadoraHuella | 1 | La calculadora no guarda datos; la sesión la posee para hacer las cuentas. |
| Sesion | crea y entrega | ConsumoElectrico | 0..* | El recibo se construye en la sesión y pasa a ser parte de la vivienda. La sesión no guarda otra lista. |
| Sesion | produce | LineaInforme | 0..* | Arma el informe que pinta Consultar resultados individuales. |
| Vivienda | asociación | Persona | 0..* | Guarda las mismas instancias que la sesión. No las crea ni las destruye. `desasociar_habitantes` vacía la lista y las personas siguen en la sesión hasta que esa lista también se limpia. |
| Vivienda | composición | ConsumoElectrico | 0..* | Los recibos viven dentro de la vivienda y desaparecen con ella. |
| ConsumoElectrico | composición | Bimestre | 1 | El periodo es parte del recibo. No se comparte con otro consumo. |
| Resultado | composición | Bimestre | 1 | Copia el número de bimestre. No apunta al recibo original. |
| Resultado | copia de valor | Persona | n/a | No guarda la Persona. Copia los nombres en el momento del cálculo. |
| Resultado | copia de valor | FactorEmision | n/a | No guarda el factor. Copia el número y el año usados. |
| Resultado | produce | LineaInforme | 1..* | `partes` describe el resultado línea por línea. |
| CalculadoraHuella | dependencia | Vivienda, ConsumoElectrico, FactorEmision | usa | Los recibe por parámetro y no los conserva. |
| CalculadoraHuella | crea | Resultado | 1 por cálculo | Devuelve el objeto y no lo almacena. |
| CalculadoraHuella | dependencia | Bimestre | usa `MESES` | El promedio del recibo es 154.85 kWh/mes × `Bimestre.MESES` = 309.71 kWh. |
| Aplicacion | composición | Sesion | 1 | La ventana no calcula: delega en la sesión. |
| Aplicacion | composición | PanelSeccion | 6 | Una instancia de cada pantalla del menú. |
| PanelSeccion | herencia | PanelVivienda, PanelHabitantes, PanelConsumo, PanelCalcular, PanelResultados, PanelComparar | 6 subclases | Comparten título, campos y botones. |
| PanelSeccion | asociación | Aplicacion | 1 | Cada panel conoce la ventana para llamar a la sesión. No la posee. |
| CajaTexto | herencia | CajaResultados | 1 subclase | Solo el módulo de resultados resalta las cifras. |
| CajaResultados | dependencia | LineaInforme | lee | El rol de la línea elige el color y la fuente. |
| MenuLateral | asociación | Aplicacion | 1 | Al pulsar un botón llama a `Aplicacion.mostrar`. |
| Tabla | dependencia | colecciones de la vivienda | muestra | El índice de la fila es el índice en `habitantes` o `consumos`. |

No hay subclases en el dominio. `Persona` no se hereda: todos los habitantes cuentan igual dentro de `N`.

## Variables, tipos y relaciones

| Clase o módulo | Variable | Tipo | Relación | Descripción |
| --- | --- | --- | --- | --- |
| factor_emision | FACTOR_MEXICO_2024 | float | valor inicial de FactorEmision | 0.444 kg CO2e/kWh. |
| factor_emision | ANIO_FACTOR_MEXICO | int | valor inicial de FactorEmision | 2024. |
| FactorEmision | _factor | float | atributo propio | Kilogramos de CO2e por cada kWh. Se lee con `valor`. |
| FactorEmision | _anio | int | atributo propio | Año del factor. Se lee con `anio`. |
| calculadora_huella | CONSUMO_ANUAL_VIVIENDA_MEXICO_KWH | float | lo usa CalculadoraHuella | 1858.24 kWh por vivienda al año (CONUEE, BIEE 2019). |
| calculadora_huella | PROMEDIO_RESIDENCIAL_MEXICO_KWH | float | lo usa CalculadoraHuella | 1858.24 / 12 = 154.85 kWh/mes. |
| calculadora_huella | OCUPANTES_PROMEDIO_VIVIENDA_MEXICO | float | lo usa CalculadoraHuella | 3.6 ocupantes por vivienda (INEGI, Censo 2020). Sirve para la huella promedio por persona. |
| CalculadoraHuella | (sin atributos) | — | dependencia de los objetos que recibe | No guarda vivienda, recibo ni factor. |
| Bimestre | MESES | int | lo usa CalculadoraHuella | 2. Meses que cubre un recibo. |
| Bimestre | _PERIODOS | tuple[tuple[int, int, str], ...] | catálogo de la clase | Seis bimestres: mes inicial, mes final y nombre. |
| Bimestre | _numero | int | atributo propio | Del 1 (enero-febrero) al 6 (noviembre-diciembre). |
| Bimestre | mes_inicio | int | derivado de _PERIODOS | Primer mes del bimestre. No se guarda aparte. |
| Bimestre | mes_fin | int | derivado de _PERIODOS | Segundo mes del bimestre. No se guarda aparte. |
| Bimestre | nombre | str | derivado de _PERIODOS | Por ejemplo `marzo-abril`. No se guarda aparte. |
| Persona | _nombre | str | atributo propio | Nombre del habitante, sin espacios sobrantes. |
| Persona | _edad | int | atributo propio | Entero de 0 a 130. |
| Persona | _identificacion | str | atributo propio | Identificación, sin espacios sobrantes. |
| Vivienda | _direccion | str | atributo propio | Dirección del hogar. |
| Vivienda | _habitantes | list[Persona] | asociación 0..* | Mismas instancias que guarda la sesión. |
| Vivienda | _consumos | list[ConsumoElectrico] | composición 0..* | Recibos de luz de la vivienda. |
| ConsumoElectrico | _kwh | float | atributo propio | Consumo total del recibo, mayor que cero. |
| ConsumoElectrico | _bimestre | Bimestre | composición 1 | Periodo de dos meses de ese recibo. |
| ConsumoElectrico | _anio | int | atributo propio | Año del recibo, entre 1990 y 2100. |
| Resultado | _kg_co2 | float | atributo propio | Huella individual del bimestre, `HC`. |
| Resultado | _consumo_individual | float | atributo propio | `Ci`, kWh del recibo entre `N`. |
| Resultado | _consumo_total | float | copia del kWh del recibo | `Ct` usado en ese cálculo. |
| Resultado | _direccion | str | copia de Vivienda.direccion | Dirección en el momento del cálculo. |
| Resultado | _bimestre | Bimestre | composición 1 | Copia del bimestre del recibo. |
| Resultado | _anio | int | copia de ConsumoElectrico.anio | Año del recibo calculado. |
| Resultado | _habitantes | int | copia de `N` | Cantidad de habitantes usada al dividir. |
| Resultado | _factor | float | copia de FactorEmision.valor | FE usado. No es el objeto FactorEmision. |
| Resultado | _anio_factor | int | copia de FactorEmision.anio | Año del FE usado. |
| Resultado | _nombres | tuple[str, ...] | copia de Persona.nombre | Nombres en el orden de la vivienda. Sin enlace a Persona. |
| LineaInforme | ENCABEZADO, CONTEXTO, RESULTADO, ETIQUETA, PERSONA, TITULO_RECOMENDACION, RECOMENDACION, ERROR, AVISO, SEPARADOR | str | constantes de clase | Papel de la línea. `RESULTADO` y `PERSONA` son los que se resaltan. |
| LineaInforme | _texto | str | atributo propio | Texto visible de la línea. |
| LineaInforme | _rol | str | atributo propio | Una de las constantes anteriores. Lo lee CajaResultados. |
| Sesion | _personas | list[Persona] | composición 0..* | Habitantes creados por la sesión. |
| Sesion | _vivienda | Vivienda \| None | composición 0..1 | Vivienda activa. `None` hasta el primer registro. |
| Sesion | _factor | FactorEmision | composición 1 | Factor de la sesión. |
| Sesion | _calculadora | CalculadoraHuella | composición 1 | Servicio de cálculo. |
| ecohuella | FONDO, VERDE, VERDE_OSCURO, LATERAL, TEXTO, TEXTO_SUAVE, ERROR, BLANCO | str | colores de la ventana | No son datos del dominio. VERDE y el ámbar `#ffe8a3` marcan los resultados. |
| Aplicacion | sesion | Sesion | composición 1 | Estado de la ejecución. |
| Aplicacion | _paneles | dict[str, PanelSeccion] | composición | Clave del menú → pantalla. |
| Aplicacion | encabezado | Encabezado | composición 1 | Título y barra de contexto. |
| Aplicacion | menu | MenuLateral | composición 1 | Botones del menú. |
| Aplicacion | contenido | tk.Frame | composición 1 | Zona donde se apilan los paneles. |
| Aplicacion | estado | BarraEstado | composición 1 | Último aviso, en verde o en rojo. |
| Aplicacion | PANELES | tuple de clases | catálogo de la clase | Orden del menú. No incluye historial. |
| Encabezado | _lbl_contexto | tk.Label | muestra Sesion.resumen_contexto | Vivienda, habitantes y cantidad de recibos. |
| MenuLateral | _al_elegir | callable | asociación con Aplicacion.mostrar | Cambia de panel. |
| MenuLateral | _botones | dict[str, tk.Button] | composición | Un botón por pantalla. |
| PanelSeccion | clave | str | atributo de clase | Identificador del panel: vivienda, habitantes, consumo, calcular, resultados, comparar. |
| PanelSeccion | etiqueta_menu | str | atributo de clase | Texto del botón. |
| PanelSeccion | app | Aplicacion | asociación 1 | Acceso a la sesión. |
| PanelVivienda | var_direccion | tk.StringVar | entrada → Vivienda.direccion | Dirección escrita en el formulario. |
| PanelVivienda | lbl_actual | tk.Label | muestra Sesion.descripcion_vivienda_actual | Dirección ya registrada. |
| PanelHabitantes | var_nombre | tk.StringVar | entrada → Persona.nombre | |
| PanelHabitantes | var_edad | tk.StringVar | entrada → Persona.edad | El texto se convierte a int antes de crear la persona. |
| PanelHabitantes | var_identificacion | tk.StringVar | entrada → Persona.identificacion | |
| PanelHabitantes | lbl_total | tk.Label | muestra `N` | Cantidad de habitantes de la vivienda. |
| PanelHabitantes | tabla | Tabla | muestra Vivienda.habitantes | Columnas nombre, edad, identificación. |
| PanelConsumo | var_kwh | tk.StringVar | entrada → ConsumoElectrico.kwh | Acepta coma o punto decimal. |
| PanelConsumo | var_bimestre | tk.StringVar | entrada → Bimestre | Opción `1 - enero-febrero` … `6 - noviembre-diciembre`. |
| PanelConsumo | var_anio | tk.StringVar | entrada → ConsumoElectrico.anio | Arranca con el año de hoy. |
| PanelConsumo | combo | ttk.Combobox | muestra Bimestre.opciones | Lista fija de los seis bimestres. |
| PanelConsumo | tabla | Tabla | muestra Vivienda.consumos | Bimestre y kWh del recibo. |
| PanelCalcular | tabla | Tabla | muestra Vivienda.consumos | El recibo elegido es el que se calcula. |
| PanelCalcular | caja | CajaTexto | muestra Resultado y la recomendación | Texto plano, sin los resaltes del otro módulo. |
| PanelResultados | caja | CajaResultados | muestra LineaInforme | Verde: Ci, HC individual y huella de la vivienda. Ámbar: cada habitante. Franja verde: el recibo. |
| PanelComparar | caja | CajaTexto | muestra Vivienda.comparar_consumos | Diferencias entre recibos y el promedio de 309.71 kWh/bimestre. |
| Tabla | arbol | ttk.Treeview | muestra una colección | La fila `i` corresponde al elemento `i` de la tupla. |
| CajaTexto | texto | tk.Text | muestra un str | Solo lectura. |
| BarraEstado | text, fg | str | muestra el aviso | `fg` es VERDE o ERROR. El widget es la propia barra. |

## Cómo se reconoce un resultado

En Consultar resultados individuales cada `LineaInforme` se pinta según `_rol`:

| Rol | Qué línea es | Cómo se ve |
| --- | --- | --- |
| encabezado | `Recibo n: bimestre año` | Franja verde, texto blanco. |
| contexto | Vivienda, recibo, Ct, N y FE | Texto normal. |
| resultado | Ci, huella individual y huella de la vivienda | Negrita, fondo verde. |
| etiqueta | «Resultado por habitante» | Negrita verde, sin fondo. |
| persona | Nombre, kWh y kg CO2e de cada habitante | Negrita, fondo ámbar. |
| titulo_recomendacion | Título de las recomendaciones | Negrita verde, más pequeño. |
| recomendacion | Hábitos sugeridos | Texto suave, para que no compita con las cifras. |
| error | Motivo por el que no se pudo calcular | Negrita roja. |
| aviso | Falta la vivienda o faltan recibos | Texto normal. |
