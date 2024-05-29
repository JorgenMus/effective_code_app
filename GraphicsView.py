"""Soubor obsahuje třídu GraphicsView určenou pro jednotlivá zobrazení dat.

GraphicsView dědí z třídy tk.Frame a zabaluje do sebe předané"""

import tkinter as tk
import gui_variables as gv
from EquationsManager import EquationsManager
from binary_tree_maker import BinaryTreeMaker
import platform  # ziskani jaky OS ma uzivatel

class GraphicsView(tk.Frame):
    """Třída umožňuje po inicializaci ukládat předané data do tk.Frame."""
    def __init__(self, parent):
        """Inicializace pro úvodní nastavení objektu."""
        super().__init__(parent)
        self.parent = parent
        self.graphics_font = (gv.FONT_UNIVERSAL, gv.FONT_SIZE)
        #self.configure(highlightbackground = gv.BLACK_COLOR,
        #               highlightcolor = gv.BLACK_COLOR,
        #               highlightthickness = gv.GRID_HIGHLIGHT_THICKNESS)
        parent.bind("<Configure>", self.on_configure)

        # inicializace manazera vzorcu
        self.equations_manager = EquationsManager(gv.FONT_EQUATIONS)
        self.equations_manager.load_images()

        # generator binarnich stromu
        self.bt_maker = BinaryTreeMaker()
        self.bt_current_image = None
        
        # rozmery pro grafy
        self.screen_size = self.get_screen_size()


    # event handler
    def on_configure(self, event):
        self.adjust_frame_size()

    # funkce vraci cely dictionary (nazev vzorce : vzorec string)
    def get_equations_dict(self):
        """Funkce vrací celý dictionary rovnic.
        
        dictionary rovnic: Nazev vzorce (string) : vzorec (latex string)"""
        return self.equations_manager.get_equations()
    
    # helper function vraci list latex stringu rovnic z equationsmanager tridy
    def get_equations_latex_string(self):
        # ziskani dictionary
        latex_dict = self.equations_manager.get_equations()

        latex_strings = [string for string in latex_dict.values()]

        # debug print
        #print(f"vracim stringy rovnic:\n{latex_strings}")

        return latex_dict  

    # funkce vraci rozmery monitoru
    def get_screen_size(self):
        """Funkce pomocí modulu ctype vraci sirku a vysku monitoru."""

        user_platform = platform.system()

        #debug
        #print(f"zjistena platforma: {user_platform}")

        screen_size = (gv.WINDOW_MIN_WIDTH, gv.WINDOW_MIN_HEIGHT)

        match user_platform:
            case "Windows":
                # windows pro ziskani velikosti obrazovky
                import ctypes
                user32 = ctypes.windll.user32
                screen_width = user32.GetSystemMetrics(0)
                screen_height = user32.GetSystemMetrics(1)
                screen_size = (screen_width, screen_height)
            case "Linux":
                # linux
                import subprocess
                output = subprocess.check_output(['xdpyinfo']).decode("utf-8")
                lines = output.split("\n")
                for line in lines:
                    if "dimensions:" in line:
                        size_str = line.split(":")[-1].strip()
                        width, height = map(int, size_str.split("x"))
                        screen_size = (width, height)
            case _:
                print(f"Systém {user_platform} neni podporován, některé rozměry"
                      "můžou být špatně nastaveny.")
        
        # debug
       # print(f"zjistena velikost obrazovky: {screen_size}")
        return screen_size

    # Funkce upravi rozmer frame na aktualni velikost gridu uvnitr
    def adjust_frame_size(self):
        """Funkce pro upravu rozmeru"""
        #debug
        #print("\t\tZavolano adjust_frame_size")

        # pokus update idletasks (neupdatujou se scrollbary v graphics_canvas)
        self.update_idletasks()

        # debug
        #print(f"adjusting frame size called start\n\tbefore update_idletasts\n\tbbox = {self.bbox('all')}\n")
        # update udalosti (zmena rozmeru atd)
        #self.update_idletasks()

        # vypocet nove width a height
        bbox = self.bbox("all")

        # pokud nejaky bounding-box (bbox) je, spocitej
        if bbox:
            #new_width = bbox[2] - bbox[0] + (2 * gv.GRID_BUFFER)
            #new_height = bbox[3] - bbox[1] + (2 * gv.GRID_BUFFER)
            new_width = bbox[2] - bbox[0]
            new_height = bbox[3] - bbox[1]
            self.config(width = new_width,
                        height = new_height)
        self.parent.config(scrollregion = self.parent.bbox("all"))

        

        #print(f"\tfnc end\n\tbbox = {self.bbox('all')}\nadjusting frame size end\n")


    def clear_frame(self):
        """Funkce vymaže veškerý obsah který má v tk.Frame uložený."""
        # vymazani udaju v gridu
        for slave in self.grid_slaves():
            slave.destroy()
            self.grid_forget()

        # vymazani predchozich grafu
        self.bt_maker = BinaryTreeMaker()  # vytvoreni noveho

    # funkce nastavi instanci teto tridy graf binarniho stromu
    def show_binary_tree(self, code_words, characters, graph_name=None):
        """Funkce využije třídu BinaryTreeMaker k zobrazení binarniho stromu."""
        # debug
        #print(f"zavolana show_binary_tree funkce.. ted by se mel vykreslit binarni strom...")  # debug
        # nejdrive vymaz predchozi obsah
        self.clear_frame()
        
        tree_label = tk.Label(self,
                              borderwidth = gv.LABEL_BORDER_WIDTH,
                              relief = "solid",
                              padx = gv.LABEL_BUFFER_X)
        try:
            # upraveni velikost pro graf
            graph_width = self.screen_size[0] - gv.WINDOW_BUFFER
            graph_height = self.screen_size[1] - gv.WINDOW_BUFFER

            # method 2 - velikost grafu podle velkosti parentu (canvas)-buffer
            graph_width = self.parent.winfo_width()
            graph_height = self.parent.winfo_height()

            #debug
            #print(f"velikost grafu: ({graph_width}, {graph_height})")

            self.bt_current_image = self.bt_maker.get_tree_image(code_words,
                                                                 characters,
                                                                 graph_name,
                                                                 (graph_width,
                                                                  graph_height))
            tree_label.configure(image = self.bt_current_image)
        except Exception as ex:
            # debug print
            #print(f"Nepodarilo se nacist obrazek grafu: {ex}")
            tree_label.configure(image = None)
        tree_label.grid(row = 0,
                     column = 0,
                     sticky = "nsew")
        print("\t\tted by se mel zobrazit binarni strom")

        # updatuj velikost
        self.adjust_frame_size()
    
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
                             padx = gv.LABEL_BUFFER_X,
                             pady = gv.LABEL_BUFFER_Y,
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
                                 padx = gv.LABEL_BUFFER_X,
                                 anchor = "w")
                label.grid(row = row_index + 1,  # plus 1 kvuli prvni rade jmen sloupcu
                           column = col_index,
                           sticky = "nsew")
        
        # pod posledni vytvoreny radek pridej data z bottom_dala_list
        # format: string, LaTex string, hodnota, jednotka
        starting_row_index = max_list_length + 1  # zacinajici radek pro bottom data
        for i, row_data in enumerate(bottom_data_list):
            # aktualizace indexu row
            row_index = starting_row_index + i

            # debug
            #print(f"zapisuju do row = {row_index} hodnoty {row_data[0]} a {row_data[1]}")


            # prvni label (text)
            label_1 = tk.Label(self,
                               text = row_data[0],
                               font = self.graphics_font,
                               borderwidth = gv.LABEL_BORDER_WIDTH,
                               relief = "solid",
                               padx = gv.LABEL_BUFFER_X,
                               anchor = "w")
            label_1.grid(row = row_index,
                         column = 0,
                         columnspan = num_of_lists - 2,
                         sticky = "nsew")
            # druhy label (vzorec nebo prazdne pole)
            label_2 = tk.Label(self,
                               borderwidth = gv.LABEL_BORDER_WIDTH,
                               relief = "solid",
                               padx = gv.LABEL_BUFFER_X)
            try:
                image = self.equations_manager.get_image(row_data[1])
                label_2.configure(image = image)
            except Exception as ex:
                # debug print
                #print(f"Nepodarilo se nacist obrazek rovnice: {ex}")
                label_2.configure(image = None)
            label_2.grid(row = row_index,
                         column = num_of_lists - 2,
                         sticky = "nsew")
            # treti label (vysledek + jednotka)
            label_3 = tk.Label(self,
                               text = f"{row_data[2]} {row_data[3]}",
                               font = self.graphics_font,
                               borderwidth = gv.LABEL_BORDER_WIDTH,
                               relief = "solid",
                               padx = gv.LABEL_BUFFER_X,
                               pady = gv.LABEL_BUFFER_Y)
                               #anchor = "e")
            label_3.grid(row = row_index,
                         column = num_of_lists - 1,
                         sticky = "nsew")
            
        # updatuj velikost
        self.adjust_frame_size()

    def show_test_info(self):
        self.clear_frame()
        test_label = tk.Label(self,
                              text = "TESTING MODE",
                              bg = "pink",
                              borderwidth=gv.LABEL_BORDER_WIDTH,
                              relief="solid")
        test_label.grid(row = 0, column = 0, sticky = "nsew")
        self.adjust_frame_size()

    # funkce zobrazi defaultni zpravu
    def show_default_message(self, txt_msg = "Zatím není co zobrazit"):
        print(f"byla zavolana show_default_message se zpravou '{txt_msg}'")
        self.clear_frame()
        
        default_label = tk.Label(self,
                                 text = txt_msg,
                                 bg = gv.RED_COLOR,
                                 background = gv.GRAY_COLOR,
                                 relief = "solid",
                                 anchor = "center")
        default_label.grid(row = 0,
                        column = 0,
                        columnspan = 5,
                        rowspan = 3,
                        sticky = "nsew")
        
        self.adjust_frame_size()


    # funkce vraci nutnou sirku a vysku pro obsazeni sebe sama
    def get_req_width_height(self):
        """Funkce vraci reqwidth a reqheight sebe sama."""
        # aktualizuj obsah
        self.update_idletasks()

        # vytazeni rozmeru
        reqwidth = self.winfo_reqwidth
        reqheight = self.winfo_reqheight

        # vrat rozmery jako tuple
        return reqwidth, reqheight
    
    #def center_position(self):
    #    self.parent.update_idletasks()
    #    parent_width = self.parent.winfo_width()
    #    parent_height = self.parent.winfo_height()
    #    width = self.winfo_reqwidth()
    #    height = self.winfo_reqheight()
    #    
    #    new_x = (parent_width // 2) - (width // 2)
    #    new_y = (parent_height // 2) - (height // 2)
    #    
    #    # pokus o center
    #    self.parent.create_window((0, 0),
    #                              window = self,
    #                              anchor = "center")