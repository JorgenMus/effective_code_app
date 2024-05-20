import tkinter as tk  # pro vykresleni GUI aplikace
from tkinter import filedialog, messagebox # dialog okno a message okno
import pandas as pd  # pro pripadne nacitani a zpracovani dat z excel souboru
import math
import heapq  # prace s haldami (implementace Huffmanova kodovani)
import matplotlib.pyplot as pplt  # vytvoreni grafu/diagramu atd..
import networkx as nx  # vytvareni, manipulace grafu a siti (pro binarni stromy)
import gui_variables as gv  # global variables pro GUI
import json  # ulozeni/nacteni abecedy z JSON souboru

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
                                              command=self.on_load_alphabet)
        self.button_load_alphabet.pack(fill=tk.X)

        # tlacitko pro manualni zadani abecedy
        self.button_manual_input_alphabet = tk.Button(self.panel_alphabet,
                                                      text="Vytvořit abecedu",
                                                      command=self.manual_input_alphabet)
        self.button_manual_input_alphabet.pack(fill=tk.X)

        # data - pri inicializaci prazdne
        self.chars = []
        self.probabilities = []

    def on_load_alphabet(self):
        """Funkce provede nacteni abecedy ze souboru a kontrolu abecedy."""
        # nacti data abecedy z json souboru
        chars, probs = self.load_alphabet_from_json_file()

        # validace abecedy (pokud nejaka chyba spust editaci abecedy)
        if self.is_alphabet_valid(chars, probs) == False:
            size = max(len(chars), len(probs))
            chars, probs = self.edit_alphabet_window(size,
                                                     chars,
                                                     probs,
                                                     self.root)
            
        # DEBUG
        print(f"on_load_function: on exiting the function (alphabet should be repaierd):\nchars:\n{chars}\nprobs:\n{probs}")
        

    # funkce pro overeni predane abecedy, znaky abeedy museji byt kazdy 1 znak
    # pravdepodobnosti museji mit soucet 1.0 (100 procent)
    def is_alphabet_valid(self, chars, probs):
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
            if len(char) != 1:
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
            if prob_sum != 1.0:  # kontrola souctu pravdepodobnosti
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

    def load_alphabet_from_json_file(self):
        """Funkce načte abecedu zdrojových znaků ze souboru z JSON souboru.
        
        Funkce vrací 2 listy: [characters, probabilities]."""
        try:
            # prompt uzivateli kde muze otevrit json soubory s abecedou
            file_name = filedialog.askopenfilename(filetypes=[("JSON files",
                                                               "*.json")])
            
            # pokud uzivatel zvolil soubor pokracuj
            if file_name:
                with open(file_name, "r") as json_file:
                    # nacteni json dat do listu chars a probs
                    alphabet_data = json.load(json_file)
                    chars = alphabet_data.get(gv.JSON_CHARACTERS_NAME, [])
                    probs = alphabet_data.get(gv.JSON_PROBABILITIES_NAME, [])

                    # DEBUG
                    print("load_alphabet function:\n"
                          f"chars:\n{chars}\n"
                          f"probs:\n{probs}\n")
                    print(f"sum of probabilities: {sum(probs)}\n")
                    

                    return chars, probs
        except Exception as ex:
            messagebox.showerror("Chyba načtení abecedy",
                                 f"Došlo k chybě při načítání abecedy.\n{ex}")

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
        
    def save_alphabet_to_json(self, chars_list, probs_list):
        """Funkce ulozi abecedu prozatim do JSON formatu"""
        # try-except blok ulozi data do uzivatelem zadaneho souboru
        try:
            # zobrazeni dialogoveho okna uzivateli s moznosti ulozeni
            file_path = filedialog.asksaveasfilename(defaultextension=".json",
                                                     filetypes=[("JSON files",
                                                                 "*.json")])
            
            # vytvoreni dictionary udaju k ulozeni
            alphabet_data = {gv.JSON_CHARACTERS_NAME: chars_list,
                             gv.JSON_PROBABILITIES_NAME: probs_list}
            
            # otevrenni souboru pro zapis (automaticke uzavreni)
            with open(file_path, "w") as json_file:
                # zapis do json souboru
                json.dump(alphabet_data, json_file, indent=4)
            
            messagebox.showinfo("Uložení úspěšné",
                                "Abeceda byla uložena úspěšně do souboru "
                                f"{json_file.name}.")
        # zachyceni chybi pri ulozeni
        except Exception as ex:
            messagebox.showerror("Chyba uložení souboru",
                                 "Došlo k chybě při uložení souboru. "
                                 f"Chybové hlášení:\n{ex}")

    def edit_alphabet_window(self, size, chars_list, probs_list, parent_window):
        """Funkce vytvoří editační okno pro předanou abecedu.
        
        Umožní také abecedu uložit. a nebo ji použít pro program,
        tím pádem vrací 2 listy [characters, probabilities]."""
        # vytvoreni editacniho okna pro zadanou abecedu
        window = tk.Toplevel(parent_window)
        window.transient(parent_window)
        window.grab_set()

        # promenne pro navrat z funkce
        result_chars_list = []
        result_probs_list = []

        # omezeni velikosti okna
        screen_width = parent_window.winfo_screenwidth()
        screen_height = parent_window.winfo_screenheight()
        window.maxsize(width= int(screen_width - (gv.WINDOW_BUFFER * 2)),
                       height= int(screen_height - (gv.WINDOW_BUFFER * 8)))
        
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

        # DEBUG
        print(f"vytvareni celkem {size} polozek do okna\n")

        # vytvoreni input poli pro zadani znaku a jeho pravdepodobnosti
        # pokud byla funkce zavolana s hodnotami v chars a probs zapis je taky
        for i in range(size):
            # DEBUG
            print(f"row index = {i}\n")
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
            
            # pokud je pritomna hodnota vloz ji to policka
            if chars_list and i < len(chars_list):
                char_input.insert(0, chars_list[i])
            
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
            # pokud je pritomna hodnota s listu probs vloz ji
            if probs_list and i < len(probs_list):
                probability_input.insert(0, probs_list[i])

        def get_data():
            """Pomocná funkce získá znaky a pravdepodobnosti z user inputu.
            
            Funkce vrací 2 listy: [chars, probs]."""
            chars = []
            probs = []

            # for-loop projde vsechny slaves v okne a postupne ulozi hodnoty
            _, num_of_rows = alphabet_frame.grid_size()  # pocet rad v gridu
            
            # projdi vsechny rady mimo prvni a posledni
            for current_row in range(1, num_of_rows - 1):
                # ulozeni hodnoty v entry policku pro znak
                char_input = alphabet_frame.grid_slaves(row = current_row,
                                                        column = char_input_column)[0]
                prob_input = alphabet_frame.grid_slaves(row = current_row,
                                                        column = prob_input_column)[0]
                
                # pripojeni hodnot do seznamu chars a probs
                chars.append(char_input.get())
                probs.append(float(prob_input.get()))

            # vrat oba listy hodnot
            return chars, probs
        
        def on_save_alphabet(event=None):
            """Pomocná funkce získá zapsané hodnoty a uloží je."""
            # ziskani dat z kolonek znaku a pravdepodobnosti
            chars, probs = get_data()
            self.save_alphabet_to_json(chars, probs)

        def on_use_alphabet(event=None):
            """Pomocná funkce vrací 2 listy ze zadaných hodnot: [chars, probs]."""
            nonlocal result_chars_list, result_probs_list
            result_chars_list, result_probs_list = get_data()
            window.destroy()
            return result_chars_list, result_probs_list
        
        # pridani tlacitek pod zobrazene kolonky
        _, num_of_rows = alphabet_frame.grid_size()
        button_save_alphabet = tk.Button(alphabet_frame,
                                         text="Uložit",
                                         command=on_save_alphabet)
        button_save_alphabet.grid(row=num_of_rows,
                                  column=prob_label_column,
                                  sticky='e',
                                  pady=gv.LABEL_BUFFER_Y)
        button_use_alphabet = tk.Button(alphabet_frame,
                                        text="Použít abecedu",
                                        command=on_use_alphabet)
        button_use_alphabet.grid(row=num_of_rows,
                                 column=prob_input_column,
                                 pady=gv.LABEL_BUFFER_Y)

        # vycentrovani okna
        self.center_subwindow(window, parent_window)

        # update podokna
        window.update_idletasks()
        
        # reseni udalosti pro canvas
        def on_configure(event):
            """Pomocná funkce updatuje velikost okna a vycentruje ho."""
            canvas.configure(scrollregion=canvas.bbox("all"))
            resize_window()  # podle potreby zvetsi cele okno
            self.center_subwindow(window, parent_window)
        alphabet_frame.bind("<Configure>", on_configure)
        
        # posouvani nahoru-dolu koleckem
        def on_mouse_wheel(event):
            """Pomocná funkce řeší event scrollování kolečka myši."""
            canvas.yview_scroll(-int(event.delta / 60), "units")
        window.bind_all("<MouseWheel>", on_mouse_wheel)  # kolecko funguje po celem okne

        def resize_window():
            """Pomocná funkce upraví velikost okna podle jeho obsahu."""
            # ziskani rozmeru frame (ktery obsahuje kolonky pro zapis)
            frame_width = alphabet_frame.winfo_reqwidth() + scrollbar.winfo_width()
            frame_height = alphabet_frame.winfo_reqheight()

            # ziskani max rozmeru
            max_width, max_height = window.maxsize()

            # vypocet nove velikosti pro okno
            new_width = min(frame_width, max_width)
            new_height = min(frame_height, max_height)

            # update geometrie
            window.geometry(f"{new_width}x{new_height}")

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
