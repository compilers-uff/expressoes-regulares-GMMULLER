import sys

from funcoes_conversao import *

#OBS: None representa epsilon.

if sys.argv[1] == "-f":
    arquivo = sys.argv[2]
    palavra = sys.argv[3]

    with open(arquivo) as file:

        er = file.readline()

        while er:

            er = er.replace('\n','')

            retorno = match(er, palavra)

            if retorno:
                retorno = "OK"
            else:
                retorno = "Not OK"

            print("match("+er+","+palavra+") == "+retorno)

            er = file.readline()

else:
    er = sys.argv[1]
    palavra = sys.argv[2]
    retorno = match(er, palavra)

    if retorno:
        retorno = "OK"
    else:
        retorno = "Not OK"

    print("match("+er+","+palavra+") == "+retorno)
