"""Soubor obsahuje třídu GraphicsView určenou pro jednotlivá zobrazení dat.

GraphicsView dědí z třídy tk.Frame a zabaluje do sebe předané"""

import tkinter as tk

class GraphicsView(tk.Frame):
    def __init__(self, parent):
        """Inicializace pro úvodní nastavení objektu."""
        super().__init__(parent)

