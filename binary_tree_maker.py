"""Tento soubor slouží jako wrapper pro třídu BinaryTreeMaker.

Třída umí vytvořit binární strom s využitím knihovny networkx
a následně z něj vytvoří obrázek použitelný v tkinter aplikace
(.png obrázek)."""
import os
import networkx as nx
import matplotlib.pyplot as pplt
from PIL import Image, ImageTk
from networkx.drawing.nx_agraph import graphviz_layout

class BinaryTreeMaker:
    """Třída umí vytvořit graf binárního stromu a udělat z něj obrázek.
    
    funkcí create_binary_tree se vytvoří pomocí networkx graf binárního stromu
    a funkcí draw_binary_tree se vytvoří a vrátí .png obrázek."""
    # pocitadlo vytvorenych grafu
    graph_counter = 0

    def __init__(self):
        self.generated_tree = None
        self.images = {}
        

    
    # generovani stromu pomoci knihovny graphviz
    def create_binary_tree_graphviz(self, code_words, characters, graph_name):
        tree = nx.DiGraph()
        tree.add_node('root')  # kořenový uzel

        for code, char in zip(code_words, characters):
            current_node = 'root'
            for bit in code:
                next_node = f'{current_node}_{bit}'
                if not tree.has_node(next_node):
                    tree.add_node(next_node)
                tree.add_edge(current_node, next_node, label=bit)
                current_node = next_node
            tree.nodes[current_node]['label'] = char

        self.generated_tree = tree

    # funkce vytvoreni obrazku ze stromu (varianta graphviz)
    def create_image_graphviz(self, file_name, size = (400, 400)):
        # Vykreslení grafu s Graphviz uspořádáním
        pos = graphviz_layout(self.generated_tree, prog='dot')
        labels = nx.get_node_attributes(self.generated_tree, 'label')
        edge_labels = nx.get_edge_attributes(self.generated_tree, 'label')

        pplt.figure(figsize=(10, 8))
        nx.draw(self.generated_tree, pos, with_labels=True, labels=labels, node_size=500, node_color="lightblue", font_size=12, font_weight="bold")
        nx.draw_networkx_edge_labels(self.generated_tree, pos, edge_labels=edge_labels)
        
        pplt.savefig(file_name, bbox_inches="tight")
        pplt.close()

        return os.path.exists(file_name)
    
    # generovani stromu pomoci knihovny networkx
    # zatim nefunkcni
    def create_binary_tree(self, code_words, characters, graph_name):
        tree = nx.DiGraph()
        tree.add_node('root')  # korenovy uzel

        for code, char in zip(code_words, characters):
            current_node = 'root'
            for bit in code:
                next_node = f'{current_node}_{bit}'
                if not tree.has_node(next_node):
                    tree.add_node(next_node)
                tree.add_edge(current_node, next_node, label=bit)
                current_node = next_node
            tree.nodes[current_node]['label'] = char

        self.generated_tree = tree

        # vytvoreni prazdneho grafu

        #tree = nx.Graph(name = graph_name)
#
        ## pridani uzlu
        #tree.add_node(1)
        #tree.add_node(2)
        #tree.add_node(3)
        #tree.add_node(4)
#
        ## pridani hran
        #tree.add_edge(1, 2)
        #tree.add_edge(1, 3)
        #tree.add_edge(2, 4)

        self.generated_tree = tree

    # funkce vytvoreni obrazku ze stromu (varianta networkx)
    def create_image(self, file_name, size=(400, 400)):
        # Vytvoření prázdného obrázku
        #image = Image.new("RGB", size, color="white")
#
        ## Uložení pozic uzlů
        #pos = nx.spring_layout(G)
#
        ## Vykreslení uzlů a hran
        #nx.draw(G, pos, with_labels=True,
        #        arrows=True, node_size=3000,
        #        font_size=10, node_color='lightblue',
        #        ax=None)
#
        ## Převod obrázku do formátu pro Tkinter
        #image_tk = ImageTk.PhotoImage(image)
#
        #return image_tk

        # vykresleni grafu
        position = nx.spring_layout(self.generated_tree)
        nx.draw(self.generated_tree, position,
                with_labels = True,
                node_size = 500,
                node_color = "red",
                font_size = 12,
                font_weight = "bold")
        
        pplt.savefig(file_name, bbox_inches = "tight")
        pplt.close()

        return os.path.exists(file_name)

    # funkce pro predane kodove slova a znaky (pripadny nazev grafu)
    # vygeneruje a vrati obrazek
    def get_tree_image(self, code_words, characters, graph_name, size = (400, 400)):
        # overeni zda jiz takovy graph byl vygenerovan
        if graph_name in self.images:
            # debug print
            print(f"\tnalezen graph se jmenem '{graph_name}' vracim ho z MAKERU.")
            return self.images.get(graph_name)
        # graph dosud nebyl vygenerovan pokracuj
        else:
            #debug print
            print(f"\tgraph se jmenem '{graph_name}' neni v dict images, vytvarim...")
            
            # pokud nebyl pridan graph_name vygeneruj
            if graph_name == None:
                graph_name = f"graf_" + str(self.graph_counter)

            # debug print
            print(f"\tnove jmeno grafu: '{graph_name}'")
            # vytvoreni a ulozeni stromu pro graph
            
            
            # debug semestralni priklad
            graph_name = "Semestralni_priklad"
            self.create_binary_tree_graphviz(["111", "101", "001", "0001", "0000", "100", "0100", "011", "0101", "110"],
                                             ["a", "e", "i", "o", "u", "t", "r", "s", "n", "p"],
                                             graph_name)
            #self.create_binary_tree(code_words, characters, graph_name) # TODO vratit zpet po debugu
            
            # pouziti stromu pro vytvoreni a ulozeni obrazku
            file_name = graph_name + ".png"
            #if self.create_image(file_name, size):  # networkx varianta
            if self.create_image_graphviz(file_name, size):
                # pokud se obrazek dobre vytvoril a ulozil nacti jej do tree makeru
                image = Image.open(file_name)
                self.images[graph_name] = ImageTk.PhotoImage(image)

                # zvyseni pocitadla grafu
                self.graph_counter += 1

                return self.images[graph_name]
            else:
                # nepovedlo se vytvorit ze stromu obrazek grafu
                print(f"Nepodarilo se vytvorit graf s nazvem {graph_name}.\n")
        return None
