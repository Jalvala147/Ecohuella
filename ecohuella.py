#!/usr/bin/env python3
"""EcoHuella: ventana para calcular la huella de carbono del recibo de luz."""

from __future__ import annotations

from datetime import date

import tkinter as tk
from tkinter import ttk

from bimestre import Bimestre
from resultado import LineaInforme
from sesion import Sesion

FONDO = "#f7faf8"
VERDE = "#1f6b45"
VERDE_OSCURO = "#184e34"
LATERAL = "#e7f2eb"
TEXTO = "#143026"
TEXTO_SUAVE = "#3d5c4c"
ERROR = "#a12626"
BLANCO = "#ffffff"


class Tabla(tk.Frame):
    """Lista con encabezados. El índice de la fila es el de la colección del dominio."""

    def __init__(
        self,
        parent: tk.Misc,
        columnas: tuple[str, ...],
        encabezados: tuple[str, ...],
        altura: int,
    ) -> None:
        super().__init__(parent, bg=FONDO)
        self.arbol = ttk.Treeview(self, columns=columnas, show="headings", height=altura)
        scroll = ttk.Scrollbar(self, orient="vertical", command=self.arbol.yview)
        self.arbol.configure(yscrollcommand=scroll.set)
        for columna, encabezado in zip(columnas, encabezados):
            self.arbol.heading(columna, text=encabezado)
            self.arbol.column(columna, width=160, anchor="w", stretch=True)
        self.arbol.grid(row=0, column=0, sticky="nsew")
        scroll.grid(row=0, column=1, sticky="ns")
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)

    def vaciar(self) -> None:
        hijos = self.arbol.get_children()
        if hijos:
            self.arbol.delete(*hijos)

    def llenar(self, filas) -> None:
        self.vaciar()
        for indice, valores in enumerate(filas):
            self.arbol.insert("", "end", iid=str(indice), values=valores)

    def indice_seleccionado(self) -> int | None:
        seleccion = self.arbol.selection()
        if not seleccion:
            return None
        return int(seleccion[0])


class CajaTexto(tk.Frame):
    """Texto de solo lectura para resultados y comparaciones."""

    def __init__(self, parent: tk.Misc, altura: int) -> None:
        super().__init__(parent, bg=FONDO)
        self.texto = tk.Text(
            self,
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
        scroll = ttk.Scrollbar(self, command=self.texto.yview)
        self.texto.configure(yscrollcommand=scroll.set, state="disabled")
        self.texto.grid(row=0, column=0, sticky="nsew")
        scroll.grid(row=0, column=1, sticky="ns")
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)

    def poner(self, texto: str) -> None:
        self.texto.configure(state="normal")
        self.texto.delete("1.0", "end")
        self.texto.insert("1.0", texto)
        self.texto.configure(state="disabled")

    def contenido(self) -> str:
        return self.texto.get("1.0", "end").strip()


class CajaResultados(CajaTexto):
    """Caja de Consultar resultados. Resalta las cifras para distinguirlas del resto."""

    def __init__(self, parent: tk.Misc, altura: int) -> None:
        super().__init__(parent, altura)
        self._configurar_estilos()

    def _configurar_estilos(self) -> None:
        texto = self.texto
        texto.tag_configure(
            LineaInforme.ENCABEZADO,
            font=("DejaVu Sans", 11, "bold"),
            background=VERDE,
            foreground=BLANCO,
            spacing1=8,
            spacing3=4,
            lmargin1=6,
            lmargin2=6,
        )
        texto.tag_configure(
            LineaInforme.RESULTADO,
            font=("DejaVu Sans", 11, "bold"),
            background="#b7e4c7",
            foreground="#0d3b24",
            spacing1=3,
            spacing3=3,
            lmargin1=8,
            lmargin2=8,
        )
        texto.tag_configure(
            LineaInforme.PERSONA,
            font=("DejaVu Sans", 10, "bold"),
            background="#ffe8a3",
            foreground="#5c4308",
            spacing1=2,
            spacing3=2,
            lmargin1=16,
            lmargin2=16,
        )
        texto.tag_configure(
            LineaInforme.ETIQUETA,
            font=("DejaVu Sans", 10, "bold"),
            foreground=VERDE_OSCURO,
            spacing1=6,
            spacing3=2,
        )
        texto.tag_configure(LineaInforme.CONTEXTO, font=("DejaVu Sans", 10), foreground=TEXTO)
        texto.tag_configure(
            LineaInforme.TITULO_RECOMENDACION,
            font=("DejaVu Sans", 10, "bold"),
            foreground=VERDE,
            spacing1=6,
        )
        texto.tag_configure(LineaInforme.RECOMENDACION, font=("DejaVu Sans", 9), foreground=TEXTO_SUAVE)
        texto.tag_configure(LineaInforme.ERROR, font=("DejaVu Sans", 10, "bold"), foreground=ERROR)
        texto.tag_configure(LineaInforme.AVISO, font=("DejaVu Sans", 10), foreground=TEXTO)

    def mostrar_informe(self, lineas: tuple[LineaInforme, ...]) -> None:
        self.texto.configure(state="normal")
        self.texto.delete("1.0", "end")
        for linea in lineas:
            if linea.rol == LineaInforme.SEPARADOR:
                self.texto.insert("end", "\n")
                continue
            inicio = self.texto.index("end-1c")
            self.texto.insert("end", linea.texto)
            self.texto.tag_add(linea.rol, inicio, self.texto.index("end-1c"))
            self.texto.insert("end", "\n")
        self.texto.configure(state="disabled")


class ValidadorEntrada:
    """Convierte el texto del formulario en valores del dominio."""

    @staticmethod
    def entero(texto: str, etiqueta: str) -> int:
        limpio = texto.strip()
        if not limpio:
            raise ValueError(f"Escribe {etiqueta}.")
        try:
            return int(limpio)
        except ValueError:
            raise ValueError(f"{etiqueta.capitalize()} no es un número válido.") from None

    @staticmethod
    def kwh(texto: str) -> float:
        limpio = texto.strip().replace(",", ".")
        if not limpio:
            raise ValueError("Consumo inválido: escribe los kWh del recibo con número.")
        try:
            return float(limpio)
        except ValueError:
            raise ValueError("Consumo inválido: escribe los kWh del recibo con número.") from None

    @staticmethod
    def bimestre(texto: str) -> Bimestre:
        bimestre = Bimestre.desde_texto(texto)
        if bimestre is None:
            raise ValueError("Bimestre inválido: selecciona un bimestre del recibo.")
        return bimestre


class Encabezado(tk.Frame):
    """Título de la ventana y resumen de la sesión."""

    def __init__(self, master: tk.Misc, texto_factor: str) -> None:
        super().__init__(master, bg=VERDE)
        tk.Label(
            self,
            text="EcoHuella",
            bg=VERDE,
            fg=BLANCO,
            font=("DejaVu Sans", 20, "bold"),
            anchor="w",
        ).pack(fill="x", padx=16, pady=(12, 0))
        tk.Label(
            self,
            text="Huella de carbono por consumo eléctrico",
            bg=VERDE,
            fg="#d9f2e4",
            font=("DejaVu Sans", 10),
            anchor="w",
        ).pack(fill="x", padx=16)
        tk.Label(
            self,
            text=texto_factor,
            bg=VERDE,
            fg=BLANCO,
            font=("DejaVu Sans", 9),
            anchor="w",
        ).pack(fill="x", padx=16, pady=(2, 8))
        barra = tk.Frame(self, bg=VERDE_OSCURO)
        barra.pack(fill="x")
        self._lbl_contexto = tk.Label(
            barra,
            text="",
            bg=VERDE_OSCURO,
            fg="#e7f6ee",
            font=("DejaVu Sans", 9),
            anchor="w",
        )
        self._lbl_contexto.pack(fill="x", padx=16, pady=6)

    def actualizar_contexto(self, texto: str) -> None:
        self._lbl_contexto.configure(text=texto)


class BarraEstado(tk.Label):
    """Mensajes de la última acción, en verde o en rojo."""

    def __init__(self, master: tk.Misc) -> None:
        super().__init__(
            master,
            text="Listo.",
            anchor="w",
            justify="left",
            bg=LATERAL,
            fg=VERDE,
            font=("DejaVu Sans", 9),
            padx=16,
            pady=8,
        )

    def avisar(self, texto: str, error: bool = False) -> None:
        self.configure(text=texto, fg=ERROR if error else VERDE)


class MenuLateral(tk.Frame):
    """Botones que cambian el panel visible."""

    def __init__(self, master: tk.Misc, entradas: tuple[tuple[str, str], ...], al_elegir, al_salir) -> None:
        super().__init__(master, bg=LATERAL)
        self._al_elegir = al_elegir
        self._botones: dict[str, tk.Button] = {}
        tk.Label(
            self,
            text="MENÚ",
            bg=LATERAL,
            fg=VERDE,
            font=("DejaVu Sans", 9, "bold"),
            anchor="w",
        ).pack(fill="x", padx=14, pady=(14, 6))
        for clave, texto in entradas:
            boton = tk.Button(
                self,
                text=texto,
                command=lambda c=clave: self._al_elegir(c),
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
            self._botones[clave] = boton
        tk.Frame(self, bg=LATERAL).pack(fill="both", expand=True)
        tk.Button(
            self,
            text="Salir",
            command=al_salir,
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

    def marcar(self, clave: str) -> None:
        for nombre, boton in self._botones.items():
            activo = nombre == clave
            boton.configure(
                bg=VERDE if activo else "#d5e6db",
                fg=BLANCO if activo else TEXTO,
                activebackground=VERDE_OSCURO if activo else "#c3ddd0",
                activeforeground=BLANCO if activo else TEXTO,
            )

    def etiquetas(self) -> tuple[str, ...]:
        return tuple(boton.cget("text") for boton in self._botones.values())


class PanelSeccion(tk.Frame):
    """Base de cada ventana del menú. Las secciones heredan el estilo común."""

    clave = ""
    etiqueta_menu = ""

    def __init__(self, master: tk.Misc, app: Aplicacion) -> None:
        super().__init__(master, bg=FONDO)
        self.app = app
        self.grid(row=0, column=0, sticky="nsew", padx=20, pady=16)
        self.columnconfigure(0, weight=1)
        self.construir()

    def construir(self) -> None:
        raise NotImplementedError

    def refrescar(self) -> None:
        return

    def titulo(self, titulo: str, subtitulo: str) -> None:
        tk.Label(
            self,
            text=titulo,
            bg=FONDO,
            fg=TEXTO,
            font=("DejaVu Sans", 16, "bold"),
            anchor="w",
        ).grid(row=0, column=0, sticky="ew")
        tk.Label(
            self,
            text=subtitulo,
            bg=FONDO,
            fg=TEXTO_SUAVE,
            font=("DejaVu Sans", 9),
            anchor="w",
            justify="left",
            wraplength=680,
        ).grid(row=1, column=0, sticky="ew", pady=(2, 12))

    def fila(self, parent: tk.Frame, fila: int, etiqueta: str, variable: tk.StringVar, ancho: int = 36) -> tk.Entry:
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

    def boton(self, parent: tk.Misc, texto: str, comando, primario: bool = True) -> tk.Button:
        if primario:
            colores = (VERDE, BLANCO, VERDE_OSCURO, BLANCO)
            fuente = ("DejaVu Sans", 10, "bold")
        else:
            colores = ("#d5e6db", TEXTO, "#c3ddd0", TEXTO)
            fuente = ("DejaVu Sans", 10)
        return tk.Button(
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


class PanelVivienda(PanelSeccion):
    clave = "vivienda"
    etiqueta_menu = "Registrar vivienda"

    def construir(self) -> None:
        self.titulo(
            "Registrar vivienda",
            "Dirección del hogar. Registrar otra vivienda reinicia habitantes y recibos.",
        )
        formulario = tk.Frame(self, bg=FONDO)
        formulario.grid(row=2, column=0, sticky="ew")
        formulario.columnconfigure(1, weight=1)
        self.var_direccion = tk.StringVar()
        entrada = self.fila(formulario, 0, "Dirección", self.var_direccion)
        entrada.bind("<Return>", lambda _evento: self._registrar())
        self.boton(self, "Registrar vivienda", self._registrar).grid(row=3, column=0, sticky="w", pady=(12, 8))
        self.lbl_actual = tk.Label(
            self,
            text="Vivienda actual: ninguna",
            bg=FONDO,
            fg=TEXTO,
            font=("DejaVu Sans", 10),
            anchor="w",
            justify="left",
            wraplength=680,
        )
        self.lbl_actual.grid(row=4, column=0, sticky="ew")

    def refrescar(self) -> None:
        self.lbl_actual.configure(text=self.app.sesion.descripcion_vivienda_actual())

    def _registrar(self) -> None:
        try:
            habia = self.app.sesion.registrar_vivienda(self.var_direccion.get())
        except ValueError as exc:
            self.app.avisar(str(exc), error=True)
            return
        direccion = self.app.sesion.vivienda.direccion
        self.app.sincronizar(limpiar_calculo=True)
        if habia:
            self.app.avisar(f"Vivienda registrada: {direccion}. Se reiniciaron habitantes y recibos.")
        else:
            self.app.avisar(f"Vivienda registrada: {direccion}.")


class PanelHabitantes(PanelSeccion):
    clave = "habitantes"
    etiqueta_menu = "Registrar habitantes"

    def construir(self) -> None:
        self.rowconfigure(6, weight=1)
        self.titulo(
            "Registrar habitantes",
            "Cada persona queda asociada a la vivienda. N es la cantidad de habitantes de la lista.",
        )
        formulario = tk.Frame(self, bg=FONDO)
        formulario.grid(row=2, column=0, sticky="ew")
        formulario.columnconfigure(1, weight=1)
        self.var_nombre = tk.StringVar()
        self.var_edad = tk.StringVar()
        self.var_identificacion = tk.StringVar()
        self.fila(formulario, 0, "Nombre", self.var_nombre)
        self.fila(formulario, 1, "Edad", self.var_edad)
        identificacion = self.fila(formulario, 2, "Identificación", self.var_identificacion)
        identificacion.bind("<Return>", lambda _evento: self._agregar())
        botones = tk.Frame(self, bg=FONDO)
        botones.grid(row=3, column=0, sticky="w", pady=(10, 6))
        self.boton(botones, "Agregar habitante", self._agregar).pack(side="left")
        self.boton(botones, "Quitar seleccionado", self._quitar, primario=False).pack(side="left", padx=(8, 0))
        self.lbl_total = tk.Label(
            self,
            text="Habitantes (N): 0",
            bg=FONDO,
            fg=TEXTO,
            font=("DejaVu Sans", 10, "bold"),
            anchor="w",
        )
        self.lbl_total.grid(row=4, column=0, sticky="ew", pady=(4, 6))
        self.tabla = Tabla(
            self,
            ("nombre", "edad", "identificacion"),
            ("Nombre", "Edad", "Identificación"),
            8,
        )
        self.tabla.grid(row=6, column=0, sticky="nsew")

    def refrescar(self) -> None:
        personas = () if self.app.sesion.vivienda is None else self.app.sesion.vivienda.habitantes
        self.tabla.llenar((persona.nombre, persona.edad, persona.identificacion) for persona in personas)
        self.lbl_total.configure(text=f"Habitantes (N): {len(personas)}")

    def _agregar(self) -> None:
        try:
            self.app.sesion.exigir_vivienda()
            edad = ValidadorEntrada.entero(self.var_edad.get(), "la edad")
            persona = self.app.sesion.agregar_habitante(
                self.var_nombre.get(),
                edad,
                self.var_identificacion.get(),
            )
        except ValueError as exc:
            self.app.avisar(str(exc), error=True)
            return
        self.var_nombre.set("")
        self.var_edad.set("")
        self.var_identificacion.set("")
        self.app.sincronizar(limpiar_calculo=True)
        self.app.avisar(f"Registrado: {persona.mostrar()}.")

    def _quitar(self) -> None:
        try:
            self.app.sesion.exigir_vivienda()
        except ValueError as exc:
            self.app.avisar(str(exc), error=True)
            return
        indice = self.tabla.indice_seleccionado()
        if indice is None:
            self.app.avisar("Selecciona un habitante.", error=True)
            return
        try:
            self.app.sesion.quitar_habitante(indice)
        except ValueError as exc:
            self.app.avisar(str(exc), error=True)
            return
        self.app.sincronizar(limpiar_calculo=True)
        self.app.avisar("Habitante quitado de la vivienda.")


class PanelConsumo(PanelSeccion):
    clave = "consumo"
    etiqueta_menu = "Registrar consumo eléctrico"

    def construir(self) -> None:
        self.rowconfigure(6, weight=1)
        self.titulo(
            "Registrar consumo eléctrico",
            "Captura los datos del recibo de luz. El consumo es el total del bimestre, en kWh.",
        )
        formulario = tk.Frame(self, bg=FONDO)
        formulario.grid(row=2, column=0, sticky="ew")
        formulario.columnconfigure(1, weight=1)
        self.var_kwh = tk.StringVar()
        self.var_bimestre = tk.StringVar()
        self.var_anio = tk.StringVar(value=str(date.today().year))
        self.fila(formulario, 0, "kWh del recibo", self.var_kwh)
        tk.Label(formulario, text="Bimestre", bg=FONDO, fg=TEXTO, font=("DejaVu Sans", 10)).grid(
            row=1, column=0, sticky="w", pady=4, padx=(0, 10)
        )
        self.combo = ttk.Combobox(
            formulario,
            textvariable=self.var_bimestre,
            values=Bimestre.opciones(),
            state="readonly",
            width=34,
            font=("DejaVu Sans", 10),
        )
        self.combo.grid(row=1, column=1, sticky="ew", pady=4)
        anio = self.fila(formulario, 2, "Año", self.var_anio)
        anio.bind("<Return>", lambda _evento: self._registrar())
        botones = tk.Frame(self, bg=FONDO)
        botones.grid(row=3, column=0, sticky="w", pady=(10, 6))
        self.boton(botones, "Registrar recibo", self._registrar).pack(side="left")
        self.boton(botones, "Quitar seleccionado", self._quitar, primario=False).pack(side="left", padx=(8, 0))
        self.tabla = Tabla(self, ("periodo", "kwh"), ("Bimestre", "kWh del recibo"), 8)
        self.tabla.grid(row=6, column=0, sticky="nsew")

    def refrescar(self) -> None:
        consumos = () if self.app.sesion.vivienda is None else self.app.sesion.vivienda.consumos
        self.tabla.llenar((consumo.periodo(), f"{consumo.kwh:.2f}") for consumo in consumos)

    def _registrar(self) -> None:
        try:
            self.app.sesion.exigir_vivienda()
            kwh = ValidadorEntrada.kwh(self.var_kwh.get())
            bimestre = ValidadorEntrada.bimestre(self.var_bimestre.get())
            anio = ValidadorEntrada.entero(self.var_anio.get(), "el año")
            consumo = self.app.sesion.registrar_consumo(kwh, bimestre, anio)
        except ValueError as exc:
            self.app.avisar(str(exc), error=True)
            return
        self.var_kwh.set("")
        self.app.sincronizar(limpiar_calculo=True)
        self.app.avisar(f"Recibo registrado: {consumo.resumen()}.")

    def _quitar(self) -> None:
        try:
            self.app.sesion.exigir_vivienda()
        except ValueError as exc:
            self.app.avisar(str(exc), error=True)
            return
        indice = self.tabla.indice_seleccionado()
        if indice is None:
            self.app.avisar("Selecciona un recibo.", error=True)
            return
        try:
            self.app.sesion.quitar_consumo(indice)
        except ValueError as exc:
            self.app.avisar(str(exc), error=True)
            return
        self.app.sincronizar(limpiar_calculo=True)
        self.app.avisar("Recibo eliminado.")


class PanelCalcular(PanelSeccion):
    clave = "calcular"
    etiqueta_menu = "Calcular huella de carbono"

    def construir(self) -> None:
        self.rowconfigure(5, weight=1)
        factor = self.app.sesion.factor
        promedio = self.app.sesion.calculadora.promedio_bimestral_kwh()
        self.titulo(
            "Calcular huella de carbono",
            (
                f"Ci = Ct / N    y    HC = Ci × FE "
                f"({factor.valor:.3f} kg CO2e/kWh). "
                f"Ct es el kWh del recibo. Se compara con {promedio:.0f} kWh por bimestre."
            ),
        )
        self.tabla = Tabla(self, ("periodo", "kwh"), ("Bimestre", "kWh del recibo"), 5)
        self.tabla.grid(row=2, column=0, sticky="ew")
        self.boton(self, "Calcular huella", self._calcular).grid(row=3, column=0, sticky="w", pady=8)
        self.caja = CajaTexto(self, 10)
        self.caja.grid(row=5, column=0, sticky="nsew")
        self.limpiar()

    def refrescar(self) -> None:
        consumos = () if self.app.sesion.vivienda is None else self.app.sesion.vivienda.consumos
        self.tabla.llenar((consumo.periodo(), f"{consumo.kwh:.2f}") for consumo in consumos)

    def limpiar(self) -> None:
        self.caja.poner("Selecciona un recibo y pulsa Calcular huella.")

    def _calcular(self) -> None:
        try:
            vivienda = self.app.sesion.exigir_vivienda()
        except ValueError as exc:
            self.app.avisar(str(exc), error=True)
            return
        if not vivienda.consumos:
            self.app.avisar("No hay recibos registrados.", error=True)
            return
        indice = self.tabla.indice_seleccionado()
        if indice is None:
            self.app.avisar("Selecciona un recibo.", error=True)
            return
        try:
            resultado, recomendacion = self.app.sesion.calcular_en(indice)
        except ValueError as exc:
            self.app.avisar(str(exc), error=True)
            self.caja.poner(str(exc))
            return
        self.caja.poner(f"{resultado.mostrar()}\n\n{recomendacion}")
        self.app.avisar("Cálculo realizado.")


class PanelResultados(PanelSeccion):
    clave = "resultados"
    etiqueta_menu = "Consultar resultados individuales"

    def construir(self) -> None:
        self.rowconfigure(2, weight=1)
        self.titulo(
            "Resultados individuales",
            "En verde, el consumo individual y las huellas. En ámbar, el resultado de cada habitante.",
        )
        self.caja = CajaResultados(self, 16)
        self.caja.grid(row=2, column=0, sticky="nsew")

    def refrescar(self) -> None:
        self.caja.mostrar_informe(self.app.sesion.lineas_resultados())


class PanelComparar(PanelSeccion):
    clave = "comparar"
    etiqueta_menu = "Comparar consumos bimestrales"

    def construir(self) -> None:
        self.rowconfigure(2, weight=1)
        promedio = self.app.sesion.calculadora.promedio_bimestral_kwh()
        self.titulo(
            "Comparar consumos bimestrales",
            f"Diferencia entre los recibos registrados y el promedio residencial de {promedio:.0f} kWh por bimestre.",
        )
        self.caja = CajaTexto(self, 16)
        self.caja.grid(row=2, column=0, sticky="nsew")

    def refrescar(self) -> None:
        self.caja.poner(self.app.sesion.comparar())


class Aplicacion(tk.Tk):
    """Ventana principal. Delega el estado en Sesion y cada pantalla en un panel."""

    PANELES = (
        PanelVivienda,
        PanelHabitantes,
        PanelConsumo,
        PanelCalcular,
        PanelResultados,
        PanelComparar,
    )

    def __init__(self) -> None:
        super().__init__()
        self.title("EcoHuella")
        self.geometry("1000x700")
        self.minsize(900, 640)
        self.configure(bg=FONDO)
        self.sesion = Sesion()
        self._paneles: dict[str, PanelSeccion] = {}
        self._configurar_estilo()
        self._construir_interfaz()
        self.sincronizar()
        self.mostrar("vivienda")

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

        factor = self.sesion.factor
        calculadora = self.sesion.calculadora
        texto_factor = (
            f"Factor de emisión: {factor.valor:.3f} kg CO2e/kWh ({factor.anio})"
            f"    ·    Promedio del recibo: {calculadora.promedio_bimestral_kwh():.0f} kWh/bimestre"
            f" ({calculadora.promedio_residencial_kwh():.0f} kWh/mes)"
        )
        self.encabezado = Encabezado(self, texto_factor)
        self.encabezado.grid(row=0, column=0, columnspan=2, sticky="ew")

        entradas = tuple((clase.clave, clase.etiqueta_menu) for clase in self.PANELES)
        self.menu = MenuLateral(self, entradas, self.mostrar, self.destroy)
        self.menu.grid(row=1, column=0, sticky="nsew")

        self.contenido = tk.Frame(self, bg=FONDO)
        self.contenido.grid(row=1, column=1, sticky="nsew")
        self.contenido.grid_rowconfigure(0, weight=1)
        self.contenido.grid_columnconfigure(0, weight=1)
        for clase in self.PANELES:
            panel = clase(self.contenido, self)
            self._paneles[clase.clave] = panel

        self.estado = BarraEstado(self)
        self.estado.grid(row=2, column=0, columnspan=2, sticky="ew")

    def panel(self, clave: str) -> PanelSeccion:
        return self._paneles[clave]

    def mostrar(self, clave: str) -> None:
        self._paneles[clave].tkraise()
        self.menu.marcar(clave)
        self._paneles[clave].refrescar()

    def avisar(self, texto: str, error: bool = False) -> None:
        self.estado.avisar(texto, error)

    def sincronizar(self, limpiar_calculo: bool = False) -> None:
        self.encabezado.actualizar_contexto(self.sesion.resumen_contexto())
        for clave in ("vivienda", "habitantes", "consumo", "calcular"):
            self._paneles[clave].refrescar()
        if limpiar_calculo:
            self.panel("calcular").limpiar()


def main() -> None:
    app = Aplicacion()
    app.mainloop()


if __name__ == "__main__":
    main()
