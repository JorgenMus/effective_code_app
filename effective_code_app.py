import tkinter as tk  # pro vykresleni GUI aplikace
from tkinter import filedialog, messagebox  # dialog okno a message okno
import pandas as pd  # pro pripadne nacitani a zpracovani dat z excel souboru
import math
import heapq  # prace s haldami (implementace Huffmanova kodovani)
import matplotlib.pyplot as pplt  # vytvoreni grafu/diagramu atd..
import networkx as nx  # vytvareni, manipulace grafu a siti (pro binarni stromy)
import gui_variables as gv  # global variables pro GUI

# trida pro hlavni okno aplikace
class EffectiveCodeApp:
    """Třída pro vykreslení okna aplikace a řešení GUI.
    
    Při inicializaci nastaví hlavní okno aplikace a vytvoří widgets."""

    def __init__(self, root):
        """Nastavení hlavního okna a titulku, vytvoření widgets."""
        # vytvoreni a pojmenovani okna
        self.root = root
        self.root.title("Efektivní kódování")
        
        # hlavni frame ktery bude obsahovat vsechny ostatni panely
        self.main_frame = tk.Frame(self.root)
        self.main_frame.pack(fill=tk.BOTH, expand=True)

        # panel nastroju
        self.panel_tools = tk.Frame(self.main_frame,
                                    height=gv.PANEL_TOOLS_HEIGHT,
                                    bg=gv.PANEL_TOOLS_BG,
                                    borderwidth=gv.PANEL_BORDER_WIDTH,
                                    relief=gv.PANEL_RELIEF_STYLE)
        self.panel_tools.pack(fill=tk.X)  # fill na sirku

        # panel pro abecedu
        self.panel_alphabet = tk.Frame(self.main_frame,
                                       width=gv.PANEL_ALPHABET_WIDTH,
                                       bg=gv.PANEL_ALPHABET_BG,
                                       borderwidth=gv.PANEL_BORDER_WIDTH,
                                       relief=gv.PANEL_RELIEF_STYLE)
        self.panel_alphabet.pack(side=tk.LEFT,  # leva strana okna
                                 fill=tk.Y)  # fill na vysku

        # panel pro grafiku (vykreslovani stromu atd..)
        self.panel_graphics = tk.Frame(self.main_frame,
                                       bg=gv.PANEL_GRAPHICS_BG,
                                       borderwidth=gv.PANEL_BORDER_WIDTH,
                                       relief=gv.PANEL_RELIEF_STYLE)
        self.panel_graphics.pack(side=tk.RIGHT,
                                 fill=tk.BOTH,
                                 expand=True)
        
        # label pro panel abecedy
        self.label_alphabet = tk.Label(self.panel_alphabet,
                                       text="Zdrojová abeceda",
                                       bg=gv.PANEL_ALPHABET_LABEL_BG)
        self.label_alphabet.pack(fill=tk.X)

        # tlacitko pro nacteni ze souboru
        self.button_load_alphabet = tk.Button(self.panel_alphabet,
                                              text="Načíst ze souboru",
                                              command=self.load_alphabet_from_file)
        self.button_load_alphabet.pack(fill=tk.X)

        # tlacitko pro manualni zadani abecedy
        self.button_manual_input_alphabet = tk.Button(self.panel_alphabet,
                                                      text="Zadat ručně",
                                                      command=self.manual_input_alphabet)
        self.button_manual_input_alphabet.pack(fill=tk.X)

        # data - pri inicializaci prazdne
        self.chars = []
        self.probabilities = []

        # trackovani otevreneho podokna
        self.manual_input_window_opened = False

    # funkce pro overeni predane abecedy, znaky abeedy museji byt kazdy 1 znak
    # pravdepodobnosti museji mit soucet 100 (procent)
    def validate_alphabet(self, chars, probs):
        """Funkce ověřuje předanou abecedu.
        
        Počet znaků musí být roven počtu pravděpodobností,
        v seznamu znaků musí být každý znak o délce 1,
        v seznamu probs musí pouze čísla a jejich součet roven 100 (%)."""
        # overeni delky obou seznamu
        if len(chars) != len(probs):
            messagebox.showerror("Chyba ve zdrojové abecedě",
                                 "počet znaků zdrojové abecedy je jiný než "
                                 "počet předaných pravděpodobností.")
            return False
        
        # overeni znaku
        for i, char in enumerate(chars):
            if len(char) != 1:
                messagebox.showerror("Chyba ve zdrojové abecedě",
                                     f"Znak ({char}) na pozici {i + 1} "
                                     "je neplatný.")
                return False
        
        # overeni pravdepodobnosti
        try:
            prob_sum = 0
            for i, prob in enumerate(probs):
                if prob > 100 or prob < 0:  # kontrola hodnoty (0-100)
                    messagebox.showerror("Chyba ve zdrojové abecedě",
                                         f"Pravděpodobnost ({prob}) na pozici"
                                         f" {i + 1} není v rozsahu 0-100 %.")
                    return False
                prob_sum += i
            if prob_sum != 100:  # kontrola souctu pravdepodobnosti
                messagebox.showerror("Chyba ve zdrojové abecedě",
                                     "Součet pravděpodobností musí být roven"
                                     " 100 %, tato abeceda má součet "
                                     f"{prob_sum}%.")
                return False
        
        except ValueError:  # hodnota v pravdepodobnosti nejspis neni cislo
            messagebox.showerror("Chyba ve zdrojové abecedě",
                                 "Některá pravděpodobnost není platné číslo.")
            return False
        
        # kontroly OK vraci se True
        return True
    
    # pomocna funkce k zavreni predaneho okna a zmenu predaneho statusu na false
    def close_window(self, window, window_status):
        """Pomocná funkce uzavře předané okno a nastaví status na false."""
        window_status[0] = False  # nutno predat jako list, aby se zmena projevila mimo funkci
        window.destroy()

    def load_alphabet_from_file(self):
        """Funkce načte abecedu zdrojových znaků ze souboru."""
        file_name = filedialog.askopenfilename(filetypes=[("Text files", "*.txt"),
                                                          ("Excel files", "*.xlsx")])
        if file_name:
            # TODO implementace nacteni souboru a vykresleni abecedy do panelu abecedy
            pass

    def manual_input_alphabet(self):
        """Funkce umožní uživateli manuálně zadat zdrojovou abecedu.
        
        Okno je nastaveno tak, aby se nejdříve zeptalo uživatele
        na počet znaků v abecedě a podle toho vytvořilo odpovídající
        počet kolonek pro znaky a pravděpodobnosti. Uživatel má stále
        možnost změnit počet znaků v abecedě, pokaždé se vytvoří nové
        a prázdné kolonky. Okno má rovněž nastavený event handler
        pro uzavření okna a po otevření tohoto okna musí uživatel
        okno jedním ze způsobů ukončit (např. křížek, potvrzení abecedy)
        aby se mohl vrátit do hlavního okna."""
        # zamezeni otevreni tohoto okna vicekrat
        if (self.manual_input_window_opened == True):
            return  # nic nedelej a vrat se do hlavniho okna
        
        self.manual_input_window_opened = True
        
        # vytvoreni noveho okna kam bude uzivatel zadavat znaky abecedy
        manual_input_window = tk.Toplevel(self.root)

        # nastaveni aby okno muselo byt vyreseno pred navratem do hlavniho okna
        manual_input_window.transient(self.root)
        manual_input_window.grab_set()

        # rozmery noveho okna
        window_width = int(gv.WINDOW_MIN_WIDTH // 2)
        window_height = int(gv.WINDOW_MIN_HEIGHT // 2)
        manual_input_window.minsize(window_width, window_height)
        
        # titulek okna
        manual_input_window.title("Ruční zadání zdrojové abecedy")

        # label prompt a entry field pro uzivatele k zadani poctu znaku v abecede
        num_of_characters_label = tk.Label(manual_input_window,
                                           text="Zadejte počet znaků abecedy:")
        num_of_characters_label.grid(row=0, column=0,
                                     padx=gv.LABEL_BUFFER_X, pady=gv.LABEL_BUFFER_Y)
        num_of_characters_input = tk.Entry(manual_input_window,
                                           bd=3, relief=tk.GROOVE)
        num_of_characters_input.grid(row=0, column=1,
                                     padx=gv.LABEL_BUFFER_X, pady=gv.LABEL_BUFFER_Y)       
        
        # nastaveni eventu pro zavreni okna (status nutno predat jako list)
        manual_input_window.protocol(
            "WM_DELETE_WINDOW",
            lambda: self.close_window(manual_input_window,
                                      [self.manual_input_window_opened]))

        def center_subwindow(event=None):
            """Funkce automaticky zvětší rozměry podokna podle jejího obsahu.

            Dále jej vycentruje do hlavniho okna (bere v uvahu velikost hlavního okna)."""
            # ziskani updatovanych rozmeru podokna
            manual_input_window.update_idletasks()
            updated_width = manual_input_window.winfo_reqwidth() + gv.WINDOW_BUFFER
            updated_height = manual_input_window.winfo_reqheight() + gv.WINDOW_BUFFER

            # ziskani aktualnich rozmeru hlavniho okna
            root_width = self.root.winfo_width()

            # vypocet novych koordinatu podokna
            subwindow_x = self.root.winfo_x() + (root_width - updated_width) // 2
            subwindow_y = self.root.winfo_y() + gv.WINDOW_BUFFER

            # nastaveni nove pozice a rozmeru + vycentrovani do hlavniho okna
            manual_input_window.geometry(
                f"{updated_width}x{updated_height}+{subwindow_x}+{subwindow_y}")
        
        def save_alphabet(event=None):
            """Funkce ulozi abecedu."""
            # TODO dopsat
            pass

        def use_alphabet(event=None):
            """Funkce použije vyplnenou abecedu a uzavře okno manual inputu."""
            # TODO dopsat
            pass

        def create_input_fields(event=None):
            """Pomocná funkce pro vytvoření požadovaného počtu input položek."""
            # vytvoreni variable pro zadany pocet znaku abecedy
            # a kontrola zda uzivatel zadal hodnotu
            try:
                num_of_characters = int(num_of_characters_input.get())
                if num_of_characters <= 0:  # uzivatel by mel zadat alespon 1
                    raise ValueError
            except ValueError:
                messagebox.showerror("Chyba počtu zdrojových znaků abecedy.",
                                     "Zadejte prosím celé kladné číslo "
                                     "pro počet znaků zdrojové abecedy.")
                return

            # vymaze predchozi radky
            for widget in manual_input_window.grid_slaves():
                if int(widget.grid_info()["row"]) > 0:
                    widget.grid_forget()

            # vytvoreni input poli pro zadani znaku a jeho pravdepodobnosti
            for i in range(num_of_characters):
                # label prompt pro zadani znaku
                char_label = tk.Label(manual_input_window, text=f"Znak {i + 1}:")
                char_label.grid(row=i + 1, column=0,
                                padx=gv.LABEL_BUFFER_X,
                                pady=gv.LABEL_BUFFER_Y)
                # pole pro zadani znaku
                char_input = tk.Entry(manual_input_window,
                                      bd=3, relief=tk.GROOVE)
                char_input.grid(row=i + 1, column=1,
                                padx=gv.LABEL_BUFFER_X,
                                pady=gv.LABEL_BUFFER_Y)
                
                #label prompt pro zadani pravdepodobnosti znaku
                probability_label = tk.Label(manual_input_window,
                                             text=f"Pravděpodobnost znaku {i + 1}:")
                probability_label.grid(row=i + 1, column=2,
                                       padx=gv.LABEL_BUFFER_X,
                                       pady=gv.LABEL_BUFFER_Y)
                # pole pro zadani pravdepodobnosti
                probability_input = tk.Entry(manual_input_window,
                                             bd=3, relief=tk.GROOVE)
                probability_input.grid(row=i + 1, column=3,
                                       padx=gv.LABEL_BUFFER_X,
                                       pady=gv.LABEL_BUFFER_Y)
                
            # pridani tlacitek pod zobrazene kolonky
            num_of_cols, num_of_rows = manual_input_window.grid_size()
            button_save_alphabet = tk.Button(manual_input_window,
                                             text="Uložit",
                                             command=save_alphabet)
            button_save_alphabet.grid(row=num_of_rows,
                                      column=num_of_cols-2,
                                      sticky='e',
                                      pady=gv.LABEL_BUFFER_Y)
            button_use_alphabet = tk.Button(manual_input_window,
                                            text="Použít abecedu",
                                            command=use_alphabet)
            button_use_alphabet.grid(row=num_of_rows,
                                     column=num_of_cols-1,
                                     pady=gv.LABEL_BUFFER_Y)
                
            # update podokna
            center_subwindow()
                
        # tlacitko pro potvrzeni poctu znaku v abecede
        # (toto vygeneruje policka pro zadani znaku a pravdepodobnosti)
        confirm_num_of_chars_button = tk.Button(manual_input_window,
                                                text="Nová abeceda",
                                                command=create_input_fields)
        confirm_num_of_chars_button.grid(row=0, column=2, sticky='w',
                                         padx=gv.LABEL_BUFFER_X,
                                         pady=gv.LABEL_BUFFER_Y*2)
        # shortcut pro enter (ekvivalent stiskuti tlacitka "nova abeceda")
        num_of_characters_input.bind("<Return>", create_input_fields)

        # update podokna
        center_subwindow()

        

# pokud se jedna o spousteci soubor spust aplikaci
if __name__ == "__main__":
    root = tk.Tk()  # vytvoreni hlavniho okna
    root.minsize(gv.WINDOW_MIN_WIDTH, gv.WINDOW_MIN_HEIGHT)  # minimalni velikost okna
    
    # vycentrovani aplikace
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    x = (screen_width - gv.WINDOW_MIN_WIDTH) // 2
    y = (screen_height - gv.WINDOW_MIN_HEIGHT) // 2
    root.geometry(f"{gv.WINDOW_MIN_WIDTH}x{gv.WINDOW_MIN_HEIGHT}+{x}+{y}")

    app = EffectiveCodeApp(root)  # vytvoreni instance tridy pro program
    root.mainloop()  # hlavni smycka pro zobrazovani GUI a reseni eventu..
