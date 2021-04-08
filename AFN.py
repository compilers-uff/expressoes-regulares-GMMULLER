class AFN:
    # alfabeto = {'a', 'b', 'c'}
    # estados = {'q0', 'q1', 'q2'}
    # func_programa = {'q0': [('a', {'q1'}), ('b', {'q2'})]}
    # estado_inicial = 'q0'
    # estados_finais = {'qf'}
    def __init__(self, alfabeto, estados, func_programa, estado_inicial, estados_finais):

        for key,value in enumerate(func_programa):
            for transicao in func_programa[value]:
                if transicao[0] == None:
                    raise ValueError("AFN nao pode possuir transicoes epsilon")

        self.alfabeto = alfabeto
        self.estados = estados
        self.func_programa = func_programa
        self.estado_inicial = estado_inicial
        self.estados_finais = estados_finais

    def __str__(self):
        return "alfabeto: "+str(self.alfabeto)+"\n"+"estados: "+str(self.estados)+"\n"+"func_programa: "+str(self.func_programa)+"\n"+"estado_inicial: "+str(self.estado_inicial)+"\n"+"estados_finais: "+str(self.estados_finais)

    #renomear funcao para delta*
    #estados eh um set
    def funcProgramaEstendida(self, estados, palavra):
        if palavra == None:
            return estados
        
        a = None
        w = None

        a = palavra[0]
        w = palavra[1:]

        if w == '':
            w = None

        resultado = set()

        for estado in estados:
            if estado not in self.estados:
                raise Exception("Estado inexistente")

            if estado in self.func_programa:
                transicoes = self.func_programa[estado]
                for transicao in transicoes:
                    if transicao[0] == a:
                        resultado = resultado.union(transicao[1])

        return self.funcProgramaEstendida(resultado, w)