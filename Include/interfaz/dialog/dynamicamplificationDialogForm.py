import tkinter as tk
from tkinter import messagebox
from Include.validacion import es_flotante, es_entero
from pprint import pprint

class DynamicAmplificationDialogo(tk.simpledialog.Dialog):
    def __init__(self, parent, title="Dynamic Magnification"):
        self.zeta1 = tk.DoubleVar()
        self.zeta2 = tk.DoubleVar()
        self.deltazeta = tk.DoubleVar()
        self.tevaluado = tk.DoubleVar()
        self.resultDialog = tk.BooleanVar()

        
        #self.zeta1.set(0.05)
        #self.zeta2.set(0.2)
        #self.deltazeta.set(0.01)
        #self.tevaluado.set(1)
        self.resultDialog.set(False)

        super().__init__(parent, title)

    def body(self, master):
        tk.Label(master, text="ζ1:").grid(row=0, column=0)
        self.zeta1_entry = tk.Entry(master)
        self.zeta1_entry.grid(row=0, column=1)
        tk.Label(master, text="Example: 0.05").grid(row=0, column=2, sticky="w")

        tk.Label(master, text="ζ2:").grid(row=1, column=0)
        self.zeta2_entry = tk.Entry(master)
        self.zeta2_entry.grid(row=1, column=1)
        tk.Label(master, text="Example: 0.2").grid(row=1, column=2, sticky="w")

        tk.Label(master, text="Δζ:").grid(row=2, column=0)
        self.delta_entry = tk.Entry(master)
        self.delta_entry.grid(row=2, column=1)
        tk.Label(master, text="Example: 0.01").grid(row=2, column=2, sticky="w")

        tk.Label(master, text="Period (s):").grid(row=3, column=0)
        self.period_entry = tk.Entry(master)
        self.period_entry.grid(row=3, column=1)
        tk.Label(master, text="Example: 1").grid(row=3, column=2, sticky="w")

        #return self.zeta1

    def apply(self):
        con_errores = False
        if es_flotante(self.zeta1_entry.get() ) == False:
            con_errores = True
        if es_flotante(self.zeta2_entry.get() ) == False:
            con_errores = True
        if es_flotante(self.delta_entry.get() ) == False:
            con_errores = True
        if es_flotante(self.period_entry.get() ) == False:
            con_errores = True

        if con_errores == False:
            self.zeta1.set( float( self.zeta1_entry.get() ))
            self.zeta2.set( float( self.zeta2_entry.get() ))
            self.deltazeta.set( float( self.delta_entry.get() ))
            self.tevaluado.set( float( self.period_entry.get() ))
            self.resultDialog.set(True)
        else:
            messagebox.showinfo(
                        "Alert", 'Verify that all data has been entered and is of the required data type'
                    )              