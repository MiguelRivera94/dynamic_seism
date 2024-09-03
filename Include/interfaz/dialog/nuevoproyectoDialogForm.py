import tkinter as tk

class NuevoProyectoDialog(tk.simpledialog.Dialog):
    def body(self, master):
        # Create a label and entry widget for project name input.
        tk.Label(master, text="Project Name:").grid(row=0, sticky="w")
        self.entry_proyecto = tk.Entry(master) # Entry widget for project name.
        self.entry_proyecto.grid(row=0, column=1) # Place entry widget in the grid.
        return self.entry_proyecto # Return the entry widget for focus management.

    def apply(self):
        # Get the project name from the entry widget.
        nuevo_proyecto = self.entry_proyecto.get()
        self.result = nuevo_proyecto  # Store the result to access later.