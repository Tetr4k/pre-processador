import sys, os, platform, re

def fazIncludeAspas(codigo):
    buffer = []                                                                             #Buffer vazio
    while codigo:                                                                           #Enquanto tem linha
        linha = codigo[0]                                                                   #Copia primeira linha
        codigo.pop(0)                                                                       #Remove primeira linha
        include = re.search("#include\s*\"[\d\w]*\.[ch]\"\s*\n", linha)                     #Expressão regular para verificar se tem include na linha
        if include and include.group() == linha:                                            #Se tiver e for valido
            nomeArquivo = re.search("(?<=\")[\d\w]*\.[ch](?=\")", include.group()).group()  #Pega nome do arquivo incluido
#Forma entre aspas	O pré-processador pesquisa por arquivos de inclusão nesta ordem:
#1) no mesmo diretório que o arquivo que contém a #include instrução.
#2) nos diretórios dos arquivos de inclusão abertos no momento, na ordem inversa em que foram abertos. A pesquisa começará no diretório do arquivo de inclusão pai e continuará para cima até os diretórios de qualquer arquivo de inclusão avô.
#3) ao longo do caminho especificado por cada /I opção de compilador.
#4) ao longo dos caminhos especificados pela variável de INCLUDE ambiente.
#verificar se arquivo existe
            #if True:#arquivoExiste()
            arquivo = open(nomeArquivo, 'r')                                                #Abre arquivo se existir na pasta
            #else:
            #    if platform.system() == "Windows":
            #        arquivo = open("#PASTA/"+nomeArquivo, 'r')#PASTA NO WINDOWS
            #    elif platform.system() == "Linux":
            #        arquivo = open("#PASTA/"+nomeArquivo, 'r')#PASTA NO LINUX
            #    else:
            #        exit()
            conteudo = arquivo.readlines()                                                  #Le conteudo
            arquivo.close()                                                                 #Fecha arquivo
            conteudo = fazIncludeAspas(conteudo)                                            #Inclui arquivos incluidos no arquivo incluido com """s
            conteudo = fazIncludeMQMQ(conteudo)                                            #Inclui arquivos incluidos no arquivo incluido com "<" e ">"
            for linhaConteudo in conteudo:                                                  #Copia pro buffer conteudo do include
                buffer.append(linhaConteudo)
        else:                                                                               #Se não tiver ou não for valido
            buffer.append(linha)                                                            #Mantém a linha
    return buffer                                                                           #Retorna codigo resultado

def fazIncludeMQMQ(codigo):
    buffer = []                                                                             #Buffer vazio
    while codigo:                                                                           #Enquanto tem linha
        linha = codigo[0]                                                                   #Copia primeira linha
        codigo.pop(0)                                                                       #Remove primeira linha
        include = re.search("#include\s*<[\d\w]*\.[ch]>\s*\n", linha)                     #Expressão regular para verificar se tem include na linha
        if include and include.group() == linha:                                            #Se tiver e for valido
            nomeArquivo = re.search("(?<=<)[\d\w]*\.[ch](?=>)", include.group()).group()  #Pega nome do arquivo incluido
#Forma de colchete angular	O pré-processador pesquisa por arquivos de inclusão nesta ordem:
#Colchete angular --> "<",">"
#1) ao longo do caminho especificado por cada /I opção de compilador.
#2) quando a compilação ocorre na linha de comando, ao longo dos caminhos especificados pela INCLUDE variável de ambiente.
#            arquivo = open(nomeArquivo, 'r') 
#            conteudo = arquivo.readlines()                                                  #Le conteudo
#            arquivo.close()                                                                 #Fecha arquivo
#            conteudo = fazIncludeAspas(conteudo)                                            #Inclui arquivos incluidos no arquivo incluido com """s
#            conteudo = fazIncludeMQMQ(conteudo)                                            #Inclui arquivos incluidos no arquivo incluido com "<" e ">"
#            for linhaConteudo in conteudo:                                                  #Copia pro buffer conteudo do include
#                buffer.append(linhaConteudo)
        else:                                                                               #Se não tiver ou não for valido
            buffer.append(linha)                                                            #Mantém a linha
    return buffer 
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
    #VALIDAR """s
    novaLinha = re.sub("//.*$", "\n", linha)      #Substitui comentario de linha por "" usando regex
    return novaLinha                                    #Retorna nova linha
def tiraTabulacao(linha):
    novaLinha = re.sub("^\s*", "", linha)
    return novaLinha
def tiraEspacos(linha):
    novaLinha = re.sub("\s*(?=[-+*\/<>=,&|!(){}\[\];])|(?<=[-+*\/<>=,&|!(){}\[\];])\s*", "", linha)
    return novaLinha
def tiraQuebras(linha):
    novaLinha = re.sub("\\n$", "", linha)
    return novaLinha
def preprocessa(buffer):#Manipulacao do buffer
#Para cada include com Aspas no arquivo, se o arquivo incluido existir e estiver na pasta, copia seu conteudo, se não estiver na pasta, procura em INCLUDE, se o arquivo não existir, mantém o erro de sintaxe.
    buffer = fazIncludeAspas(buffer)            #Includes ""
#LOGICA COLCHETES ANGULARES
    #buffer = fazIncludeMQMQ(buffer)            #Includes <> 
#LOGICA DEFINES
    #                                           #Defines
#Para cada linha, se a linha tem // valido(fora de "" validas), apaga conteudo até \n
    buffer = map(tiraComentarioLinha, buffer)   #Remove comentario do tipo "//" de cada linha
#Para cada linha, remove espaço antes
    buffer = map(tiraTabulacao, buffer)         #Remove tabulação de cada linha
#Para cada linha, remove espaços em volta de -+*\/<>=,&|!(){}[];
    buffer = map(tiraEspacos, buffer)
#Para cada linha, remove o ultimo "\n"
    buffer = map(tiraQuebras, buffer)           #Remove "/n" de cada linha, defines ja estarão resolvidos
#LOGICA REMOVER /**/
    #buffer = tiraComentarioParagrafo(buffer)   #Remove comentario do tipo "/*"
#LOGICA REMOVER " "s
    #                                           #Remove " "s
    return buffer                               #Retorna conteudo após manipulação

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
    codigo = arquivo.readlines()                        #Pega o conteudo do arquivo
    arquivo.close()                                     #Fecha o arquivo
    codigo = preprocessa(codigo)
    arquivo = open(nomeArquivo, 'w')    #Abre arquivo para escrita
    arquivo.writelines(codigo)          #Escreve o conteudo do arquivo
    arquivo.close()                     #Fecha o arquivo

#defines 
# "Sobre os defines, é importante considerar macros também".
# COMO ASSIM MACROS?????

#Forma entre aspas	O pré-processador pesquisa por arquivos de inclusão nesta ordem:
#1) no mesmo diretório que o arquivo que contém a #include instrução.
#2) nos diretórios dos arquivos de inclusão abertos no momento, na ordem inversa em que foram abertos. A pesquisa começará no diretório do arquivo de inclusão pai e continuará para cima até os diretórios de qualquer arquivo de inclusão avô.
#3) ao longo do caminho especificado por cada /I opção de compilador.
#4) ao longo dos caminhos especificados pela variável de INCLUDE ambiente.

#Forma de colchete angular	O pré-processador pesquisa por arquivos de inclusão nesta ordem:
#Colchete angular --> "<",">"
#1) ao longo do caminho especificado por cada /I opção de compilador.
#2) quando a compilação ocorre na linha de comando, ao longo dos caminhos especificados pela INCLUDE variável de ambiente.