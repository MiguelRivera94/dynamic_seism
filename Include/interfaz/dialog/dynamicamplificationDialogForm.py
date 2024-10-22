import tkinter as tk
from tkinter import messagebox
from Include.validacion import es_flotante, es_entero
from pprint import pprint


class DynamicAmplificationDialogo(tk.simpledialog.Dialog):
    def __init__(self, parent, title="Dynamic Magnification"):
        # Initialize instance variables using DoubleVar for storing float values
        self.zeta1 = tk.DoubleVar()
        self.zeta2 = tk.DoubleVar()
        self.deltazeta = tk.DoubleVar()
        self.tevaluado = tk.DoubleVar()
        self.resultDialog = tk.BooleanVar()
        self.resultDialog.set(False)
        super().__init__(parent, title)

    def body(self, master):
        # Create the labels of the damping 1 for the calculation of dynamic magnification in the Dynamic Seism software
        tk.Label(master, text="ζ1:").grid(row=0, column=0)
        self.zeta1_entry = tk.Entry(master)
        self.zeta1_entry.grid(row=0, column=1)
        tk.Label(master, text="Example: 0.05").grid(row=0, column=2, sticky="w")
        # Create the labels of the damping 2 for the calculation of dynamic magnification in the Dynamic Seism software
        tk.Label(master, text="ζ2:").grid(row=1, column=0)
        self.zeta2_entry = tk.Entry(master)
        self.zeta2_entry.grid(row=1, column=1)
        tk.Label(master, text="Example: 0.2").grid(row=1, column=2, sticky="w")
        # Create the labels of the delta damping for the calculation of dynamic magnification in the Dynamic Seism software
        tk.Label(master, text="Δζ:").grid(row=2, column=0)
        self.delta_entry = tk.Entry(master)
        self.delta_entry.grid(row=2, column=1)
        tk.Label(master, text="Example: 0.01").grid(row=2, column=2, sticky="w")
        # Create the labels of the period for the calculation of dynamic magnification in the Dynamic Seism software
        tk.Label(master, text="Period (s):").grid(row=3, column=0)
        self.period_entry = tk.Entry(master)
        self.period_entry.grid(row=3, column=1)
        tk.Label(master, text="Example: 1").grid(row=3, column=2, sticky="w")

        # return self.zeta1

    def apply(self):
        # Validate and convert user input to float, set instance variables
        con_errores = False
        # Validate each entry field for float values
        if es_flotante(self.zeta1_entry.get()) == False:
            con_errores = True
        if es_flotante(self.zeta2_entry.get()) == False:
            con_errores = True
        if es_flotante(self.delta_entry.get()) == False:
            con_errores = True
        if es_flotante(self.period_entry.get()) == False:
            con_errores = True
        else:
        # Comprobar si el período es mayor que cero después de convertirlo a float
            if float(self.period_entry.get()) <= 0:
                con_errores = True
                messagebox.showinfo("Alert", "The period must be greater than zero")
                return
                
        #if int(self.period_entry.get()) <= 0:
            #messagebox.showinfo("Alert", "The period must be greater than zero")
        # If no validation errors, convert and set the values to instance variables
        if con_errores == False:
            self.zeta1.set(float(self.zeta1_entry.get()))
            self.zeta2.set(float(self.zeta2_entry.get()))
            self.deltazeta.set(float(self.delta_entry.get()))
            self.tevaluado.set(float(self.period_entry.get()))
            self.resultDialog.set(True)
        else:
            # Display message if there are validation errors
            messagebox.showinfo(
                "Alert",
                "Verify that all data has been entered and is of the required data type",
            )
