"""Tento soubor obsahuje konstanty a nastaveni pouzite pro GUI aplikace."""


# rozmery panelu
PANEL_MODES_HEIGHT = 35
PANEL_ALPHABET_WIDTH = 200
PANEL_BORDER_WIDTH = 2
PANEL_RELIEF_STYLE = "groove"

# rozmery okna
WINDOW_MIN_WIDTH = 800
WINDOW_MIN_HEIGHT = 600
WINDOW_BUFFER = 20

# scrollbar
SCROLLBAR_VERTICAL_LIMIT = 3000
SCROLLBAR_HORIZONTAL_LIMIT = 5000
SCROLLBAR_WIDTH = 25

# buffer pro labels
LABEL_BUFFER_X = 10
LABEL_BUFFER_Y = 5
LABEL_BUFFER_Y_SMALL = 2
LABEL_BORDER_WIDTH = 1

# buffer pro buttons
BUTTON_BUFFER = 5

# grid nastaveni
GRID_HIGHLIGHT_THICKNESS = 5
GRID_BUFFER = 10

# barvy
PANEL_MODES_BG = "#9AA2A3"  # gray
PANEL_ALPHABET_BG = "#bbbfbf"  # gray-ish
PANEL_ALPHABET_LABEL_BG = "#888c8c"
PANEL_GRAPHICS_BG = "#D3D3D3"  # lightgray
RED_COLOR = "#FF0000"  # red
BLACK_COLOR = "#000000"  # black
GREEN_COLOR = "#008000"  # green
GRAY_COLOR = "#808080"  # gray

# stav (active/inactive) tlacitek
ACTIVE_BUTTON_COLOR = "#add8e6"  # lightblue
ACTIVE_BUTTON_RELIEF = "sunken"
INACTIVE_BUTTON_COLOR = "SystemButtonFace"  # neaktivni tlacitko barva
INACTIVE_BUTTON_RELIEF = "raised"

# mody grafickeho panelu (podle stiskleho tlacitka)
MODE_ALPHABET_INFORMATION = "INFO"
MODE_ALPHABET_GRAPH = "GRAPH"
MODE_TESTING = "TESTING"
MODE_USE_ENCODING_METHOD = "ENCODE"


DRAG_MOVEMENT_SPEED = 1  # rychlost posouvani pro graficky panel

# hodnoty pro matematicke operace
NUM_OF_DECIMAL_PLACES = 5

# prace se soubory
JSON_CHARACTERS_NAME = "characters"
JSON_PROBABILITIES_NAME = "probabilities"

# tags pro oznaceni widgetu ktere se nesmi mazat
PERMANENT_TAG_STRING = "permanent"

# snad univerzalni font pro text
FONT_UNIVERSAL = "Arial"
FONT_SIZE = 14
FONT_EQUATIONS = 20

# udaje pro grafy (binarni stromy)
GRAPH_WIDTH = 800
GRAPH_HEIGHT = 600
GR_MINW = 400
GR_DPI = 100
GR_FONT_SIZE = 16

# udaje pro enkoder
ENCODER_WIDTH = 400


# hodnoty pro combobox selekci metod
COMBOBOX_METHOD_SHANNON = "Shannon-Fanova"
COMBOBOX_METHOD_HUFFMAN = "Huffmanova"
COMBOBOX_PROMPT = "Vybrat metodu kódování"

# text tlacitka pro enkoder
ENCODER_PROMPT_USE_METHOD = "Zakódovat"
ENCODER_PROMPT_ENCODE_EVEN_PARITY = "Spustit enkodér\n(zabezpečení sudou paritou)"

# nazvy vzorcu pro vypocty
EQ_NAME_AVG_INFO_VALUE = "AVG_INFORMATION_VALUE"
EQ_NAME_AVG_CODEWORD_LEN = "AVG_CODEWORD_LENGTH"
EQ_NAME_SOURCE_ENTROPY = "SOURCE_ENTROPY"
EQ_NAME_CODE_EFFECTIVITY = "CODE_EFFECTIVITY"
EQ_NAME_KRAFT_MCMILLAN_INEQUALITY = "KRAFT_MCMILLAN_INEQUALITY"