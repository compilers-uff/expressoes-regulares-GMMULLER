class AFD:
    #alfabeto = {'a', 'b', 'c'}
    # estados = {'q0', 'q1', 'q2'}
    # func_programa = {'q0': [('a', {'q1'}), ('b', {'q2'})]}
    # estado_inicial = 'q0'
    # estados_finais = {'qf'}
    # precisa adicionar coerencia interna, isto eh os estados presentes na func_programa devem aparecer em estados?
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

    #estado eh um set de tamanho 1 
    def funcProgramaEstendida(self, estado, palavra):
        if list(estado)[0] not in self.estados:
            raise Exception("Estado inexistente")

        if palavra == None:
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

        return self.funcProgramaEstendida(resultado, w)