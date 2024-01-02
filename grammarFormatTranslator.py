import xml.etree.ElementTree as ET
from xml.dom import minidom
import re

# Con este script se traducen a los distintos formatos
# Cuando se escribe a jflap se guarda en un archivo jff para importar en jflap
# El resto se imprimen por pantalla
# Autores : Felix Garcia Narocki con ayuda de chatGPT

# Aqui se escribe el input en formato latex(examen), jflap, parsing o calgary
input_string = """
A -> B
  | C u
  | v C
  | v B u.
B -> D.
C -> D.
D -> x D
  | .
"""  
# Tipo de traduccion
translation_type = "calgary_to_latex" # USO : {input_format}_to_{output_format}
# latex, calgary, parsing, jflap

def grammar_format_translator(input_string, translation_type):
    """
    Tool to translate grammar between different formats.
    Parameters:
    input_string (str): The grammar in the original format.
    translation_type (str): The type of translation to perform. Options are:
                            'parsing_to_jflap', 'jflap_to_calgary', 'calgary_to_parsing',
                            'parsing_to_calgary', 'latexo_to_calgary', 'latex_to_parsing'.
    """
    
    # To Calgary
    if translation_type == 'jflap_to_calgary':
        return jflap_to_calgary(input_string)
    elif translation_type == 'parsing_to_calgary':
        return parsing_to_calgary(input_string)
    elif translation_type == 'latex_to_calgary':
        tmpParsingTraduction = latex_to_parsing(input_string)
        return parsing_to_calgary(tmpParsingTraduction)

    # To Parsing
    elif translation_type == 'latex_to_parsing':
        return latex_to_parsing(input_string)
    elif translation_type == 'calgary_to_parsing':
        return calgary_to_parsing(input_string)
    elif translation_type == 'jflap_to_parsing':
        tmpCalgaryTraduction = jflap_to_calgary(input_string)
        return calgary_to_parsing(tmpCalgaryTraduction)
   
    # To JFLAP    
    elif translation_type == 'parsing_to_jflap':
        return parsing_to_jflap(input_string)
    elif translation_type == 'latex_to_jflap':
        tmpParsingTraduction = latex_to_parsing(input_string)
        return parsing_to_jflap(tmpParsingTraduction)
    elif translation_type == 'calgary_to_jflap':
        tmpParsingTraduction = latex_to_parsing(input_string)
        return parsing_to_jflap(tmpParsingTraduction)

    # To LaTeX
    elif translation_type == 'calgary_to_latex':
        return calgary_to_latex(input_string)
    elif translation_type == 'parsing_to_latex':
        tmpCalgaryTraduction = parsing_to_calgary(input_string)
        return calgary_to_latex(tmpCalgaryTraduction)
    elif translation_type == 'jflap_to_latex':
        tmpCalgaryTraduction = jflap_to_calgary(input_string)
        return calgary_to_latex(tmpCalgaryTraduction)

    else:
        return "Invalid translation type."

# Funciones de traduccion de formato

def parsing_to_jflap(parsing_grammar):
    # Crear la estructura base del XML
    structure = ET.Element('structure')
    ET.SubElement(structure, 'type').text = 'grammar'

    # Procesar cada producción
    productions = parsing_grammar.strip().split('\n')
    for prod in productions:
        if '->' in prod:
            left, right = prod.split('->')
            if 'I' in left:
                continue
            production = ET.SubElement(structure, 'production')
            # Manejar la cadena vacía
            ET.SubElement(production, 'left').text = left.strip()
            if right != 'e':
                ET.SubElement(production, 'right').text = right.strip()
            else:
                ET.SubElement(production, 'right')

    # Convertir la estructura de ElementTree a una cadena XML
    xml_str = ET.tostring(structure, encoding='unicode')

    # Formatear el XML con minidom y agregar &#13; al final de cada línea
    dom = minidom.parseString(xml_str)
    formatted_xml = dom.toprettyxml(indent="    ")
    formatted_xml = formatted_xml.replace('\n', '&#13;\n')

    # Agregar manualmente la declaración XML al principio del XML formateado
    declaration = '<?xml version="1.0" encoding="UTF-8" standalone="no"?><!--Created with JFLAP 7.1.-->\n'
    formatted_xml = formatted_xml.replace("<?xml version=\"1.0\" ?>&#13;\n", "")
    formatted_xml = declaration + formatted_xml
    formatted_xml = formatted_xml[:-6] # Quita el ultimo &#13
    return formatted_xml

def jflap_to_calgary(input_string):
    """
    Converts a given string from a specific format to the Calgary grammar format.
    """
    lines = input_string.split('\n')
    converted_lines = []
    current_head = None

    for line in lines:
        parts = line.split('\t')
        if len(parts) >= 3:
            left_side = parts[0].strip()
            right_side = ' '.join(parts[2].strip()) if parts[2].strip() else ' '  # Espacio entre cada carácter

            if current_head == left_side:
                # Si es el mismo encabezado, agregar '|' y la producción
                converted_lines[-1] += '\n  | ' + right_side
            else:
                # Si es un nuevo encabezado, agregar con '->'
                if current_head is not None:  # Agregar un punto si no es la primera línea
                    converted_lines[-1] += '.'
                converted_lines.append(left_side + ' -> ' + right_side)
                current_head = left_side

    # Agregando un punto al final de la última línea
    if converted_lines:
        converted_lines[-1] += '.'

    return '\n'.join(converted_lines)

def calgary_to_parsing(calgary_grammar):
    """
    Converts a grammar from Calgary format to Parsing format.
    """
    lines = calgary_grammar.split('\n')
    first_nonterminal = lines[0].split('->')[0].strip()  # Identify the first nonterminal
    parsing_grammar = f"I->{first_nonterminal}\n"  # Set the first nonterminal as the target of 'I'
    for line in lines:
        if '->' in line:
            head, productions = line.split('->')
            for production in productions.split('|'):
                # Removing spaces from the production and handling empty production
                production = production.strip()
                if production == '.':
                    parsing_production = head.strip() + '->e'  # Replace empty production with 'e'
                else:
                    parsing_production = head.strip() + '->' + ''.join(production.split())
                parsing_production = parsing_production.replace(".", "")
                parsing_grammar += parsing_production + '\n'
    return parsing_grammar.strip()

def parsing_to_calgary(parsing_grammar):
    """
    Converts a grammar from Parsing format to Calgary format.
    """
    lines = parsing_grammar.split('\n')
    calgary_grammar = ""
    current_head = ""
    for line in lines:
        if 'I' in line:
            # Ignoring the initial 'I' in Parsing grammars
            continue
        if '->' in line:
            head, production = line.split('->')
            head = head.strip()
            # Replacing 'e' with empty production for Calgary format
            production = production.strip().replace('e', '')
            production = " ".join(production)
            if head == current_head:
                calgary_grammar += '\n  | ' + production  # Add new line and spaces before '|'
            else:
                if current_head:  # If not the first production, add a period to end the previous one
                    calgary_grammar += '.\n'
                calgary_grammar += head + ' -> ' + production
                current_head = head
    calgary_grammar += '.'  # Add final period
    return calgary_grammar.strip()

def latex_to_calgary(latex_grammar):
    """
    Converts a grammar from latex format to Calgary format.
    """
    lines = latex_grammar.strip().split('\n')  # Elimina líneas vacías al principio y final
    calgary_grammar = ""
    for line in lines:
        if '→' in line:
            # Reemplazar 'ε' con espacio para la producción vacía en Calgary
            line = line.replace('ε', ' ').replace('→', '->').replace('|', '\n  |') + '.'
        calgary_grammar += line + '\n'
    return calgary_grammar.strip()

def latex_to_parsing(latex_grammar):
    """
    Converts a grammar from latex format to Parsing format.
    """
    lines = latex_grammar.strip().split('\n')  # Elimina líneas vacías al principio y final
    first_nonterminal = lines[0].split('→')[0].strip()  # Identify the first nonterminal
    parsing_grammar = f"I->{first_nonterminal}\n"  # Set the first nonterminal as the target of 'I'
    for line in lines:
        if '→' in line:
            head, productions = line.split('→')
            for production in productions.split('|'):
                # Manejando 'ε' como producción vacía en Parsing
                production = production.strip().replace('ε', 'e').replace('λ', 'e')
                # Eliminar espacios entre símbolos de producción
                production = ''.join(production.split())
                parsing_production = head.strip() + '->' + production
                parsing_grammar += parsing_production + '\n'
    return parsing_grammar.strip()

def calgary_to_latex(calgary_grammar):
    """
    Converts a grammar from Calgary format to LaTeX format.
    """
    lines = calgary_grammar.strip().split('\n')
    latex_grammar = "\\[\n\\begin{cases} \n"
    current_head = ""
    production = ""

    for line in lines:
        if '->' in line:
            current_head, production = line.split('->')
            current_head = current_head.strip()
        elif '|' in line:
            _, production = line.split('|')

        production = production.strip().replace('.', '')
        if production == '':
            production = 'ε'
        latex_grammar += f"\\text{{{current_head}}} \\quad \\xrightarrow{{}} \\quad \\text{{{production}}} \\\\ \n"
    latex_grammar += "\\end{cases}\n\\]"
    return latex_grammar


output_string = grammar_format_translator(input_string, translation_type)

def save_to_file(content, filename):

    with open(filename, 'w', encoding='utf-8') as file:
        file.write(content)

# Si la traducción involucra jflap, guardar en un archivo; de lo contrario, imprimir
if "jflap" in translation_type:
    save_to_file(output_string, "aaJflapGrammar.jff")
    print("Grammar saved to aaJflapGrammar.jff")
else:
    print(output_string)