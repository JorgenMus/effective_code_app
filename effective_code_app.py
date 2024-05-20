import tkinter as tk  # pro vykresleni GUI aplikace
from tkinter import filedialog, messagebox # dialog okno a message okno
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
                                                      text="Vytvořit abecedu",
                                                      command=self.manual_input_alphabet)
        self.button_manual_input_alphabet.pack(fill=tk.X)

        # data - pri inicializaci prazdne
        self.chars = []
        self.probabilities = []

    # funkce pro overeni predane abecedy, znaky abeedy museji byt kazdy 1 znak
    # pravdepodobnosti museji mit soucet 1.0 (100 procent)
    def validate_alphabet(self, chars, probs):
        """Funkce ověřuje předanou abecedu.
        
        Počet znaků musí být roven počtu pravděpodobností,
        v seznamu znaků musí být každý znak o délce 1,
        v seznamu probs musí pouze čísla a jejich součet roven 1.0 "
        "(tzn 100 %)."""
        # overeni delky obou seznamu
        if len(chars) != len(probs):
            messagebox.showerror("Chyba ve zdrojové abecedě",
                                 "počet znaků zdrojové abecedy je jiný než "
                                 "počet předaných pravděpodobností.")
            return False
        
        # overeni znaku
        for i, char in enumerate(chars):
            if len(char) != 1.0:
                messagebox.showerror("Chyba ve zdrojové abecedě",
                                     f"Znak ({char}) na pozici {i + 1} "
                                     "je neplatný.")
                return False
        
        # overeni pravdepodobnosti
        try:
            prob_sum = 0.0
            for i, prob in enumerate(probs):
                if prob > 1 or prob < 0:  # kontrola hodnoty (0.0-1.0)
                    messagebox.showerror("Chyba ve zdrojové abecedě",
                                         f"Pravděpodobnost ({prob}) na pozici"
                                         f" {i + 1} není v rozsahu 0.0-1.0.")
                    return False
                prob_sum += i
            if prob_sum != 1:  # kontrola souctu pravdepodobnosti
                messagebox.showerror("Chyba ve zdrojové abecedě",
                                     "Součet pravděpodobností musí být roven"
                                     " 1 (tzn. 100 %), tato abeceda má součet "
                                     f"{prob_sum}%.")
                return False
        
        except ValueError:  # hodnota v pravdepodobnosti nejspis neni cislo
            messagebox.showerror("Chyba ve zdrojové abecedě",
                                 "Některá pravděpodobnost není platné číslo.")
            return False
        
        # kontroly OK vraci se True
        return True
    
    # pomocna funkce k zavreni predaneho okna a zmenu predaneho statusu na false
    def close_window(self, window):
        """Pomocná funkce uzavře předané okno"""
        window.destroy()

    def load_alphabet_from_file(self):
        """Funkce načte abecedu zdrojových znaků ze souboru."""
        file_name = filedialog.askopenfilename(filetypes=[("Text files", "*.txt"),
                                                          ("Excel files", "*.xlsx")])
        if file_name:
            # TODO implementace nacteni souboru a vykresleni abecedy do panelu abecedy
            pass

    def center_subwindow(self, window, parent_window):
        """Funkce vycentruje predane okno do rodicovskeho okna."""
        # update udalosti v okne
        window.update_idletasks()

        # ziskani pozice a rozmeru rodicovskeho okna
        parent_x = parent_window.winfo_x()
        parent_y = parent_window.winfo_y()
        parent_width = parent_window.winfo_width()
        parent_height = parent_window.winfo_height()

        # rozmery okna ktere se ma vycentrovat
        window_width = window.winfo_width()
        window_height = window.winfo_height()

        # vypocet nove (x, y) pozice pro okno
        new_x = parent_x + (parent_width // 2) - (window_width // 2)
        new_y = parent_y + (parent_height // 2) - (window_height // 2)
        window.geometry(f"{window_width}x{window_height}+{new_x}+{new_y}")
        
    def save_alphabet(self):
        """Funkce ulozi abecedu."""
        # TODO dopsat
        pass

    def use_alphabet(self):
        """Funkce použije vyplnenou abecedu a uzavře okno manual inputu."""
        # TODO dopsat
        pass

    def edit_alphabet_window(self, size, chars_list, probs_list, parent_window):
        """Pomocná funkce pro vytvoření požadovaného počtu input položek."""
        # vytvoreni editacniho okna pro zadanou abecedu
        window = tk.Toplevel(parent_window)
        window.transient(parent_window)
        window.grab_set()

        # omezeni velikosti okna
        screen_width = parent_window.winfo_screenwidth()
        screen_height = parent_window.winfo_screenheight()
        window.maxsize(width= int(screen_width - gv.WINDOW_BUFFER * 2),
                       height= int(screen_height - gv.WINDOW_BUFFER * 4))
        
        # nutno pouzit canvas pro umozneni scrolovani (scrollregion(l,t,r,b))
        canvas = tk.Canvas(window, scrollregion=(0, 0, 0,
                                                 gv.SCROLLBAR_VERTICAL_LIMIT))
        canvas.pack(side="left", fill="both", expand=True)

        # scrollbar na strane
        scrollbar = tk.Scrollbar(window, orient="vertical", command=canvas.yview)
        canvas.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side="right", fill="y")

        # vytvoreni frame pro zapouzdreni kolonek do gridu
        alphabet_frame = tk.Frame(canvas)
        canvas.create_window((0, 0), window = alphabet_frame, anchor="nw")

        # promenne pro urceni poradi sloupcu polozek v okne
        char_label_column = 0
        char_input_column = 1
        prob_label_column = 2
        prob_input_column = 3

        # vytvoreni input poli pro zadani znaku a jeho pravdepodobnosti
        for i in range(size):
            # label prompt pro zadani znaku
            char_label = tk.Label(alphabet_frame, text=f"Znak {i + 1}:")
            char_label.grid(row=i + 1, column=char_label_column,
                            padx=gv.LABEL_BUFFER_X,
                            pady=gv.LABEL_BUFFER_Y)
            # pole pro zadani znaku
            char_input = tk.Entry(alphabet_frame,
                                    bd=3, relief=tk.GROOVE)
            char_input.grid(row=i + 1, column=char_input_column,
                            padx=gv.LABEL_BUFFER_X,
                            pady=gv.LABEL_BUFFER_Y)
            
            #label prompt pro zadani pravdepodobnosti znaku
            probability_label = tk.Label(alphabet_frame,
                                         text=f"Pravděpodobnost znaku {i + 1}:")
            probability_label.grid(row=i + 1, column=prob_label_column,
                                   padx=gv.LABEL_BUFFER_X,
                                   pady=gv.LABEL_BUFFER_Y)
            # pole pro zadani pravdepodobnosti
            probability_input = tk.Entry(alphabet_frame,
                                         bd=3, relief=tk.GROOVE)
            probability_input.grid(row=i + 1, column=prob_input_column,
                                   padx=gv.LABEL_BUFFER_X,
                                   pady=gv.LABEL_BUFFER_Y)
        
        # udaje pro urceni delek predanych seznamu znaku a pravdepodobnosti
        alphabet_index = 0
        chars_length = len(chars_list)
        probs_length = len(probs_list)

        # projiti vsech slaves v okne a zapis pritomne predane hodnoty
        for slave in alphabet_frame.grid_slaves():
            # update rady na ktere se nachazi aktualni slave
            alphabet_index = int(slave.grid_info()["row"])
            # reseni zapisu znaku abecedy
            if int(slave.grid_info()["column"]) == char_input_column:
                if isinstance(slave, tk.Entry) and alphabet_index < chars_length:
                    slave.insert(tk.END, chars_list[alphabet_index])
            # reseni zapisu pravdepodobnosti znaku
            if int(slave.grid_info()["column"]) == prob_input_column:
                if isinstance(slave, tk.Entry) and alphabet_index < probs_length:
                    slave.insert(tk.END, probs_list[alphabet_index])

        # pridani tlacitek pod zobrazene kolonky
        _, num_of_rows = alphabet_frame.grid_size()
        button_save_alphabet = tk.Button(alphabet_frame,
                                         text="Uložit",
                                         command=self.save_alphabet)
        button_save_alphabet.grid(row=num_of_rows,
                                  column=prob_label_column,
                                  sticky='e',
                                  pady=gv.LABEL_BUFFER_Y)
        button_use_alphabet = tk.Button(alphabet_frame,
                                        text="Použít abecedu",
                                        command=self.use_alphabet)
        button_use_alphabet.grid(row=num_of_rows,
                                 column=prob_input_column,
                                 pady=gv.LABEL_BUFFER_Y)

        # vycentrovani okna
        self.center_subwindow(window, parent_window)

        # update podokna
        window.update_idletasks()
        
        # reseni udalosti pro canvas
        def on_configure(event):
            canvas.configure(scrollregion=canvas.bbox("all"))
        alphabet_frame.bind("<Configure>", on_configure)
        
        # posouvani nahoru-dolu koleckem
        def on_mouse_wheel(event):
            canvas.yview_scroll(-int(event.delta / 60), "units")
        window.bind_all("<MouseWheel>", on_mouse_wheel)  # kolecko funguje po celem okne

    def prompt_for_alphabet_size(self, parent_window):
        """Funkce vytvoří nové podokno do předaného root okna.
        
        Získá input od uživatele kolik znaků nové zdrojové abecedy má vytvořit
        výsledný počet vrátí."""
        # prvotni hodnota v zadanem poctu znaku
        num_of_chars = None

        # pomocna funkce resi kliknuti na tlacitko pro potvrzeni abecedy
        def confirm():
            """Pomocná funkce oveří zda uživatelem zadaná hodnota je v pořádku."""
            nonlocal num_of_chars
            try:
                input_value = int(input_field.get())
                if input_value <= 0:  # uzivatel by mel zadat alespon 1
                    raise ValueError
                num_of_chars = input_value
                self.close_window(window)
            except ValueError:
                messagebox.showerror("Chyba počtu zdrojových znaků abecedy.",
                                    "Zadejte prosím celé kladné číslo "
                                    "pro počet znaků zdrojové abecedy.")
                num_of_chars = None
        
        # pomocna funkce resi udalost pri zavreni okna
        def on_close():
            """Funkce uzavira okno a vraci None."""
            nonlocal num_of_chars
            num_of_chars = None
            self.close_window(window)

        # vytvoreni noveho okna (nastaveni transient a grab_set)
        window = tk.Toplevel(parent_window)
        window.transient(parent_window)
        window.grab_set()

        # rozmery a titulek okna
        window_width = int(gv.WINDOW_MIN_WIDTH // 2)
        window_height = int(gv.WINDOW_MIN_HEIGHT // 2)
        window.minsize(window_width, window_height)
        window.title("Ruční zadání zdrojové abecedy")

        # label a pole pro zadani poctu znaku abecedy
        label = tk.Label(window, text="Zadejte počet znaků abecedy:")
        label.grid(row=0, column=0,
                   padx=gv.LABEL_BUFFER_X,
                   pady=gv.LABEL_BUFFER_Y)

        # input pole a shortcut (klavesa enter)
        input_field = tk.Entry(window, bd=3, relief=tk.GROOVE)
        input_field.grid(row=0, column=1,
                   padx=gv.LABEL_BUFFER_X,
                   pady=gv.LABEL_BUFFER_Y)

        input_field.bind("<Return>", lambda event: confirm())  
        
        # nastaveni eventu pro zavreni okna (status nutno predat jako list)
        window.protocol("WM_DELETE_WINDOW", on_close)
        
        # tlacitko pro potvrzeni poctu znaku v abecede
        confirm_button = tk.Button(window,
                                   text="Nová abeceda",
                                   command=lambda: confirm())
        confirm_button.grid(row=0, column=2, sticky='w',
                            padx=gv.LABEL_BUFFER_X,
                            pady=gv.LABEL_BUFFER_Y*2)
        
        # update pozice podokna
        self.center_subwindow(window, parent_window)

        self.root.wait_window(window)

        return num_of_chars
        
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
        # ziskani poctu znaku pro novou abecedu
        num_of_characters = self.prompt_for_alphabet_size(self.root)

        # pokud nebyl zadan pocet znaku vrat se do hlavniho okna
        if num_of_characters == None:
            return
        

        # DEBUG
        print(f"fce manual_input_alphabet: num_of_characters = {num_of_characters}\n")


        # debug cvicne znaky a pravdepodobnosti
        default_chars = ['A', 'B', 'C', 'D']
        default_probs = [0.25, 0.50, 0.20, 0.05]

        # otevreni editace abecedy s prazdnou abecedou
        chars = []
        probs = []
        data = self.edit_alphabet_window(num_of_characters, chars, probs, self.root)
       

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
