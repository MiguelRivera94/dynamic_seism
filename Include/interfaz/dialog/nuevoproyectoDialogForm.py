import tkinter as tk

class NuevoProyectoDialog(tk.simpledialog.Dialog):
    def body(self, master):
        # Generates a project name label that is entered by users in the Dynamic Seism Software
        tk.Label(master, text="Project Name:").grid(row=0, sticky="w")
        self.entry_proyecto = tk.Entry(master) # Entry widget for project name.
        self.entry_proyecto.grid(row=0, column=1) # Place entry widget in the grid.
        return self.entry_proyecto # Return the entry widget for focus management.

    def apply(self):
        # Get the project name that is entered by users from the windows in the Dynamic Seism Software
        nuevo_proyecto = self.entry_proyecto.get()
        self.result = nuevo_proyecto  # Store the result to access later.