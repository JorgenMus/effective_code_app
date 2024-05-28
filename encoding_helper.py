import math
import tkinter as tk
import gui_variables as gv

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
        self.encoding_window = None
        self.special_keys = [
            'Up', 'Down', 'Left', 'Right', 'End', 'Home', 'BackSpace'
        ]

    def show_encoding_window(self):
        """Funkce zobrazí uživateli okno umožnující zabezpečit kód.
        
        Uživatel má možnost psát do UI_txtbox pole, každý jeho input je 
        ověřen zda se jedná o znak z předané abecedy znaků."""
        self.window_encoder = tk.Toplevel()
        self.window_encoder.title("Zabezpečení sudou paritou")

        # label oznacujici input text box
        self.input_label = tk.Label(self.window_encoder, text="Zadejte zprávu")
        self.input_label.pack()

        # text box pro psani zpravy uzivatelem
        self.UI_txtbox = tk.Text(self.window_encoder,
                            height=5,
                            width=40)
        self.UI_txtbox.pack()
        self.UI_txtbox.bind("<KeyRelease>", self.check_input)

        # label abecedy znaku
        txt_alphabet = ""
        for char, code_word in zip(self.chars, self.code_words):
            txt_alphabet += f"{char} = {code_word}, "
        self.alphabet_label = tk.Label(self.window_encoder,
                                  text = txt_alphabet)
        self.alphabet_label.pack()

        # tlacitko pro zabezpeceni (spousti event handler)
        self.encode_button = tk.Button(self.window_encoder,
                                       text = "Zabezpečit",
                                       command = self.on_encode_button_click)
        self.encode_button.pack()

        # Create output labels
        self.code_output = tk.Label(self.window_encoder,
                                     text="kód zabezpečený sudou paritou:")
        self.code_output.pack()




    # event handler overi zda zadany znak je povoleny
    def check_input(self, event):
        """Pokud předany znak není v listu znaků abecedy smaže ho.
        
        lze obejit rychlim cvakanim na klavesnicik, bude vyreseno dalsi metodou."""
        pressed_char = event.keysym

        # ignoruj znaky jako sipky, home, end, mezernik (pokud je v abecede)
        if pressed_char == 'space' and ' ' in self.chars:
            return
        
        if pressed_char in self.special_keys:
            return  # ignoruj

        # debug print
        print(f"porovnavam znak: >>{pressed_char}<<")
        # pokud je soucasny znak "tisknutelny" a neni povoleny smaz ho
        if pressed_char.isprintable() and pressed_char not in self.chars:
            #debug print
            print("\tmazu znak..")
            # Získání pozice kurzoru
            cursor_position = self.UI_txtbox.index(tk.INSERT)

            # pokud neni kurzor na zacatku posuneme ho o 1 zpet
            if cursor_position != "0.0":
                prev_char_pos = self.UI_txtbox.index(tk.INSERT + "-1c")
                self.UI_txtbox.delete(prev_char_pos)
            else:
                # Kurzor je na začátku, takže smažeme první znak
                self.UI_txtbox.delete("0")

    # event handler pro tlacitko
    def on_encode_button_click(self):
        """Funkce řeší event kdy uživatel klikne na tlačítko zabezpečit."""
        # debug
        print("nyni se udela kodovani se zabezpecenim a zobrazi..")
        
        
        # ziskani textu co zadal uzivatel 
        text = self.UI_txtbox.get("1.0", tk.END)
        
        # list comprehension k ziskani stringu pouze s povolenymi znaky
        text_formated = "".join([char for char in text if char in self.chars])

        print(f"naformatovany string: >>{text_formated}<<")

        
        ## METHOD 1
        #### debug
        ###print("ziskany string textu pred jakymkoliv formatovanim..."
        ###      f">{text}<")
###
        #### pokud neni mezera jednim ze znaku abecedy odmaz mezery
        ###if " " not in self.chars:
        ###    text.replace(" ", "")
        ###
        #### odstraneni new-line znaku
        ###text.replace('\r', '')
        ###text.replace('\n', '')
        ###
        #### debug
        ###print("ziskany string textu po odstraneni mezer:"
        ###      f">{text}<")
        ###
        ###text.format()
        #### naformatovani do jednoho stringu
        ###text_formatted = "".join(text)
###
        #### debug
        ###print(f"preformatovany text (spojeni):>{text_formatted}<")
###
        ###for char in text_formatted:
        ###    print(f"znak >{char}<")




    