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
SCROLLBAR_VERTICAL_LIMIT = 5000

# buffer pro labels
LABEL_BUFFER_X = 10
LABEL_BUFFER_Y = 5
LABEL_BUFFER_Y_SMALL = 2

# buffer pro buttons
BUTTON_BUFFER = 5

# barvy
PANEL_MODES_BG = "#9AA2A3"  # gray
PANEL_ALPHABET_BG = "#bbbfbf"  # gray-ish
PANEL_ALPHABET_LABEL_BG = "#888c8c"
PANEL_GRAPHICS_BG = "#D3D3D3"  # lightgray
RED_COLOR = "#FF0000"  # red
BLACK_COLOR = "#000000"  # black
GREEN_COLOR = "#008000"  # green

# stav (active/inactive) tlacitek
ACTIVE_BUTTON_COLOR = "#add8e6"  # lightblue
ACTIVE_BUTTON_RELIEF = "sunken"
INACTIVE_BUTTON_COLOR = "SystemButtonFace"  # neaktivni tlacitko barva
INACTIVE_BUTTON_RELIEF = "raised"

# mody grafickeho panelu (podle stiskleho tlacitka)
MODE_ALPHABET_INFORMATION = "INFO"
MODE_TESTING = "TESTING"


# prace se soubory
JSON_CHARACTERS_NAME = "characters"
JSON_PROBABILITIES_NAME = "probabilities"

# tags pro oznaceni widgetu ktere se nesmi mazat
PERMANENT_TAG_STRING = "permanent"