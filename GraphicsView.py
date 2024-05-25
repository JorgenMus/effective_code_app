"""Soubor obsahuje třídu GraphicsView určenou pro jednotlivá zobrazení dat.

GraphicsView dědí z třídy tk.Frame a zabaluje do sebe předané"""

import tkinter as tk
import gui_variables as gv

class GraphicsView(tk.Frame):
    """Třída umožňuje po inicializaci ukládat předané data do tk.Frame."""
    def __init__(self, parent):
        """Inicializace pro úvodní nastavení objektu."""
        super().__init__(parent)
        self.parent = parent

    def clear_frame(self):
        """Funkce vymaže veškerý obsah který má v tk.Frame uložený."""
        for slave in self.grid_slaves():
            slave.destroy()
    
    def show_alphabet(self, avg_info_value, *lists_of_values):
        """Funkce do vytvoří tabulku předaných údajů.
        1 předaný list = 1 sloupec dat v tabulce.
        Všechny předané listy hodnot musí mít stejnou délku, pokud nemají
        bude do tabulky doplnena prázdná hodnota."""
        # nejdrive vymaz predchozi obsah
        self.clear_frame()

        # ziskani poctu predanych listu hodnot (1 list = 1 sloupec tabulky)
        num_of_lists = len(lists_of_values)

        # zjisteni nejdelsiho listu pro pripad ze nejaky predany list je kratsi
        max_list_length = max(len(list) for list in lists_of_values)

        # prochazet se budou indexy pro nejdelsi list
        for row_index in range(max_list_length):  # row zastupuje dany element konkretnim listu
            # kazdemu listu se priradi jeho index (col) a projdou se vsechny listy
            for col_index, list in enumerate(lists_of_values):  # enumerate >> (number, list)
                # try-except blok zkusi vlozit hodnotu pod indexem
                try:
                    value = list[row_index]  # kazdy element z listu na svuj radek
                except IndexError:  # pokud list neni tak dlouhy dopln stringem
                    value = "prázdné"
                
                # vytvoreni label do tk.Frame
                label = tk.Label(self, text = f"{value}",     
                                 borderwidth = gv.LABEL_BORDER_WIDTH,
                                 relief = "solid")
                label.grid(row = row_index,
                           column = col_index,
                           sticky = "nsew")
        
        # pod posledni vytvoreny radek pridej label pro avg_info_value
        label_avg = tk.Label(self,
                             text = f"Průměrná informační hodnota znaku: {avg_info_value}",
                             borderwidth = gv.LABEL_BORDER_WIDTH,
                             relief = "solid")
        label_avg.grid(row = max_list_length,
                       column = 0,
                       columnspan = num_of_lists, sticky = "nsew")
        
        # zabalit do okna s novou velikosti
        self.center_position()

    def show_test_info(self):
        self.clear_frame()
        test_label = tk.Label(self,
                              text = "TESTING MODE",
                              bg = "pink",
                              borderwidth=gv.LABEL_BORDER_WIDTH,
                              relief="solid")
        test_label.grid(row = 0, column = 0, sticky = "nsew")
        self.center_position()

    def center_position(self):
        self.parent.update_idletasks()
        parent_width = self.parent.winfo_width()
        parent_height = self.parent.winfo_height()
        width = self.winfo_reqwidth()
        height = self.winfo_reqheight()
        new_x = (parent_width // 2) - (width // 2)
        new_y = (parent_height // 2) - (height // 2)
        self.parent.create_window((new_x, new_y),
                                  window = self,
                                  anchor = "center")
        
        #debug
        print(f"centruju pozici graphicsview:\n"
              f"\tparent width, height: ({parent_width}, {parent_height})\n"
              f"\twidth, height: ({width}, {height})\n"
              f"\tstare coords: ({self.winfo_x()}, {self.winfo_y()}\n"
              f"\tnove coords: ({new_x}, {new_y})\n")

    def move_to(self, x, y):
        # TODO
        pass