class TratamientoRecord:
    def __init__(
        self,
        ruta_registro: str, # Path to the record file
        filebasename: str,  # Basename of the file
        presentacion_datos: str = "Multiple Column", # Data presentation format
        filas_inutiles: int = None, # Number of useless rows
        unidades_aceleracion: str = "g", # Units of acceleration
        factor_conversion: int = None, # Conversion factor
        dt: float = None,  # Time step
        realiza_correccion: str = "No", # Whether baseline correction is performed
        grado_cbaseline: int = 0, # Degree of baseline correction
        type_filtro: str = "Bandpass", # Type of filter
        fcorte1: float = None, # First cutoff frequency
        fcorte2: int = None, # Second cutoff frequency
        grado_filtro: int = None, # Filter Order
        num_ventanas: int = None, # Number of windows
        zeta1: float = None, # First damping ratio
        zeta2: float = None, # Second damping ratio
        deltazeta: float = None, # Damping ratio increment
        Tevaluado: int = None, # Evaluated period
        fregistros_90=[], # 
        isNew=True,  # Whether the record is new
        numImages=None,  # Number of processed seismic record images
        numImagesDynamic=None, # Number of dynamic magnification images
        dynamic_amplification=False, # Whether dynamic amplification is enabled
        energy_90 = [],
        Rd_evaluado_lineal = None,
        Rd_evaluado_nolineal = None,
        zeta = None,
    ):
    # Assigning the parameters to instance variables.
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
        self.energy_90 = energy_90
        self.Rd_evaluado_lineal = Rd_evaluado_lineal
        self.Rd_evaluado_nolineal = Rd_evaluado_nolineal
        self.zeta = zeta
# The __repr__ method returns a string representation of the instance, use for a debug
    def __repr__(self):
        return f"Tratamiento(ruta_registro='{self.ruta_registro}',filebasename='{self.filebasename}', presentacion_datos='{self.presentacion_datos}', filas_inutiles={self.filas_inutiles}, unidades_aceleracion='{self.unidades_aceleracion}', factor_conversion={self.factor_conversion}, dt={self.dt}, realiza_correccion={self.realiza_correccion}, grado_cbaseline={self.grado_cbaseline}, type_filtro='{self.type_filtro}', fcorte1={self.fcorte1}, fcorte2={self.fcorte2}, grado_filtro={self.grado_filtro}, num_ventanas={self.num_ventanas})"
