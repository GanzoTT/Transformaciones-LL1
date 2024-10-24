class GramaticaLL1:
    def __init__(self):
        self.producciones = {}
        self.first = {}
        self.follow = {}
        self.tabla_predictiva = {}
        self.no_terminales = set()
        self.terminales = set()
        self.debug = True
        
    def agregar_produccion(self, no_terminal, produccion):
        if no_terminal not in self.producciones:
            self.producciones[no_terminal] = []
        self.producciones[no_terminal].append(produccion)
        self.no_terminales.add(no_terminal)
        for simbolo in produccion:
            if not simbolo.isupper() and simbolo != 'ε':
                self.terminales.add(simbolo)

    def calcular_first(self, simbolo):
        if simbolo in self.first:
            return self.first[simbolo]

        first_set = set()
        
        if simbolo not in self.no_terminales or simbolo == 'ε':
            first_set.add(simbolo)
            return first_set

        for produccion in self.producciones[simbolo]:
            if produccion[0] == 'ε':
                first_set.add('ε')
            else:
                for sim in produccion:
                    curr_first = self.calcular_first(sim)
                    first_set.update(curr_first - {'ε'})
                    if 'ε' not in curr_first:
                        break
                else:
                    first_set.add('ε')

        self.first[simbolo] = first_set
        return first_set

    def calcular_follow(self, inicial):
        self.follow = {nt: set() for nt in self.no_terminales}
        self.follow[inicial].add('$')
        
        cambio = True
        while cambio:
            cambio = False
            for A in self.no_terminales:
                for produccion in self.producciones[A]:
                    for i, B in enumerate(produccion):
                        if B in self.no_terminales:
                            resto = produccion[i+1:] if i < len(produccion)-1 else ['ε']
                            first_resto = set()
                            
                            for sim in resto:
                                curr_first = self.calcular_first(sim)
                                first_resto.update(curr_first - {'ε'})
                                if 'ε' not in curr_first:
                                    break
                            else:
                                first_resto.add('ε')
                            
                            if 'ε' in first_resto:
                                tam_anterior = len(self.follow[B])
                                self.follow[B].update(self.follow[A])
                                if len(self.follow[B]) > tam_anterior:
                                    cambio = True
                            
                            first_resto.discard('ε')
                            tam_anterior = len(self.follow[B])
                            self.follow[B].update(first_resto)
                            if len(self.follow[B]) > tam_anterior:
                                cambio = True

    def construir_tabla_predictiva(self):
        self.tabla_predictiva = {nt: {} for nt in self.no_terminales}
        
        for A in self.no_terminales:
            for produccion in self.producciones[A]:
                first_prod = set()
                
                if produccion[0] == 'ε':
                    first_prod = {'ε'}
                else:
                    for sim in produccion:
                        curr_first = self.calcular_first(sim)
                        first_prod.update(curr_first - {'ε'})
                        if 'ε' not in curr_first:
                            break
                    else:
                        first_prod.add('ε')
                
                for terminal in first_prod - {'ε'}:
                    if terminal in self.tabla_predictiva[A]:
                        raise Exception(f"La gramática no es LL(1): Conflicto en {A} -> {produccion}")
                    self.tabla_predictiva[A][terminal] = produccion
                
                if 'ε' in first_prod:
                    for terminal in self.follow[A]:
                        if terminal in self.tabla_predictiva[A]:
                            raise Exception(f"La gramática no es LL(1): Conflicto en {A} -> {produccion}")
                        self.tabla_predictiva[A][terminal] = ['ε']

    def analizar(self, cadena):
        # Tokenize the input string
        tokens = self.tokenizar(cadena)
        tokens.append('$')
        pila = ['$', self.inicial]
        i = 0
        
        if self.debug:
            print("\nAnálisis paso a paso:")
            print(f"Cadena de entrada: {tokens}")
            print(f"Pila inicial: {pila}")
        
        while pila[-1] != '$':
            X = pila[-1]
            a = tokens[i]
            
            if self.debug:
                print(f"\nPaso actual:")
                print(f"Tope de pila: {X}")
                print(f"Símbolo actual: {a}")
                print(f"Pila completa: {pila}")
                print(f"Entrada restante: {tokens[i:]}")
            
            if X in self.terminales or X == 'id':
                if X == a:
                    if self.debug:
                        print(f"Coincidencia: {X}")
                    pila.pop()
                    i += 1
                else:
                    if self.debug:
                        print(f"Error: Se esperaba {X}, se encontró {a}")
                    return False
            else:
                if X in self.tabla_predictiva and a in self.tabla_predictiva[X]:
                    produccion = self.tabla_predictiva[X][a]
                    if self.debug:
                        print(f"Aplicando producción: {X} -> {produccion}")
                    pila.pop()
                    if produccion != ['ε']:
                        for simbolo in reversed(produccion):
                            pila.append(simbolo)
                else:
                    if self.debug:
                        print(f"Error: No hay producción para {X} con entrada {a}")
                    return False
        
        return i == len(tokens) - 1

    def tokenizar(self, cadena):
        """Convierte la cadena de entrada en tokens"""
        tokens = []
        i = 0
        while i < len(cadena):
            if cadena[i:i+2] == 'id':
                tokens.append('id')
                i += 2
            else:
                tokens.append(cadena[i])
                i += 1
        return tokens

if __name__ == "__main__":
    # Crear la gramática
    gramatica = GramaticaLL1()
    
    # Agregar producciones para expresiones aritméticas
    gramatica.agregar_produccion('E', ['T', 'E\''])
    gramatica.agregar_produccion('E\'', ['+', 'T', 'E\''])
    gramatica.agregar_produccion('E\'', ['ε'])
    gramatica.agregar_produccion('T', ['F', 'T\''])
    gramatica.agregar_produccion('T\'', ['*', 'F', 'T\''])
    gramatica.agregar_produccion('T\'', ['ε'])
    gramatica.agregar_produccion('F', ['(', 'E', ')'])
    gramatica.agregar_produccion('F', ['id'])
    
    # Establecer símbolo inicial
    gramatica.inicial = 'E'
    
    # Calcular FIRST y FOLLOW
    print("Calculando conjuntos PRIMEROS...")
    for nt in gramatica.no_terminales:
        gramatica.calcular_first(nt)
    
    print("\nConjuntos PRIMEROS calculados:")
    for nt in gramatica.no_terminales:
        print(f"FIRST({nt}) = {gramatica.first[nt]}")
    
    print("\nCalculando conjuntos SIGUIENTES...")
    gramatica.calcular_follow(gramatica.inicial)
    
    print("\nConjuntos de SIGUIENTES calculados:")
    for nt in gramatica.no_terminales:
        print(f"FOLLOW({nt}) = {gramatica.follow[nt]}")
    
    # Construir tabla predictiva
    print("\nConstruyendo tabla predictiva...")
    gramatica.construir_tabla_predictiva()
    
    print("\nTabla predictiva construida:")
    for nt in gramatica.no_terminales:
        print(f"{nt}: {gramatica.tabla_predictiva[nt]}")
    
    # Analizar cadena
    cadena_prueba = "id+id*id"
    resultado = gramatica.analizar(cadena_prueba)
    print(f"\nResultado final: La cadena '{cadena_prueba}' es {'válida' if resultado else 'inválida'}")
