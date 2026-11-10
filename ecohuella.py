#!/usr/bin/env python3
"""EcoHuella: ventana para calcular la huella de carbono del consumo eléctrico."""

import tkinter as tk
from tkinter import ttk

from calculadora_huella import CalculadoraHuella
from consumo_electrico import NOMBRES_MES, ConsumoElectrico, describir_periodo
from factor_emision import FactorEmision
from historial import Historial
from persona import Persona
from vivienda import Vivienda

FONDO = "#f7faf8"
VERDE = "#1f6b45"
VERDE_OSCURO = "#184e34"
LATERAL = "#e7f2eb"
TEXTO = "#143026"
TEXTO_SUAVE = "#3d5c4c"
ERROR = "#a12626"
BLANCO = "#ffffff"
BORDE = "#c5d5cb"

NAV = (
    ("vivienda", "Registrar vivienda"),
    ("habitantes", "Registrar habitantes"),
    ("consumo", "Registrar consumo eléctrico"),
    ("calcular", "Calcular huella de carbono"),
    ("resultados", "Consultar resultados individuales"),
    ("historial", "Consultar historial"),
    ("comparar", "Comparar consumos mensuales"),
)


class Aplicacion(tk.Tk):
    """Interfaz sencilla. Los datos duran solo mientras la ventana está abierta."""

    def __init__(self) -> None:
        super().__init__()
        self.title("EcoHuella")
        self.geometry("1000x700")
        self.minsize(900, 640)
        self.configure(bg=FONDO)

        # Las Persona viven aquí. La vivienda solo guarda referencias (asociación).
        self.personas: list[Persona] = []
        self.vivienda: Vivienda | None = None
        self.factor = FactorEmision()
        self.calculadora = CalculadoraHuella()
        self.historial = Historial()

        self.opciones_mes = [f"{i} - {NOMBRES_MES[i]}" for i in range(1, 13)]
        self.botones_nav: dict[str, tk.Button] = {}
        self._configurar_estilo()
        self._construir_interfaz()
        self._actualizar_contexto()
        self._mostrar("vivienda")

    def _configurar_estilo(self) -> None:
        estilo = ttk.Style(self)
        estilo.theme_use("clam")
        estilo.configure("Treeview", font=("DejaVu Sans", 10), rowheight=26, background=BLANCO, fieldbackground=BLANCO)
        estilo.configure("Treeview.Heading", font=("DejaVu Sans", 10, "bold"))
        estilo.configure("TCombobox", padding=4)
        estilo.configure("Vertical.TScrollbar", background=LATERAL)

    def _construir_interfaz(self) -> None:
        self.columnconfigure(0, minsize=250)
        self.columnconfigure(1, weight=1)
        self.rowconfigure(1, weight=1)

        encabezado = tk.Frame(self, bg=VERDE)
        encabezado.grid(row=0, column=0, columnspan=2, sticky="ew")
        tk.Label(
            encabezado,
            text="EcoHuella",
            bg=VERDE,
            fg=BLANCO,
            font=("DejaVu Sans", 20, "bold"),
            anchor="w",
        ).pack(fill="x", padx=16, pady=(12, 0))
        tk.Label(
            encabezado,
            text="Huella de carbono por consumo eléctrico",
            bg=VERDE,
            fg="#d9f2e4",
            font=("DejaVu Sans", 10),
            anchor="w",
        ).pack(fill="x", padx=16)
        self.lbl_factor = tk.Label(
            encabezado,
            text=(
                f"Factor de emisión: {self.factor.valor:.3f} kg CO2e/kWh ({self.factor.anio})"
                f"    ·    Promedio residencial: {self.calculadora.promedio_residencial_kwh():.0f} kWh/mes"
            ),
            bg=VERDE,
            fg=BLANCO,
            font=("DejaVu Sans", 9),
            anchor="w",
        )
        self.lbl_factor.pack(fill="x", padx=16, pady=(2, 8))

        barra = tk.Frame(encabezado, bg=VERDE_OSCURO)
        barra.pack(fill="x")
        self.lbl_contexto = tk.Label(
            barra,
            text="",
            bg=VERDE_OSCURO,
            fg="#e7f6ee",
            font=("DejaVu Sans", 9),
            anchor="w",
        )
        self.lbl_contexto.pack(fill="x", padx=16, pady=6)

        lateral = tk.Frame(self, bg=LATERAL)
        lateral.grid(row=1, column=0, sticky="nsew")
        tk.Label(
            lateral,
            text="MENÚ",
            bg=LATERAL,
            fg=VERDE,
            font=("DejaVu Sans", 9, "bold"),
            anchor="w",
        ).pack(fill="x", padx=14, pady=(14, 6))
        for clave, texto in NAV:
            boton = tk.Button(
                lateral,
                text=texto,
                command=lambda c=clave: self._mostrar(c),
                bg="#d5e6db",
                fg=TEXTO,
                activebackground="#c3ddd0",
                activeforeground=TEXTO,
                relief="flat",
                anchor="w",
                justify="left",
                wraplength=210,
                font=("DejaVu Sans", 10),
                padx=10,
                pady=7,
                bd=0,
            )
            boton.pack(fill="x", padx=10, pady=3)
            self.botones_nav[clave] = boton
        tk.Frame(lateral, bg=LATERAL).pack(fill="both", expand=True)
        tk.Button(
            lateral,
            text="Salir",
            command=self.destroy,
            bg="#d5e6db",
            fg=TEXTO,
            activebackground="#c3ddd0",
            activeforeground=TEXTO,
            relief="flat",
            anchor="w",
            font=("DejaVu Sans", 10),
            padx=10,
            pady=7,
            bd=0,
        ).pack(fill="x", padx=10, pady=(3, 14))

        self.contenido = tk.Frame(self, bg=FONDO)
        self.contenido.grid(row=1, column=1, sticky="nsew")
        self.contenido.grid_rowconfigure(0, weight=1)
        self.contenido.grid_columnconfigure(0, weight=1)

        self.paneles: dict[str, tk.Frame] = {}
        self._construir_vivienda()
        self._construir_habitantes()
        self._construir_consumo()
        self._construir_calcular()
        self._construir_resultados()
        self._construir_historial()
        self._construir_comparar()

        self.estado = tk.Label(
            self,
            text="Listo.",
            anchor="w",
            justify="left",
            bg=LATERAL,
            fg=VERDE,
            font=("DejaVu Sans", 9),
            padx=16,
            pady=8,
        )
        self.estado.grid(row=2, column=0, columnspan=2, sticky="ew")

    def _panel(self, clave: str) -> tk.Frame:
        panel = tk.Frame(self.contenido, bg=FONDO)
        panel.grid(row=0, column=0, sticky="nsew", padx=20, pady=16)
        panel.columnconfigure(0, weight=1)
        self.paneles[clave] = panel
        return panel

    def _titulo(self, panel: tk.Frame, titulo: str, subtitulo: str) -> None:
        tk.Label(
            panel,
            text=titulo,
            bg=FONDO,
            fg=TEXTO,
            font=("DejaVu Sans", 16, "bold"),
            anchor="w",
        ).grid(row=0, column=0, sticky="ew")
        tk.Label(
            panel,
            text=subtitulo,
            bg=FONDO,
            fg=TEXTO_SUAVE,
            font=("DejaVu Sans", 9),
            anchor="w",
            justify="left",
            wraplength=680,
        ).grid(row=1, column=0, sticky="ew", pady=(2, 12))

    def _fila(self, parent: tk.Frame, fila: int, etiqueta: str, variable: tk.StringVar, ancho: int = 36) -> tk.Entry:
        tk.Label(parent, text=etiqueta, bg=FONDO, fg=TEXTO, font=("DejaVu Sans", 10)).grid(
            row=fila, column=0, sticky="w", pady=4, padx=(0, 10)
        )
        entrada = tk.Entry(
            parent,
            textvariable=variable,
            width=ancho,
            font=("DejaVu Sans", 10),
            relief="solid",
            bd=1,
            highlightthickness=0,
        )
        entrada.grid(row=fila, column=1, sticky="ew", pady=4)
        return entrada

    def _boton(self, parent: tk.Misc, texto: str, comando, primario: bool = True) -> tk.Button:
        if primario:
            colores = (VERDE, BLANCO, VERDE_OSCURO, BLANCO)
            fuente = ("DejaVu Sans", 10, "bold")
        else:
            colores = ("#d5e6db", TEXTO, "#c3ddd0", TEXTO)
            fuente = ("DejaVu Sans", 10)
        boton = tk.Button(
            parent,
            text=texto,
            command=comando,
            bg=colores[0],
            fg=colores[1],
            activebackground=colores[2],
            activeforeground=colores[3],
            relief="flat",
            font=fuente,
            padx=12,
            pady=6,
            bd=0,
        )
        return boton

    def _combo_mes(self, parent: tk.Misc, variable: tk.StringVar) -> ttk.Combobox:
        combo = ttk.Combobox(
            parent,
            textvariable=variable,
            values=self.opciones_mes,
            state="readonly",
            width=34,
            font=("DejaVu Sans", 10),
        )
        return combo

    def _arbol(self, parent: tk.Frame, columnas: tuple[str, ...], encabezados: tuple[str, ...], altura: int) -> ttk.Treeview:
        marco = tk.Frame(parent, bg=FONDO)
        arbol = ttk.Treeview(marco, columns=columnas, show="headings", height=altura)
        scroll = ttk.Scrollbar(marco, orient="vertical", command=arbol.yview)
        arbol.configure(yscrollcommand=scroll.set)
        for columna, encabezado in zip(columnas, encabezados):
            arbol.heading(columna, text=encabezado)
            arbol.column(columna, width=160, anchor="w", stretch=True)
        arbol.grid(row=0, column=0, sticky="nsew")
        scroll.grid(row=0, column=1, sticky="ns")
        marco.columnconfigure(0, weight=1)
        marco.rowconfigure(0, weight=1)
        marco.arbol = arbol  # type: ignore[attr-defined]
        return marco

    def _caja(self, parent: tk.Frame, altura: int) -> tk.Text:
        marco = tk.Frame(parent, bg=FONDO)
        texto = tk.Text(
            marco,
            height=altura,
            wrap="word",
            font=("DejaVu Sans", 10),
            bg=BLANCO,
            fg=TEXTO,
            relief="solid",
            bd=1,
            padx=8,
            pady=8,
            highlightthickness=0,
        )
        scroll = ttk.Scrollbar(marco, command=texto.yview)
        texto.configure(yscrollcommand=scroll.set, state="disabled")
        texto.grid(row=0, column=0, sticky="nsew")
        scroll.grid(row=0, column=1, sticky="ns")
        marco.columnconfigure(0, weight=1)
        marco.rowconfigure(0, weight=1)
        marco.texto = texto  # type: ignore[attr-defined]
        return marco

    def _poner_texto(self, widget: tk.Text, texto: str) -> None:
        widget.configure(state="normal")
        widget.delete("1.0", "end")
        widget.insert("1.0", texto)
        widget.configure(state="disabled")

    def _aviso(self, texto: str, error: bool = False) -> None:
        self.estado.configure(text=texto, fg=ERROR if error else VERDE)

    def _mes_desde_combo(self, valor: str) -> int | None:
        valor = valor.strip()
        if not valor:
            return None
        try:
            mes = int(valor.split("-", 1)[0].strip())
        except ValueError:
            return None
        if mes < 1 or mes > 12:
            return None
        return mes

    def _leer_entero(self, texto: str, etiqueta: str) -> int | None:
        limpio = texto.strip()
        if not limpio:
            self._aviso(f"Escribe {etiqueta}.", error=True)
            return None
        try:
            return int(limpio)
        except ValueError:
            self._aviso(f"{etiqueta} no es un número válido.", error=True)
            return None

    def _construir_vivienda(self) -> None:
        panel = self._panel("vivienda")
        self._titulo(
            panel,
            "Registrar vivienda",
            "Dirección del hogar. Registrar otra vivienda reinicia habitantes y consumos. El historial de cálculos se conserva.",
        )
        formulario = tk.Frame(panel, bg=FONDO)
        formulario.grid(row=2, column=0, sticky="ew")
        formulario.columnconfigure(1, weight=1)
        self.var_direccion = tk.StringVar()
        entrada = self._fila(formulario, 0, "Dirección", self.var_direccion)
        entrada.bind("<Return>", lambda _evento: self._on_registrar_vivienda())
        self._boton(panel, "Registrar vivienda", self._on_registrar_vivienda).grid(row=3, column=0, sticky="w", pady=(12, 8))
        self.lbl_vivienda_actual = tk.Label(
            panel,
            text="Vivienda actual: ninguna",
            bg=FONDO,
            fg=TEXTO,
            font=("DejaVu Sans", 10),
            anchor="w",
            justify="left",
            wraplength=680,
        )
        self.lbl_vivienda_actual.grid(row=4, column=0, sticky="ew")

    def _construir_habitantes(self) -> None:
        panel = self._panel("habitantes")
        panel.rowconfigure(6, weight=1)
        self._titulo(
            panel,
            "Registrar habitantes",
            "Cada persona queda asociada a la vivienda. N es la cantidad de habitantes de la lista.",
        )
        formulario = tk.Frame(panel, bg=FONDO)
        formulario.grid(row=2, column=0, sticky="ew")
        formulario.columnconfigure(1, weight=1)
        self.var_nombre = tk.StringVar()
        self.var_edad = tk.StringVar()
        self.var_identificacion = tk.StringVar()
        self._fila(formulario, 0, "Nombre", self.var_nombre)
        self._fila(formulario, 1, "Edad", self.var_edad)
        identificacion = self._fila(formulario, 2, "Identificación", self.var_identificacion)
        identificacion.bind("<Return>", lambda _evento: self._on_agregar_habitante())
        botones = tk.Frame(panel, bg=FONDO)
        botones.grid(row=3, column=0, sticky="w", pady=(10, 6))
        self._boton(botones, "Agregar habitante", self._on_agregar_habitante).pack(side="left")
        self._boton(botones, "Quitar seleccionado", self._on_quitar_habitante, primario=False).pack(side="left", padx=(8, 0))
        self.lbl_total_habitantes = tk.Label(
            panel,
            text="Habitantes (N): 0",
            bg=FONDO,
            fg=TEXTO,
            font=("DejaVu Sans", 10, "bold"),
            anchor="w",
        )
        self.lbl_total_habitantes.grid(row=4, column=0, sticky="ew", pady=(4, 6))
        marco = self._arbol(panel, ("nombre", "edad", "identificacion"), ("Nombre", "Edad", "Identificación"), 8)
        marco.grid(row=6, column=0, sticky="nsew")
        self.tree_habitantes = marco.arbol

    def _construir_consumo(self) -> None:
        panel = self._panel("consumo")
        panel.rowconfigure(6, weight=1)
        self._titulo(
            panel,
            "Registrar consumo eléctrico",
            "Captura el consumo mensual en kWh, por ejemplo el de tu recibo de luz.",
        )
        formulario = tk.Frame(panel, bg=FONDO)
        formulario.grid(row=2, column=0, sticky="ew")
        formulario.columnconfigure(1, weight=1)
        self.var_kwh = tk.StringVar()
        self.var_mes = tk.StringVar()
        self.var_anio = tk.StringVar(value="2024")
        self._fila(formulario, 0, "Consumo (kWh)", self.var_kwh)
        tk.Label(formulario, text="Mes", bg=FONDO, fg=TEXTO, font=("DejaVu Sans", 10)).grid(
            row=1, column=0, sticky="w", pady=4, padx=(0, 10)
        )
        self.combo_mes = self._combo_mes(formulario, self.var_mes)
        self.combo_mes.grid(row=1, column=1, sticky="ew", pady=4)
        anio = self._fila(formulario, 2, "Año", self.var_anio)
        anio.bind("<Return>", lambda _evento: self._on_registrar_consumo())
        botones = tk.Frame(panel, bg=FONDO)
        botones.grid(row=3, column=0, sticky="w", pady=(10, 6))
        self._boton(botones, "Registrar consumo", self._on_registrar_consumo).pack(side="left")
        self._boton(botones, "Quitar seleccionado", self._on_quitar_consumo, primario=False).pack(side="left", padx=(8, 0))
        marco = self._arbol(panel, ("periodo", "kwh"), ("Periodo", "kWh"), 8)
        marco.grid(row=6, column=0, sticky="nsew")
        self.tree_consumos = marco.arbol

    def _construir_calcular(self) -> None:
        panel = self._panel("calcular")
        panel.rowconfigure(5, weight=1)
        self._titulo(
            panel,
            "Calcular huella de carbono",
            (
                f"Ci = Ct / N    y    HC = Ci × FE "
                f"({self.factor.valor:.3f} kg CO2e/kWh). "
                "El consumo de la vivienda se compara con el promedio residencial."
            ),
        )
        marco = self._arbol(panel, ("periodo", "kwh"), ("Periodo", "kWh"), 5)
        marco.grid(row=2, column=0, sticky="ew")
        self.tree_calculo = marco.arbol
        self._boton(panel, "Calcular huella", self._on_calcular).grid(row=3, column=0, sticky="w", pady=8)
        caja = self._caja(panel, 10)
        caja.grid(row=5, column=0, sticky="nsew")
        self.txt_calculo = caja.texto
        self._poner_texto(self.txt_calculo, "Selecciona un consumo y pulsa Calcular huella.")

    def _construir_resultados(self) -> None:
        panel = self._panel("resultados")
        panel.rowconfigure(2, weight=1)
        self._titulo(
            panel,
            "Resultados individuales",
            "Huella de cada habitante y de la vivienda, con recomendaciones de uso.",
        )
        caja = self._caja(panel, 16)
        caja.grid(row=2, column=0, sticky="nsew")
        self.txt_resultados = caja.texto

    def _construir_historial(self) -> None:
        panel = self._panel("historial")
        panel.rowconfigure(4, weight=1)
        self._titulo(
            panel,
            "Consultar historial",
            "Cálculos de esta sesión. Puedes verlos todos o filtrar por mes y año.",
        )
        filtros = tk.Frame(panel, bg=FONDO)
        filtros.grid(row=2, column=0, sticky="ew", pady=(0, 8))
        tk.Label(filtros, text="Mes", bg=FONDO, fg=TEXTO, font=("DejaVu Sans", 10)).pack(side="left")
        self.var_filtro_mes = tk.StringVar()
        self.combo_filtro_mes = self._combo_mes(filtros, self.var_filtro_mes)
        self.combo_filtro_mes.configure(width=18)
        self.combo_filtro_mes.pack(side="left", padx=(6, 12))
        tk.Label(filtros, text="Año", bg=FONDO, fg=TEXTO, font=("DejaVu Sans", 10)).pack(side="left")
        self.var_filtro_anio = tk.StringVar(value="2024")
        tk.Entry(
            filtros,
            textvariable=self.var_filtro_anio,
            width=8,
            font=("DejaVu Sans", 10),
            relief="solid",
            bd=1,
        ).pack(side="left", padx=(6, 12))
        self._boton(filtros, "Filtrar", self._on_filtrar_historial).pack(side="left")
        self._boton(filtros, "Ver todos", self._on_ver_historial, primario=False).pack(side="left", padx=(8, 0))
        caja = self._caja(panel, 14)
        caja.grid(row=4, column=0, sticky="nsew")
        self.txt_historial = caja.texto

    def _construir_comparar(self) -> None:
        panel = self._panel("comparar")
        panel.rowconfigure(2, weight=1)
        promedio = self.calculadora.promedio_residencial_kwh()
        self._titulo(
            panel,
            "Comparar consumos mensuales",
            f"Diferencia entre los meses registrados y el promedio residencial de {promedio:.0f} kWh/mes.",
        )
        caja = self._caja(panel, 16)
        caja.grid(row=2, column=0, sticky="nsew")
        self.txt_comparar = caja.texto

    def _mostrar(self, clave: str) -> None:
        self.paneles[clave].tkraise()
        for nombre, boton in self.botones_nav.items():
            activo = nombre == clave
            boton.configure(
                bg=VERDE if activo else "#d5e6db",
                fg=BLANCO if activo else TEXTO,
                activebackground=VERDE_OSCURO if activo else "#c3ddd0",
                activeforeground=BLANCO if activo else TEXTO,
            )
        refrescos = {
            "habitantes": self._refrescar_habitantes,
            "consumo": self._refrescar_consumos,
            "calcular": self._refrescar_calculo,
            "resultados": self._refrescar_resultados,
            "historial": self._on_ver_historial,
            "comparar": self._refrescar_comparar,
        }
        if clave in refrescos:
            refrescos[clave]()

    def _actualizar_contexto(self) -> None:
        if self.vivienda is None:
            direccion = "ninguna"
            habitantes = 0
            consumos = 0
            actual = "Vivienda actual: ninguna"
        else:
            direccion = self.vivienda.direccion
            habitantes = self.vivienda.numero_habitantes()
            consumos = len(self.vivienda.consumos)
            actual = f"Vivienda actual: {direccion}"
        self.lbl_contexto.configure(
            text=f"Vivienda: {direccion}    ·    Habitantes: {habitantes}    ·    Consumos: {consumos}"
        )
        self.lbl_vivienda_actual.configure(text=actual)

    def _vaciar_arbol(self, arbol: ttk.Treeview) -> None:
        hijos = arbol.get_children()
        if hijos:
            arbol.delete(*hijos)

    def _refrescar_habitantes(self) -> None:
        self._vaciar_arbol(self.tree_habitantes)
        personas = () if self.vivienda is None else self.vivienda.habitantes
        for indice, persona in enumerate(personas):
            self.tree_habitantes.insert(
                "",
                "end",
                iid=str(indice),
                values=(persona.nombre, persona.edad, persona.identificacion),
            )
        self.lbl_total_habitantes.configure(text=f"Habitantes (N): {len(personas)}")

    def _refrescar_consumos(self) -> None:
        self._vaciar_arbol(self.tree_consumos)
        consumos = () if self.vivienda is None else self.vivienda.consumos
        for indice, consumo in enumerate(consumos):
            self.tree_consumos.insert(
                "",
                "end",
                iid=str(indice),
                values=(consumo.periodo(), f"{consumo.kwh:.2f}"),
            )

    def _refrescar_calculo(self) -> None:
        self._vaciar_arbol(self.tree_calculo)
        consumos = () if self.vivienda is None else self.vivienda.consumos
        for indice, consumo in enumerate(consumos):
            self.tree_calculo.insert(
                "",
                "end",
                iid=str(indice),
                values=(consumo.periodo(), f"{consumo.kwh:.2f}"),
            )

    def _refrescar_listas(self) -> None:
        self._refrescar_habitantes()
        self._refrescar_consumos()
        self._refrescar_calculo()

    def _limpiar_calculo(self) -> None:
        self._poner_texto(self.txt_calculo, "Selecciona un consumo y pulsa Calcular huella.")

    def _exige_vivienda(self) -> bool:
        if self.vivienda is None:
            self._aviso("Primero registra una vivienda.", error=True)
            return False
        return True

    def _on_registrar_vivienda(self) -> None:
        direccion = self.var_direccion.get().strip()
        if not direccion:
            self._aviso("La dirección no puede estar vacía.", error=True)
            return
        habia = self.vivienda is not None
        if self.vivienda is not None:
            self.vivienda.desasociar_habitantes()
        self.personas.clear()
        self.vivienda = Vivienda(direccion)
        self._refrescar_listas()
        self._limpiar_calculo()
        self._actualizar_contexto()
        if habia:
            self._aviso(f"Vivienda registrada: {direccion}. Se reiniciaron habitantes y consumos.")
        else:
            self._aviso(f"Vivienda registrada: {direccion}.")

    def _on_agregar_habitante(self) -> None:
        if not self._exige_vivienda():
            return
        nombre = self.var_nombre.get()
        identificacion = self.var_identificacion.get()
        edad = self._leer_entero(self.var_edad.get(), "la edad")
        if edad is None:
            return
        try:
            persona = Persona(nombre, edad, identificacion)
        except ValueError as exc:
            self._aviso(str(exc), error=True)
            return
        self.personas.append(persona)
        self.vivienda.agregar_habitante(persona)
        self.var_nombre.set("")
        self.var_edad.set("")
        self.var_identificacion.set("")
        self._refrescar_habitantes()
        self._actualizar_contexto()
        self._aviso(f"Registrado: {persona.mostrar()}.")

    def _on_quitar_habitante(self) -> None:
        if not self._exige_vivienda():
            return
        seleccion = self.tree_habitantes.selection()
        if not seleccion:
            self._aviso("Selecciona un habitante.", error=True)
            return
        persona = self.vivienda.habitantes[int(seleccion[0])]
        self.vivienda.quitar_habitante(persona)
        if persona in self.personas:
            self.personas.remove(persona)
        self._refrescar_habitantes()
        self._actualizar_contexto()
        self._aviso("Habitante quitado de la vivienda.")

    def _on_registrar_consumo(self) -> None:
        if not self._exige_vivienda():
            return
        texto_kwh = self.var_kwh.get().strip().replace(",", ".")
        if not texto_kwh:
            self._aviso("Consumo inválido: escribe los kWh con número.", error=True)
            return
        try:
            kwh = float(texto_kwh)
        except ValueError:
            self._aviso("Consumo inválido: escribe los kWh con número.", error=True)
            return
        mes = self._mes_desde_combo(self.var_mes.get())
        if mes is None:
            self._aviso("Mes inválido: selecciona un mes.", error=True)
            return
        anio = self._leer_entero(self.var_anio.get(), "el año")
        if anio is None:
            return
        consumo = ConsumoElectrico(kwh, mes, anio)
        try:
            self.vivienda.agregar_consumo(consumo)
        except ValueError as exc:
            self._aviso(str(exc), error=True)
            return
        self.var_kwh.set("")
        self._refrescar_consumos()
        self._refrescar_calculo()
        self._actualizar_contexto()
        self._aviso(f"Consumo registrado: {consumo.resumen()}.")

    def _on_quitar_consumo(self) -> None:
        if not self._exige_vivienda():
            return
        seleccion = self.tree_consumos.selection()
        if not seleccion:
            self._aviso("Selecciona un consumo.", error=True)
            return
        try:
            self.vivienda.quitar_consumo(int(seleccion[0]))
        except ValueError as exc:
            self._aviso(str(exc), error=True)
            return
        self._refrescar_consumos()
        self._refrescar_calculo()
        self._actualizar_contexto()
        self._aviso("Consumo eliminado.")

    def _on_calcular(self) -> None:
        if not self._exige_vivienda():
            return
        if not self.vivienda.consumos:
            self._aviso("No hay consumos registrados.", error=True)
            return
        seleccion = self.tree_calculo.selection()
        if not seleccion:
            self._aviso("Selecciona un consumo.", error=True)
            return
        consumo = self.vivienda.consumos[int(seleccion[0])]
        try:
            resultado = self.calculadora.calcular(self.vivienda, consumo, self.factor)
        except ValueError as exc:
            self._aviso(str(exc), error=True)
            self._poner_texto(self.txt_calculo, str(exc))
            return
        self.historial.agregar(resultado)
        self._poner_texto(self.txt_calculo, f"{resultado.mostrar()}\n\n{self.calculadora.recomendar(resultado)}")
        self._aviso("Cálculo realizado.")

    def _refrescar_resultados(self) -> None:
        registros = self.historial.consultar()
        if not registros:
            self._poner_texto(
                self.txt_resultados,
                "No hay resultados calculados. Usa Calcular huella de carbono.",
            )
            return
        bloques = []
        for indice, resultado in enumerate(registros, start=1):
            bloques.append(
                f"--- Resultado {indice} ---\n{resultado.mostrar()}\n\n{self.calculadora.recomendar(resultado)}"
            )
        self._poner_texto(self.txt_resultados, "\n\n".join(bloques))

    def _on_ver_historial(self) -> None:
        self._poner_texto(self.txt_historial, self.historial.mostrar())

    def _on_filtrar_historial(self) -> None:
        mes = self._mes_desde_combo(self.var_filtro_mes.get())
        if mes is None:
            self._aviso("Selecciona un mes para filtrar.", error=True)
            return
        anio = self._leer_entero(self.var_filtro_anio.get(), "el año")
        if anio is None:
            return
        encontrados = self.historial.consultar_periodo(mes, anio)
        periodo = describir_periodo(mes, anio)
        if not encontrados:
            texto = f"No hay resultados para {periodo}."
        else:
            lineas = [f"Resultados de {periodo}:"]
            lineas.extend(registro.resumen() for registro in encontrados)
            texto = "\n".join(lineas)
        self._poner_texto(self.txt_historial, texto)
        self._aviso("Filtro aplicado." if encontrados else texto)

    def _refrescar_comparar(self) -> None:
        if self.vivienda is None:
            self._poner_texto(self.txt_comparar, "Primero registra una vivienda.")
            return
        self._poner_texto(
            self.txt_comparar,
            self.vivienda.comparar_consumos(self.calculadora.promedio_residencial_kwh()),
        )


def main() -> None:
    app = Aplicacion()
    app.mainloop()


if __name__ == "__main__":
    main()
