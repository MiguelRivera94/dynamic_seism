import numpy as np
import pickle
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
from Include.interfaz.dialog.ConfigureSummarySettingsDialogForm import (
    ConfigureSummarySettingsDialogo,
)
from Include.tratamiento.record import TratamientoRecord
from Include.tratamiento.registroresumen import RegistroResumen
from Include.tratamiento.dynamicamplification import DynamicAmplification
from Include.tratamiento.summaryresults import SummaryResults
from pathlib import Path
import shutil
import os
import json
import tkinterweb
import sys
import time
import uuid

# constante version 1.3.0
VERSION = "1.3.0"


class MainForm(tk.Tk):
    def __init__(self):
        super().__init__()
        # Determine the current directory based on whether the script is frozen.
        if getattr(sys, "frozen", False) and hasattr(sys, "_MEIPASS"):
            self.current_directory = os.path.join(
                sys._MEIPASS
            )  # Set current directory for frozen application.
        else:
            self.current_directory = (
                os.getcwd()
            )  # Set current directory for normal execution.
        # Set the application icon using the icon file path.
        self.iconbitmap(self.current_directory + os.sep + "resources/icons/iconapp.ico")
        # Initialize attributes for treatments, window title, and current treatment.
        self.tratamientos = []
        self.titleWindow = "Dynamic Seism"
        self.title(self.titleWindow)  # Set the title of the main window.
        self.state("zoomed")  # Maximize the main window.
        # Define a function to handle window close event.
        self.protocol("WM_DELETE_WINDOW", self.salir)
        # Initialize attributes for project name, current treatment, and homepage URLs.
        self.tratamientos = []
        self.proyectName = ""
        self.currentTratamiento = None
        self.num_divisiones_frequ = 0
        self.num_divisiones_ELAS = 0
        self.num_divisiones_INELAS = 0

        self.frecuencias_summary = []
        self.energia_summary = []
        self.Rd_evaluado_lineal_resultado_summary = []
        self.Rd_evaluado_nolineal_resultado_summary = []

        self.guid = ""

        self.homePage = f"{self.current_directory}/resources/html/home.html"
        self.nodataPage = f"{self.current_directory}/resources/html/nodata.html"
        self.nodataPageda = f"{self.current_directory}/resources/html/nodatada.html"
        self.nodataPageSummary = f"{self.current_directory}/resources/html/nodatasummary.html"

        # Set the project directory based on whether it's already set or not.
        self.proyectDirectory = None
        if self.proyectDirectory == None:
            # Determine the current directory based on whether the script is frozen.
            if getattr(sys, "frozen", False) and hasattr(sys, "_MEIPASS"):
                # Set current directory for frozen application.
                self.current_directory = os.path.join(sys._MEIPASS)
            else:
                # Set current directory for normal execution.
                self.current_directory = os.getcwd()
            # Construct the project directory path using the current directory.
            self.proyectDirectory = (
                self.current_directory.replace("\\", os.sep) + os.sep + "projects"
            )
            print(self.proyectDirectory)
        # Call the initialize method to continue with initialization.
        self.initialize()

    def initialize(self):
        # Generate the main menu bar in the graphical interface
        self.mainMenu = tk.Menu(self)
        # Add the menu bar to the main window of the software
        self.config(menu=self.mainMenu)

        # Create a menú "File"
        self.menu_archivo = tk.Menu(self.mainMenu)
        # Add "File" to the menu bar
        self.mainMenu.add_cascade(label="File", menu=self.menu_archivo)
        # Add "New" option
        self.menu_archivo.add_command(label="New", command=self.nuevo)
        # Add "Open" option
        self.menu_archivo.add_command(label="Open", command=self.abrir)
        # Add "Save as..."
        self.menu_archivo.add_command(label="Save as...", command=self.guardar)
        # Add a separator line
        self.menu_archivo.add_separator()
        # Add "Exit" option
        self.menu_archivo.add_command(label="Exit", command=self.salir)
        # Disable the "Save as..." option
        self.menu_archivo.entryconfigure(3, state="disabled")
        # Create a top frame for project information
        self.frame_superior = tk.Frame(self)
        self.frame_superior.pack(side="top", fill="x")  # Pack the frame at the top
        # Generate a Label for "Project Location"
        self.label1 = tk.Label(
            self.frame_superior,
            text="Project Location",
            wraplength=700,
            width=20,
            justify="right",
            anchor="w",
        )
        # Place the label in the grid
        self.label1.grid(row=1, column=1)
        # Generate a Label to display the project directory
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
        # Place the label in the grid
        self.locationproyectoLabel.grid(row=1, column=2)
        # Label for "Project Name"
        self.label2 = tk.Label(
            self.frame_superior,
            text="Project Name",
            wraplength=700,
            width=20,
            justify="right",
            anchor="w",
        )
        # Place the label in the grid
        self.label2.grid(row=2, column=1)
        # Label to display the project name
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
        # Place the label in the grid
        self.proyectnameEntry.grid(row=2, column=2)
        # Create a toolbar frame
        self.barra_herramientas = tk.Frame(self, bd=1, relief=RAISED)
        # Pack the toolbar at the top
        self.barra_herramientas.pack(fill="x")

        # Create a button in the toolbar to load seismic records
        self.boton_selector = tk.Button(
            self.barra_herramientas,
            text="Load Seismic Records",
            command=self.openFilePicker,
            bg="#333333",
            fg="#FFFFFF",
        )
        # Pack the button to the left
        self.boton_selector.pack(side="left")
        # Initially disable the button
        self.boton_selector.config(state="disabled")

        # Create a button in the toolbar to calculate dynamic magnification
        self.calcular_dynamic = tk.Button(
            self.barra_herramientas,
            text="Calculate Dynamic Magnification",
            command=self.calcular_dynamic_click,
            bg="#333333",
            fg="#FFFFFF",
        )
        # Pack the button to the left
        self.calcular_dynamic.pack(side="left")
        # Initially disable the button
        self.calcular_dynamic.config(state="disabled")

        # Create a button in the toolbar to calculate dynamic magnification
        self.configure_summary_settings = tk.Button(
            self.barra_herramientas,
            text="Configure Summary Settings",
            command=self.configure_summary_settings_click,
            bg="#333333",
            fg="#FFFFFF",
        )
        # Pack the button to the left
        self.configure_summary_settings.pack(side="left")
        # Initially disable the button
        self.configure_summary_settings.config(state="disabled")

        # Create a left frame for listing files
        self.leftframe = tk.Frame(self)
        # Pack the frame to the left
        self.leftframe.pack(side=tk.LEFT, fill=tk.Y)
        # Seismic records are shown in the following listbox
        self.archivoslistbox = tk.Listbox(self.leftframe, width=50)
        # Pack the listbox at the top
        self.archivoslistbox.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        # Associate the selection event with a handler
        self.archivoslistbox.bind(
            "<<ListboxSelect>>", self.archivoslistbox_on_listbox_select
        )
        # Create an inner frame within the left frame
        self.frame_interior = tk.Frame(self.leftframe, padx=10, pady=10)
        # Pack the inner frame at the bottom
        self.frame_interior.pack(side="bottom", fill="both")
        # Create a button in the inner frame to delete the selected file
        self.boton_eliminar = tk.Button(
            self.frame_interior,
            text="Delete current file",
            command=self.boton_eliminar_click,
            justify="center",
        )
        # Pack the button to the right
        self.boton_eliminar.pack(side="right")
        # Initially disable the button
        self.boton_eliminar.config(state="disabled")

        # Create a right frame for additional content
        self.rightframe = tk.Frame(self)
        # Pack the frame to the left and allow expansion
        self.rightframe.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Create a navigation toolbar frame
        self.barra_herramientas_nav = tk.Frame(self.rightframe, bd=1, relief=RAISED)
        # Pack the toolbar at the top
        self.barra_herramientas_nav.pack(fill="x")

        # Variable to track the selection in the navigation
        self.seleccion_var = tk.StringVar()
        # Set the default selection to "home"
        self.seleccion_var.set("home")
        # Create radio buttons for navigation
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
        self.nav_opcion4 = tk.Radiobutton(
            self.barra_herramientas_nav,
            indicatoron=0,
            command=self.ShowNavVisor_select,
            text="Summary Report Charts",
            variable=self.seleccion_var,
            value="graph3",
        )

        # Pack the radio buttons horizontally
        self.nav_opcion1.pack(side="left", padx=5)
        self.nav_opcion2.pack(side="left", padx=5)
        self.nav_opcion3.pack(side="left", padx=5)
        self.nav_opcion4.pack(side="left", padx=5)
        # Create an HTML browser frame within the right frame
        self.webbrowser = tkinterweb.HtmlFrame(self.rightframe, messages_enabled=False)
        # Create HTML browser
        self.loadPage("home")  # Load the home page
        self.webbrowser.pack(
            fill="both", expand=True
        )  

    def recursive_overwrite(self, src, dest, ignore=None):
        # Check if the source path is a directory
        if os.path.isdir(src):
            # In the event that the path does not exist, it is created
            if not os.path.isdir(dest):
                os.makedirs(dest)
            # List all directories on "files"
            files = os.listdir(src)
            # Determine which files to ignore, if an ignore function is provided
            if ignore is not None:
                ignored = ignore(src, files)
            else:
                # If no ignore function, do not ignore any files
                ignored = set()
            # Iterate over all files and directories in the source
            for f in files:
                # If the file is on the ignore list, then copy it
                if f not in ignored:
                    self.recursive_overwrite(
                        os.path.join(src, f), os.path.join(dest, f), ignore
                    )
        else:
            # If the source is a file, copy it to the destination
            shutil.copyfile(src, dest)

    def buscarUbicacion(self):
        # Select the directory and store the path using a dialog box
        directorioTemporal = filedialog.askdirectory()
        # self.focus_force()
        print(self.proyectDirectory)
        # Check if a directory was selected
        if not directorioTemporal:
            # Print "cancelado" if the user canceled the directory selection
            print("cancelado")
        else:
            # Check if a project name is set
            if self.proyectName != "":
                # Construct the full path to the project directory
                ruta_directorio = directorioTemporal + "/" + self.proyectName
                # Check if a directory exists and if it is correct
                if os.path.exists(ruta_directorio) and os.path.isdir(ruta_directorio):
                    # Show an alert if the directory already exists
                    messagebox.showinfo(
                        "Alerta",
                        f'The directory "{directorioTemporal}" already exists.',
                    )
                else:
                    # Update the project directory and path
                    self.proyectDirectory = directorioTemporal
                    self.proyectPath = self.proyectDirectory + "/" + self.proyectName
                    self.locationproyectoLabel.config(text=self.proyectDirectory)
                    # Call the method to create necessary folders
                    self.CrearCarpetas()
            else:
                # If no project name is set, just update the project directory
                self.proyectDirectory = directorioTemporal
                self.proyectPath = self.proyectDirectory + "/" + self.proyectName
                # Update the label displaying the project directory
                self.locationproyectoLabel.config(text=self.proyectDirectory)

    def eliminar_archivos_y_carpetas(self, rutas):
        # Iterate over each path in the list of paths
        for ruta in rutas:
            # Check if the path exists
            if os.path.exists(ruta):
                # Check if the path is a file
                if os.path.isfile(ruta):
                    # Delete the file
                    os.remove(ruta)
                    # Print a message indicating the file was deleted
                    print(f"Archivo eliminado: {ruta}")
                # Check if the path is a directory
                elif os.path.isdir(ruta):
                    # Delete the directory and its contents recursively
                    shutil.rmtree(ruta)
                    # Print a message indicating the directory was deleted
                    print(f"Carpeta eliminada recursivamente: {ruta}")
                else:
                    # Print a message if the path is not recognized as a file or directory
                    print(f"Ruta no reconocida: {ruta}")
            else:
                # Print a message if the path does not exist
                print(f"La ruta no existe: {ruta}")

    def eliminar_item(self, tratamiento_deleted: TratamientoRecord):
        # Create a list of paths to delete based on the file basename of the deleted treatment record
        rutas_a_eliminar = [
            f"{self.proyectPath}/files/{tratamiento_deleted.filebasename}",  # Path to the file
            f"{self.proyectPath}/results/html/{tratamiento_deleted.filebasename}.html",  # Path to the HTML result file
            f"{self.proyectPath}/results/html/{tratamiento_deleted.filebasename}.temporal.html",  # Path to the temporary HTML result file
            f"{self.proyectPath}/results/pdf/{tratamiento_deleted.filebasename}.pdf",  # Path to the PDF result file
            f"{self.proyectPath}/results/html/images/{tratamiento_deleted.filebasename}",  # Path to the images directory
            f"{self.proyectPath}/results/xlsx/{tratamiento_deleted.filebasename}.xlsx",  # Path to the Excel result file
            f"{self.proyectPath}/results/html/da_{tratamiento_deleted.filebasename}.html",  # Path to the HTML result file for dynamic analysis
            f"{self.proyectPath}/results/html/da_{tratamiento_deleted.filebasename}.temporal.html",  # Path to the temporary HTML result file for dynamic analysis
            f"{self.proyectPath}/results/pdf/da_{tratamiento_deleted.filebasename}.pdf",  # Path to the PDF result file for dynamic analysis
            f"{self.proyectPath}/results/html/images/da_{tratamiento_deleted.filebasename}",  # Path to the images directory for dynamic analysis
        ]
        # Print the list of paths to delete for debugging purposes
        print(rutas_a_eliminar)
        # Call the method to delete the files and directories
        self.eliminar_archivos_y_carpetas(rutas_a_eliminar)

    def boton_eliminar_click(self):
        # Identifies the number of the selected file in the list box
        selected_index = self.archivoslistbox.index("active")
        # Check if there is a valid selection and if there are any items in the 'tratamientos' list
        if selected_index >= 0 and len(self.tratamientos) > 0:
            # Print the selected index for debugging purposes
            print(selected_index)
            # Print the length of the 'tratamientos' list for debugging purposes
            print(len(self.tratamientos))
            # Ask the user for confirmation before deletion
            respuesta = messagebox.askyesno(
                "Confirm Deletion", "Are you sure to delete? (Yes/No)"
            )
            # If the user confirms the deletion
            if respuesta:
                # Remove the treatment from the list and store it in 'tratamiento_deleted'
                tratamiento_deleted = self.tratamientos.pop(selected_index)
                print(tratamiento_deleted)
                # Call the method to delete the corresponding files and folders
                self.eliminar_item(tratamiento_deleted)
                # Refresh the listbox to reflect the changes
                self.llenarListBox()
                # Save the updated project configuration
                self.saveconfigproject()
                # generates a message notifying that the file was deleted
                print("Eliminar")
            else:
                # generates a message notifying that a file deletion has been canceled
                print("Cancelar")

    # Function for the "New" command in the menu
    def nuevo(self):
        # Add logic here to create a new file or perform an action
        # Display the dialog to select a directory
        carpeta_seleccionada = filedialog.askdirectory(
            title="Select folder for the project", initialdir=self.proyectDirectory
        )
        # print(carpeta_seleccionada)
        # If a directory is selected
        if carpeta_seleccionada:
            nuevo_proyecto_dialogo = NuevoProyectoDialog(self, "New Project Name")
            resultado = nuevo_proyecto_dialogo.result
            # If a valid project name is entered
            if resultado is not None and resultado.strip():
                # Construct the full project path
                temp_proyectpath = f"{carpeta_seleccionada}{os.path.sep}{resultado}"
                # Check if a project already exists in the selected directory with the entered name
                if os.path.exists(temp_proyectpath) and os.path.isdir(temp_proyectpath):
                    messagebox.showinfo(
                        "Alert",
                        f'A project already exists in the folder "{carpeta_seleccionada} with the name {resultado}".',
                    )
                else:
                    # Initialize an empty list for treatments
                    self.tratamientos = []
                    self.guid = uuid.uuid4()
                    # Set the selection variable to 'home' and load the corresponding page
                    self.seleccion_var.set("home")
                    self.loadPage(self.seleccion_var.get())
                    # Set project name and paths
                    self.proyectName = resultado
                    # self.guid create unique identifier
                    self.proyectPath = temp_proyectpath
                    self.proyectDirectory = carpeta_seleccionada
                    # Update the project location label
                    self.locationproyectoLabel.config(text=self.proyectDirectory)
                    # Update the project name label
                    self.proyectnameEntry.config(text=self.proyectName)
                    # Enable various buttons and menu items for the new project
                    self.boton_selector.config(state="normal")
                    self.menu_archivo.entryconfigure(3, state="normal")
                    self.boton_eliminar.config(state="normal")
                    self.calcular_dynamic.config(state="normal")
                    self.configure_summary_settings.config(state="normal")
                    # Clear the listbox
                    self.archivoslistbox.delete(0, tk.END)
                    # Print the new project name for debugging purposes
                    print("Nuevo Proyecto:", self.proyectName)

                    # Create the necessary directories for the new project
                    self.CrearCarpetas()
                    # Save the project configuration
                    self.saveconfigproject()
            else:
                # Show an alert if the project name is not entered
                messagebox.showinfo("Alert", "Enter the Project Name.")

    def abrir(self):
        # Options for the file dialog
        # Set the default file extension to .sisproj
        # Allow only .sisproj files to be selected
        # Title of the file dialog
        opciones = {
            "defaultextension": ".pkl",
            "filetypes": [("Files .pkl", "*.pkl")],
            "title": "Select _sismoanalyticsproject.pkl file",
        }

        # Open the file dialog to select a file
        ruta_archivo = filedialog.askopenfilename(**opciones)

        # Check if a file was selected
        if ruta_archivo:
            # Get the directory of the selected file
            directorio = os.path.dirname(ruta_archivo)
            # Get the file name without extension
            nombre_sin_extension = os.path.splitext(os.path.basename(ruta_archivo))[0]
            extension = os.path.splitext(os.path.basename(ruta_archivo))[1]
            # Check if the file name is "_sismoanalyticsproject"
            if nombre_sin_extension.lower() == "_sismoanalyticsproject" and extension.lower() == ".pkl":
                # Clear the list of treatments
                self.tratamientos = []
                # Set the selection variable to "home" and load the home page
                self.seleccion_var.set("home")
                self.loadPage(self.seleccion_var.get())
                # Set the project path to the directory of the selected fil
                self.proyectPath = directorio
                # Set the project directory to the parent directory of the project path
                self.proyectDirectory = os.path.normpath(f"{directorio}/../")
                # Capture the name of the last folder within a project
                nombre_ultimo_carpeta = os.path.basename(directorio)
                # Set the project name to the last folder name
                self.proyectName = nombre_ultimo_carpeta
                # Print the selected file path
                print(f"Archivo seleccionado: {ruta_archivo}")
                # Update the project directory label
                self.locationproyectoLabel.config(text=self.proyectDirectory)
                # Update the project name entry
                self.proyectnameEntry.config(text=self.proyectName)

                # Retrieve the list of treatment instances from the JSON file
                saveconfigproject = None
                with open(ruta_archivo, "rb") as archivo_pkl:
                    saveconfigproject = pickle.load(archivo_pkl)
                    # jsonFileData = json.load(archivo_pkl)
                    if saveconfigproject["version"] is not None:
                        # version = jsonFileData.get("version")
                        if saveconfigproject["version"] != VERSION:
                            messagebox.showinfo(
                                "Alert",
                                f"The file version is not compatible with the current application version {VERSION}.",
                            )
                            return
                    else:
                        messagebox.showinfo(
                            "Alert",
                            f"The file version is not compatible with the current application version {VERSION}.",
                        )
                    datos_tratamientos = saveconfigproject["tratamientos"]

                self.num_divisiones_frequ = saveconfigproject["num_divisiones_frequ"]
                self.num_divisiones_ELAS = saveconfigproject["num_divisiones_ELAS"]
                self.num_divisiones_INELAS = saveconfigproject["num_divisiones_INELAS"]
                self.guid = saveconfigproject["guid"]

                # si existe saveconfigproject['frecuencias_summary'] y saveconfigproject['energia_summary'] y saveconfigproject['Rd_evaluado_lineal_resultado_summary'] y saveconfigproject['Rd_evaluado_nolineal_resultado_summary']
                if "frecuencias_summary" in saveconfigproject:
                    self.frecuencias_summary = saveconfigproject["frecuencias_summary"]

                if "energia_summary" in saveconfigproject:
                    self.energia_summary = saveconfigproject["energia_summary"]

                if "Rd_evaluado_lineal_resultado_summary" in saveconfigproject:
                    self.Rd_evaluado_lineal_resultado_summary = saveconfigproject[
                        "Rd_evaluado_lineal_resultado_summary"
                    ]

                if "Rd_evaluado_nolineal_resultado_summary" in saveconfigproject:
                    self.Rd_evaluado_nolineal_resultado_summary = saveconfigproject[
                        "Rd_evaluado_nolineal_resultado_summary"
                    ]
                    # self.tratamientos = saveconfigproject['tratamientos']
                # Create instances of TratamientoRecord from the retrieved data
                self.tratamientos = [
                    TratamientoRecord(**datos) for datos in datos_tratamientos
                ]

                if len(self.tratamientos) >= 11:
                    self.configure_summary_settings.config(state="normal")
                # Fill the list box with the treatments
                self.llenarListBox()
                # Activate the button that allows selection
                self.boton_selector.config(state="normal")
                # Activate the "Save as..." menu option
                self.menu_archivo.entryconfigure(3, state="normal")
                # Activate the delete button
                self.boton_eliminar.config(state="normal")
                # Activate the dynamic calculation button
                self.calcular_dynamic.config(state="normal")

                # Additional actions can be performed here based on the application requirements
            else:
                # Show an alert if the file name is not "_sismoanalyticsproject"
                messagebox.showinfo(
                    "Alert",
                    f'The file name should be "_sismoanalyticsproject" but is "{nombre_sin_extension}".',
                )

    def guardar(self):
        # Function for the "Save as..." command in the menu
        # Prompt the user to select a directory for saving
        carpeta_seleccionada = filedialog.askdirectory()
        # Check if a directory was selected
        if carpeta_seleccionada:
            # Store the current project path for reference
            old_directory = self.proyectPath
            # Update the project directory to the parent directory of the selected folder
            self.proyectDirectory = os.path.normpath(f"{carpeta_seleccionada}/../")
            # Set the project path to the selected folder
            self.proyectPath = carpeta_seleccionada
            # Get the name of the last folder in the selected path and set it as the project name
            nombre_ultimo_carpeta = os.path.basename(carpeta_seleccionada)
            self.proyectName = nombre_ultimo_carpeta
            # Update the project name entry widget with the new project name
            self.proyectnameEntry.config(text=self.proyectName)
            # Update the project directory label with the new project directory
            self.locationproyectoLabel.config(text=self.proyectDirectory)
            # Print information about the selected folder for debugging or logging
            print(f"Carpeta seleccionada: {carpeta_seleccionada}")
            print(f"Carpeta seleccionada: {nombre_ultimo_carpeta}")
            print(f"Carpeta seleccionada proyecto: {self.proyectDirectory}")
            # Perform a recursive overwrite of files from the old project directory to the new one
            self.recursive_overwrite(old_directory, self.proyectPath)

    def salir(self):
        # Exit the Dynamic Seism
        self.quit()

    def show(self):
        # Display the main window
        # self.mainloop()
        pass

    def seleccionar_archivo_visor(self, index):
        # Select the treatment record at the given index
        self.currentTratamiento = self.tratamientos[index]
        # Set selection_var to 'graph1' if currently 'home'
        if self.seleccion_var.get() == "home":
            self.seleccion_var.set("graph1")
        # Load the page based on the current selection
        if self.seleccion_var.get() != 'graph3':
            self.loadPage(self.seleccion_var.get())

    def archivoslistbox_on_listbox_select(self, event):
        # Handle selection change in the listbox
        selected_index = self.archivoslistbox.curselection()
        if selected_index:
            index = int(selected_index[0])
            selected_item = self.archivoslistbox.get(index)
            print(f"Elemento seleccionado: {index} -> {selected_item}")
            # Select and display the treatment record
            self.seleccionar_archivo_visor(index)

    def CrearCarpetas(self, first=True):
        try:
            # Create necessary project folders
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
        # Populate the listbox with treatment records
        self.currentTratamiento = None
        self.archivoslistbox.delete(0, tk.END)
        i = 0
        flecha_derecha = "→"
        for tratamiento in self.tratamientos:
            i = i + 1
            self.archivoslistbox.insert(tk.END, f" s{i} {flecha_derecha} {tratamiento.filebasename}")
        # Select the first item if there are treatments
        if len(self.tratamientos) > 0:
            self.currentTratamiento = self.tratamientos[0]
            self.archivoslistbox.selection_set(0)
            self.seleccionar_archivo_visor(0)

    def ProcesoTratamiento(self):
        try:
            # shutil.rmtree(self.proyectPath)
            # Clean up existing result folders
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
        # Recreate necessary project folders
        self.CrearCarpetas(False)

        self.archivoslistbox.delete(0, tk.END)
        # Clear listbox and process each treatment record
        for tratamiento in self.tratamientos:
            print(repr(tratamiento))
            # copiar archivos en el nuevo directorio
            try:
                # Copy files and create image folders
                if tratamiento.isNew == True:
                    shutil.copy(tratamiento.ruta_registro, self.proyectPath + "/files/")
                    tratamiento.ruta_registro = "files/" + tratamiento.filebasename
                    tratamiento.isNew = False
                os.makedirs(
                    f"{self.proyectPath}/results/html/images/{tratamiento.filebasename}"
                )
            except Exception as e:
                print(f"No se pudo copiar el archivo. Error: {e}")

            # Process each treatment record
            nuevo_registro_resumen = RegistroResumen(self.proyectPath, tratamiento)
            nuevo_registro_resumen.procesar()
        # Refresh the listbox and save project configuration
        self.llenarListBox()
        self.saveconfigproject()
        # self.archivoslistbox.selection_set(0)
        # Additional controls can be added here
        # Serialize the list to JSON

    def saveconfigproject(self):
        # Lista de claves a omitir
        claves_a_omitir = ["Rd_evaluado_lineal", "Rd_evaluado_nolineal", "zeta"]
        definition_jsonTratamientos = [
            {k: v for k, v in tr.__dict__.items() if k not in claves_a_omitir}
            for tr in self.tratamientos  
        ]
        definition_json_data = json.dumps(definition_jsonTratamientos, indent=4)
        definition_jsonTratamientos_path = f"{self.proyectPath}/_definitions_sismoanalyticsproject.json"
        with open(definition_jsonTratamientos_path, "w") as archivo_definition_json:
            archivo_definition_json.write(definition_json_data)

        # Serialize treatments to JSON format
        saveProjectTemp = {}
        saveProjectTemp["version"] = VERSION
        saveProjectTemp["guid"] = self.guid
        saveProjectTemp["num_divisiones_frequ"] = self.num_divisiones_frequ
        saveProjectTemp["num_divisiones_ELAS"] = self.num_divisiones_frequ
        saveProjectTemp["num_divisiones_INELAS"] = self.num_divisiones_frequ
        saveProjectTemp["frecuencias_summary"] = self.frecuencias_summary
        saveProjectTemp["energia_summary"] = self.energia_summary
        saveProjectTemp["Rd_evaluado_lineal_resultado_summary"] = (
            self.Rd_evaluado_lineal_resultado_summary
        )
        saveProjectTemp["Rd_evaluado_nolineal_resultado_summary"] = (
            self.Rd_evaluado_nolineal_resultado_summary
        )
        saveProjectTemp["tratamientos"] = [tr.__dict__ for tr in self.tratamientos]

        json_file_path = f"{self.proyectPath}/_sismoanalyticsproject.pkl"
        # Serializar el objeto a un archivo
        # if existe json_file_path eliminarlo7
        # Pickle library to save the information of Python objects
        # Pickle libreria para guardar la informacion de los objetos de python
        with open(json_file_path, "wb") as file:
            pickle.dump(saveProjectTemp, file)
        

    def openFilePicker(self):
        # Display a file picker dialog form to select files
        filepickerform = FilerPickerDialogForm(
            self, self.tratamientos, self.proyectPath
        )
        # Proceed if the dialog returns True and there are treatments selected
        if filepickerform.returnDialog == True and len(self.tratamientos) > 0:
            # Update treatments with the selected files
            self.tratamientos = filepickerform.tratamientos
            # Delete selected items if any were marked for deletion in the dialog
            if len(filepickerform.deletedItems) > 0:
                for tratamiento_deleted in filepickerform.deletedItems:
                    self.eliminar_item(tratamiento_deleted)
            # Process treatments after file selection
            self.ProcesoTratamiento()
            # Show an information message box indicating that file processing has finished
            messagebox.showinfo("Processing", "File processing has finished")

    def calcular_dynamic_click(self):
        # Perform dynamic amplification calculation if there are treatments available
        if len(self.tratamientos) > 0:
            # Display a dialog form for dynamic amplification calculation
            calculodinamicoform = DynamicAmplificationDialogo(self)
            # Proceed if the dialog result is True
            if calculodinamicoform.resultDialog.get():
                # Delete existing files related to summary               
                self.eliminar_archivos_y_carpetas([
                    f"{self.proyectPath}/results/html/summary.html",
                    f"{self.proyectPath}/results/html/summary.temporal.html",
                    f"{self.proyectPath}/results/pdf/summary.pdf",
                    f"{self.proyectPath}/results/xlsx/summary_report.xlsx",
                ])
                # Iterate through each treatment and perform dynamic amplification tasks
                for tratamiento in self.tratamientos:
                    # Delete existing files related to dynamic amplification for the current treatment
                    self.eliminar_archivos_y_carpetas(
                        [
                            f"{self.proyectPath}/results/html/da_{tratamiento.filebasename}.html",
                            f"{self.proyectPath}/results/html/da_{tratamiento.filebasename}.temporal.html",
                            f"{self.proyectPath}/results/pdf/da_{tratamiento.filebasename}.pdf",
                            f"{self.proyectPath}/results/html/images/da_{tratamiento.filebasename}",
                        ]
                    )
                    # Create necessary folders for dynamic amplification results
                    os.makedirs(
                        f"{self.proyectPath}/results/html/images/da_{tratamiento.filebasename}"
                    )
                    # Update treatment parameters with values from the dialog form
                    tratamiento.zeta1 = calculodinamicoform.zeta1.get()
                    tratamiento.zeta2 = calculodinamicoform.zeta2.get()
                    tratamiento.deltazeta = calculodinamicoform.deltazeta.get()
                    tratamiento.Tevaluado = calculodinamicoform.tevaluado.get()
                    # Create a new instance of DynamicAmplification for the current treatment
                    nuevo_dynamic_amplification = DynamicAmplification(
                        self.proyectPath, tratamiento
                    )
                    # Process dynamic amplification for the current treatment
                    print("procesar")
                    nuevo_dynamic_amplification.procesar()
                # Show an information message box indicating that file processing has finished
                messagebox.showinfo("Processing", "File processing has finished")
                # Update treatment status to indicate that dynamic amplification has been performed
                tratamiento.dynamic_amplification = True
                # Save project configuration after processing
                self.saveconfigproject()
                # Refresh the listbox displaying treatments
                self.llenarListBox()

    def configure_summary_settings_click(self):

        if len(self.tratamientos) >= 11:

            exist_dynamic_amplification = True
            for tratamiento in self.tratamientos:
                if tratamiento.Rd_evaluado_nolineal is None:
                    exist_dynamic_amplification = False
                    break
            
            if exist_dynamic_amplification:
                # Display a dialog form for dynamic amplification calculation
                configuresummaryForm = ConfigureSummarySettingsDialogo(self)
                # Proceed if the dialog result is True
                if configuresummaryForm.resultDialog.get():
                    # zeta es amortiguamiento
                    self.frecuencias_summary = []
                    self.energia_summary = []
                    self.Rd_evaluado_lineal_resultado_summary = []
                    self.Rd_evaluado_nolineal_resultado_summary = []

                    for tratamiento in self.tratamientos:

                        frecuencias_resultado_np = np.array(tratamiento.fregistros_90)
                        frecuencias_transpuesta = frecuencias_resultado_np.reshape(1, -1)
                        self.frecuencias_summary.append(frecuencias_transpuesta)
                        self.Rd_evaluado_lineal_resultado_summary.append(
                            tratamiento.Rd_evaluado_lineal
                        )
                        self.Rd_evaluado_nolineal_resultado_summary.append(
                            tratamiento.Rd_evaluado_nolineal
                        )

                        energia_resultado_np = np.array(tratamiento.energy_90)
                        energia_resultado_transpuesta = energia_resultado_np.reshape(1, -1)
                        self.energia_summary.append(energia_resultado_transpuesta)
                    self.frecuencias_summary = [
                        array.flatten().tolist() for array in self.frecuencias_summary
                    ]
                    self.energia_summary = [
                        array.flatten().tolist() for array in self.energia_summary
                    ]
                    self.num_divisiones_frequ = configuresummaryForm.num_divisiones_frequ.get()
                    self.num_divisiones_ELAS = configuresummaryForm.num_divisiones_ELAS.get()
                    self.num_divisiones_INELAS = configuresummaryForm.num_divisiones_INELAS.get()
                    self.saveconfigproject()
                    summary = SummaryResults(
                        proyectPath=self.proyectPath,
                        amortiguamientos=tratamiento.zeta,
                        frecuencias_summary=self.frecuencias_summary,
                        energia_summary=self.energia_summary,
                        Rd_evaluado_lineal_resultado_summary=self.Rd_evaluado_lineal_resultado_summary,
                        Rd_evaluado_nolineal_resultado_summary=self.Rd_evaluado_nolineal_resultado_summary,
                        num_divisiones_frequ=self.num_divisiones_frequ,
                        num_divisiones_ELAS=self.num_divisiones_ELAS,
                        num_divisiones_INELAS=self.num_divisiones_INELAS,
                        tratamientos = self.tratamientos
                    )
                    summary.procesar()
                    #self.loadPage("graph3")
                    # si self.nav_opcion3 esta e checked load page
                    if self.seleccion_var.get() == 'graph3':
                        self.loadPage("graph3")
                    messagebox.showinfo("Processing", "Summary processing has finished")
                    print("configure_summary_settings_click")
            else:
                messagebox.showinfo('Configure Summary','You need to run the dynamic amplification calculation first')
        else:
            print("No existen suficientes tratamientos para realizar el resumen")
            messagebox.showinfo('Configure Summary','A minimum of 11 analyzed files are needed')

    def ShowNavVisor_select(self):
        # Load the selected page in the application's web browser widget
        self.loadPage(self.seleccion_var.get())

    def existehtmldatos(self, ruta, opcion):
        # Check if HTML data exists at the specified path, otherwise return a default page
        if ruta is not None and os.path.exists(ruta):
            return ruta
        # Return a specific default page based on the option if no valid HTML path is found
        if opcion == "graph1":
            return self.nodataPage
        elif opcion == "graph2":
            return self.nodataPageda
        elif opcion == "graph3":
            return self.nodataPageSummary

    def loadPage(self, opcion):
        # Load content into the application's web browser widget based on the selected option
        print(opcion)
        # Stop any current loading operation in the web browser
        self.webbrowser.stop()
        # Get the current treatment record
        tratamiento = self.currentTratamiento
        # Load the appropriate page based on the selected option
        if opcion == "home":
            # Load the home page into the web browser
            self.webbrowser.load_file(self.homePage, force=True)
        elif opcion == "graph1":
            # Simulate a delay before loading graph1 page
            time.sleep(2)
            # Determine the path to the HTML file for graph1 based on the current treatment
            archivo = None
            if tratamiento is not None:
                archivo = (
                    f"{self.proyectPath}/results/html/{tratamiento.filebasename}.html"
                )
            # Load the HTML file for graph1 into the web browser
            self.webbrowser.load_file(self.existehtmldatos(archivo, opcion), force=True)
            self.webbrowser
        elif opcion == "graph2":
            # Simulate a delay before loading graph2 page
            time.sleep(2)
            # Determine the path to the HTML file for graph2 based on the current treatment
            archivo = None
            if tratamiento is not None:
                archivo = f"{self.proyectPath}/results/html/da_{tratamiento.filebasename}.html"
            # Load the HTML file for graph2 into the web browser
            self.webbrowser.load_file(self.existehtmldatos(archivo, opcion), force=True)
        elif opcion == "graph3":
            # Simulate a delay before loading graph2 page
            time.sleep(2)
            # Determine the path to the HTML file for graph2 based on the current treatment
            archivo = None
            if tratamiento is not None:
                archivo = f"{self.proyectPath}/results/html/summary.html"
            # Load the HTML file for graph2 into the web browser
            self.webbrowser.load_file(self.existehtmldatos(archivo, opcion), force=True)
