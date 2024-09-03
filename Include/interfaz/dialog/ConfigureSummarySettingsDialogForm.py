import tkinter as tk
from tkinter import messagebox
from Include.validacion import es_entero
from pprint import pprint

class ConfigureSummarySettingsDialogo(tk.simpledialog.Dialog):
    def __init__(self, parent, title="Configure Summary Settings"):
        # Initialize instance variables using DoubleVar for storing float values
        self.num_divisiones_frequ = tk.IntVar()
        self.num_divisiones_ELAS = tk.IntVar()
        self.num_divisiones_INELAS = tk.IntVar()
        self.tevaluado = tk.DoubleVar()
        self.resultDialog = tk.BooleanVar()
        self.resultDialog.set(False)
        super().__init__(parent, title)

    def body(self, master):
        # Create labels and entry widgets for user input
        tk.Label(master, text="Frequency Intervals:").grid(row=0, column=0)
        self.num_divisiones_frequ_entry = tk.Entry(master)
        self.num_divisiones_frequ_entry.grid(row=0, column=1)
        tk.Label(master, text="Example: 5").grid(row=0, column=2, sticky="w")

        # Create labels and entry widgets for user input
        tk.Label(master, text="E. Dynamic M. Intervals:").grid(row=1, column=0)
        self.num_divisiones_ELAS_entry = tk.Entry(master)
        self.num_divisiones_ELAS_entry.grid(row=1, column=1)
        tk.Label(master, text="Example: 5").grid(row=1, column=2, sticky="w")

        # Create labels and entry widgets for user input
        tk.Label(master, text="Dynamic M. Intervals:").grid(row=2, column=0)
        self.num_divisiones_INELAS_entry = tk.Entry(master)
        self.num_divisiones_INELAS_entry.grid(row=2, column=1)
        tk.Label(master, text="Example: 5").grid(row=2, column=2, sticky="w")        

        #return self.num_divisiones_frequ

    def apply(self):
        # Validate and convert user input to float, set instance variables
        con_errores = False
        # Validate each entry field for float values
        if es_entero(self.num_divisiones_frequ_entry.get() ) == False:
            con_errores = True
        if es_entero(self.num_divisiones_ELAS_entry.get() ) == False:
            con_errores = True
        if es_entero(self.num_divisiones_INELAS_entry.get() ) == False:
            con_errores = True

        # If no validation errors, convert and set the values to instance variables
        if con_errores == False:
            print('num_divisiones_frequ_entry', self.num_divisiones_frequ_entry.get())
            self.num_divisiones_frequ.set( int( self.num_divisiones_frequ_entry.get() ))

            print('num_divisiones_ELAS_entry', self.num_divisiones_ELAS_entry.get())
            self.num_divisiones_ELAS.set( int( self.num_divisiones_ELAS_entry.get() ))

            print('num_divisiones_INELAS', self.num_divisiones_INELAS_entry.get())
            self.num_divisiones_INELAS.set( int( self.num_divisiones_INELAS_entry.get() ))

            self.resultDialog.set(True)
        else:
            # Display message if there are validation errors
            messagebox.showinfo(
                        "Alert", 'Verify that all data has been entered and is of the required data type'
                    )              