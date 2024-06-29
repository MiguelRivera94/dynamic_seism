class TratamientoRecord:
    def __init__(
        self,
        ruta_registro: str,
        filebasename: str,
        presentacion_datos: str = "Multiple Column",
        filas_inutiles: int = None,
        unidades_aceleracion: str = "g",
        factor_conversion: int = None,
        dt: float = None,
        realiza_correccion: str = "No",
        grado_cbaseline: int = 0,
        type_filtro: str = "Bandpass",
        fcorte1: float = None,
        fcorte2: int = None,
        grado_filtro: int = None,
        num_ventanas: int = None,
        zeta1: float = None,
        zeta2: float = None,
        deltazeta: float = None,
        Tevaluado: int = None,
        fregistros_90=[],
        isNew=True,
        numImages=None,
        numImagesDynamic=None,
        dynamic_amplification=False,
    ):
        self.ruta_registro = ruta_registro
        self.filebasename = filebasename
        self.presentacion_datos = presentacion_datos
        self.filas_inutiles = filas_inutiles
        self.unidades_aceleracion = unidades_aceleracion
        self.factor_conversion = factor_conversion
        self.dt = dt
        self.realiza_correccion = realiza_correccion
        self.grado_cbaseline = grado_cbaseline
        self.type_filtro = type_filtro
        self.fcorte1 = fcorte1
        self.fcorte2 = fcorte2
        self.grado_filtro = grado_filtro
        self.num_ventanas = num_ventanas
        self.zeta1 = zeta1
        self.zeta2 = zeta2
        self.deltazeta = deltazeta
        self.Tevaluado = Tevaluado
        self.fregistros_90 = fregistros_90
        self.dynamic_amplification = dynamic_amplification
        self.isNew = isNew
        self.numImages = numImages
        self.numImagesDynamic = numImagesDynamic

    def __repr__(self):
        return f"Tratamiento(ruta_registro='{self.ruta_registro}',filebasename='{self.filebasename}', presentacion_datos='{self.presentacion_datos}', filas_inutiles={self.filas_inutiles}, unidades_aceleracion='{self.unidades_aceleracion}', factor_conversion={self.factor_conversion}, dt={self.dt}, realiza_correccion={self.realiza_correccion}, grado_cbaseline={self.grado_cbaseline}, type_filtro='{self.type_filtro}', fcorte1={self.fcorte1}, fcorte2={self.fcorte2}, grado_filtro={self.grado_filtro}, num_ventanas={self.num_ventanas})"
