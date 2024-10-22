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
        # Initialize instance variables
        self.returnDialog = False # Variable to indicate dialog result
        self.tratamientos = tratamientos
        self.currentTratamiento = None # Currently selected treatment
        self.proyectPath = proyectPath # Project path
        self.directory_separator = "/" # Default directory separator
        self.deletedItems = [] # List of deleted items   
        super().__init__(parentForm, 'Load Seismic Records')

    def body(self,master):
        # Set the width of the dialog box
        # Initial setup of the main window
        dialog_width = 1024
        dialog_height = 768

        # Get screen dimensions
        screen_width = master.winfo_screenwidth()
        screen_height = master.winfo_screenheight()

        # position to center the dialog
        x_position = (screen_width - dialog_width // 2) // 2
        y_position = (screen_height - dialog_height // 2) // 2     

        # Center the dialog on the screen
        self.geometry("{}x{}+{}+{}".format(dialog_width, dialog_height, x_position, y_position)) 

        self.wm_resizable(False, False)  
        # Create top frame with toolbar
        self.frame_superior = tk.Frame(master)
        self.frame_superior.pack(side="top", fill="x")

        # Create central frame with Listbox and other elements
        self.frame_central = tk.Frame(master)    
        self.frame_central.pack(side="top", fill="both", expand=True)
        # Create subframes within the central frame
        self.frame1 = tk.Frame(self.frame_central)        
        #self.frame1.pack(fill="y", side="right")  # fill="y" significa que ocupará todo el alto
        self.frame2 = tk.Frame(self.frame_central)
        #self.frame2.pack(fill="both", expand=True)  # Ocupará todo el ancho y alto restante
        
        # Configure columns for the central frame
        # Set the size of each vertical frame
        self.frame_central.grid_columnconfigure(0, weight=1)
        self.frame_central.grid_columnconfigure(1, weight=1)
        self.frame_central.grid_columnconfigure(1, minsize=512, weight=1)  # Ancho del padre dividido en dos
        # Añadir widgets u otros elementos a cada frame si es necesario
        # En este ejemplo, solo se están estableciendo colores de fondo para diferenciar los frames
        # Puedes agregar widgets u otros elementos según tus necesidades
        
        # Layout for the vertical frames
        self.frame2.grid(row=0, column=0, sticky="nsew")
        self.frame1.grid(row=0, column=1, sticky="nsew")

        # Adjust the size of the frames according to the internal content
        self.frame2.grid_propagate(False)
        self.frame1.grid_propagate(False)        

        # Add a frame on the left side
        self.framepropiedades = tk.Frame(self.frame1)
        self.framepropiedades.pack(side="top", fill="x")
        

        # Labels 
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
        # Sample Labels
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
        # Create labels for properties
        for i, etiqueta_texto in enumerate(etiquetas):
            etiqueta = tk.Label(self.framepropiedades, text=etiqueta_texto)
            etiqueta.grid(row=i, column=0, sticky="w")
        # Create example labels for properties 
        for i, etiqueta_texto in enumerate(sample_etiquetas):
            etiqueta = tk.Label(self.framepropiedades, text=etiqueta_texto)
            etiqueta.grid(row=i, column=2, sticky="w")
        # Data types for ComboBoxes and Entries
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

        # Button to save the entered data
        self.boton_guardar = tk.Button(self.framepropiedades, text="Apply", command=self.guardar_datos)
        self.boton_guardar.grid(row=12, column=0)
        # Button to remove seismic records
        self.boton_eliminar = tk.Button(self.framepropiedades, text="Remove File", command=self.treeview_remove_item)
        self.boton_eliminar.grid(row=12, column=1)     

        self.boton_guardar.config(state=tk.DISABLED)      
        self.boton_eliminar.config(state=tk.DISABLED) 

        # End of control input

        self.frameVisor = tk.Frame(self.frame1)
        self.frameVisor.pack(fill=tk.X)
        self.frameVisor.configure(height=40)
        

        # A text widget will be created to display the content
        self.visorText = tk.Text(self.frameVisor, wrap=tk.NONE, state=tk.DISABLED)
        self.visorText.pack(fill="both", expand=True)

        # Create horizontal scrollbar
        #self.vertical_scrollbar = tk.Scrollbar(self.frameVisor, command=self.visorText.yview)
        self.horizontal_scrollbar = tk.Scrollbar(self.frameVisor, command=self.visorText.xview, orient=tk.HORIZONTAL)

        #self.visorText.config(yscrollcommand=self.vertical_scrollbar.set)
        self.visorText.config(xscrollcommand=self.horizontal_scrollbar.set)
        
        
        # Configure the horizontal scrollbar
        #self.vertical_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.horizontal_scrollbar.pack(side=tk.BOTTOM, fill=tk.X)



        # Create a Treatview to summarize the data entered by the user 
        # regarding seismic record processing and analysis
        columnas = ["File","Data Presentation:", "Useless Rows:", "Acceleration Units:",
            "Conversion Factor:", "Dt:", "Baseline Correction:",
            "Baseline C. Degree:", "Filter Type:", "Cutoff Frequency 1  (Hz):",
            "Cutoff Frequency 2  (Hz):", "Filter Order:", "Number of Windows:"]
        self.treeview = ttk.Treeview(self.frame2, columns=columnas, show="headings")
        self.treeview.configure(height=32) 
        # Configure the columns
        for col in columnas:
            self.treeview.heading(col, text=col)
            self.treeview.column(col, width=100)  # Puedes ajustar el ancho según tus necesidades

        # Agregar el Treeview a un scroll vertical

        # Add the Treeview to a horizontal scrollbar
        scroll_x = ttk.Scrollbar(self.frame2, orient="horizontal", command=self.treeview.xview)
        self.treeview.configure(xscrollcommand=scroll_x.set)

        # Pack the elements in the window
        #self.treeview.pack(fill="both", expand=True)
        self.treeview.pack(fill="x")
        #scroll_y.pack(side="right", fill="y")
        scroll_x.pack(side="bottom", fill="x")

        #Asignar evento al treeview
        # Bind events to the Treeview
        self.treeview.bind("<ButtonRelease-1>", self.treeview_item_seleccionado)
        # Configurar los eventos de teclas directamente en el TreeView
        self.treeview.bind("<KeyRelease-Up>", self.treeview_tecla_arriba)
        self.treeview.bind("<KeyRelease-Down>", self.treeview_tecla_abajo)

        # Create a Frame at the bottom with two buttons
        self.frame_inferior = tk.Frame(master)
        self.frame_inferior.configure(relief="groove")
        self.frame_inferior.pack(side="top", fill="x")
        
        # Button to select files in the modal window
        self.boton_seleccionar_archivos = tk.Button(self.frame_superior, text="Select Files", command=self.abrir_archivos,  bg="#333333", fg="#FFFFFF")
        self.boton_seleccionar_archivos.pack(side="left", padx=10)
        # Check if there are treatments to load into the Treeview
        if(len(self.tratamientos)==0):
            self.selectedIndex = -1 # No treatments available
        else:
            self.selectedIndex = 0 # Select the first treatment
            self.treeview_load()   # Load treatments into the Treeview
        
    def apply(self):
        # It is activated when we click ok
        self.closeReturnOKForm() # Call the method to close the form and return OK status
 

    def buscarUbicacion(self):
        # select a directory and store the selected path in self.proyectDirectory
        self.proyectDirectory = tkinter.filedialog.askdirectory()
        # Bring the master window to focus
        master.focus_force()
        # If a directory is selected, update the label text to show the selected directory path
        if self.proyectDirectory != None:
            self.locationproyectoLabel.config(text=self.proyectDirectory)
    
    def abrir_archivos(self):
        # Open a file dialog to select multiple files with specified file types
        archivos = tkinter.filedialog.askopenfilenames(
            title="Select files",
            filetypes=[("Text files", "*.txt"),("Information files", "*.at2")]
        )
        # If files are selected
        if archivos:
            # Iterate over the seismic records files
            for file_path in archivos:
                # Obtain the name of the seismic record through the path of this record
                file_name = os.path.basename(file_path)
                # Create a new seismic record file based on its name and path
                nuevoRegistro = TratamientoRecord(file_path,file_name)
                # Append the new seismic record to the treatments list
                self.tratamientos.append(nuevoRegistro)
                # Print the selected file path
                print("Archivo seleccionado:", file_path)  
            self.treeview_load() # Load the tree view with the new records      



    def treeview_load(self, selectIndex = None):     
        # Clean the Treeview before loading new data
        self.treeview_clean()   
        # Enter the user's data into the TreatView in the Load Seismic Records module
        for tratamiento in self.tratamientos:
            self.treeview.insert('', 'end', values=(
                tratamiento.filebasename, tratamiento.presentacion_datos, tratamiento.filas_inutiles, tratamiento.unidades_aceleracion,
                tratamiento.factor_conversion, tratamiento.dt, tratamiento.realiza_correccion, tratamiento.grado_cbaseline,
                tratamiento.type_filtro, tratamiento.fcorte1, tratamiento.fcorte2, tratamiento.grado_filtro, tratamiento.num_ventanas
            ))
        # Print the current row from treeview_load
        print("fila actual desde treeview_load")
        print(selectIndex)
        # Automatically select the first item if there are treatments
        if(len(self.tratamientos)>0):
            if selectIndex == None:
                # Select the first item if no specific index is provided
                first_item = self.treeview.get_children()[0]
                self.treeview.selection_set(first_item)
                self.asignarpropiedades()
            else:
                # Select the item at the specified index
                filaActual = self.treeview.get_children()[selectIndex]
                self.treeview.selection_set(filaActual)
                self.asignarpropiedades(selectIndex)
        else:
            # If there are no treatments, set the selectedIndex to -1
            self.selectedIndex = -1

    def asignarpropiedades(self, selectIndex = None):
        # Get the selected index
        if selectIndex == None :
            selected_iid = self.treeview.focus()        
            self.selectedIndex = self.treeview.index(selected_iid)
            print(self.selectedIndex)
        #seleccion = self.treeview.selection()
        #pprint(seleccion)
        # Get the current treatment based on the selected index
        self.currentTratamiento = self.tratamientos[self.selectedIndex]
        print(repr(self.currentTratamiento))
        # Determine the file path for the treatment
        ruta_archivo = self.currentTratamiento.ruta_registro
        if self.currentTratamiento.isNew == False:
            ruta_archivo = self.proyectPath + self.directory_separator + self.currentTratamiento.ruta_registro
        # Allows you to view the contents of a seismic record in a text viewer
        with open(ruta_archivo, 'r') as file:
            text = file.read()
            self.visorText.config(state=tk.NORMAL)  # Habilitar la edición temporalmente
            self.visorText.delete('1.0', tk.END)  # Limpiar el contenido existente
            self.visorText.insert('1.0', text)
            self.visorText.config(state=tk.DISABLED)  # Deshabilitar la edición
        # Enable the save and delete buttons
        self.boton_guardar.config(state=tk.NORMAL)      
        self.boton_eliminar.config(state=tk.NORMAL) 
        # Set the values of the form fields based on the current treatment's properties
        self.presentacion_datos_combo.set(self.currentTratamiento.presentacion_datos)
        # Clear and set the 'filas_inutiles' entry to the value from the current treatment, if available
        self.filas_inutiles_entry.delete(0, tk.END)
        if self.currentTratamiento.filas_inutiles is not None:
            self.filas_inutiles_entry.insert(0, str(self.currentTratamiento.filas_inutiles))
        else:
            self.filas_inutiles_entry.insert(0, "")
        # Set the 'unidades_aceleracion' combo box to the value from the current treatment
        self.unidades_aceleracion_combo.set(self.currentTratamiento.unidades_aceleracion)
        # Clear and set the 'factor_conversion' entry to the value from the current treatment, if available
        self.factor_conversion_entry.delete(0, tk.END)
        if self.currentTratamiento.factor_conversion is not None:
            self.factor_conversion_entry.insert(0, str(self.currentTratamiento.factor_conversion))
        else:
            self.factor_conversion_entry.insert(0, "")
        # Clear and set the 'dt' entry to the value from the current treatment, if available
        self.dt_entry.delete(0, tk.END)
        if self.currentTratamiento.dt is not None:
            self.dt_entry.insert(0, str(self.currentTratamiento.dt))
        else:
            self.dt_entry.insert(0, "")
        # Set the 'realiza_correccion' combo box to the value from the current treatment
        self.realiza_correccion_combo.set(self.currentTratamiento.realiza_correccion)
        self.grado_cbaseline_combo.set(self.currentTratamiento.grado_cbaseline)
        # Set the 'type_filtro' combo box to the value from the current treatment
        self.type_filtro_entry_combo.set(self.currentTratamiento.type_filtro)
        # Clear and set the 'fcorte1' entry to the value from the current treatment, if available
        self.fcorte1_entry.delete(0, tk.END)
        if self.currentTratamiento.fcorte1 is not None:
            self.fcorte1_entry.insert(0, str(self.currentTratamiento.fcorte1) )
        else:
            self.fcorte1_entry.insert(0, "" )
        # Clear and set the 'fcorte2' entry to the value from the current
        self.fcorte2_entry.delete(0, tk.END)
        if self.currentTratamiento.fcorte2 is not None:
            self.fcorte2_entry.insert(0, str(self.currentTratamiento.fcorte2) )
        else:
            self.fcorte2_entry.insert(0, "" )
        # Clear and set the 'grado_filtro' entry to the value from the current treatment, if available
        self.grado_filtro_entry.delete(0, tk.END)
        if self.currentTratamiento.grado_filtro is not None:
            self.grado_filtro_entry.insert(0, str(self.currentTratamiento.grado_filtro))
        else:
            self.grado_filtro_entry.insert(0, "")

        # Clear and set the 'num_ventanas' entry to the value from the current treatment, if available
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
        # Select a seismic record file on Treeview
        selected_iid = self.treeview.focus()   
        # Obtain the number that identifies the selected seismic record 
        item_index = self.treeview.index(selected_iid)
        # Retrieve the tratamiento (record) from the list of tratamientos
        deleted_tratamiento = self.tratamientos[item_index]
        # Check if the tratamiento is not new before proceeding with deletion
        if deleted_tratamiento.isNew == False:
            # Add the deleted tratamiento to the deletedItems list
            self.deletedItems.append(deleted_tratamiento)
            # Construct the full path to the file to be deleted
            ruta_archivo = self.proyectPath + "/" + deleted_tratamiento.ruta_registro  # Reemplaza con la ruta de tu archivo
            try:
                # Attempt to remove the file
                os.remove(ruta_archivo)
                print(f"El archivo {ruta_archivo} se eliminó correctamente.")
            except FileNotFoundError:
                print(f"El archivo {ruta_archivo} no existe.")
            except Exception as e:
                print(f"Error al intentar eliminar el archivo {ruta_archivo}: {e}")            
        # Remove the tratamiento from the tratamientos list
        del self.tratamientos[item_index]    
        # Remove the selected item from the Treeview display
        seleccion = self.treeview.selection()
        if seleccion:
            self.treeview.delete(seleccion)
        self.treeview_load() # Reload the Treeview to reflect the updated tratamientos list
        
    def treeview_item_seleccionado(self, event):
        self.asignarpropiedades() # Calls a method to assign properties.

    def treeview_tecla_arriba(self, event):
        self.asignarpropiedades() # Calls a method to assign properties.

    def treeview_tecla_abajo(self, event):
        self.asignarpropiedades() # Calls a method to assign properties.

    def closeForm(self):        
        #master.destroy() Uncomment to destroy the main window.
        pass

    def closeReturnOKForm(self):
        self.returnDialog = True
        #master.destroy() Uncomment to destroy the main window.
    
    def guardar_datos(self):
        # Obtener los valores
        con_errores = False # Flag to track if there are errors.
        # Logic to check if it's not an integer value
        if es_entero(self.filas_inutiles_entry.get()) == False: 
            con_errores = True
        # Logic to check if it's not an float value
        if es_flotante(self.factor_conversion_entry.get()) == False: 
            con_errores = True
        # Logic to check if it's not an float value
        if es_flotante(self.dt_entry.get()) == False: 
            con_errores = True
        # Logic to check if it's not an integer value
        if es_entero(self.grado_cbaseline_combo.get()) == False: 
            con_errores = True
        # Logic to check if it's not an float value
        if es_flotante(self.fcorte1_entry.get()) == False: 
            con_errores = True
        # Logic to check if it's not an float value
        if es_flotante(self.fcorte2_entry.get()) == False: 
            con_errores = True
        # Logic to check if it's not an integer value
        if es_entero(self.grado_filtro_entry.get()) == False: 
            con_errores = True
        # Logic to check if it's not an integer value
        if es_entero(self.num_ventanas_entry.get()) == False: 
            con_errores = True
            
        if con_errores == False: # If there are no errors:
            # Assign values from inputs to currentTratamiento object attributes.
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
            print(self.selectedIndex) # Prints current index.
            print(self.currentTratamiento) # Prints current treatment object.
            
            self.treeview_load(self.selectedIndex)  # Calls a method to reload treeview data
        else:
            # Shows an info message if there are input errors.
            messagebox.showinfo(
                        "Alert", 'Verify that all data has been entered and is of the required data type'
                    )
        

    def showModal(self):
        #master.focus_set()
        #master.grab_set()
        #master.wait_window(master)
        pass # Placeholder function, does nothing.
