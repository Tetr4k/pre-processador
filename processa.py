import sys

nomesArquivos = sys.argv
nomesArquivos.pop(0)

for nomeArquivo in nomesArquivos:
    arquivo = open(nomeArquivo, 'r')
    print(arquivo.readlines())

    
    arquivo.close()

#Includes

#Includes de Includes?

# Enquanto tiver include no arquivo{
#   busca o primeiro include
#   usa ""? -> procura na pasta do projeto
#   usa <>? -> procura na pasta do gcc
#   inclui o conteudo
# }

#defines 
# Sobre os defines, é importante considerar macros também.
# como assim macros?????

#Remover comentarios

# Busca //
# Se encontrou{
#   remove conteudo entre // e o /n
#   Busca //
# }
#
# Busca /*
# Se encontrou{
#   remove conteudo até encontrar */
#   Busca /*
# }

#Tira quebras de linha e espaços