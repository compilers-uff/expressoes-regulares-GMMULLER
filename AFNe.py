class AFNe:

  '''
    @param set    alfabeto
    @param set    estados
    @param dict   func_programa Exemplo: {'q0': [('a', {'q1'}), ('b', {'q2'})]}.
    @param string estado_inicial
    @param set    estados_finais
  '''
  def __init__(self, alfabeto, estados, func_programa, estado_inicial, estados_finais):
    self.alfabeto = alfabeto
    self.estados = estados
    self.func_programa = func_programa
    self.estado_inicial = estado_inicial
    self.estados_finais = estados_finais

  def __str__(self):
    return "alfabeto: "+str(self.alfabeto)+"\n"+"estados: "+str(self.estados)+"\n"+"func_programa: "+str(self.func_programa)+"\n"+"estado_inicial: "+str(self.estado_inicial)+"\n"+"estados_finais: "+str(self.estados_finais)

  '''
    Retorna False ou True dado uma palavra de acordo com sua aceitacao pelo automato.

    @param string w
  '''
  def accepted(self, w):
    
    estados_alcancados = self.deltaEstrela(self.estado_inicial, w)

    if estados_alcancados.isdisjoint(estados_finais):
      return False
    else:
      return True

  '''
    @param set    estados
    @param string palavra
  '''
  def deltaEstrela(self, estados, palavra):
    if palavra == None:
      return self.fechoVazioEstendido(estados)

    w = None
    a = None

    if(palavra[:-1] != ''):
      w = palavra[:-1] #n primeiros caracteres excluindo o ultimo

    a = palavra[-1] #ultimo caracter

    conjunto_S = self.deltaEstrela(estados, w)
    conjunto_R = set()

    for s in conjunto_S:
      if s in self.func_programa:
        possibilidades = self.func_programa[s]
        for p in possibilidades:
          if p[0] == a:
            conjunto_R = conjunto_R.union(p[1])
    
    return self.fechoVazioEstendido(conjunto_R)

  '''
    Calcula o fecho vazio para um conjunto de estados.

    @param set estados
  '''
  def fechoVazioEstendido(self, estados):

    retorno = set()

    for e in estados:
      retorno = retorno.union(self.fechoVazio(e))

    return retorno

  '''
    @param string estado
  '''
  def fechoVazio(self, estado):
    
    retorno = set()

    explorado = set()
    explorar = [estado]

    #Faz uma busca em largura porque recursao pode resultar num loop infinito
    while len(explorar) > 0:
      e = explorar[0]
      retorno.add(e)

      if e in self.func_programa:
        possibilidades = self.func_programa[e]

        for p in possibilidades:
          if p[0] == None:
            if explorado == set(): #se explorado ainda esta vazio
              for a in p[1]: #o que ainda nao foi explorado
                explorar.append(a)
            else:
              for a in p[1]: 
                if a not in explorado: #o que ainda nao foi explorado
                  explorar.append(a)

      explorar.remove(e)
      explorado.add(e)

    return retorno