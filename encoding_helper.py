import math

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


    