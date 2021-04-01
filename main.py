from AFNe import *
from AFN import *
from AFD import *

alfabeto_er = {'a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z'}

def erToAFNe(er):
    #Gera um AFNe que aceita um termo qualquer
    def gera_afne(termo):
        aux_func_programa = {
                                'q0': [(termo, {'qf'})]
                            }
        afne = AFNe({termo}, {'q0','qf'}, aux_func_programa, 'q0', {'qf'})

        return afne

        # r = vazio => M1 = (vazio, {q0}, delta1, q0, vazio)
        # r = epsilon => M2 = (vazio, {qf}, delta2, qf, {qf})
        # r = x => M3 = ({x}, {q0, qf}, delta3, q0, {qf})

    #Concatena um valor (string) qualquer ao final de cada estado de um conjunto de transicoes
    def add_value_transitions(valor, transicoes):
        retorno = []

        for transicao in transicoes:
            retorno.append((transicao[0], set(map(lambda elem: elem+valor, transicao[1]))))        

        print(transicoes,retorno)

        return retorno

    #Concatena um valor (string) qualquer ao final de cada estado de um afne (retorna um novo afne)
    def add_value_afne_states(valor, afne):

        estados = afne.estados
        estados = set(map(lambda elem: elem+valor, estados))

        func_programa = afne.func_programa
        func_programa = dict(map(lambda kv: (kv[0]+valor, add_value_transitions(valor,kv[1])), func_programa.items()))
        
        estado_inicial = afne.estado_inicial+valor
        
        estados_finais = afne.estados_finais
        estados_finais = set(map(lambda elem: elem+valor, estados_finais))
        
        return AFNe(afne.alfabeto, estados, func_programa, estado_inicial, estados_finais)

    #Tratando a string
    er = er.replace(' ','').replace('(','').replace(')','').replace(',','')[::-1]
    
    pilha = []

    for caracter in er:
        er = er[1:]
        
        if caracter not in alfabeto_er:

            primeiro_termo = pilha.pop()

            #Gerando AFNe a partir de um termo da ER
            if primeiro_termo in alfabeto_er:
                primeiro_termo = gera_afne(primeiro_termo)

            #Concatenando 1 no final de todos os estados para diferencia-los na juncao
            novo_primeiro_termo = add_value_afne_states('1', primeiro_termo)

            segundo_termo = None
            novo_segundo_termo = None
            alfabeto = None

            #* nao precisa do segundo termo
            if(caracter != '*'):
                segundo_termo = pilha.pop()
                    
                if segundo_termo in alfabeto_er:
                    segundo_termo = gera_afne(segundo_termo)

                #Concatenando 2 no final de todos os estados para diferencia-los na juncao
                novo_segundo_termo = add_value_afne_states('2', segundo_termo)

                alfabeto = novo_primeiro_termo.alfabeto.union(novo_segundo_termo.alfabeto)
            else:
                alfabeto = novo_primeiro_termo.alfabeto.copy()

            # print(novo_primeiro_termo)
            # print()
            # print(novo_segundo_termo)
            # print()

            if caracter == '.':
                
                estados = novo_primeiro_termo.estados.union(novo_segundo_termo.estados)
                #Adicionando transicao do estado final do primeiro automato para o estado inicial do segundo
                func_programa = {list(novo_primeiro_termo.estados_finais)[0]:[(None, {novo_segundo_termo.estado_inicial})]}
                #Concatenando as funcoes de transicao de ambos os automatos
                func_programa.update(novo_primeiro_termo.func_programa)
                func_programa.update(novo_segundo_termo.func_programa)
                estado_inicial = novo_primeiro_termo.estado_inicial
                #O estado final eh unico
                estados_finais = {list(novo_segundo_termo.estados_finais)[0]}

                afne_resultante = AFNe(alfabeto, estados, func_programa, estado_inicial, estados_finais)

                #Empilhando o afne resultante
                pilha.append(afne_resultante) 

            elif caracter == '+':

                estados = novo_primeiro_termo.estados.union(novo_segundo_termo.estados)
                estados.add('q0')
                estados.add('qf')

                func_programa = {
                                    'q0': [(None, {novo_primeiro_termo.estado_inicial}), (None, {novo_segundo_termo.estado_inicial})],
                                    list(novo_primeiro_termo.estados_finais)[0]:[(None,{'qf'})],
                                    list(novo_segundo_termo.estados_finais)[0]:[(None,{'qf'})]
                                }
                func_programa.update(novo_primeiro_termo.func_programa)
                func_programa.update(novo_segundo_termo.func_programa)

                estado_inicial = 'q0'
                estados_finais = {'qf'}

                afne_resultante = AFNe(alfabeto, estados, func_programa, estado_inicial, estados_finais)

                #Empilhando o afne resultante
                pilha.append(afne_resultante) 

            elif caracter == '*':   
                
                estados = novo_primeiro_termo.estados
                estados.add('q0')
                estados.add('qf')

                func_programa = {
                                    'q0': [(None, {'qf'}), (None, {novo_primeiro_termo.estado_inicial})],
                                    list(novo_primeiro_termo.estados_finais)[0]:[(None, {novo_primeiro_termo.estado_inicial}), (None, {'qf'})],

                                }
                func_programa.update(novo_primeiro_termo.func_programa)
                
                estado_inicial = 'q0'
                estados_finais = {'qf'}

                afne_resultante = AFNe(alfabeto, estados, func_programa, estado_inicial, estados_finais)

                #Empilhando o afne resultante
                pilha.append(afne_resultante) 

        else:
            pilha.append(caracter)

    return pilha.pop()

#Acho que o nome dessa funcao estah errado no enunciado
def afneToAFN(afne):

    alfabeto = afne.alfabeto.copy()
    estados = afne.estados.copy()
    func_programa = {}
    estado_inicial = afne.estado_inicial
    estados_finais = set()

    for estado in estados:
        estados_alcancados = afne.fechoVazio(estado)

        #Se ha alguma intercecao
        if not estados_alcancados.isdisjoint(afne.estados_finais):
            estados_finais.add(estado)

        #Criando a funcao programa
        for letra in alfabeto:
            resultados = afne.funcProgramaEstendida({estado}, letra)
            if len(resultados) != 0:
                if estado in func_programa:
                    func_programa[estado].append((letra, resultados))
                else:
                    func_programa[estado] = [(letra, resultados)]

    return AFN(alfabeto, estados, func_programa, estado_inicial, estados_finais)


def afntoAFD(afn):

    def string_to_set(conjunto):
        return set(conjunto.replace('{','').replace('}','').replace(' ','').split(','))

    #key eh um conjunto e func_programa possui stringfied sets como chaves
    def list_has_set(lista, conjunto):
        for value in lista:
            key_set = string_to_set(value)
            if key_set == conjunto:
                return str(key_set)

        return False

    alfabeto = afn.alfabeto.copy()
    estados = set()
    func_programa = {}
    estado_inicial = None
    estados_finais = set()

    explorado = []
    explorar = [{afn.estado_inicial}]

    todas_transicoes = []

    while len(explorar) > 0:
        e = explorar.pop(0)
        explorado.append(e)

        for letra in alfabeto:
            resultado = afn.funcProgramaEstendida(e,letra)
            if len(resultado) > 0:
                todas_transicoes.append([e.copy(), letra, resultado])
                if resultado not in explorado:
                    explorar.append(resultado)

    #Renomeando todos os estados
    nome_estado_contador = 0
    for transicao in todas_transicoes:
        estado = transicao[0]
        destino = transicao[2]
        
        if isinstance(estado, set): #Caso nao tenha sido convertido ainda

            estados.add('q'+str(nome_estado_contador))

            if not estado.isdisjoint(afn.estados_finais):
                estados_finais.add('q'+str(nome_estado_contador))

            if list(estado)[0] == afn.estado_inicial and estado_inicial == None:
                print(estado, afn.estado_inicial)
                estado_inicial = 'q'+str(nome_estado_contador)

            for t in todas_transicoes:
                if t[0] == estado:
                    t[0] = 'q'+str(nome_estado_contador)
                if t[2] == estado:
                    t[2] = 'q'+str(nome_estado_contador)
            nome_estado_contador += 1

        if estado != destino:

            if isinstance(destino, set): #Caso nao tenha sido convertido ainda

                estados.add('q'+str(nome_estado_contador))

                if not destino.isdisjoint(afn.estados_finais):
                    estados_finais.add('q'+str(nome_estado_contador))

                if list(destino)[0] == afn.estado_inicial and estado_inicial == None:
                    print(list(destino)[0], afn.estado_inicial)
                    estado_inicial = 'q'+str(nome_estado_contador)

                for t in todas_transicoes:
                    if t[0] == destino:
                        t[0] = 'q'+str(nome_estado_contador)
                    if t[2] == destino:
                        t[2] = 'q'+str(nome_estado_contador)
                nome_estado_contador += 1

    for transicao in todas_transicoes:
        estado = transicao[0]
        termo = transicao[1]
        destino = transicao[2]

        if estado not in func_programa:
            func_programa[estado] = [(termo, {destino})]
        else:
            func_programa[estado].append((termo, {destino}))

    return AFD(alfabeto, estados, func_programa, estado_inicial, estados_finais)

func_programa = {
                    'q0': [('a', {'q0','q1'}), ('b', {'q0'})],
                    'q1': [('a', {'q2'})],
                    'q2': [('a', {'qf'})]
                }

afn = AFN({'a','b'}, {'q0','q1','q2','qf'}, func_programa, 'q0', {'qf'})

# print(afn.funcProgramaEstendida({'q0'}, "c"))
print(afntoAFD(afn))
# set(a.replace('{','').replace('}','').replace(' ','').split(','))