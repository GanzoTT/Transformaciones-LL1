# Transformaciones-LL1

Este proyecto es una implementación de un analizador sintáctico LL(1), que utiliza una gramática libre de contexto para validar si una cadena de entrada cumple con las reglas sintácticas definidas por la gramática. El analizador está diseñado para ser utilizado con una gramática de expresiones aritméticas simples, aunque puede ser extendido para otras gramáticas LL(1).

El analizador sigue un enfoque descendente predictivo, construyendo una tabla predictiva con los conjuntos 'PRIMEROS' y 'SIGUIENTES' de los símbolos no terminales de la gramática. Luego utiliza esta tabla para procesar y validar cadenas de entrada.

## Estructura del proyecto

El archivo principal contiene una clase GramaticaLL1, que incluye los siguientes componentes:

    producciones: Un diccionario que almacena las reglas de producción de la gramática.
    first: Un diccionario que almacena los conjuntos FIRST de los símbolos no terminales.
    follow: Un diccionario que almacena los conjuntos FOLLOW de los no terminales.
    tabla_predictiva: La tabla LL(1) generada para el análisis predictivo.
    no_terminales: Un conjunto de los símbolos no terminales de la gramática.
    terminales: Un conjunto de los símbolos terminales de la gramática.

## Métodos principales

    agregar_produccion(no_terminal, produccion): Agrega una producción a la gramática. Toma como argumentos el no terminal y su respectiva producción (una lista de símbolos).

    calcular_first(simbolo): Calcula el conjunto FIRST de un símbolo (terminal o no terminal).

    calcular_follow(inicial): Calcula los conjuntos FOLLOW de todos los no terminales. El símbolo inicial de la gramática es pasado como argumento.

    construir_tabla_predictiva(): Crea la tabla predictiva a partir de los conjuntos FIRST y FOLLOW.

    analizar(cadena): Realiza el análisis sintáctico de una cadena de entrada utilizando la tabla predictiva. Retorna True si la cadena es válida, o False si no lo es.

    tokenizar(cadena): Convierte una cadena de entrada en tokens, separando identificadores y símbolos terminales.

## Flujo de ejecución

    Definición de la gramática: Se crean las reglas de producción para una gramática LL(1) que reconoce expresiones aritméticas básicas con los operadores +, *, paréntesis y identificadores (id).

    Cálculo de los conjuntos FIRST y FOLLOW: Para cada no terminal de la gramática, se calculan los conjuntos FIRST y FOLLOW.

    Construcción de la tabla predictiva: Utilizando los conjuntos FIRST y FOLLOW, se genera una tabla predictiva que define cómo debe proceder el análisis basado en el símbolo de entrada actual y el tope de la pila de análisis.

    Análisis de una cadena: La cadena de entrada se analiza paso a paso, simulando el proceso de un parser descendente predictivo. Si la cadena sigue las reglas definidas por la gramática, se considera válida.

## Ejecución

  Instanciar la gramática: Se crea un objeto de la clase GramaticaLL1.

    gramatica = GramaticaLL1()

  Agregar producciones: Las reglas de la gramática se definen utilizando el método agregar_produccion.

    gramatica.agregar_produccion('E', ['T', 'E\''])

  Establecer el símbolo inicial: El símbolo inicial de la gramática se debe asignar.

    gramatica.inicial = 'E'

  Cálculo de PRIMEROS y SIGUIENTES: Los conjuntos 'PRIMEROS' y 'SIGUIENTES' se calculan con los métodos calcular_first y calcular_follow.
    
    for nt in gramatica.no_terminales:
        gramatica.calcular_first(nt)
    gramatica.calcular_follow(gramatica.inicial)

  Construir la tabla predictiva: Se construye la tabla LL(1).

    gramatica.construir_tabla_predictiva()

  Analizar una cadena: Se pasa una cadena de entrada y el analizador determinará si es válida o no según la gramática definida.

    cadena = "id+id*id"
    resultado = gramatica.analizar(cadena)

  Resultado: El resultado será True si la cadena es válida, y False si no lo es.

## Ejemplo

    python analizador_ll1.py

Salida esperada:

    Calculando conjuntos PRIMEROS...
    FIRST(E) = {'(', 'id'}
    FIRST(T) = {'(', 'id'}
    ...
    
    Calculando conjuntos SIGUIENTES...
    FOLLOW(E) = {'$', ')'}
    ...
    
    Construyendo tabla predictiva...
    
    Tabla predictiva construida:
    E: {'(': ['T', "E'"], 'id': ['T', "E'"]}
    ...
    
    Resultado final: La cadena 'id+id*id' es válida
