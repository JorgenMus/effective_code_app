"""Tento soubor je určen pro vytvoření obrázků matematických vzorců.

Pro svou činnost používá matplotlib a PIL (Image, ImageTk)."""
import matplotlib.pyplot as pplt
import gui_variables as gv
from PIL import Image, ImageTk
import os  # kontrola vytvoreni souboru s obrazkem

class EquationsManager:
    """Třída inicializuje dictionary používaných vzorcu a vytvoří pro ně images.
    
    create_image() vytvoří pomocí pyplot obrázek jako .png pro
    předaný vzorec.
    load_images() postupně vytvoří všechny obrázky pomoci create_image
    a uloží si na ně referenci do images dictionary.
    get_image() vrací obrázek použitelný v tk.Label."""
    def __init__(self, font_size=20):
        """Inicializace dictionary equations a images."""
        self.equations_dict = {
            gv.EQ_NAME_AVG_INFO_VALUE : r"I = \sum_{i=1}^{n} P_i \cdot \log_b \left( \frac{1}{P_i} \right)",
            gv.EQ_NAME_AVG_CODEWORD_LEN : r"\overline{d} = \sum_{i=1}^n d_i \cdot p_i",
            gv.EQ_NAME_SOURCE_ENTROPY : r"H(X) = -\sum_{i=1}^n P(x_i) \log_b P(x_i)",
            gv.EQ_NAME_CODE_EFFECTIVITY : r"\eta = \frac{H(X)}{\overline{d}}",
            gv.EQ_NAME_KRAFT_MCMILLAN_INEQUALITY : r"\sum_{i=1}^n b^{-l_i} \leq 1"
        }

        self.images = {}
        self.font_size = font_size

    # funkce vraci dict rovnic pro mozny zapis do csv souboru
    def get_equations(self):
        """Pomocná funkce vrátí svůj nadefinovaný seznam rovnic.
        
        Rovnice jsou formátované LaTeX stringy."""
        return self.equations_dict
    
    # vytvoreni obrazku pro vzorec
    def create_image(self, equation, file_name):
        """Vytvoření obrázku pro předanou rovnici do předaného souboru."""
        # figure a axes pyplotu
        fig, ax = pplt.subplots()
        
        # nastaveni vzorce (0.5, 0.5) - stred podgrafu, $...$ LaTeX format
        ax.text(0.5, 0.5,
                f"${equation}$",
                fontsize = self.font_size,
                ha = "center")  # ha - horizontal alignment
        
        # vypnuti zobrazeni os X a Y a uprava velikosti (co nejtesnejsi k vzorci)
        ax.axis("off") 
        ax.figure.set_size_inches(0, 0)

        # ulozeni vzorce do obrazku (tesny ramecek kolem obsahu)
        pplt.savefig(file_name,
                     bbox_inches = "tight")
        pplt.close(fig)
        return os.path.exists(file_name)

    # nacteni vsech znamych vzorcu
    def load_images(self):
        """Funkce postupně volá create_image a načte všechny obrázky."""
        # vytazeni jmena a vzorce z dictionary
        for name, equation in self.equations_dict.items():
            # nazev souboru podle jmena vzorce
            file_name = f"{name}.png"

            # pokus se vytvorit soubory
            if self.create_image(equation, file_name):
                image = Image.open(file_name)
                self.images[name] = ImageTk.PhotoImage(image)
            else:
                # debug print
                print(f"Nepodarilo se vytvorit vzorec: {name}, {equation}.")

    # funkce vraci image pokud je takovy nazev ve slovnimu obrazku, jinak None
    def get_image(self, equation_name):
        """Funkce vraci image ktery je pouzitelny pro tk.Label.
        
        Pokud predane equation_name neni ve slovniku vraci se None."""
        if equation_name in self.images:
            return self.images.get(equation_name)
        else:
            return None