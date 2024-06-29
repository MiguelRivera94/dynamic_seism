import tkinter as tk

class NuevoProyectoDialog(tk.simpledialog.Dialog):
    def body(self, master):
        tk.Label(master, text="Project Name:").grid(row=0, sticky="w")
        self.entry_proyecto = tk.Entry(master)
        self.entry_proyecto.grid(row=0, column=1)
        return self.entry_proyecto

    def apply(self):
        nuevo_proyecto = self.entry_proyecto.get()
        self.result = nuevo_proyecto  # Guardar el resultado para acceder después