import math
import tkinter as tk
from tkinter import scrolledtext
import gui_variables as gv
#import unicodedata  # normalizace znaku unicode pro mapovani kodovych slov

# tato trida (uzel) ukazuje na 2 potomky (pouziti v huffman kodovani)
# zna orig znak abecedy soucet jejich pravdepodobnosti
class Node:
    """Malá třída využito při konstrukci stromů u Huffmanova kódování."""
    def __init__(self, orig_char_index=None, prob=None):
        self.orig_char_index = orig_char_index
        self.prob = prob
        self.left = None
        self.right = None

# vypocet prumerne delky kodoveho slova
def get_average_word_length(chars_list, probs_list):
    """Funkce vrací průměrnou délku kódového slova v bitech."""
    average_length = 0
    for code_word, prob in zip(chars_list, probs_list):
        average_length += len(code_word) * prob
    return average_length

# vypocet entropie zdroje
def get_source_entropy(probs_list):
    """Funkce vrací entropii zdroje."""
    source_entropy = 0
    for prob in probs_list:
        source_entropy -= prob * math.log2(prob)  # zaporna suma
    
    return source_entropy

def get_code_effectivity(entropy, avg_length):
    """Funkce vrací efektivitu kódu (v procentech)."""
    return ((entropy / avg_length) * 100.0)

class EvenParityEncoder:
    def __init__(self, chars, code_words):
        self.chars = chars
        self.code_words = code_words
        self.code_dict = dict(zip(chars, code_words))  # pro encode_string
        self.encoding_window = None
        self.special_keys = [
            'Up', 'Down', 'Left', 'Right',
            'End', 'Home', 'BackSpace'
        ]

    def show_encoding_window(self):
        """Funkce zobrazí uživateli okno umožnující zabezpečit kód.
        
        Uživatel má možnost psát do UI_txtbox pole, každý jeho input je 
        ověřen zda se jedná o znak z předané abecedy znaků."""
        self.window_encoder = tk.Toplevel()
        self.window_encoder.title("Zabezpečení sudou paritou")
        self.window_encoder.geometry()

        #### label oznacujici input text box
        self.input_label = tk.Label(self.window_encoder,
                                    text="Zadejte zprávu")
        self.input_label.pack()

        # text box pro psani zpravy uzivatelem
        self.UI_txtbox = scrolledtext.ScrolledText(self.window_encoder,
                                                    wrap = "word")
        self.UI_txtbox.pack()
        self.UI_txtbox.bind("<KeyRelease>", self.check_input)

        # label abecedy znaku
        txt_alphabet = ""
        for char, code_word in zip(self.chars, self.code_words):
            txt_alphabet += f"{char} = {code_word}, "
        self.alphabet_label = tk.Label(self.window_encoder,
                                       wraplength = gv.LABEL_WRAP_LENGTH,
                                       text = txt_alphabet)
        self.alphabet_label.pack()

        # tlacitko pro zabezpeceni (spousti event handler)
        self.encode_button = tk.Button(self.window_encoder,
                                       text = "Zabezpečit",
                                       command = self.on_encode_button_click)
        self.encode_button.pack()

        # output label
        self.code_output_label = tk.Label(self.window_encoder,
                                          text="kód zabezpečený sudou paritou:")
        self.code_output_label.pack()

        # pole pro zobrazeni vysledku zabezpeceni sudou paritou
        self.code_output_field = scrolledtext.ScrolledText(self.window_encoder,
                                                           wrap = "word")
        self.code_output_field.pack()

    # event handler overi zda zadany znak je povoleny
    def check_input(self, event):
        """Pokud předany znak není v listu znaků abecedy smaže ho.
        
        lze obejit rychlim cvakanim na klavesnice, bude vyreseno dalsi metodou."""

        # varianta 2
        pressed_char = event.char

        # overeni zda je znak alfanumericky nebo mezera
        if pressed_char.isalnum() or pressed_char == ' ':
            # pokud ano over ze je v abecede
            if pressed_char in self.chars:
                return  # povol jeho zapsani
            # pokud neni v abecede tak ho smaz
            else:
                # posun kurzor
                cursor_position = self.UI_txtbox.index(tk.INSERT)

                # pokud pozice neni uplni zacatek posun o jeden doleva
                if cursor_position != "1.0":
                    previous_char_position = self.UI_txtbox.index(tk.INSERT + "-1c")
                    # a smaz tuto pozici
                    self.UI_txtbox.delete(previous_char_position)
                else:
                    # pokud byl kurzor na zacatku textu smaz tento znak
                    self.UI_txtbox.delete("1.0")
        # jnak ignoruj znak
        else:
            return

    # event handler pro tlacitko
    def on_encode_button_click(self):
        """Funkce řeší event kdy uživatel klikne na tlačítko zabezpečit."""
        # debug
        #print("nyni se udela kodovani se zabezpecenim a zobrazi..")
        
        
        # ziskani textu co zadal uzivatel 
        text = self.UI_txtbox.get("1.0", tk.END)
        
        # list comprehension k ziskani stringu pouze s povolenymi znaky
        text_formated = "".join([char for char in text if char in self.chars])

        # pripadny update textu co zadal uzivatel do povolenych znaku
        if text_formated != text:
            # aktualizace textu do policka pro user input
            self.UI_txtbox.delete("1.0", tk.END)
            self.UI_txtbox.insert("1.0", text_formated)


        print(f"naformatovany string: >>{text_formated}<<")

        # vytvoreni noveho stringu mapovanim znaku na kodove slova
        encoded_string = self.encode_string(text_formated)

        print(f"zakodovane slovo: {encoded_string}")

        even_parity_string = self.use_even_parity(encoded_string)

        print(f"po zabezpeceni sudou paritou string je {even_parity_string}")

        self.code_output_field.delete("1.0", tk.END)
        self.code_output_field.insert("1.0", even_parity_string)

    # helper function pro kazdy predany znak pouzije odpovidajici kodove slovo
    def encode_string(self, string):
        """Pomocná funkce namapuje stringy kódových slov na předané znaky."""
        # promenna pro pridavani kodovych slov
        encoded_string = ""

        # pro kazdy znak najdi odpovidajici kodove slovo a pripoj
        for char in string:
            # najdi pripis odpovidajici kodove slovo
            encoded_string += self.code_dict[char]
        
        return encoded_string

    # zabezpeceni sudou paritou
    def use_even_parity(self, encoded_string):
        """Funkce pro předaný string provede zabezpečení sudé parity.
        
        Očekává že dostala již string '0' a '1'.
        vrací opět string s '0' nebo '1' na konci podle výsledku zabezpečení."""
        # spocitej pocet jednicek
        count_ones = 0
        for char in encoded_string:
            if char == '1':
                count_ones += 1
        
        #debug
        #print(f"pocet jednicek je {count_ones}")

        # pokud je '1' sudy pocet pridej znak '0'
        if count_ones % 2 == 0:
            encoded_string += '0'
        # pokud je '1' lichy pocet pridej znak '1'
        else:
            encoded_string += '1'
        
        return encoded_string


