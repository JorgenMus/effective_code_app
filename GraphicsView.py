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
        self.graphics_font = (gv.FONT_UNIVERSAL, gv.FONT_SIZE)

    def clear_frame(self):
        """Funkce vymaže veškerý obsah který má v tk.Frame uložený."""
        for slave in self.grid_slaves():
            slave.destroy()
            self.grid_forget()
    
    def show_alphabet(self, column_names_list, bottom_data_list, *lists_of_values):
        """Funkce do vytvoří tabulku předaných údajů.
        1 předaný list = 1 sloupec dat v tabulce.
        Všechny předané listy hodnot musí mít stejnou délku, pokud nemají
        bude do tabulky doplnena prázdná hodnota.
        
        avg_info_value - bude zobrazena v poslednim radku
        comun_names_list - list nazvu pro sloupce
        lists_of_values - listy hodnot pro jednotlive sloupce."""
        # nejdrive vymaz predchozi obsah
        self.clear_frame()

        # ziskani poctu predanych listu hodnot (1 list = 1 sloupec tabulky)
        num_of_lists = len(lists_of_values)

        # zjisteni nejdelsiho listu pro pripad ze nejaky predany list je kratsi
        max_list_length = max(len(data_list) for data_list in lists_of_values)

        # do prvniho radku umistit predane nazvy sloupcu
        for col, col_name in enumerate(column_names_list):
            label = tk.Label(self, text = col_name,
                             font = self.graphics_font,
                             borderwidth = gv.LABEL_BORDER_WIDTH,
                             relief = "solid")
            label.grid(row = 0,
                       column = col,
                       sticky = "nsew")
        # kazdemu listu se priradi jeho index (col) a projdou se vsechny listy
        for col_index, data_list in enumerate(lists_of_values):
            # prochazet se budou indexy (pro row) pro nejdelsi list
            for row_index in range(max_list_length):
                # try-except blok zkusi vlozit hodnotu pod indexem
                try:
                    value = data_list[row_index]  # kazdy element z listu na svuj radek
                except IndexError:  # pokud list neni tak dlouhy dopln stringem
                    value = "prázdné"
                
                # v pripade cisel zaokrouhli na 5 mist pro hezci zobrazeni
                if isinstance(value, (int, float)):
                    value = round(value, gv.NUM_OF_DECIMAL_PLACES)

                # vytvoreni label do tk.Frame
                label = tk.Label(self, text = f"{value}",  
                                 font = self.graphics_font, 
                                 borderwidth = gv.LABEL_BORDER_WIDTH,
                                 relief = "solid",
                                 anchor = "w")
                label.grid(row = row_index + 1,  # plus 1 kvuli prvni rade jmen sloupcu
                           column = col_index,
                           sticky = "nsew")
        
        # pod posledni vytvoreny radek pridej data z bottom_dala_list
        starting_row_index = max_list_length + 1  # zacinajici radek pro bottom data
        for i, row_data in enumerate(bottom_data_list):
            # aktualizace indexu row
            row_index = starting_row_index + i

            # prvni label
            label_1 = tk.Label(self,
                               text = row_data[0],
                               borderwidth = gv.LABEL_BORDER_WIDTH,
                               relief = "solid",
                               anchor = "w")
            label_1.grid(row = row_index,
                         column = 0,
                         columnspan = num_of_lists // 2,
                         sticky = "nsew")
            # druhy label
            label_2 = tk.Label(self,
                               text = row_data[1],
                               borderwidth = gv.LABEL_BORDER_WIDTH,
                               relief = "solid",
                               anchor = "w")
            label_2.grid(row = row_index,
                         column = num_of_lists // 2,
                         columnspan = num_of_lists // 2,
                         sticky = "nsew")
            
        label_avg = tk.Label(self,
                             text = "",
                             font = self.graphics_font,
                             borderwidth = gv.LABEL_BORDER_WIDTH,
                             relief = "solid")
        label_avg.grid(row = max_list_length + 1,
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

        # debug
        #print(f"show_test_info after: grid size = {self.grid_size()}\n")

    def center_position(self):
        self.parent.update_idletasks()
        parent_width = self.parent.winfo_width()
        parent_height = self.parent.winfo_height()
        width = self.winfo_reqwidth()
        height = self.winfo_reqheight()
        
        new_x = (parent_width // 2) - (width // 2)
        new_y = (parent_height // 2) - (height // 2)
        # debug 2. pokus o center
        #self.parent.create_window((new_x, new_y),
        #                          window = self,
        #                          anchor = "center")
        
        # debug 3. pokus o center
        self.parent.create_window((0, 0),
                                  window = self,
                                  anchor = "center")

    def move_to(self, x, y):
        # TODO
        pass