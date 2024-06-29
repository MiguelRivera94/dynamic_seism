import tkinter as tk
from tkinter import (
    LEFT,
    END,
    TOP,
    X,
    FLAT,
    RAISED,
    filedialog,
    messagebox,
)
from Include.tools import create_slug
from Include.interfaz.dialog.filepickerDialogForm import FilerPickerDialogForm
from Include.interfaz.dialog.nuevoproyectoDialogForm import NuevoProyectoDialog
from Include.interfaz.dialog.dynamicamplificationDialogForm import (
    DynamicAmplificationDialogo,
)
from Include.tratamiento.record import TratamientoRecord
from Include.tratamiento.registroresumen import RegistroResumen
from Include.tratamiento.dynamicamplification import DynamicAmplification
from pathlib import Path
import shutil
import os
import json
import tkinterweb
import sys
import time


class MainForm(tk.Tk):
    def __init__(self):
        super().__init__()

        if getattr(sys, "frozen", False) and hasattr(sys, "_MEIPASS"):
            self.current_directory = os.path.join(sys._MEIPASS)
        else:
            self.current_directory = os.getcwd()

        self.iconbitmap(self.current_directory + os.sep + "resources/icons/iconapp.ico")
        self.tratamientos = []
        self.titleWindow = "Dynamic Seism"
        self.title(self.titleWindow)
        self.state("zoomed")
        self.protocol("WM_DELETE_WINDOW", self.salir)
        self.tratamientos = []
        self.proyectName = ""
        self.currentTratamiento = None

        self.homePage = f"{self.current_directory}/resources/html/home.html"
        self.nodataPage = f"{self.current_directory}/resources/html/nodata.html"
        self.nodataPageda = f"{self.current_directory}/resources/html/nodatada.html"

        self.proyectDirectory = None
        if self.proyectDirectory == None:
            if getattr(sys, "frozen", False) and hasattr(sys, "_MEIPASS"):
                self.current_directory = os.path.join(sys._MEIPASS)
            else:
                self.current_directory = os.getcwd()
            self.proyectDirectory = (
                self.current_directory.replace("\\", os.sep) + os.sep + "projects"
            )
            print(self.proyectDirectory)

        self.initialize()

    def initialize(self):
        self.mainMenu = tk.Menu(self)
        self.config(menu=self.mainMenu)

        # Crear un menú "Archivo"
        self.menu_archivo = tk.Menu(self.mainMenu)
        self.mainMenu.add_cascade(label="File", menu=self.menu_archivo)
        self.menu_archivo.add_command(label="New", command=self.nuevo)
        self.menu_archivo.add_command(label="Open", command=self.abrir)
        self.menu_archivo.add_command(label="Save as...", command=self.guardar)
        self.menu_archivo.add_separator()
        self.menu_archivo.add_command(label="Exit", command=self.salir)

        self.menu_archivo.entryconfigure(3, state="disabled")

        self.frame_superior = tk.Frame(self)
        self.frame_superior.pack(side="top", fill="x")
        self.label1 = tk.Label(
            self.frame_superior,
            text="Project Location",
            wraplength=700,
            width=20,
            justify="right",
            anchor="w",
        )
        self.label1.grid(row=1, column=1)

        self.locationproyectoLabel = tk.Label(
            self.frame_superior,
            text=self.proyectDirectory,
            wraplength=700,
            width=100,
            borderwidth=1,
            relief="solid",
            justify="left",
            anchor="w",
        )
        self.locationproyectoLabel.grid(row=1, column=2)

        self.label2 = tk.Label(
            self.frame_superior,
            text="Project Name",
            wraplength=700,
            width=20,
            justify="right",
            anchor="w",
        )
        self.label2.grid(row=2, column=1)

        self.proyectnameEntry = tk.Label(
            self.frame_superior,
            text=self.proyectName,
            wraplength=700,
            width=100,
            justify="left",
            anchor="w",
            borderwidth=1,
            relief="solid",
        )

        self.proyectnameEntry.grid(row=2, column=2)
        # Crear la barra de herramientasindow
        self.barra_herramientas = tk.Frame(self, bd=1, relief=RAISED)
        self.barra_herramientas.pack(fill="x")

        # Crear el botón en la barra de herramientas
        self.boton_selector = tk.Button(
            self.barra_herramientas,
            text="Load Seismic Records",
            command=self.openFilePicker,
            bg="#333333", fg="#FFFFFF"
        )
        self.boton_selector.pack(side="left")
        self.boton_selector.config(state="disabled")

        self.calcular_dynamic = tk.Button(
            self.barra_herramientas,
            text="Calculate Dynamic Magnification",
            command=self.calcular_dynamic_click,
            bg="#333333", fg="#FFFFFF"
        )
        self.calcular_dynamic.pack(side="left")
        self.calcular_dynamic.config(state="disabled")

        self.leftframe = tk.Frame(self)
        self.leftframe.pack(side=tk.LEFT, fill=tk.Y)

        self.archivoslistbox = tk.Listbox(self.leftframe, width=50)
        self.archivoslistbox.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        self.archivoslistbox.bind(
            "<<ListboxSelect>>", self.archivoslistbox_on_listbox_select
        )

        # Crear el segundo frame (frame_interior) dentro del frame_exterior
        self.frame_interior = tk.Frame(self.leftframe, padx=10, pady=10)
        self.frame_interior.pack(side="bottom", fill="both")
        # Agregar un botón al frame_interior
        self.boton_eliminar = tk.Button(
            self.frame_interior,
            text="Delete current file",
            command=self.boton_eliminar_click,
            justify="center",
        )
        self.boton_eliminar.pack(side="right")
        self.boton_eliminar.config(state="disabled")

        # Marco en el resto de la ventana
        self.rightframe = tk.Frame(self)
        self.rightframe.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Crear la barra de herramientasindow
        self.barra_herramientas_nav = tk.Frame(self.rightframe, bd=1, relief=RAISED)
        self.barra_herramientas_nav.pack(fill="x")

        # Variable para rastrear la selección
        self.seleccion_var = tk.StringVar()
        self.seleccion_var.set("home")
        # Crear los Radiobuttons
        self.nav_opcion1 = tk.Radiobutton(
            self.barra_herramientas_nav,
            indicatoron=0,
            command=self.ShowNavVisor_select,
            text="Home",
            variable=self.seleccion_var,
            value="home",
        )
        self.nav_opcion2 = tk.Radiobutton(
            self.barra_herramientas_nav,
            indicatoron=0,
            command=self.ShowNavVisor_select,
            text="Seismic Record Processing and Signal Frequency Content Charts",
            variable=self.seleccion_var,
            value="graph1",
        )
        self.nav_opcion3 = tk.Radiobutton(
            self.barra_herramientas_nav,
            indicatoron=0,
            command=self.ShowNavVisor_select,
            text="Dynamic Magnification Charts",
            variable=self.seleccion_var,
            value="graph2",
        )

        # Empaquetar los Radiobuttons horizontalmente usando el método pack
        self.nav_opcion1.pack(side="left", padx=5)
        self.nav_opcion2.pack(side="left", padx=5)
        self.nav_opcion3.pack(side="left", padx=5)

        self.webbrowser = tkinterweb.HtmlFrame(
            self.rightframe, messages_enabled=False
        )  # create HTML browser
        self.loadPage("home")
        # load a website
        self.webbrowser.pack(
            fill="both", expand=True
        )  # attach the HtmlFrame widget to the parent window

    def recursive_overwrite(self, src, dest, ignore=None):
        if os.path.isdir(src):
            if not os.path.isdir(dest):
                os.makedirs(dest)
            files = os.listdir(src)
            if ignore is not None:
                ignored = ignore(src, files)
            else:
                ignored = set()
            for f in files:
                if f not in ignored:
                    self.recursive_overwrite(
                        os.path.join(src, f), os.path.join(dest, f), ignore
                    )
        else:
            shutil.copyfile(src, dest)

    def buscarUbicacion(self):
        directorioTemporal = filedialog.askdirectory()
        # self.focus_force()
        print(self.proyectDirectory)
        if not directorioTemporal:
            print("cancelado")
        else:
            if self.proyectName != "":
                ruta_directorio = directorioTemporal + "/" + self.proyectName
                if os.path.exists(ruta_directorio) and os.path.isdir(ruta_directorio):
                    messagebox.showinfo(
                        "Alerta", f'The directory "{directorioTemporal}" already exists.'
                    )
                else:
                    self.proyectDirectory = directorioTemporal
                    self.proyectPath = self.proyectDirectory + "/" + self.proyectName
                    self.locationproyectoLabel.config(text=self.proyectDirectory)
                    self.CrearCarpetas()
            else:
                self.proyectDirectory = directorioTemporal
                self.proyectPath = self.proyectDirectory + "/" + self.proyectName
                self.locationproyectoLabel.config(text=self.proyectDirectory)

    def eliminar_archivos_y_carpetas(self, rutas):
        for ruta in rutas:
            if os.path.exists(ruta):
                if os.path.isfile(ruta):
                    # Eliminar archivo
                    os.remove(ruta)
                    print(f"Archivo eliminado: {ruta}")
                elif os.path.isdir(ruta):
                    # Eliminar carpeta y su contenido de manera recursiva
                    shutil.rmtree(ruta)
                    print(f"Carpeta eliminada recursivamente: {ruta}")
                else:
                    print(f"Ruta no reconocida: {ruta}")
            else:
                print(f"La ruta no existe: {ruta}")

    def eliminar_item(self, tratamiento_deleted: TratamientoRecord):
        rutas_a_eliminar = [
            f"{self.proyectPath}/files/{tratamiento_deleted.filebasename}",
            f"{self.proyectPath}/results/html/{tratamiento_deleted.filebasename}.html",
            f"{self.proyectPath}/results/html/{tratamiento_deleted.filebasename}.temporal.html",
            f"{self.proyectPath}/results/pdf/{tratamiento_deleted.filebasename}.pdf",
            f"{self.proyectPath}/results/html/images/{tratamiento_deleted.filebasename}",
            f"{self.proyectPath}/results/xlsx/{tratamiento_deleted.filebasename}.xlsx",
            f"{self.proyectPath}/results/html/da_{tratamiento_deleted.filebasename}.html",
            f"{self.proyectPath}/results/html/da_{tratamiento_deleted.filebasename}.temporal.html",
            f"{self.proyectPath}/results/pdf/da_{tratamiento_deleted.filebasename}.pdf",
            f"{self.proyectPath}/results/html/images/da_{tratamiento_deleted.filebasename}",
        ]
        print(rutas_a_eliminar)
        self.eliminar_archivos_y_carpetas(rutas_a_eliminar)

    def boton_eliminar_click(self):
        selected_index = self.archivoslistbox.index("active")
        if selected_index >= 0 and len(self.tratamientos) > 0:
            print(selected_index)
            print(len(self.tratamientos))
            respuesta = messagebox.askyesno(
                "Confirm Deletion", "Are you sure to delete? (Yes/No)"
            )
            if respuesta:
                tratamiento_deleted = self.tratamientos.pop(selected_index)
                print(tratamiento_deleted)
                self.eliminar_item(tratamiento_deleted)
                self.llenarListBox()
                self.saveconfigproject()
                print("Eliminar")
            else:
                print("Cancelar")

    # Funciones para los comandos del menú
    def nuevo(self):
        # Agregar aquí la lógica para crear un nuevo archivo o realizar una acción
        # nuevo_proyecto_dialogo = NuevoProyectoDialog(self, "Nuevo Proyecto")
        # resultado = nuevo_proyecto_dialogo.result

        # Mostrar el cuadro de diálogo para seleccionar un directorio
        carpeta_seleccionada = filedialog.askdirectory(
            title="Select folder for the project",
            initialdir=self.proyectDirectory
        )
        # print(carpeta_seleccionada)
        if carpeta_seleccionada:
            nuevo_proyecto_dialogo = NuevoProyectoDialog(self, "New Project Name")
            resultado = nuevo_proyecto_dialogo.result
            if resultado is not None and resultado.strip():
                temp_proyectpath = f"{carpeta_seleccionada}{os.path.sep}{resultado}"
                if os.path.exists(temp_proyectpath) and os.path.isdir(
                    temp_proyectpath
                ):
                    messagebox.showinfo(
                        "Alert",
                        f'A project already exists in the folder "{carpeta_seleccionada} with the name {resultado}".',
                    )
                else:
                    self.tratamientos = []
                    self.seleccion_var.set('home')
                    self.loadPage(self.seleccion_var.get())
                    self.proyectName = resultado
                    self.proyectPath = temp_proyectpath
                    self.proyectDirectory = carpeta_seleccionada

                    self.locationproyectoLabel.config(text=self.proyectDirectory)
                    self.proyectnameEntry.config(text=self.proyectName)

                    self.boton_selector.config(state="normal")                    
                    self.menu_archivo.entryconfigure(3, state="normal")
                    self.boton_eliminar.config(state="normal")
                    self.calcular_dynamic.config(state="normal")
                    self.archivoslistbox.delete(0, tk.END)
                    print("Nuevo Proyecto:", self.proyectName)


                    self.CrearCarpetas()
                    self.saveconfigproject()                    
            else:
                messagebox.showinfo(
                    "Alert",
                    'Enter the Project Name.'
                )


    def abrir(self):
        opciones = {
            "defaultextension": ".sisproj",
            "filetypes": [("Files .sisproj", "*.sisproj")],
            "title": "Select _sismoanalyticsproject.sisproj file",
        }

        ruta_archivo = filedialog.askopenfilename(**opciones)

        # Verificar si se seleccionó un archivo
        if ruta_archivo:
            directorio = os.path.dirname(ruta_archivo)
            nombre_sin_extension = os.path.splitext(os.path.basename(ruta_archivo))[0]
            if nombre_sin_extension == "_sismoanalyticsproject":
                self.tratamientos = []

                self.seleccion_var.set("home")
                self.loadPage(self.seleccion_var.get())

                self.proyectPath = directorio
                self.proyectDirectory = os.path.normpath(f"{directorio}/../")

                nombre_ultimo_carpeta = os.path.basename(directorio)
                self.proyectName = nombre_ultimo_carpeta

                print(f"Archivo seleccionado: {ruta_archivo}")
                self.locationproyectoLabel.config(text=self.proyectDirectory)
                self.proyectnameEntry.config(text=self.proyectName)

                # Recuperar la lista de instancias desde el archivo JSON
                with open(ruta_archivo, "r") as archivo_json:
                    datos_tratamientos = json.load(archivo_json)
                # Crear instancias de TratamientoRecord desde los datos recuperados
                self.tratamientos = [
                    TratamientoRecord(**datos) for datos in datos_tratamientos
                ]
                self.llenarListBox()
                self.boton_selector.config(state="normal")
                self.menu_archivo.entryconfigure(3, state="normal")
                self.boton_eliminar.config(state="normal")
                self.calcular_dynamic.config(state="normal")

                # Aquí puedes realizar acciones adicionales según tu aplicación
            else:
                messagebox.showinfo(
                    "Alert",
                    f'The file name should be "_sismoanalyticsproject" but is "{nombre_sin_extension}".',
                )

    def guardar(self):
        # Agregar aquí la lógica para guardar un archivo o realizar una acción
        carpeta_seleccionada = filedialog.askdirectory()
        if carpeta_seleccionada:
            old_directory = self.proyectPath

            self.proyectDirectory = os.path.normpath(f"{carpeta_seleccionada}/../")
            self.proyectPath = carpeta_seleccionada
            nombre_ultimo_carpeta = os.path.basename(carpeta_seleccionada)
            self.proyectName = nombre_ultimo_carpeta
            self.proyectnameEntry.config(text=self.proyectName)
            self.locationproyectoLabel.config(text=self.proyectDirectory)
            print(f"Carpeta seleccionada: {carpeta_seleccionada}")
            print(f"Carpeta seleccionada: {nombre_ultimo_carpeta}")
            print(f"Carpeta seleccionada proyecto: {self.proyectDirectory}")
            self.recursive_overwrite(old_directory, self.proyectPath)

    def salir(self):
        self.quit()

    def show(self):
        # self.mainloop()
        pass

    def seleccionar_archivo_visor(self, index):
        self.currentTratamiento = self.tratamientos[index]
        if self.seleccion_var.get() == "home":
            self.seleccion_var.set("graph1")
        self.loadPage(self.seleccion_var.get())

    def archivoslistbox_on_listbox_select(self, event):
        # Obtener el índice del elemento seleccionado
        selected_index = self.archivoslistbox.curselection()
        if selected_index:
            index = int(selected_index[0])
            selected_item = self.archivoslistbox.get(index)
            print(f"Elemento seleccionado: {index} -> {selected_item}")
            self.seleccionar_archivo_visor(index)
            # load a website

    def CrearCarpetas(self, first=True):
        try:
            if first == True:
                os.makedirs(self.proyectPath + "/files")
            os.makedirs(self.proyectPath + "/results")
            os.makedirs(self.proyectPath + "/results/xlsx")
            os.makedirs(self.proyectPath + "/results/pdf")
            os.makedirs(self.proyectPath + "/results/html")
            os.makedirs(self.proyectPath + "/results/html/images")
            print(self.proyectPath + "/files")
        except Exception as e:
            print(f"No se pudieron crear las carpetas. Error: {e}")

    def llenarListBox(self):
        self.currentTratamiento = None
        self.archivoslistbox.delete(0, tk.END)
        for tratamiento in self.tratamientos:
            self.archivoslistbox.insert(tk.END, f"{tratamiento.filebasename}")

        if len(self.tratamientos) > 0:
            self.currentTratamiento = self.tratamientos[0]
            self.archivoslistbox.selection_set(0)
            self.seleccionar_archivo_visor(0)

    def ProcesoTratamiento(self):
        try:
            # shutil.rmtree(self.proyectPath)
            shutil.rmtree(self.proyectPath + "/results")
            shutil.rmtree(self.proyectPath + "/results/xlsx")
            shutil.rmtree(self.proyectPath + "/results/pdf")
            shutil.rmtree(self.proyectPath + "/results/html")
            shutil.rmtree(self.proyectPath + "/results/html/images")
            print(
                f"La carpeta {self.proyectPath} y su contenido han sido eliminados con éxito."
            )
        except Exception as e:
            print(f"No se pudo eliminar la carpeta {self.proyectPath}. Error: {e}")

        # Utiliza os.makedirs para crear las carpetas de forma recursiva
        self.CrearCarpetas(False)

        self.archivoslistbox.delete(0, tk.END)

        for tratamiento in self.tratamientos:
            print(repr(tratamiento))
            # copiar archivos en el nuevo directorio
            try:
                if tratamiento.isNew == True:
                    shutil.copy(tratamiento.ruta_registro, self.proyectPath + "/files/")
                    tratamiento.ruta_registro = "files/" + tratamiento.filebasename
                    tratamiento.isNew = False
                os.makedirs(
                    f"{self.proyectPath}/results/html/images/{tratamiento.filebasename}"
                )
            except Exception as e:
                print(f"No se pudo copiar el archivo. Error: {e}")

            nuevo_registro_resumen = RegistroResumen(self.proyectPath, tratamiento)
            nuevo_registro_resumen.procesar()
        self.llenarListBox()
        self.saveconfigproject()
        # self.archivoslistbox.selection_set(0)

        # agregar a controles

        # Serializar la lista a JSON

    def saveconfigproject(self):
        json_data = json.dumps([tr.__dict__ for tr in self.tratamientos], indent=4)
        # Guardar el JSON en un archivo
        # json_file_path = f"{self.proyectPath}/{self.proyectName}.sisproj"
        json_file_path = f"{self.proyectPath}/_sismoanalyticsproject.sisproj"
        with open(json_file_path, "w") as archivo_json:
            archivo_json.write(json_data)
        # self.title = f"{self.title}"

    def openFilePicker(self):
        filepickerform = FilerPickerDialogForm(
            self, self.tratamientos, self.proyectPath
        )
        if filepickerform.returnDialog == True and len(self.tratamientos) > 0:
            self.tratamientos = filepickerform.tratamientos
            if len(filepickerform.deletedItems) > 0:
                for tratamiento_deleted in filepickerform.deletedItems:
                    self.eliminar_item(tratamiento_deleted)
            self.ProcesoTratamiento()
            messagebox.showinfo(
                "Processing", "File processing has finished"
            )

    def calcular_dynamic_click(self):
        if len(self.tratamientos) > 0:
            calculodinamicoform = DynamicAmplificationDialogo(self)
            if calculodinamicoform.resultDialog.get():
                for tratamiento in self.tratamientos:
                    self.eliminar_archivos_y_carpetas(
                        [
                            f"{self.proyectPath}/results/html/da_{tratamiento.filebasename}.html",
                            f"{self.proyectPath}/results/html/da_{tratamiento.filebasename}.temporal.html",
                            f"{self.proyectPath}/results/pdf/da_{tratamiento.filebasename}.pdf",
                            f"{self.proyectPath}/results/html/images/da_{tratamiento.filebasename}",
                        ]
                    )
                    os.makedirs(
                        f"{self.proyectPath}/results/html/images/da_{tratamiento.filebasename}"
                    )
                    tratamiento.zeta1 = calculodinamicoform.zeta1.get()
                    tratamiento.zeta2 = calculodinamicoform.zeta2.get()
                    tratamiento.deltazeta = calculodinamicoform.deltazeta.get()
                    tratamiento.Tevaluado = calculodinamicoform.tevaluado.get()

                    nuevo_dynamic_amplification = DynamicAmplification(
                        self.proyectPath, tratamiento
                    )
                    print("procesar")
                    nuevo_dynamic_amplification.procesar()

                messagebox.showinfo(
                    "Processing", "File processing has finished"
                )
                tratamiento.dynamic_amplification = True
                self.saveconfigproject()
                self.llenarListBox()

    def ShowNavVisor_select(self):
        self.loadPage(self.seleccion_var.get())

    def existehtmldatos(self, ruta,opcion):
        if ruta is not None and os.path.exists(ruta):
            return ruta
        
        if opcion == "graph1":
            return self.nodataPage
        else:
            return self.nodataPageda

    def loadPage(self, opcion):
        print(opcion)
        self.webbrowser.stop()
        tratamiento = self.currentTratamiento
        if opcion == "home":
            self.webbrowser.load_file(self.homePage,
                force=True)
        elif opcion == "graph1":
            time.sleep(2)
            archivo = None
            if tratamiento is not None:
                archivo = f"{self.proyectPath}/results/html/{tratamiento.filebasename}.html"
            self.webbrowser.load_file(
                self.existehtmldatos(
                     archivo ,opcion
                ),
                force=True
            )
            self.webbrowser
        elif opcion == "graph2":
            time.sleep(2)
            archivo = None
            if tratamiento is not None:
                archivo = f"{self.proyectPath}/results/html/da_{tratamiento.filebasename}.html"
            self.webbrowser.load_file(
                self.existehtmldatos(
                    archivo ,opcion
                ),
                force=True
            )
