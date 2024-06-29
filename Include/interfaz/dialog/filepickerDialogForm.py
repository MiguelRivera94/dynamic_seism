import tkinter as tk
from tkinter import ttk
import tkinter.filedialog
from tkinter import END,messagebox
import platform
import os
import sys
from datetime import datetime
from Include.tools import create_slug
from Include.tratamiento.record import TratamientoRecord
from pprint import pprint
from Include.validacion import es_entero, es_flotante


class FilerPickerDialogForm(tk.simpledialog.Dialog):
    def __init__(self,parentForm, tratamientos,proyectPath):
        #system_name = platform.system()
        #newTratamiento = TratamientoRecord('...','fgfgf')
        #print(repr(newTratamiento))
        #if system_name == "Windows":
        #    self.directory_separator = "\\"
        #else:
        self.returnDialog = False
        self.tratamientos = tratamientos
        self.currentTratamiento = None
        self.proyectPath = proyectPath
        self.directory_separator = "/"
        self.deletedItems = []
        # Crear la ventana principal
        #self.parentForm = parentForm
        #master = tk.Toplevel(self.parentForm)
        #master = tk.Tk()
        #master.title("Seleccionar Archivos")
        #master.state("zoomed")
        #master.resizable(0,0)
        #master.attributes('-toolwindow', True)

       
            
        #self.initialize()     
        super().__init__(parentForm, 'Load Seismic Records')

    def body(self,master):
        # Set the width of the dialog box
        #self.geometry("1024x768+{}+{}".format(master.winfo_rootx()+50, master.winfo_rooty()+50))
        #self.geometry("1024x768+%d+%d" % (master.winfo_rootx()+50, master.winfo_rooty()+50))       
        # Dimensiones del cuadro de diálogo
        dialog_width = 1024
        dialog_height = 768

        # Obtener dimensiones de la pantalla
        screen_width = master.winfo_screenwidth()
        screen_height = master.winfo_screenheight()

        # Calcular la posición para centrar el cuadro de diálogo
        x_position = (screen_width - dialog_width // 2) // 2
        y_position = (screen_height - dialog_height // 2) // 2     

        #centrar el diálogo
        self.geometry("{}x{}+{}+{}".format(dialog_width, dialog_height, x_position, y_position)) 

        self.wm_resizable(False, False)  
        # Crear un Frame en la parte superior con una barra de herramientas
        self.frame_superior = tk.Frame(master)
        self.frame_superior.pack(side="top", fill="x")

        # Crear un Frame en la parte central con un Listbox
        self.frame_central = tk.Frame(master)    
        self.frame_central.pack(side="top", fill="both", expand=True)
        #self.frame_central.configure(bg="lightgreen")

        self.frame1 = tk.Frame(self.frame_central)        
        #self.frame1.pack(fill="y", side="right")  # fill="y" significa que ocupará todo el alto

        self.frame2 = tk.Frame(self.frame_central)
        #self.frame2.pack(fill="both", expand=True)  # Ocupará todo el ancho y alto restante
        

        # Establecer el tamaño de cada frame vertical
        self.frame_central.grid_columnconfigure(0, weight=1)
        self.frame_central.grid_columnconfigure(1, weight=1)
        self.frame_central.grid_columnconfigure(1, minsize=512, weight=1)  # Ancho del padre dividido en dos
        # Añadir widgets u otros elementos a cada frame si es necesario
        # En este ejemplo, solo se están estableciendo colores de fondo para diferenciar los frames
        # Puedes agregar widgets u otros elementos según tus necesidades
        
        # Diseño de cuadrícula para los frames verticales
        self.frame2.grid(row=0, column=0, sticky="nsew")
        self.frame1.grid(row=0, column=1, sticky="nsew")

        # Ajustar el tamaño de los frames según el contenido interno
        self.frame2.grid_propagate(False)
        self.frame1.grid_propagate(False)        

        #anexar un frame en el lateral izquierdo
        self.framepropiedades = tk.Frame(self.frame1)
        self.framepropiedades.pack(side="top", fill="x")
        

#inicio de ingreso de controles
        # Etiquetas y cuadros de texto
        etiquetas = [            
            "Data Presentation:", 
            "Useless Rows:", 
            "Acceleration Units:",
            "Conversion Factor:", 
            "Dt (s):", 
            "Baseline Correction:",
            "Baseline C. Polynomial Degree:", 
            "Filter Type:", 
            "Cutoff Frequency 1 (Hz):",
            "Cutoff Frequency 2  (Hz):", 
            "Filter Order:", 
            "Number of Windows:"
        ]
        sample_etiquetas = [            
            "", 
            "Example: 4", 
            "",
            "Example: 1", 
            "Example: 0.005", 
            "",
            "", 
            "", 
            "Example: 0.1",
            "Example: 20", 
            "Example: 4", 
            "Example: 15"
        ]

        for i, etiqueta_texto in enumerate(etiquetas):
            etiqueta = tk.Label(self.framepropiedades, text=etiqueta_texto)
            etiqueta.grid(row=i, column=0, sticky="w")
            
        for i, etiqueta_texto in enumerate(sample_etiquetas):
            etiqueta = tk.Label(self.framepropiedades, text=etiqueta_texto)
            etiqueta.grid(row=i, column=2, sticky="w")

        tipo_presentacion_datos = ['Simple Column', 'Multiple Column', 'Time Acceleration']
        self.presentacion_datos_combo = ttk.Combobox(self.framepropiedades, values=tipo_presentacion_datos, state="readonly")
        self.presentacion_datos_combo.grid(row=0, column=1)

        self.filas_inutiles_entry = tk.Entry(self.framepropiedades, width=23)
        self.filas_inutiles_entry.grid(row=1, column=1)

        tipo_unidades_aceleracion = ["g","cm/s^2"]
        self.unidades_aceleracion_combo = ttk.Combobox(self.framepropiedades, values=tipo_unidades_aceleracion, state="readonly")
        self.unidades_aceleracion_combo.grid(row=2, column=1)

        self.factor_conversion_entry = tk.Entry(self.framepropiedades, width=23)
        self.factor_conversion_entry.grid(row=3, column=1)

        self.dt_entry = tk.Entry(self.framepropiedades, width=23)
        self.dt_entry.grid(row=4, column=1)

        tipo_realiza_correccion = ["Yes","No"]
        self.realiza_correccion_combo = ttk.Combobox(self.framepropiedades, values=tipo_realiza_correccion, state="readonly")
        self.realiza_correccion_combo.grid(row=5, column=1)

        #self.grado_cbaseline_entry = tk.Entry(self.framepropiedades, width=23)
        #self.grado_cbaseline_entry.grid(row=6, column=1)
        tipo_grado_cbaseline = [0,1,2,3,4]
        self.grado_cbaseline_combo = ttk.Combobox(self.framepropiedades, values=tipo_grado_cbaseline, state="readonly")
        self.grado_cbaseline_combo.grid(row=6, column=1)

        tipo_filtro = ["Highpass", "Lowpass", "Bandpass", "None"]
        self.type_filtro_entry_combo = ttk.Combobox(self.framepropiedades, values = tipo_filtro, state="readonly")
        self.type_filtro_entry_combo.grid(row=7, column=1)

        self.fcorte1_entry = tk.Entry(self.framepropiedades, width=23)
        self.fcorte1_entry.grid(row=8, column=1)

        self.fcorte2_entry = tk.Entry(self.framepropiedades, width=23)
        self.fcorte2_entry.grid(row=9, column=1)

        self.grado_filtro_entry = tk.Entry(self.framepropiedades, width=23)
        self.grado_filtro_entry.grid(row=10, column=1)

        self.num_ventanas_entry = tk.Entry(self.framepropiedades, width=23)
        self.num_ventanas_entry.grid(row=11, column=1)

        # Botón para guardar los datos ingresados
        self.boton_guardar = tk.Button(self.framepropiedades, text="Apply", command=self.guardar_datos)
        self.boton_guardar.grid(row=12, column=0)

        self.boton_eliminar = tk.Button(self.framepropiedades, text="Remove File", command=self.treeview_remove_item)
        self.boton_eliminar.grid(row=12, column=1)     

        self.boton_guardar.config(state=tk.DISABLED)      
        self.boton_eliminar.config(state=tk.DISABLED) 

#fin de ingreso de controles

        self.frameVisor = tk.Frame(self.frame1)
        #self.frameVisor.pack(fill=tk.BOTH, expand=True)
        self.frameVisor.pack(fill=tk.X)
        self.frameVisor.configure(height=40)
        

        # Create a Text widget to display the contents
        self.visorText = tk.Text(self.frameVisor, wrap=tk.NONE, state=tk.DISABLED)
        self.visorText.pack(fill="both", expand=True)

        # Crear barras de desplazamiento vertical y horizontal
        #self.vertical_scrollbar = tk.Scrollbar(self.frameVisor, command=self.visorText.yview)
        self.horizontal_scrollbar = tk.Scrollbar(self.frameVisor, command=self.visorText.xview, orient=tk.HORIZONTAL)

        #self.visorText.config(yscrollcommand=self.vertical_scrollbar.set)
        self.visorText.config(xscrollcommand=self.horizontal_scrollbar.set)
        
        
        # Configurar las barras de desplazamiento
        #self.vertical_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.horizontal_scrollbar.pack(side=tk.BOTTOM, fill=tk.X)



        # Crear un Treeview
        columnas = ["File","Data Presentation:", "Useless Rows:", "Acceleration Units:",
            "Conversion Factor:", "Dt:", "Baseline Correction:",
            "Baseline C. Degree:", "Filter Type:", "Cutoff Frequency 1  (Hz):",
            "Cutoff Frequency 2  (Hz):", "Filter Order:", "Number of Windows:"]
        self.treeview = ttk.Treeview(self.frame2, columns=columnas, show="headings")
        self.treeview.configure(height=32) 
        # Configurar las columnas
        for col in columnas:
            self.treeview.heading(col, text=col)
            self.treeview.column(col, width=100)  # Puedes ajustar el ancho según tus necesidades

        # Agregar el Treeview a un scroll vertical
        #scroll_y = ttk.Scrollbar(self.frame2, orient="vertical", command=self.treeview.yview)
        #self.treeview.configure(yscrollcommand=scroll_y.set)

        # Agregar el Treeview a un scroll horizontal
        scroll_x = ttk.Scrollbar(self.frame2, orient="horizontal", command=self.treeview.xview)
        self.treeview.configure(xscrollcommand=scroll_x.set)

        # Empaquetar los elementos en la ventana
        #self.treeview.pack(fill="both", expand=True)
        self.treeview.pack(fill="x")
        #scroll_y.pack(side="right", fill="y")
        scroll_x.pack(side="bottom", fill="x")

        #Asignar evento al treeview
        self.treeview.bind("<ButtonRelease-1>", self.treeview_item_seleccionado)
        # Configurar los eventos de teclas directamente en el TreeView
        self.treeview.bind("<KeyRelease-Up>", self.treeview_tecla_arriba)
        self.treeview.bind("<KeyRelease-Down>", self.treeview_tecla_abajo)

        # Crear un Frame en la parte inferior con dos botones
        self.frame_inferior = tk.Frame(master)
        self.frame_inferior.configure(relief="groove")
        self.frame_inferior.pack(side="top", fill="x")
        
        # Botón "Cerrar" en la ventana modal
        self.boton_seleccionar_archivos = tk.Button(self.frame_superior, text="Select Files", command=self.abrir_archivos,  bg="#333333", fg="#FFFFFF")
        self.boton_seleccionar_archivos.pack(side="left", padx=10)

        if(len(self.tratamientos)==0):
            self.selectedIndex = -1
        else:
            self.selectedIndex = 0
            self.treeview_load()
        
        # Botón "Cerrar" en la ventana modal
        #self.boton_cerrar = tk.Button(self.frame_inferior, text="Cerrar", command=self.closeForm )
        #self.boton_cerrar.pack(side="right", padx=10)

        # Botón "Cerrar" en la ventana modal
        #self.boton_aceptar = tk.Button(self.frame_inferior, text="Aceptar", command=self.closeReturnOKForm )
        #self.boton_aceptar.pack(side="right", padx=10)
    def apply(self):
        # Se llamará cuando el botón "OK" sea presionado
        self.closeReturnOKForm()


    def buscarUbicacion(self):
        self.proyectDirectory = tkinter.filedialog.askdirectory()
        master.focus_force()
        if self.proyectDirectory != None:
            self.locationproyectoLabel.config(text=self.proyectDirectory)
    
    def abrir_archivos(self):
        archivos = tkinter.filedialog.askopenfilenames(
            title="Select files",
            filetypes=[("Text files", "*.txt"),("Information files", "*.at2")]
        )
        
        if archivos:
            for file_path in archivos:
                file_name = os.path.basename(file_path)
                nuevoRegistro = TratamientoRecord(file_path,file_name)
                self.tratamientos.append(nuevoRegistro)
                print("Archivo seleccionado:", file_path)  
            self.treeview_load()       



    def treeview_load(self, selectIndex = None):     
        self.treeview_clean()   
        for tratamiento in self.tratamientos:
            self.treeview.insert('', 'end', values=(
                tratamiento.filebasename, tratamiento.presentacion_datos, tratamiento.filas_inutiles, tratamiento.unidades_aceleracion,
                tratamiento.factor_conversion, tratamiento.dt, tratamiento.realiza_correccion, tratamiento.grado_cbaseline,
                tratamiento.type_filtro, tratamiento.fcorte1, tratamiento.fcorte2, tratamiento.grado_filtro, tratamiento.num_ventanas
            ))
        print("fila actual desde treeview_load")
        print(selectIndex)
        # Seleccionar automáticamente el primer elemento
        if(len(self.tratamientos)>0):
            if selectIndex == None:
                first_item = self.treeview.get_children()[0]
                self.treeview.selection_set(first_item)
                self.asignarpropiedades()
            else:
                filaActual = self.treeview.get_children()[selectIndex]
                self.treeview.selection_set(filaActual)
                self.asignarpropiedades(selectIndex)
        else:
            self.selectedIndex = -1

    def asignarpropiedades(self, selectIndex = None):
        # Get the selected index
        if selectIndex == None :
            selected_iid = self.treeview.focus()        
            self.selectedIndex = self.treeview.index(selected_iid)
            print(self.selectedIndex)
        #seleccion = self.treeview.selection()
        #pprint(seleccion)
        self.currentTratamiento = self.tratamientos[self.selectedIndex]
        print(repr(self.currentTratamiento))
        ruta_archivo = self.currentTratamiento.ruta_registro
        if self.currentTratamiento.isNew == False:
            ruta_archivo = self.proyectPath + self.directory_separator + self.currentTratamiento.ruta_registro
        with open(ruta_archivo, 'r') as file:
            text = file.read()
            self.visorText.config(state=tk.NORMAL)  # Habilitar la edición temporalmente
            self.visorText.delete('1.0', tk.END)  # Limpiar el contenido existente
            self.visorText.insert('1.0', text)
            self.visorText.config(state=tk.DISABLED)  # Deshabilitar la edición

        self.boton_guardar.config(state=tk.NORMAL)      
        self.boton_eliminar.config(state=tk.NORMAL) 
        
        self.presentacion_datos_combo.set(self.currentTratamiento.presentacion_datos)

        self.filas_inutiles_entry.delete(0, tk.END)
        if self.currentTratamiento.filas_inutiles is not None:
            self.filas_inutiles_entry.insert(0, str(self.currentTratamiento.filas_inutiles))
        else:
            self.filas_inutiles_entry.insert(0, "")

        self.unidades_aceleracion_combo.set(self.currentTratamiento.unidades_aceleracion)

        self.factor_conversion_entry.delete(0, tk.END)
        if self.currentTratamiento.factor_conversion is not None:
            self.factor_conversion_entry.insert(0, str(self.currentTratamiento.factor_conversion))
        else:
            self.factor_conversion_entry.insert(0, "")

        self.dt_entry.delete(0, tk.END)
        if self.currentTratamiento.dt is not None:
            self.dt_entry.insert(0, str(self.currentTratamiento.dt))
        else:
            self.dt_entry.insert(0, "")

        self.realiza_correccion_combo.set(self.currentTratamiento.realiza_correccion)

        #self.grado_cbaseline_entry.delete(0, tk.END)
        #self.grado_cbaseline_entry.insert(0, str(self.currentTratamiento.grado_cbaseline))
        self.grado_cbaseline_combo.set(self.currentTratamiento.grado_cbaseline)

        self.type_filtro_entry_combo.set(self.currentTratamiento.type_filtro)

        self.fcorte1_entry.delete(0, tk.END)
        if self.currentTratamiento.fcorte1 is not None:
            self.fcorte1_entry.insert(0, str(self.currentTratamiento.fcorte1) )
        else:
            self.fcorte1_entry.insert(0, "" )

        self.fcorte2_entry.delete(0, tk.END)
        if self.currentTratamiento.fcorte2 is not None:
            self.fcorte2_entry.insert(0, str(self.currentTratamiento.fcorte2) )
        else:
            self.fcorte2_entry.insert(0, "" )

        self.grado_filtro_entry.delete(0, tk.END)
        if self.currentTratamiento.grado_filtro is not None:
            self.grado_filtro_entry.insert(0, str(self.currentTratamiento.grado_filtro))
        else:
            self.grado_filtro_entry.insert(0, "")

        
        self.num_ventanas_entry.delete(0, tk.END)
        if self.currentTratamiento.num_ventanas is not None:
            self.num_ventanas_entry.insert(0, str(self.currentTratamiento.num_ventanas) )
        else:
            self.num_ventanas_entry.insert(0, "" )

    def treeview_clean(self):
        self.treeview.delete(*self.treeview.get_children())
        self.visorText.config(state=tk.NORMAL)  # Habilitar la edición temporalmente
        self.visorText.delete('1.0', tk.END)  # Limpiar el contenido existente
        self.visorText.config(state=tk.DISABLED)  # Deshabilitar la edición  
        self.boton_guardar.config(state=tk.DISABLED)      
        self.boton_eliminar.config(state=tk.DISABLED)      

    def treeview_remove_item(self):
        selected_iid = self.treeview.focus()        
        item_index = self.treeview.index(selected_iid)
        deleted_tratamiento = self.tratamientos[item_index]
        if deleted_tratamiento.isNew == False:
            self.deletedItems.append(deleted_tratamiento)
            # Ruta del archivo que deseas eliminar
            ruta_archivo = self.proyectPath + "/" + deleted_tratamiento.ruta_registro  # Reemplaza con la ruta de tu archivo
            try:
                # Intenta eliminar el archivo
                os.remove(ruta_archivo)
                print(f"El archivo {ruta_archivo} se eliminó correctamente.")
            except FileNotFoundError:
                print(f"El archivo {ruta_archivo} no existe.")
            except Exception as e:
                print(f"Error al intentar eliminar el archivo {ruta_archivo}: {e}")            

        del self.tratamientos[item_index]    
        seleccion = self.treeview.selection()
        if seleccion:
            self.treeview.delete(seleccion)
        self.treeview_load()
        
    def treeview_item_seleccionado(self, event):
        self.asignarpropiedades()

    def treeview_tecla_arriba(self, event):
        self.asignarpropiedades()

    def treeview_tecla_abajo(self, event):
        self.asignarpropiedades()

    def closeForm(self):        
        #master.destroy()
        pass

    def closeReturnOKForm(self):
        self.returnDialog = True
        #master.destroy()
    
    def guardar_datos(self):
        # Obtener los valores ingresados
        con_errores = False
        if es_entero(self.filas_inutiles_entry.get()) == False: 
            con_errores = True
        if es_flotante(self.factor_conversion_entry.get()) == False: 
            con_errores = True
        if es_flotante(self.dt_entry.get()) == False: 
            con_errores = True
        if es_entero(self.grado_cbaseline_combo.get()) == False: 
            con_errores = True
        if es_flotante(self.fcorte1_entry.get()) == False: 
            con_errores = True
        if es_flotante(self.fcorte2_entry.get()) == False: 
            con_errores = True
        if es_entero(self.grado_filtro_entry.get()) == False: 
            con_errores = True
        if es_entero(self.num_ventanas_entry.get()) == False: 
            con_errores = True
            
        if con_errores == False:
            self.currentTratamiento.presentacion_datos = self.presentacion_datos_combo.get()
            self.currentTratamiento.filas_inutiles = int(self.filas_inutiles_entry.get())
            self.currentTratamiento.unidades_aceleracion = self.unidades_aceleracion_combo.get()
            self.currentTratamiento.factor_conversion = float(self.factor_conversion_entry.get())
            self.currentTratamiento.dt = float(self.dt_entry.get())
            self.currentTratamiento.realiza_correccion = self.realiza_correccion_combo.get()
            self.currentTratamiento.grado_cbaseline = int(self.grado_cbaseline_combo.get())
            self.currentTratamiento.type_filtro = self.type_filtro_entry_combo.get()
            self.currentTratamiento.fcorte1 = float(self.fcorte1_entry.get())
            self.currentTratamiento.fcorte2 = float(self.fcorte2_entry.get())
            self.currentTratamiento.grado_filtro = int(self.grado_filtro_entry.get())
            self.currentTratamiento.num_ventanas = int(self.num_ventanas_entry.get())
            
            print("fila actual desde guardar")
            print(self.selectedIndex)
            print(self.currentTratamiento)
            
            self.treeview_load(self.selectedIndex)  
        else:
            messagebox.showinfo(
                        "Alert", 'Verify that all data has been entered and is of the required data type'
                    )         
        

    def showModal(self):
        #master.focus_set()
        #master.grab_set()
        #master.wait_window(master)
        pass
