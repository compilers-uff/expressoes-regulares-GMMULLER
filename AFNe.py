class AFNe:
  # alfabeto = {'a', 'b', 'c'}
  # estados = {'q0', 'q1', 'q2'}
  # func_programa = {'q0': [('a', {'q1'}), ('b', {'q2'})]}
  # estado_inicial = 'q0'
  # estados_finais = {'qf'}
  def __init__(self, alfabeto, estados, func_programa, estado_inicial, estados_finais):
    self.alfabeto = alfabeto
    self.estados = estados
    self.func_programa = func_programa
    self.estado_inicial = estado_inicial
    self.estados_finais = estados_finais

  def __str__(self):
    return "alfabeto: "+str(self.alfabeto)+"\n"+"estados: "+str(self.estados)+"\n"+"func_programa: "+str(self.func_programa)+"\n"+"estado_inicial: "+str(self.estado_inicial)+"\n"+"estados_finais: "+str(self.estados_finais)

  #mudar nome para accepted
  def aceita(self, palavra):
    
    estados_alcancados = self.funcProgramaEstendida(self.estado_inicial, palavra)

    if estados_alcancados.isdisjoint(estados_finais):
      return False
    else:
      return True

  #renomear funcao para delta*
  #estados eh um set
  def funcProgramaEstendida(self, estados, palavra):
    if palavra == None:
      return self.fechoVazioEstendido(estados)

    w = None
    a = None

    if(palavra[:-1] != ''):
      w = palavra[:-1] #n primeiros caracteres excluindo o ultimo

    a = palavra[-1] #ultimo caracter

    conjunto_S = self.funcProgramaEstendida(estados, w)
    conjunto_R = set()

    for s in conjunto_S:
      if s in self.func_programa:
        possibilidades = self.func_programa[s]
        for p in possibilidades:
          if p[0] == a:
            conjunto_R = conjunto_R.union(p[1])
    
    return self.fechoVazioEstendido(conjunto_R)

  # Recebe um conjunto e retorna um conjunto (set)
  def fechoVazioEstendido(self, estados):

    retorno = set()

    for e in estados:
      retorno = retorno.union(self.fechoVazio(e))

    return retorno

  # Recebe um estado (nao pode ser um conjunto) e retorna um conjunto (set)
  # Recursivo causa iteracoes infinitas se houver loop de transicoes vazias
  def fechoVazio(self, estado):
    
    retorno = set()

    explorado = set()
    explorar = [estado]

    while len(explorar) > 0:
      e = explorar[0]
      retorno.add(e)

      if e in self.func_programa:
        possibilidades = self.func_programa[e]

        for p in possibilidades:
          if p[0] == None:
            if explorado == set(): #se explorado ainda estah vazio
              for a in p[1]: #o que ainda nao foi explorado
                explorar.append(a)
            else:
              for a in p[1]: 
                if a not in explorado: #o que ainda nao foi explorado
                  explorar.append(a)

      explorar.remove(e)
      explorado.add(e)

    return retorno