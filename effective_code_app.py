import tkinter as tk  # pro vykresleni GUI aplikace
from tkinter import filedialog, messagebox, ttk # dialog, message okna a combobox(ttk)
import pandas as pd  # pro pripadne nacitani a zpracovani dat z excel souboru
import math
import heapq  # prace s haldami (implementace Huffmanova kodovani)
import matplotlib.pyplot as pplt  # vytvoreni grafu/diagramu atd..
import networkx as nx  # vytvareni, manipulace grafu a siti (pro binarni stromy)
import gui_variables as gv  # global variables pro GUI
import json  # ulozeni/nacteni abecedy z JSON souboru
from GraphicsView import GraphicsView  # moje trida pro zapouzdreni ruznych zobrazeni dat

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

        # panel pro jednotlive mody zobrazeni (tk.Frame pro pripadne budouci
        # zabaleni dalsich ovladacich prvku nad zobrazene udaje)
        self.panel_graphics = tk.Frame(self.main_frame,
                                        bg=gv.PANEL_GRAPHICS_BG,
                                        borderwidth=gv.PANEL_BORDER_WIDTH,
                                        relief=gv.PANEL_RELIEF_STYLE)
        self.panel_graphics.pack(side=tk.RIGHT,
                                 fill=tk.BOTH,
                                 expand=True)
        # canvas do ktereho se vlozi zabalene informace ktere pujde posouvat po canvasu
        self.graphics_canvas = tk.Canvas(self.panel_graphics,
                                         scrollregion=(0, 0,
                                                       gv.SCROLLBAR_HORIZONTAL_LIMIT,
                                                       gv.SCROLLBAR_VERTICAL_LIMIT))        
        # vytvoreni a nastaveni vertikalnich (v) a horizontalnich (h) scrollbaru
        self.v_scrollbar = tk.Scrollbar(self.panel_graphics,
                                        orient = tk.VERTICAL,
                                        command = self.graphics_canvas.yview)
        self.v_scrollbar.pack(side = tk.RIGHT, fill = tk.Y)
        self.h_scrollbar = tk.Scrollbar(self.panel_graphics,
                                        orient = tk.HORIZONTAL,
                                        command = self.graphics_canvas.xview)
        self.h_scrollbar.pack(side = tk.BOTTOM, fill = tk.X)    
        self.graphics_canvas.pack(side = tk.TOP,
                                  fill = tk.BOTH,
                                  expand = True)
        self.graphics_canvas.bind("<Configure>", self.on_graphics_canvas_configure)

        # zabalene informace pomoci tridy GraphicsView
        self.graphics_view = GraphicsView(self.graphics_canvas)
        self.graphics_canvas.create_window((gv.WINDOW_BUFFER, gv.WINDOW_BUFFER),
                                           window = self.graphics_view,
                                           anchor = "center",
                                           width = gv.SCROLLBAR_HORIZONTAL_LIMIT,
                                           height = gv.SCROLLBAR_VERTICAL_LIMIT)
        #self.graphics_view.bind("<Configure>", self.on_graphics_view_configure)


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

        # inicializace promennych, ktere jsou pouzivany pro vypocty
        self.calc_probabilities_list = []
        self.calc_characters_information_list = []
        self.calc_average_information_amount = 0

        # podle zvolene metody kodovani sem se budou ukladat vypoctene hodnoty
        self.shannon_complete = False
        self.shannon_encoded_chars_list = []
        self.shannon_avg_codeword_length = 0
        self.shannon_code_effectivity = 0.0
        self.shannon_source_entropy = 0.0

        self.huffman_complete = False
        self.huffman_encoded_chars_list = []
        self.huffman_avg_codeword_length = 0
        self.huffman_code_effectivity = 0.0
        self.huffman_source_entropy = 0.0

        # metoda kodovani
        self.encoding_method = None

    # event vyberu metody kodovani uzivatelem
    def on_method_selected(self, event):
        """Funcke řeší event výběru metody z comboboxu."""
        self.encoding_method = event.widget.get()

        # debug
        print(f"vybrana hodnota z comboboxu: {self.encoding_method}\n")

    # event konfigurace canvasu
    def on_graphics_canvas_configure(self, event):
        """Funkce se stará o nastaveni scrollregionu a vycentrovani obsahu."""
        self.graphics_canvas.update_idletasks()
        self.graphics_canvas.configure(scrollregion = self.graphics_canvas.bbox("all"))
        self.graphics_canvas.config(yscrollcommand=self.v_scrollbar.set,
                                    yscrollincrement=1,
                                    xscrollcommand=self.h_scrollbar.set,
                                    xscrollincrement = 1)
        self.v_scrollbar.config(width = gv.SCROLLBAR_WIDTH)
        self.h_scrollbar.config(width = gv.SCROLLBAR_WIDTH)

        # debug pokus o pohyb scrollbaru do jejich stredu
        ratio_x = 0.3
        ratio_y = 0.35
        self.graphics_canvas.yview_moveto(ratio_y)
        self.graphics_canvas.xview_moveto(ratio_x)
        self.graphics_canvas.update_idletasks()
        
        # pokud je neco v graphics_view vycentruj to
        #if self.graphics_view.winfo_children():
        #    self.graphics_view.center_position()
        #else:
        #    return


    # event funkce pri stisknu tlacitka mysi
    def on_mouse_click(self, event):
        """Pomocná funkce řeší event stisku levého tlačítka myši."""
        #print(f"Canvas button press at ({event.x}, {event.y})")  # debug
        #self.graphics_canvas.scan_mark(event.x, event.y)

        self.mouse_click_start_x = event.x
        self.mouse_click_start_y = event.y

    #event funkce pri pohybu mysi
    def on_mouse_movement(self, event):
        """Pomocná funkce řeší event pohybu myši."""
        #print(f"Canvas mouse movement at ({event.x}, {event.y})")  # debug

        #self.graphics_canvas.scan_dragto(event.x, event.y, gain = gv.DRAG_MOVEMENT_SPEED)
        # vypocet mnozstvi o kolik ma byt posunuty graphics_view
        x_amount = event.x - self.mouse_click_start_x
        y_amount = event.y - self.mouse_click_start_y

        self.graphics_canvas.move(tk.ALL, x_amount, y_amount)
        
        # aktualizovat souradnice pro pripadny dalsi event
        self.mouse_click_start_x = event.x
        self.mouse_click_start_y = event.y

    # funkce updatuje vzhled tlacitek podle aktualniho modu
    def update_buttons_style(self, active_button):
        """Funkce updatuje vzhled tlačítek panelu módů podle aktuálního módu."""
        # projdi vsechny buttons v panelu modu
        for button in self.panel_modes.winfo_children():
            # nastav styl pouze widgetum ktere jsou tk.Button
            if isinstance(button, tk.Button):
                # pro aktivni tlacitko se nastavi odlisny vzhled
                if button == active_button:
                    button.configure(bg = gv.ACTIVE_BUTTON_COLOR,  # aktivni button
                                  relief = gv.ACTIVE_BUTTON_RELIEF)
                else:
                    button.configure(bg = gv.INACTIVE_BUTTON_COLOR,  # neaktivni button
                                  relief = gv.INACTIVE_BUTTON_RELIEF)

    # funkce vymaze widgety z panelu modu
    def clear_panel_modes(self):
        """Funkce vymaže obsah panelu módů."""
        for widget in self.panel_modes.winfo_children():
            widget.destroy()

    # funkce vymaze widgety v grafickem panelu a pripravi tak pro nove udaje
    def clear_panel_graphics(self):
        """Funkce vymaže obsah grafického panelu (widgets)."""
        #for widget in self.graphics_canvas.winfo_children():
        #    widget.destroy()
        return  # prozatim nemusi mazat nic

    # Funkce vypise do panel_graphics informace o abecede
    def show_alphabet_info(self):
        """Funkce do grafického panelu vypíše informace o zdrojové abecedě."""
        # nejdrive vycistit panel
        self.clear_panel_graphics()
        # sestaveni stringu pro prvni rade

        self.graphics_view.show_alphabet(self.calc_average_information_amount,
                                         ["Znak", "Pravděpodobnost (P [%])", "Množství informace [bitů]"],
                                         self.characters_list,
                                         self.calc_probabilities_list,
                                         self.calc_characters_information_list)
    # debug test function (to be replaces later)
    def show_test_stuff(self):
        self.clear_panel_graphics()
        self.graphics_view.show_test_info()   
    
    # pomocna funcke resetuje hodnoty pouzivane pri kodovani
    def reset_calc_values_shannon(self):
        """Funkce resetuje proměnné (calc) pouzivane shannonem"""
        self.shannon_encoded_chars_list = []
        self.shannon_avg_codeword_length = 0
        self.shannon_code_effectivity = 0.0
        self.shannon_source_entropy = 0.0

    # kodovani zdrojove abecedy pomoci metody shannon-fanovy
    def encode_alphabet_shannon(self):
        """Funkce použije Shannon-fanovu metodu kódování na zdrojovou abecedu."""

        #print(f"listy serazene:\n{sorted_values_descending}\n")  # debug print
        #print(f"listy serazenych hodnot:\nchars:\n{chars_sorted}\nprobs:\n{probs_sorted}\n")  #debug print

        def shannon_recursive(probs_list, codes, prefix = ""):
            """Očekává serazeny list pravdepodobnosti sestupne."""
            # pokud predany list pravdepodobnosti nema alespon 2 elementy (2 pravdepodobnosti)
            # vrat list kodu obsahujici prazdny string ""

            #debug
            print(f"\tshannon_recursive obdrzel typ>{type(probs_list)}<: {probs_list}\n"
                  f"\tobdrzene kody: {codes}\n")

            if len(probs_list) == 1:
                # debug
                print(f"\t\tlist s delkou jedna, vracim kod >> {prefix}")
                codes.append(prefix)
                return codes

            # rozdel predany list na 2 listy s co nejblizsi sumou pravdepodobnosti
            ones_list, zeros_list = split_list(probs_list)

            #debug
            print(f"ones_list: {ones_list}, higher_list: {zeros_list}\n"
                  f"volam na kazdy rekurzy")

            # ziskani kodu pro oba listy - REKURZE
            codes = shannon_recursive(ones_list, codes, prefix + "1")
            codes = shannon_recursive(zeros_list, codes, prefix + "0")

            # debug
            print(f"Výsledné kódy pro seznam: {probs_list} ->"
                  f"{codes}\n")

            return codes

        # pomocna funkce pro rozdeleni na 2 listy podle sum
        def split_list(probs_list):
            """Pomocná funkce rozdělí předaný list dvojic na 2 mensi listy.

            Očekává serazeny list pravdepodobnosti
            - např. [0.30, 0.25, 0.11, ... ]
            Vrací dva listy pravdepodobnosti s co nejblizsi sumou
            -> ones_list, zeros_list."""

            #debug
            print(f"\tsplitting list: {probs_list}...")

            ones_list = []
            zeros_list = []

            # pokud predany list neni prazdny proved vypocty
            if probs_list:
                # pokud jsou v listu pouze 2 elementy, rozdel na 2 listy s 1 elementem
                if len(probs_list) == 2:
                    print(f"\t\tdelka probs_list je rovna 2 rozdeluji na 2 listy:\n"
                          f"\t\tones_list: [{probs_list[0]}], zeros_list: [{probs_list[1]}]\n")
                    return [probs_list[0]], [probs_list[1]]

                # pokud je delsi pokracuj vypocty
                else: 
                    # index prvku ktery je poslednim prvkem horniho listu
                    split_index = 0
                    # polovina souctu pravdepodobnosti
                    # - limit pro sumu ones_list
                    limit_sum = sum(probs_list) / 2

                    # debug
                    print(f"\t\tlimit_sum = {limit_sum}")

                    # prubezna suma
                    cumulative_sum = 0.0

                    # smycka postupne scita pravdepodobnosti a hleda kde rozdelit list
                    for index, prob in enumerate(probs_list):
                        # ukonci loop pokud by suma prekrocila limit
                        cumulative_sum += prob
                        # pokud dosavadni suma presahla limit zde se list rozdeli
                        if cumulative_sum > limit_sum:
                            # debug
                            print(f"\t\toveruji ktera suma je lepsi: (cumul - limit) < (limit - previous_cumul):\n"
                                  f"\t\t({cumulative_sum:.3f} - {limit_sum:.3f}) < ({limit_sum:.3f} - {(cumulative_sum - prob):.3f})\n"
                                  f"\t\t{(cumulative_sum - limit_sum)} < {(limit_sum - (cumulative_sum - prob))} = {(cumulative_sum - limit_sum) < (limit_sum - (cumulative_sum - prob))}\n")
                            # pokud by dalsi index mel mensi rozdil sum pouzij ho taky
                            if (cumulative_sum - limit_sum) < (limit_sum - (cumulative_sum - prob)):
                                index += 1
                            split_index = index
                            break
                        
            #debug
            print(f"\t\tnalezen index: {split_index}")

            # nalezen index rozdeleni, vloz hodnoty do 2 mensich listu
            ones_list = probs_list[:split_index]  # do indexu
            zeros_list = probs_list[split_index:]  # od index

            print(f"\t\tlisty: {ones_list} and {zeros_list}")

            # vrat 2 listy (pokud predany argument byl prazdny vrati se
            # 2 prazdne listy pri overeni na zacatku funkce, ale usetri se vypocty
            return ones_list, zeros_list

        # debug
        print(f"spusteno kodovani podle shannona..\n")



        # overeni ze byla vybrana metoda kodovani
        if self.encoding_method == None:
            return False
        
        # overeni ze jsou pritomny jiz vypocitane potrebne hodnoty
        if not self.calc_probabilities_list:
            return False

        # reset hodnot
        self.shannon_complete = False
        self.reset_calc_values_shannon()

        #do teto promenne se ulozi list hodnot (kodu)
        codes_list = []

        # algoritmus
        # list dvojic [char, prob] - napr [['a', 0.2], ['b', 0.23],...]
        # pro budouci namapovani kodovych slov do puvodniho poradi
        paired_values = list(zip(self.characters_list, self.calc_probabilities_list))
        sorted_values_descending = sorted(paired_values,
                                          key = lambda x: x[1],  # podle 2. prvku (prob)
                                          reverse = True)  # descending order
        
        # vytazeni listu pravdepodobnosti pro shannon_recursive funkci
        # v serazenem (sestupne) listu
        probs_list = [pair[1] for pair in sorted_values_descending]

        # debug
        print(f"zistane probs ze serazeneho listu dvojic: {probs_list}\n")

        # vygenerovani kodovych slov
        codes_list = shannon_recursive(probs_list, codes_list)

        # namapovani kodovych slov ve spravnem poradi do promenne tridy
        for i, orig_char in enumerate(self.characters_list):
            # najdi na kterem indexu je v serazenem listu dvojic [char,prob]
            # znak z originalne ulozeneho listu znaku kodove kabecedy
            # nalezeny index bude zaroven index odpovidajiciho kodoveho slova
            # z listu codes_list
            code_word_index = [item[0] for item in sorted_values_descending].index(orig_char)

            # uloz kodove slovo
            self.shannon_encoded_chars_list.append(codes_list[code_word_index])
        
        # debug
        #print(f"shannonuv algoritmus hotovo...\nnalezene kodove slova pro znaky:\n")
        #for (char, _), code in zip(sorted_values_descending, codes_list):
        #    print(f"({char}, {code})\n")

        # debug
        print(f"kodove slova ulozene v tomto poradi:\n")
        for char, code_word in zip(self.characters_list, self.shannon_encoded_chars_list):
            print(f"char: {char} || code: {code_word}")

        # dopocitani ostatnich udaju vygenerovaneho kodu
        # vypocet prumerne delky kodoveho slova

        self.shannon_avg_codeword_length = 0  # TODO
        
        # vypocet efektivity kodu
        self.shannon_code_effectivity = 0.0  # TODO

        # vypocet entropie zdroje
        self.shannon_source_entropy = 0.0  # TODO

        # hotovo oznac shannon metodu za vypocitanou
        self.shannon_complete = True
        

    def encode_alphabed_huffman(self):
        print("spusteno kodovani podle huffmana..\n")
        pass

    def show_encoded_data(self):
        # TODO
        pass

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
        # event kliknuti na button ktery pokud je vybrana metoda kodovani provede encode
        def on_encode_button_click():
            """Funkce řeší event kliknutí na tlačítko použití zvolené metody kódování."""
            # zvolena metoda kodovani
            method = self.encoding_method

            # debug
            print(f"vybrana metoda {method} pro kodovani..")

            #pro kazdou metodu zavolej odpovidajici funkci kodovani
            if (method == gv.COMBOBOX_METHOD_SHANNON):
                # vybran shannon, zkontroluj jestli neexistuji predchozi vysledky
                if self.shannon_complete:
                    # shannon jiz byl proveden, nepocitej znovu
                    # debug print
                    print(f"\tjiz existuje vypocteny vysledek pro shannona\n")
                else:
                    self.encode_alphabet_shannon()
            elif (method == gv.COMBOBOX_METHOD_HUFFMAN):
                # opet kontrola existujicich vysledku
                if self.huffman_complete:
                    #debug print
                    print(f"\tjiz existuje vypocteny vysledek pro huffmana\n")
                else:
                    self.encode_alphabed_huffman()
            else:
                #debug print
                print("Nebyla vybrana zadna metoda kodovani vracim se z funkce.")
                return
            #debug
            print(f"zakodovani metodou {method} probehlo ted by se mel zobrazit vysledek.\n")

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
        
        # combobox pro vyber metody kodovani
        self.encoding_method = None  # reset vybrane metody
        modes_combobox_encoding_method_selection = ttk.Combobox(
            self.panel_modes,
            values = [gv.COMBOBOX_METHOD_HUFFMAN,
                      gv.COMBOBOX_METHOD_SHANNON]
        )
        modes_combobox_encoding_method_selection.pack(side = tk.LEFT,
                                                      padx = gv.BUTTON_BUFFER,
                                                      pady = gv.BUTTON_BUFFER)
        modes_combobox_encoding_method_selection.set(gv.COMBOBOX_PROMPT)
        modes_combobox_encoding_method_selection.bind("<<ComboboxSelected>>",
                                                      self.on_method_selected)
        
        modes_button_use_method = tk.Button(self.panel_modes,
                                            text = "Použít kódování",
                                            command = on_encode_button_click)
        modes_button_use_method.pack(side = tk.LEFT,
                                     padx = gv.BUTTON_BUFFER,
                                     pady = gv.BUTTON_BUFFER)
        
        #debug
        print(f"combobox obnovet, aktualni hodnota v nej: {self.encoding_method}.\n")

        
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

        # nastaveni calc_ promennych podle pouzite abecedy pro dalsi vypocty
        # prevod pravdepodobnosti do desetinneho zapisu procent (zaokrouhleno na 3 desetinna mista)
        self.calc_probabilities_list = [prob / 100.0
                                         for prob in probs]


        # debug
        #print(f"\toriginal chars: {chars}\n"
        #      f"\toriginal probs: {probs}\n"
        #      f"\tcalc_probs: {self.calc_probabilities_list}\n")
        
        # vypocet mnozstvi informace kterou nese kazdy znak (shannonova formule)
        self.calc_characters_information_list = [
            round(-math.log2(prob),
                  gv.NUM_OF_DECIMAL_PLACES)
                  for prob in self.calc_probabilities_list
        ]
        # vypocet prumerne informacni hodnoty jednoho znaku
        self.calc_average_information_amount = 0.0
        for prob, information_value in zip(self.calc_probabilities_list,
                                           self.calc_characters_information_list):
            self.calc_average_information_amount += prob * information_value        
        round(self.calc_average_information_amount, gv.NUM_OF_DECIMAL_PLACES)
        # debug
        #print("calc_ promenne:\n"
        #      f"calc_probabilities_list: {self.calc_probabilities_list}\n"
        #      f"calc_characters_information_list: {self.calc_characters_information_list}\n"
        #      f"calc_average_information_amount: {self.calc_average_information_amount}\n")
        
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
                             
        # vymazani predchozich udaju k abecede
        clear_alphabet_panel()

        # vytvoreni udaju pro vybranou (novou) abecedu
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
            prob_sum = round(sum(probs), gv.NUM_OF_DECIMAL_PLACES)
            for i, prob in enumerate(probs):
                if prob > 100.0 or prob < 0.0:  # kontrola hodnoty (0.0-100.0)
                    messagebox.showerror("Chyba ve zdrojové abecedě",
                                         f"Pravděpodobnost ({prob}) na pozici"
                                         f" {i + 1} není v rozsahu 0.0-100.0.")
                    return False
            if prob_sum != 100.0:  # kontrola souctu pravdepodobnosti
                messagebox.showerror("Chyba ve zdrojové abecedě",
                                     "Součet pravděpodobností musí být (po "
                                     "zaokrouhlení na 5 desetinných míst) roven"
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

            # pokus o zamezeni moznym chybam vzniklych pravdepodobne pri
            # prevozu z binarni soustavy pri souctech
            probability_sum = round(probability_sum, gv.NUM_OF_DECIMAL_PLACES)

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
