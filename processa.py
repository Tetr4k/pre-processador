import sys, os, platform, re
def fazIncludeAspas(codigo):
    for linha in codigo:
        include = re.search("#include\s*\"[\d\w]*\.[ch]\"\s*\n", linha)
        if include and include.group() == linha:
            nomeArquivo = re.search("(?<=\")[\d\w]*\.[ch](?=\")", include.group()).group()
            arquivo = open(nomeArquivo, 'r')
            if not arquivo:
                #Procura na pasta do compilador
                print("pra tirar erro")
            conteudo = arquivo.readlines()
            arquivo.close()
            for linha2 in codigo:
                conteudo.append(linha2)
            codigo = conteudo
    return codigo
# def fazIncludeMQMQ(codigo):
#     for linha in codigo:
#         include = re.search("#include\s*<[\d\w]*\.[ch]>\s*\n", linha)
#         if include and include.group() == linha:
#             nomeArquivo = re.search("(?<=<)[\d\w]*\.[ch](?=>)", include.group()).group()
#             arquivo = open(nomeArquivo, 'r')#Arrumar endereço
#             conteudo = arquivo.readlines()
#             arquivo.close()
#             conteudo = fazIncludeMQMQ(conteudo)
#             conteudo.append(codigo)
#             codigo.clear()
#             codigo = conteudo
#     return codigo
def tiraComentarioLinha(linha):                         #Funcao para remover comentarios de linha
    novaLinha = re.sub("//(.*)\\n", "", linha)          #Substitui comentario de linha por "" usando regex
    return novaLinha                                    #Retorna nova linha
def tiraQuebras(codigo):#Fazer -> não feito
    #texto = re.sub()
    return codigo
# def tiraComentarioParagrafo(codigo):#Fazer -> possiveis erros
#     codigo = re.sub("/\*(.*)\*/", "", codigo)
#     return codigo
sistema = platform.system()                             #Identifica sistema
os.system("mkdir backup")
nomesArquivos = sys.argv                                #Acessa parametros passados
nomesArquivos.pop(0)                                    #Remove primeiro parametro("processa.py")
for nomeArquivo in nomesArquivos:                       #Faz o pre-processamento para cada arquivo passado por parametro. 
    if sistema == "Windows":                            #Faz Backup do arquivo em Windows
        os.system("copy "+nomeArquivo+" backup")
    elif sistema == "Linux":                            #Faz Backup do arquivo em Linux
        os.system("cp "+nomeArquivo+" backup")
    else:
        print("Sistema não identificado")
        exit()
    arquivo = open(nomeArquivo, 'r')                    #Abre arquivo para leitura
    buffer = arquivo.readlines()                        #Pega o conteudo do arquivo
    arquivo.close()                                     #Fecha o arquivo

    
    #Manipulacao do buffer
    
    buffer = fazIncludeAspas(buffer)                       #Includes ""
    #buffer = fazIncludeMQMQ(buffer)                       #Includes <> 
    
    #Defines
    buffer = map(tiraComentarioLinha, buffer)           #Remove comentario do tipo "//" de cada linha

    #buffer = tiraQuebras(buffer)                       #Remove "/n"s
    
    #buffer = tiraComentarioParagrafo(buffer)           #Remove comentario do tipo "/*"
                
                #Remove " "s

    arquivo = open(nomeArquivo, 'w')    #Abre arquivo para escrita
    arquivo.writelines(buffer)          #Escreve o conteudo do arquivo
    arquivo.close()                     #Fecha o arquivo
print("Fim de execução")

#Includes

#Includes de Includes?

# Enquanto tiver include no arquivo{
#   Para cada linha{
#       Testa regex{
#           se deu match inclui
#       }
#   }
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