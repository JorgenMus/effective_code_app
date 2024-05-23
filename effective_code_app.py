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
        self.panel_modes = tk.Frame(self.main_frame,
                                    height=gv.PANEL_MODES_HEIGHT,
                                    bg=gv.PANEL_MODES_BG,
                                    borderwidth=gv.PANEL_BORDER_WIDTH,
                                    relief=gv.PANEL_RELIEF_STYLE)
        self.panel_modes.pack(fill=tk.X)  # fill na sirku

        # panel pro abecedu
        self.panel_alphabet = tk.Frame(self.main_frame,
                                       width=gv.PANEL_ALPHABET_WIDTH,
                                       bg=gv.PANEL_ALPHABET_BG,
                                       borderwidth=gv.PANEL_BORDER_WIDTH,
                                       relief=gv.PANEL_RELIEF_STYLE)
        self.panel_alphabet.pack(side=tk.LEFT,  # leva strana okna
                                 fill=tk.Y,  # fill na vysku
                                 expand = False)  # nebude se rozsirovat  

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
        self.label_alphabet.bindtags((gv.PERMANENT_TAG_STRING,)
                                     + self.label_alphabet.bindtags())

        # tlacitko pro nacteni ze souboru
        self.button_load_alphabet = tk.Button(self.panel_alphabet,
                                              text="Načíst ze souboru",
                                              command=self.on_load_alphabet)
        self.button_load_alphabet.pack(fill=tk.X)
        self.button_load_alphabet.bindtags((gv.PERMANENT_TAG_STRING,)
                                     + self.button_load_alphabet.bindtags())

        # tlacitko pro manualni zadani abecedy
        self.button_manual_input_alphabet = tk.Button(self.panel_alphabet,
                                                      text="Vytvořit abecedu",
                                                      command=self.manual_input_alphabet)
        self.button_manual_input_alphabet.pack(fill=tk.X)
        self.button_manual_input_alphabet.bindtags((gv.PERMANENT_TAG_STRING,)
                                                   + self.button_manual_input_alphabet.bindtags())

        # data - pri inicializaci prazdne
        self.characters_list = []
        self.probabilities_list = []

        # aktualni mod zobrazeni pro graficky panel
        self.current_mode = None

    # funkce updatuje vzhled tlacitek podle aktualniho modu
    def update_buttons_style(self, active_button):
        """Funkce updatuje vzhled tlačítek panelu módů podle aktuálního módu."""
        # projdi vsechny buttons v panelu modu
        for button in self.panel_modes.winfo_children():
            # pro aktivni tlacitko se nastavi odlisny vzhled
            if button == active_button:
                button.config(bg = gv.ACTIVE_BUTTON_COLOR,  # aktivni button
                              relief = gv.ACTIVE_BUTTON_RELIEF)
            else:
                button.config(bg = gv.INACTIVE_BUTTON_COLOR,  # neaktivni button
                              relief = gv.INACTIVE_BUTTON_RELIEF)

    # funkce vymaze widgety z panelu modu
    def clear_panel_modes(self):
        """Funkce vymaže obsah panelu módů."""
        for widget in self.panel_modes.winfo_children():
            widget.destroy()

    # funkce vymaze widgety v grafickem panelu a pripravi tak pro nove udaje
    def clear_panel_graphics(self):
        """Funkce vymaže obsah grafického panelu (widgets)."""
        for widget in self.panel_graphics.winfo_children():
            widget.destroy()

    # Funkce vypise do panel_graphics informace o abecede
    def show_alphabet_info(self):
        """Funkce do grafického panelu vypíše informace o zdrojové abecedě."""
        # nejdrive vycistit panel
        self.clear_panel_graphics()
        
        # informace o abecede
        txt = "informace o zdrojové abecedě:\n"
        for char, prob in zip(self.characters_list, self.probabilities_list):
            txt += f"{char}: {prob:.2f} %\n"

        label_info = tk.Label(self.panel_graphics,
                              text = txt,
                              justify = tk.LEFT)
        label_info.pack(fill = tk.BOTH,
                        expand = True)

    # debug test function (to be replaces later)
    def show_test_stuff(self):
        self.clear_panel_graphics()
        test_label = tk.Label(self.panel_graphics,
                              text = "TESTING MODE",
                              bg = "pink")
        test_label.pack(fill="both", expand=True)

    # funkce pro vytvoreni tlacitek pro prepinani modu zobrazeni abecedy
    def create_modes_buttons(self):
        """Funkce vytvoří sadu tlačítek na panel nástrojů.
        
        Tlačítka se uživateli zobrazí až v případě, že načte, nebo
        vytvoří a použije abecedu znaků. Slouží k přepínání režimů zobrazení
        informací o zdrojové abecedě a použití."""

        # funkce nastavi aktualni mod podle stisknuteho button modu
        def set_active_mode(mode, button):
            """Funkce nastaví aktuální mód a updatuje vzhled tlačítek."""
            self.current_mode = mode
            self.update_buttons_style(button)

            # podle modu zobraz pozadovane data do grafickeho panelu
            match mode:
                case gv.MODE_ALPHABET_INFORMATION:
                    self.show_alphabet_info()
                case gv.MODE_TESTING:
                    self.show_test_stuff()
                # TODO zde doplnit dalsi tlacitka co se pridaji do panelu modu
                case None:
                    pass
                case _:  # default
                    messagebox.showerror("Error módu",
                                         "Pokus o spuštění módu ("
                                         f"{str(mode)}) se nezdařil.")

        # tlacitko pro mod informaci o abecede
        modes_button_info = tk.Button(self.panel_modes,
                                      text = "Informace o abecedě",
                                      command = lambda: set_active_mode(gv.MODE_ALPHABET_INFORMATION,
                                                                        modes_button_info))
        modes_button_info.pack(side = tk.LEFT,
                               padx = gv.BUTTON_BUFFER,
                               pady = gv.BUTTON_BUFFER)
        
        # debug - test button, need to add more functionality for shannon stuff etc.
        modes_button_second = tk.Button(self.panel_modes,
                                        text = "test button",
                                        command = lambda: set_active_mode(gv.MODE_TESTING,
                                                                          modes_button_second))
        modes_button_second.pack(side = tk.LEFT,
                                 padx = gv.BUTTON_BUFFER,
                                 pady = gv.BUTTON_BUFFER)
        
        # pri prvotni inicializaci aktivuj tlacitko pro info o abecede
        set_active_mode(gv.MODE_ALPHABET_INFORMATION, modes_button_info)


    def on_load_alphabet(self):
        """Funkce provede načtení abecedy ze souboru a kontrolu abecedy.
        
        V případě špatně zadaných znaků v abecedě otevře editační okno."""
        # nacti data abecedy z json souboru
        chars, probs = self.load_alphabet_from_json_file()

        # validace abecedy (pokud nejaka chyba spust editaci abecedy)
        if self.is_alphabet_valid(chars, probs) == False:
            size = max(len(chars), len(probs))
            chars, probs = self.edit_alphabet_window(size,
                                                     chars,
                                                     probs,
                                                     self.root)
            
        # validace po editaci abecedy
        if self.is_alphabet_valid(chars, probs):
            # predej abecedu oknu pro dalsi praci
            self.use_alphabet(chars, probs)
        else:
            messagebox.showwarning("Varování",
                                   "Předaná abeceda není validní.")


    def use_alphabet(self, chars, probs):
        """Funkce nastavi predanou abecedu do hlavniho okna pro dalsi praci.
        
        Po uložení abecedy do okna projde widgety v panelu abecedy a vymaže
        předchoží abecedu pomoci winfo_children() funkce, která vrací
        pouze přímé potomky uložené v panel_alphabet, které smaže,
        pokud nejsou označeny jako permanentní."""
        # ulozeni znaku a pravdepodobnosti do okna
        self.characters_list = chars
        self.probabilities_list = probs

        # zamezeni zvetseni panelu pro abecedu (dulezite) jinak se po pridani
        # labels nize panel rozsiri
        self.panel_alphabet.pack_propagate(False)

        def clear_alphabet_panel():
            """Pomocná funkce vymaze ne-permanentní widgety z panelu abecedy."""
            # vymazani predchozich widgetu mimo funkcnich tlacitek
            for widget in self.panel_alphabet.winfo_children():
                if gv.PERMANENT_TAG_STRING not in widget.bindtags():
                    widget.destroy()
            
            # vycisti i panel modu a grafiku jelikoz soucasna abeceda jiz nebude
            self.clear_panel_modes()
            self.clear_panel_graphics()

        def create_alphabet_widgets():
            """Pomocná funkce do panelu abecedy vytvoří potřebné widgety."""
            # pridani button pro editaci abecedy pod existujici widgety
            def on_button_edit_click(event=None):
                """Pomocná funkce reší event kliknutí na tlačítko pro editaci abecedy."""
                chars, probs = self.edit_alphabet_window(len(self.characters_list),
                                                             self.characters_list,
                                                             self.probabilities_list,
                                                             self.root)
                # validace po editace, pokud je editace platna pouzij novou
                if chars and probs:
                    if self.is_alphabet_valid(chars, probs):
                        self.use_alphabet(chars, probs)
                else:
                    return
                
            button_edit = tk.Button(self.panel_alphabet,
                                    text = "Editace abecedy",
                                    command = on_button_edit_click)
            button_edit.pack(fill = "x")

            # nutno pouzit canvas pro umozneni scrolovani (scrollregion(l,t,r,b))
            canvas = tk.Canvas(self.panel_alphabet,
                               scrollregion=(0, 0, 0,
                                             gv.SCROLLBAR_VERTICAL_LIMIT))
            canvas.pack(side="left", fill="both", expand=False)

            # scrollbar na strane
            scrollbar = tk.Scrollbar(self.panel_alphabet,
                                     orient="vertical",
                                     command=canvas.yview)
            scrollbar.pack(side="right", fill="y")
            canvas.configure(yscrollcommand=scrollbar.set)

            # vytvoreni frame pro zabouzdreni abecedy
            alphabet_frame = tk.Frame(canvas)
            canvas.create_window((0, 0), window = alphabet_frame, anchor="nw")

            # pridani labels pro znaky a pravdepodobnosti abecedy
            for char, prob in zip(self.characters_list, self.probabilities_list):
                char_label = tk.Label(alphabet_frame,
                                      text = f"{char}: {prob: .2f} %")
                char_label.pack(anchor = "w", padx=gv.LABEL_BUFFER_X)

            # posouvani nahoru-dolu koleckem
            def on_mouse_wheel(event):
                """Pomocná funkce řeší event scrollování kolečka myši."""
                canvas.yview_scroll(-int(event.delta / 60), "units")

            # po celem canvasu lze scrollovat
            self.root.bind("<MouseWheel>", on_mouse_wheel)

            # update scrolovane oblasti
            alphabet_frame.update_idletasks()

            # nastaveni oblasti regionu pro scrollovani na updatovanou oblast
            canvas.config(scrollregion = canvas.bbox("all"))
                             
        # vytvoreni udaju pro vybranou abecedu
        clear_alphabet_panel()
        create_alphabet_widgets()
        self.create_modes_buttons()


    # funkce pro overeni predane abecedy, znaky abeedy museji byt kazdy 1 znak
    # pravdepodobnosti museji mit soucet 100 (procent)
    def is_alphabet_valid(self, chars, probs):
        """Funkce ověřuje předanou abecedu.
        
        Počet znaků musí být roven počtu pravděpodobností,
        v seznamu znaků musí být každý znak o délce 1,
        v seznamu probs musí pouze čísla a jejich součet roven 100.0 "
        "(tzn 100.0 %)."""
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
            prob_sum = sum(probs)
            for i, prob in enumerate(probs):
                if prob > 100.0 or prob < 0.0:  # kontrola hodnoty (0.0-100.0)
                    messagebox.showerror("Chyba ve zdrojové abecedě",
                                         f"Pravděpodobnost ({prob}) na pozici"
                                         f" {i + 1} není v rozsahu 0.0-100.0.")
                    return False
            if prob_sum != 100.0:  # kontrola souctu pravdepodobnosti
                messagebox.showerror("Chyba ve zdrojové abecedě",
                                     "Součet pravděpodobností musí být roven"
                                     " 100.0 (tzn. 100 %), tato abeceda má součet "
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
                with open(file_name, "r", encoding = "utf-8") as json_file:
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
            
            # pokud uzivatel nezvoli soubor a napr. zavre okno, vrat se
            if not file_path:
                return
            
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
        
        def update_probability_sum(event=None):
            """Pomocná funkce spočítá aktuální součet pravděpodobností a updatuje label."""
            # pomocne variables
            probability_sum = 0.0
            cols, rows = alphabet_frame.grid_size()

            # vypocet souctu pravdepodobnosti, ignorovat neplatne hodnoty
            for row in range(1, rows-1): # bez posledniho radku
                probability_input = alphabet_frame.grid_slaves(row = row,
                                                               column = prob_input_column)[0]
                probability_value = probability_input.get()
                # pokud je pritomen input proved
                if probability_value.strip():  # ignoruj prazdne stringy
                    #try-except blok pro soucet hodnot
                    try:
                        probability_sum += float(probability_value)
                    except ValueError:
                        # ignoruj jine hodnoty
                        pass
            # update hodnoty v label
            label_prob_sum.config(text=f"Suma: {probability_sum} %")

            # uprav barvu textu pokud hodnota presahuje 100.000
            if probability_sum > 100.000:
                label_prob_sum.config(fg = gv.RED_COLOR)
            elif probability_sum == 100.0:
                label_prob_sum.config(fg = gv.GREEN_COLOR)
            else:
                label_prob_sum.config(fg = gv.BLACK_COLOR)

        # vytvoreni editacniho okna pro zadanou abecedu
        window = tk.Toplevel(parent_window)
        window.transient(parent_window)
        window.grab_set()
        window.title("Editace abecedy")

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

        # vytvoreni input poli pro zadani znaku a jeho pravdepodobnosti
        # pokud byla funkce zavolana s hodnotami v chars a probs zapis je taky
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
            # udalosti ktere spusti update sumy pravdepodobnosti
            probability_input.bind("<FocusIn>", update_probability_sum)
            probability_input.bind("<KeyRelease>", update_probability_sum)
            probability_input.bind("<FocusOut>", update_probability_sum)
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
                # konverze jinych znaku nez cisel (do probs promenne)
                try:
                    probs.append(float(prob_input.get()))
                except ValueError:
                    probs.append(0.0)
                
            # vrat oba listy hodnot
            return chars, probs
        
        def on_save_alphabet(event=None):
            """Pomocná funkce získá zapsané hodnoty a uloží je."""
            # ziskani dat z kolonek znaku a pravdepodobnosti
            chars, probs = get_data()
            self.save_alphabet_to_json(chars, probs)

        def on_use_alphabet(event=None):
            """Pomocná funkce vrací 2 listy ze zadaných hodnot: [chars, probs]."""
            # promenne z venku teto funkce
            nonlocal result_chars_list, result_probs_list
            temp_chars, temp_probs = get_data()

            # pokud je abeceda v poradku uloz do listu mimo tuto funkci
            if (self.is_alphabet_valid(temp_chars, temp_probs)):
                result_chars_list = temp_chars
                result_probs_list = temp_probs
                on_edit_window_close()
            else:
                return
        
        # pridani tlacitek pod zobrazene kolonky a label pravdepodobnosti
        _, num_of_rows = alphabet_frame.grid_size()
        button_save_alphabet = tk.Button(alphabet_frame,
                                         text="Uložit",
                                         command=on_save_alphabet)
        button_save_alphabet.grid(row=num_of_rows,
                                  column=char_input_column,
                                  sticky='e',
                                  pady=gv.LABEL_BUFFER_Y)
        button_use_alphabet = tk.Button(alphabet_frame,
                                        text="Použít abecedu",
                                        command=on_use_alphabet)
        button_use_alphabet.grid(row=num_of_rows,
                                 column=prob_label_column,
                                 pady=gv.LABEL_BUFFER_Y)
        label_prob_sum = tk.Label(alphabet_frame,
                                  text = "Suma: 0.0 %")
        label_prob_sum.grid(row = num_of_rows,
                            column = prob_input_column,
                            pady = gv.LABEL_BUFFER_Y)
        # reseni udalosti pro canvas
        def on_configure(event):
            """Pomocná funkce updatuje velikost okna a vycentruje ho."""
            canvas.configure(scrollregion=canvas.bbox("all"))
            resize_window()  # podle potreby zvetsi cele okno
            #self.center_subwindow(window, parent_window)
        alphabet_frame.bind("<Configure>", on_configure)
        
        # posouvani nahoru-dolu koleckem
        def on_mouse_wheel(event):
            """Pomocná funkce řeší event scrollování kolečka myši."""
            canvas.yview_scroll(-int(event.delta / 60), "units")
        window.bind("<MouseWheel>", on_mouse_wheel)  # kolecko funguje po celem okne

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

        # cinnosti pri zavreni okna
        def on_edit_window_close():
            # unbind eventu kolecka mysi
            window.unbind("<MouseWheel>")
            window.destroy()

        # protokol pri zavreni okna
        window.protocol("WM_DELETE_WINDOW", on_edit_window_close)

        # vycentrovani okna
        self.center_subwindow(window, parent_window)

        # update podokna
        window.update_idletasks()
        update_probability_sum()

        # cekani na zavreni okan (jeho destroy())
        window.wait_window(window)

        return result_chars_list, result_probs_list


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

        input_field.bind_all("<Return>", lambda event: confirm())  
        
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
        
        # otevreni editace abecedy s prazdnou abecedou
        chars = []
        probs = []
        chars, probs = self.edit_alphabet_window(num_of_characters, chars, probs, self.root)

        # kontrola zda seznamy nejsou prazdne
        if chars and probs:
            self.use_alphabet(chars, probs)
        else:
            messagebox.showwarning("Varování",
                                   "Abeceda je prázdná, zkuste abecedu "
                                   "vytvořit a uložit, poté jí načíst.")
       

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
