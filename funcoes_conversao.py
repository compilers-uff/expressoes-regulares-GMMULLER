from AFNe import *
from AFN import *
from AFD import *

alfabeto_er = {'a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z'}

'''
    Retorna a instancia de um AFNe.

    @param string er
'''
def erToAFNe(er):

    '''
        Gera um AFNe que aceita um termo qualquer do alfabeto er
    '''
    def gera_afne(termo):
        aux_func_programa = {
                                'q0': [(termo, {'qf'})]
                            }
        afne = AFNe({termo}, {'q0','qf'}, aux_func_programa, 'q0', {'qf'})

        return afne

        #TODO r = vazio => M1 = (vazio, {q0}, delta1, q0, vazio)
        #TODO r = epsilon => M2 = (vazio, {qf}, delta2, qf, {qf})
        #TODO r = x => M3 = ({x}, {q0, qf}, delta3, q0, {qf})

    '''
        Concatena um valor qualquer ao final de cada estado de uma lista de transicoes

        @param string valor
        @param list   transicoes  
    '''
    def add_value_transitions(valor, transicoes):
        retorno = []

        for transicao in transicoes:
            retorno.append((transicao[0], set(map(lambda elem: elem+valor, transicao[1]))))        

        return retorno

    '''
        Concatena um valor qualquer ao final de cada estado de um AFNe, retornando um novo AFNe

        @param string valor
        @param AFNe   afne
    '''
    def add_value_afne_states(valor, afne):

        estados = afne.estados
        estados = set(map(lambda elem: elem+valor, estados))

        func_programa = afne.func_programa
        func_programa = dict(map(lambda kv: (kv[0]+valor, add_value_transitions(valor,kv[1])), func_programa.items()))
        
        estado_inicial = afne.estado_inicial+valor
        
        estados_finais = afne.estados_finais
        estados_finais = set(map(lambda elem: elem+valor, estados_finais))
        
        return AFNe(afne.alfabeto, estados, func_programa, estado_inicial, estados_finais)

    #Tratando a string de entrada
    er = er.replace(' ','').replace('(','').replace(')','').replace(',','').replace('\'', '').replace('\"', '')[::-1]
    
    pilha = []

    while len(er) > 0:
        caracter = er[0]
        er = er[1:]

        #Se o caracter eh um operador ou um outro AFNe
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

            #O operador * eh unario
            if(caracter != '*'):
                segundo_termo = pilha.pop()
                    
                #Gerando AFNe a partir de um termo da ER
                if segundo_termo in alfabeto_er:
                    segundo_termo = gera_afne(segundo_termo)

                #Concatenando 2 no final de todos os estados para diferencia-los na juncao
                novo_segundo_termo = add_value_afne_states('2', segundo_termo)

                alfabeto = novo_primeiro_termo.alfabeto.union(novo_segundo_termo.alfabeto)
            else:
                alfabeto = novo_primeiro_termo.alfabeto.copy()

            if caracter == '.':
                
                estados = novo_primeiro_termo.estados.union(novo_segundo_termo.estados)

                func_programa = {list(novo_primeiro_termo.estados_finais)[0]:[(None, {novo_segundo_termo.estado_inicial})]}
                func_programa.update(novo_primeiro_termo.func_programa)
                func_programa.update(novo_segundo_termo.func_programa)
                estado_inicial = novo_primeiro_termo.estado_inicial

                estados_finais = {list(novo_segundo_termo.estados_finais)[0]}

                afne_resultante = AFNe(alfabeto, estados, func_programa, estado_inicial, estados_finais)

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

                pilha.append(afne_resultante) 

        else:
            pilha.append(caracter)

    ultimo_elemento = pilha.pop()

    #Caso tenha sobrado um operador na pilha
    if ultimo_elemento in {'*','.','+'}:
        raise Exception("Notacao errada para ER")

    if ultimo_elemento in alfabeto_er:
        ultimo_elemento = gera_afne(ultimo_elemento)

    return ultimo_elemento

'''
    Retorna a instancia de um AFN.

    @param AFNe afne
'''
def afneToAFN(afne):

    alfabeto = afne.alfabeto.copy()
    estados = afne.estados.copy()
    func_programa = {}
    estado_inicial = afne.estado_inicial
    estados_finais = set()

    #Montando funcao programa e estados finais
    for estado in estados:
        estados_alcancados = afne.fechoVazio(estado)

        if not estados_alcancados.isdisjoint(afne.estados_finais):
            estados_finais.add(estado)

        for letra in alfabeto:
            resultados = afne.deltaEstrela({estado}, letra)
            if len(resultados) != 0:
                if estado in func_programa:
                    func_programa[estado].append((letra, resultados))
                else:
                    func_programa[estado] = [(letra, resultados)]

    afn = AFN(alfabeto, estados, func_programa, estado_inicial, estados_finais)

    return afn


'''
    Retorna a instancia de um AFD.

    @param AFN afn
'''
def afnToAFD(afn):

    alfabeto = afn.alfabeto.copy()
    estados = set()
    func_programa = {}
    estado_inicial = None
    estados_finais = set()

    explorado = []
    explorar = [{afn.estado_inicial}]

    todas_transicoes = [] #Guarda todas as transicoes de maneira 'planificada' [estado_origem, letra, estado_destino]

    #Criando todos os estados a partir do inicial
    while len(explorar) > 0:
        e = explorar.pop(0)
        explorado.append(e)

        for letra in alfabeto:
            resultado = afn.deltaEstrela(e,letra)
            if len(resultado) > 0:
                todas_transicoes.append([e.copy(), letra, resultado])
                if resultado not in explorado:
                    explorar.append(resultado)

    #Renomeando todos os estados
    nome_estado_contador = 0
    for transicao in todas_transicoes:
        estado = transicao[0]
        destino = transicao[2]
        
        #Caso nao tenha sido convertido ainda
        if isinstance(estado, set):

            estados.add('q'+str(nome_estado_contador))

            if not estado.isdisjoint(afn.estados_finais):
                estados_finais.add('q'+str(nome_estado_contador))

            if list(estado)[0] == afn.estado_inicial and estado_inicial == None:
                estado_inicial = 'q'+str(nome_estado_contador)

            for t in todas_transicoes:
                if t[0] == estado:
                    t[0] = 'q'+str(nome_estado_contador)
                if t[2] == estado:
                    t[2] = 'q'+str(nome_estado_contador)
            nome_estado_contador += 1

        if estado != destino:

            #Caso nao tenha sido convertido ainda
            if isinstance(destino, set):

                estados.add('q'+str(nome_estado_contador))

                if not destino.isdisjoint(afn.estados_finais):
                    estados_finais.add('q'+str(nome_estado_contador))

                if list(destino)[0] == afn.estado_inicial and estado_inicial == None:
                    estado_inicial = 'q'+str(nome_estado_contador)

                for t in todas_transicoes:
                    if t[0] == destino:
                        t[0] = 'q'+str(nome_estado_contador)
                    if t[2] == destino:
                        t[2] = 'q'+str(nome_estado_contador)
                nome_estado_contador += 1

    #Montando funcao de transicao
    for transicao in todas_transicoes:
        estado = transicao[0]
        termo = transicao[1]
        destino = transicao[2]

        if estado not in func_programa:
            func_programa[estado] = [(termo, {destino})]
        else:
            func_programa[estado].append((termo, {destino}))

    afd = AFD(alfabeto, estados, func_programa, estado_inicial, estados_finais)

    return afd

'''
    Retorna a instancia de um AFD.

    @param AFD afd
'''
def afdToAFDmin(afd):

    '''
        Modifica o proprio afd passado como argumento

        @param AFD afd
    '''
    def remove_estados_inacessiveis(afd):

        visitados = set()
        visitar = [afd.estado_inicial]

        #Realizando uma busca em largura para definir os estados inacessiveis
        while len(visitar) > 0:
            estado_atual = visitar.pop(0)
            visitados.add(estado_atual)

            if estado_atual in afd.func_programa:
                for transicao in afd.func_programa[estado_atual]:
                    if list(transicao[1])[0] not in visitados:
                        visitar.append(list(transicao[1])[0])

        estados_inacessiveis = afd.estados - visitados

        afd.estados = afd.estados - estados_inacessiveis

        afd.estados_finais = afd.estados_finais - estados_inacessiveis

        #Removendo os estados inacessiveis da funcao programa
        for estado in estados_inacessiveis:
            if estado in afd.func_programa:
                del afd.func_programa[estado]

    '''
        Totaliza a funcao de transicao de um afd se necessario. Modifica o proprio afd passado como argumento

        @param AFD afd
    '''
    def totaliza_func_programa(afd):
        sink_criado = False
        sink = 'd' 

        while(sink in afd.estados): #Caso jah exista um estado com o nome d entre os estados
            sink = sink+'d'

        estados_existentes = set()
        for estado in afd.func_programa:
            estados_existentes.add(estado)
            transicoes_existentes = set()
            for transicao in afd.func_programa[estado]:
                transicoes_existentes.add(transicao[0])
            #A funcao eh parcial
            if transicoes_existentes != afd.alfabeto:
                if not sink_criado:
                    sink_criado = True
                    afd.estados.add(sink)
                transicoes_a_adicionar = afd.alfabeto - transicoes_existentes
                for letra in transicoes_a_adicionar:
                    afd.func_programa[estado].append((letra, {sink}))

        #Estados inexistentes na funcao programa
        estados_a_adicionar = afd.estados - estados_existentes
        if len(estados_a_adicionar) > 0:
            if not sink_criado:
                sink_criado = True
                afd.estados.add(sink)
                estados_a_adicionar.add(sink)

            for estado in estados_a_adicionar:
                afd.func_programa[estado] = []
                for letra in afd.alfabeto:
                    afd.func_programa[estado].append((letra, {sink}))

    '''
        Gera a tabela de minimizacao de um AFD.

        @param AFD afd
    '''
    def gera_tabela(afd):
        tabela = {}
        estados = list(afd.estados)

        for estado in estados:
            tabela[estado] = {}
            for e in estados:
                if e != estado: #nao faz sentido testar se um estado e equivalente a ele mesmo
                    if e in afd.estados_finais and estado not in afd.estados_finais: #marcando estados trivialmente nao equivalentes
                        tabela[estado][e] = False #false para nao equivalentes
                    elif e not in afd.estados_finais and estado in afd.estados_finais:
                        tabela[estado][e] = False #false para nao equivalentes
                    else:
                        tabela[estado][e] = True #true para equivalentes
        return tabela

    '''
        Processa a tabela de minimizacao de um AFD para descobrir quais estados sao equivalentes. Modifica a propria tabela passada como argumento.

        @param AFD  afd
        @param dict tabela
    '''
    def processa_tabela(afd, tabela):

        '''
            @param set        estados Um conjunto de tamanho 2
            @param list(list) lista   Uma lista contendo todas as listas de dependencias  
        '''
        def fecha_lista_encabecada(estados, lista, tabela):
            for elem in lista:
                if elem[0] == estados: #se a lista eh encabecada pelos estados
                    for i in range(1,len(elem)):
                        if tabela[list(elem[i])[0]][list(elem[i])[1]]: #se ainda nao foi marcado (para evitar qualquer loop de dependencia)
                            tabela[list(elem[i])[0]][list(elem[i])[1]] = False
                            tabela[list(elem[i])[1]][list(elem[i])[0]] = False
                            fecha_lista_encabecada(elem[i], lista, tabela) #fecha outras listas recursivamente

        '''
            Adiciona estados2 numa lista encabecada por estados1.

            @param set        estados1 Um conjunto de tamanho 2
            @param set        estados2 Um conjunto de tamanho 2
            @param list(list) lista    Uma lista contendo todas as listas de dependencias
        '''
        def add_lista_encabecada(estados1, estados2, lista, tabela):
            encabeca = False
            key = None

            for i,elem in enumerate(lista):
                if elem[0] == estados1:
                    encabeca = True
                    key = i

            #Se a lista de dependencia para esse conjunto de estados ja foi criada
            if encabeca:
                lista[key].append(estados2)
            else:
                lista.append([estados1,estados2])

        estados = list(afd.estados)
        listas_dependencias = []
        visitados = []

        for estado in estados:
            for e in estados:
                if e != estado and tabela[estado][e] and {estado, e} not in visitados: #nao eh a si mesmo e ainda nao foi marcado
                    visitados.append({estado, e})
                    for letra in afd.alfabeto:
                        resultado1 = list(afd.deltaEstrela({estado}, letra))[0]
                        resultado2 = list(afd.deltaEstrela({e}, letra))[0]
                        if resultado1 != resultado2:
                            if not tabela[resultado1][resultado2]: #se os estados resultado1 e resultado2 nao sao equivalentes
                                tabela[estado][e] = False
                                tabela[e][estado] = False
                                fecha_lista_encabecada({estado, e}, listas_dependencias, tabela)
                                break #basta uma condicao se verificar para marcar
                            else:
                                add_lista_encabecada({resultado1,resultado2}, {estado,e}, listas_dependencias, tabela)

    '''
        Calcula equivalencia de um estado de forma transitiva.

        @param dict   tabela
        @param string estado
    '''
    def fecho_equivalencia(tabela, estado):
        retorno = set()
        retorno.add(estado)

        explorado = []
        explorar = [estado]

        while len(explorar) > 0:
            e = explorar.pop(0)
            explorado.append(e)

            for elem in tabela[e]:
                if tabela[e][elem]: #se sao equivalentes
                    retorno.add(elem)
                    if elem not in explorado:
                        explorar.append(elem)

        return retorno

    '''
        @param AFD afd
    '''
    def remove_estados_inuteis(afd):

        estados_inuteis = set()

        for estado in afd.estados:
            visitados = set()
            visitar = [estado]

            #Realizando uma busca em largura para definir os estados inuteis
            while len(visitar) > 0:
                estado_atual = visitar.pop(0)
                visitados.add(estado_atual)

                if estado_atual in afd.func_programa:
                    for transicao in afd.func_programa[estado_atual]:
                        if list(transicao[1])[0] not in visitados:
                            visitar.append(list(transicao[1])[0])

            if visitados.isdisjoint(afd.estados_finais):
                estados_inuteis.add(estado)

        afd.estados = afd.estados - estados_inuteis

        afd.estados_finais = afd.estados_finais - estados_inuteis

        #Removendo os estados inuteis da funcao programa
        for estado in estados_inuteis:
            if estado in afd.func_programa:
                del afd.func_programa[estado]

        transicoes_inuteis = []
        #Removendo as transicoes para estados inuteis
        for estado in afd.func_programa:
            novas_transicoes = []

            for transicao in afd.func_programa[estado]:
                if list(transicao[1])[0] not in estados_inuteis:
                    novas_transicoes.append(transicao)

            if len(novas_transicoes) == 0:
                transicoes_inuteis.append(estado)

            afd.func_programa[estado] = novas_transicoes

        for estado in transicoes_inuteis:
            del afd.func_programa[estado]

    if not isinstance(afd, AFD):
        raise Exception("Automato precisa ser deterministico para ser minimizado")

    #Fazendo uma copia para nao modificar o objeto original
    afdmin = AFD(afd.alfabeto.copy(), afd.estados.copy(), afd.func_programa.copy(), afd.estado_inicial, afd.estados_finais.copy())

    remove_estados_inacessiveis(afdmin)
    totaliza_func_programa(afdmin)
    tabela = gera_tabela(afdmin)
    processa_tabela(afdmin, tabela)

    conjuntos_resultantes = []
    estados_unificados = []

    #Descobrindo quais estados sao equivalentes
    for estado in tabela:
        explorado = False #marca se o estado ja foi explorado
        for cr in conjuntos_resultantes:
            if estado in cr:
                explorado = True
                break
            
        if not explorado:
            conjuntos_resultantes.append(fecho_equivalencia(tabela, estado))

    for i in range(len(conjuntos_resultantes)):
        estados_unificados.append('q'+str(i))

    afdmin.estados = set(estados_unificados)

    func_programa_resultante = {}
    todas_transicoes = []

    #Transformando transicoes numa lista de listas [inicio, letra, destino]
    for estado in afdmin.func_programa:
        for transicao in afdmin.func_programa[estado]:
            todas_transicoes.append([estado, transicao[0], transicao[1]])

    #Convertendo os estados das transicoes nos estados unificados
    for transicao in todas_transicoes:
        inicio = transicao[0]
        inicio_traduzido = None
        destino = list(transicao[2])[0]
        destino_traduzido = None

        for index,conjunto in enumerate(conjuntos_resultantes):
            if inicio in conjunto:
                inicio_traduzido = estados_unificados[index]

            if destino in conjunto:
                destino_traduzido = estados_unificados[index]

        transicao[0] = inicio_traduzido
        transicao[2] = {destino_traduzido}

    #Remontando a funcao programa resultante da minimizacao
    for transicao in todas_transicoes:
        if transicao[0] not in func_programa_resultante:
            func_programa_resultante[transicao[0]] = []

        if (transicao[1], transicao[2]) not in func_programa_resultante[transicao[0]]: #se eh uma transicao nova
            func_programa_resultante[transicao[0]].append((transicao[1], transicao[2]))

    estados_finais_resultante = set()
    estado_inicial_resultante = None

    #Decidindo quais estados sao finais e o estado inicial
    for index,conjunto in enumerate(conjuntos_resultantes):
        for estado in conjunto:
            if estado in afdmin.estados_finais:
                estados_finais_resultante.add(estados_unificados[index])
            
            if estado == afdmin.estado_inicial:
                estado_inicial_resultante = estados_unificados[index]

    afdmin.estado_inicial = estado_inicial_resultante
    afdmin.estados_finais = estados_finais_resultante
    afdmin.func_programa = func_programa_resultante

    remove_estados_inuteis(afdmin)

    return afdmin

'''
    @param string er
    @param string w
'''
def match(er, w):

    if(er == ''):
        return False

    #None representa epsilon
    if(er == None):
        return True

    return afdToAFDmin(afnToAFD(afneToAFN(erToAFNe(er)))).accepted(w)