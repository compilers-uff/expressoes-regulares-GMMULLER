class AFD:

    '''
        @param set    alfabeto
        @param set    estados
        @param dict   func_programa Exemplo: {'q0': [('a', {'q1'}), ('b', {'q2'})]}.
        @param string estado_inicial
        @param set    estados_finais
    '''
    def __init__(self, alfabeto, estados, func_programa, estado_inicial, estados_finais):

        for key,value in enumerate(func_programa):
            for transicao in func_programa[value]:
                if len(transicao[1]) > 1 or transicao[0] == None:
                    raise ValueError("AFD nao suporta indeterminismo")

        self.alfabeto = alfabeto
        self.estados = estados
        self.func_programa = func_programa
        self.estado_inicial = estado_inicial
        self.estados_finais = estados_finais

    def __str__(self):
        return "alfabeto: "+str(self.alfabeto)+"\n"+"estados: "+str(self.estados)+"\n"+"func_programa: "+str(self.func_programa)+"\n"+"estado_inicial: "+str(self.estado_inicial)+"\n"+"estados_finais: "+str(self.estados_finais)

    '''
        @param set    estado  Conjunto de tamanho 1
        @param string palavra 
    '''
    def deltaEstrela(self, estado, palavra):

        if list(estado)[0] not in self.estados:
            raise Exception("Estado inexistente")

        if palavra == None or palavra == '':
            return estado

        if list(estado)[0] not in self.func_programa:
            return None

        a = None
        w = None

        a = palavra[0]
        w = palavra[1:]

        if w == '':
            w = None

        resultado = None

        for transicao in self.func_programa[list(estado)[0]]:
            if transicao[0] == a:
                resultado = transicao[1]

        #Caso a funcao esteja parcialmente definida para o simbolo e o estado atual
        if resultado == None:
            return None

        return self.deltaEstrela(resultado, w)

    '''
        Retorna False ou True dado uma palavra de acordo com sua aceitacao pelo automato.

        @param string w
    '''
    def accepted(self,w):
        
        estado_alcancado = self.deltaEstrela({self.estado_inicial}, w) 

        if estado_alcancado and not estado_alcancado.isdisjoint(self.estados_finais):
            return True
        
        return False