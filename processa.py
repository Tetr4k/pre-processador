import sys, os, platform

sistema = platform.system() #Identifica sistema

nomesArquivos = sys.argv    #Acessa parametros passados
nomesArquivos.pop(0)        #Remove primeiro parametro("processa.py")

# Faz o pre-processamento para cada
# arquivo passado por parametro.
for nomeArquivo in nomesArquivos:
    print("Indentificando sistema")
    if sistema == "Windows":#Faz Backup do arquivo em Windows
        os.system("copy "+nomeArquivo+" backup")
        os.system("cls")
    elif sistema == "Linux":#Faz Backup do arquivo em Linux
        os.system("cp "+nomeArquivo+" backup")
        os.system("clear")
    else:
        print("Sistema não identificado")
        exit()
    print(sistema)

    arquivo = open(nomeArquivo, 'r')    #Abre arquivo para leitura
    buffer = arquivo.readlines()        #Pega o conteudo do arquivo
    arquivo.close()                     #Fecha o arquivo



    print(buffer)
    #Manipula o buffer
    buffer.reverse()                    #Palhaçada



    arquivo = open(nomeArquivo, 'w')    #Abre arquivo para escrita
    arquivo.writelines(buffer)          #Escreve o conteudo do arquivo
    arquivo.close()                     #Fecha o arquivo
print("Fim de execução")

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