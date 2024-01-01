# Grammar Format Translator

## Descripción
Este script es un traductor de formatos de gramáticas diseñado para trabajar con diversas herramientas y formatos, incluyendo JFLAP, ParsingEmulator, Context-free Grammar Checker (formato de Calgary), y el formato humano (matemático). Permite la conversión entre estos distintos formatos de manera eficiente y automática.

## Características
- **Soporte de Formatos**: Capaz de traducir gramáticas entre los formatos utilizados por JFLAP, ParsingEmulator, Context-free Grammar Checker (Calgary), y el formato humano (matemático).
- **Salida para JFLAP**: Las gramáticas traducidas a formato JFLAP se guardan en un archivo `.jff`, listo para ser importado en la herramienta JFLAP.
- **Impresión en Pantalla**: Para los demás formatos, el resultado de la traducción se imprime directamente en la pantalla.

## Uso
1. **Especificar la Gramática de Entrada**: Escribir la gramática en el formato deseado dentro de la variable `input_string`.
2. **Elegir el Tipo de Traducción**: Establecer el tipo de traducción en la variable `translation_type` utilizando el formato `{input_format}_to_{output_format}`. Los formatos soportados son: `human`, `calgary`, `parsing`, `jflap`.
3. **Ejecutar el Script**: Al ejecutar el script, se realizará la traducción según lo especificado y se mostrará el resultado de acuerdo con el formato de salida seleccionado.

## Notas Adicionales
- **Input de JFLAP**: Para obtener el input en formato JFLAP, seleccionar todas las celdas en JFLAP y copiarlas con `Ctrl+C`.
- **Autores**: Felix Garcia Narocki con la ayuda de ChatGPT.

## Ejemplo de Uso
Para realizar una traducción de una gramática en formato humano a formato JFLAP, el script se usaría de la siguiente manera:

```python
input_string = """
S → a S B | b
A → a | a A
B → A a C | b A
C → c C c
"""
translation_type = "human_to_jflap"
output_string = grammar_format_translator(input_string, translation_type)
```

En este caso, el resultado se guardará en un archivo llamado `aaJflapGrammar.jff`, listo para ser importado en JFLAP.

---

Este README proporciona una visión general clara de tu script, su uso y características. Si hay algo más que quisieras añadir o modificar, házmelo saber.Aquí tienes un ejemplo de README para tu script de traducción de formatos de gramáticas:

---

# Grammar Format Translator

## Descripción
Este script es un traductor de formatos de gramáticas diseñado para trabajar con diversas herramientas y formatos, incluyendo JFLAP, ParsingEmulator, Context-free Grammar Checker (formato de Calgary), y el formato humano (matemático). Permite la conversión entre estos distintos formatos de manera eficiente y automática.

## Características
- **Soporte de Formatos**: Capaz de traducir gramáticas entre los formatos utilizados por JFLAP, ParsingEmulator, Context-free Grammar Checker (Calgary), y el formato humano (matemático).
- **Salida para JFLAP**: Las gramáticas traducidas a formato JFLAP se guardan en un archivo `.jff`, listo para ser importado en la herramienta JFLAP.
- **Impresión en Pantalla**: Para los demás formatos, el resultado de la traducción se imprime directamente en la pantalla.

## Uso
1. **Especificar la Gramática de Entrada**: Escribir la gramática en el formato deseado dentro de la variable `input_string`.
2. **Elegir el Tipo de Traducción**: Establecer el tipo de traducción en la variable `translation_type` utilizando el formato `{input_format}_to_{output_format}`. Los formatos soportados son: `human`, `calgary`, `parsing`, `jflap`.
3. **Ejecutar el Script**: Al ejecutar el script, se realizará la traducción según lo especificado y se mostrará el resultado de acuerdo con el formato de salida seleccionado.

## Notas Adicionales
- **Input de JFLAP**: Para obtener el input en formato JFLAP, seleccionar todas las celdas en JFLAP y copiarlas con `Ctrl+C`.
- **Autores**: Felix Garcia Narocki con la ayuda de ChatGPT.

## Ejemplo de Uso
Para realizar una traducción de una gramática en formato humano a formato JFLAP, el script se usaría de la siguiente manera:

```python
input_string = """
S → a S B | b
A → a | a A
B → A a C | b A
C → c C c
"""
translation_type = "human_to_jflap"
output_string = grammar_format_translator(input_string, translation_type)
```

En este caso, el resultado se guardará en un archivo llamado `aaJflapGrammar.jff`, listo para ser importado en JFLAP.