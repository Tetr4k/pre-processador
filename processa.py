import sys, os, platform, re

bufferIncludes = []                                     #Lista de arquivos incluidos
sistema = platform.system()                             #Informa qual o sistema
if not sistema == ("Windows" or "Linux" or "Darwin"):   #Valida sistema
    print("O sistema", sistema, "não é reconhecido.")
    exit()

def leArquivo(arquivo):                                     #Função para ler conteudo do arquivo e tratar os includes dele
    conteudoArquivo = arquivo.readlines()                   #Le conteudo
    conteudoPreprocessado = preprocessa(conteudoArquivo)    #Pre-processa conteudo
    return conteudoPreprocessado                            #Retorna conteudo tratado

def abreCompilador(nomeArquivo):
    if sistema == "Windows":
        return open("c:\\mingw\\include\\"+nomeArquivo, 'r')         #Se o sistema for Windows procura a partir de C:
    else:
        return open("\\usr\\include\\"+nomeArquivo, 'r')             #Se o sistema for Linux/MAC procura a partir da raiz          

def fazIncludeAspas(codigo):                                                                #Função para resolver includes com Aspas
    buffer = []                                                                             #Buffer vazio
    while codigo:                                                                           #Enquanto existem linhas não processadas
        linha = codigo[0]                                                                   #Faz uma copia da primeira linha
        codigo.pop(0)                                                                       #Remove a primeira linha da lista
        include = re.search("#include\s*\"[\d\w]*\.[ch]\"\s*\n", linha)                     #Expressão regular para verificar se tem include na linha
        if include and include.group() == linha:                                            #Se tiver include na linha e for valido
            nomeArquivo = re.search("(?<=\")[\d\w]*\.[ch](?=\")", include.group()).group()  #Pega nome do arquivo incluido
            if not nomeArquivo in bufferIncludes:                                           #Se arquivo ainda não foi incluido
                bufferIncludes.append(nomeArquivo)                                          #Inclui arquivo na lista de arquivos incluidos
                try:
                    try:
                        arquivo = open(nomeArquivo, 'r')                                        #Abre arquivo se existir
                    except:                                                                     #Se gerar erro tenta abrir do compilador
                        if sistema == "Windows":
                            arquivo = open("c:\\mingw\\include\\"+nomeArquivo, 'r')             #Se o sistema for Windows procura a partir de C:
                        else:
                            arquivo = open("\\usr\\include\\"+nomeArquivo, 'r')                 #Se o sistema for Linux/MAC procura a partir da raiz
                except:
                    buffer.append(linha)                                                    #Mantém linha caso arquivo não seja encontrado
                    continue
                conteudo = leArquivo(arquivo)                                               #Pega conteudo do arquivo com includes
                arquivo.close()                                                             #Fecha arquivo
                for linhaConteudo in conteudo:                                              #Copia conteudo do include para o buffer
                    buffer.append(linhaConteudo)
        else:                                                                               #Se não tiver ou não for valido
            buffer.append(linha)                                                            #Mantém a linha
    return buffer                                                                           #Retorna codigo resultado

def fazIncludeAngular(codigo):      #Função para resolver includes com Colchetes Angulares
    buffer = []                                                                             #Buffer vazio
    while codigo:                                                                           #Enquanto existem linhas não processadas
        linha = codigo[0]                                                                   #Faz uma copia da primeira linha
        codigo.pop(0)                                                                       #Remove primeira linha da lista
        include = re.search("#include\s*<[\d\w]*\.[ch]>\s*\n", linha)                       #Expressão regular para verificar se tem include na linha
        if include and include.group() == linha:                                            #Se tiver include na linha e for valido
            nomeArquivo = re.search("(?<=<)[\d\w]*\.[ch](?=>)", include.group()).group()    #Pega nome do arquivo incluido
            if not nomeArquivo in bufferIncludes:                                           #Se arquivo ainda não foi incluido
                bufferIncludes.append(nomeArquivo)                                          #Inclui arquivo na lista de arquivos incluidos
                try:
                    if sistema == "Windows":
                        arquivo = open("c:\\mingw\\include\\"+nomeArquivo, 'r')                 #Se o sistema for Windows procura a partir de C:
                    else:
                        arquivo = open("\\usr\\include\\"+nomeArquivo, 'r')                     #Se o sistema for Linux/MAC procura a partir da raiz
                except:
                    buffer.append(linha)                                                    #Mantém linha caso arquivo não seja encontrado
                    continue
                conteudo = leArquivo(arquivo)
                arquivo.close()                                                             #Fecha arquivo
                for linhaConteudo in conteudo:                                              #Copia pro buffer conteudo do include
                    buffer.append(linhaConteudo)
        else:                                                                               #Se não tiver ou não for valido
            buffer.append(linha)                                                            #Mantém a linha
    return buffer                                                                           #Retorna codigo resultado

def tiraComentarioLinha(linha):     #Funcao para remover comentarios de linha
    '''tem problema com """s -> VALIDAR """s'''
    return re.sub("//.*$", "\n", linha)                                                             #Substitui comentario de linha por "" usando regex e retorna

def tiraComentarioParagrafo(linha): #Funcao para remover comentarios de paragrafo
    '''tem problema com """s -> VALIDAR """s'''
    procura = re.search("\/\*.*?\*\/", linha)
    if procura:
        print(procura)
    return re.sub("\/\*.*?\*\/", "", linha)                                                         #Substitui comentario de paragrafo por "" usando regex e retorna

def tiraEspacos(linha):             #Funcao para remover espaços não uteis
    '''tem problema com """s -> validar """s'''
    return re.sub("\s*(?=[-+*\/<>=,&|!(){}\[\];])|(?<=[-+*\/<>=,&|!(){}\[\];])\s*", "", linha) #Substitui espaços não uteis por "" usando regex e retorna

def tiraQuebras(linha):             #Função para remover quebras de linha
    return re.sub("\\n$", "", linha)                                                                #Substitui quebras de linha por "" usando regex e retorna

def preprocessa(buffer):            #Função para pre-processar o codigo
#Para cada include com Aspas no arquivo, se o arquivo incluido existir e estiver na pasta, copia seu conteudo, se não estiver na pasta, procura no compilador, se o arquivo não existir, mantém o erro de sintaxe.
    buffer = fazIncludeAspas(buffer)            #Includes ""

#Para cada include com Colchetes angulares no arquivo, se o arquivo incluido existir e estiver no compilador, copia seu conteudo, se o arquivo não existir, mantém o erro de sintaxe.
    buffer = fazIncludeAngular(buffer)          #Includes <> 
    
    '''LOGICA DEFINES'''
    #                                           #Defines

    '''Tira do \n até o // atras'''   
#Para cada linha, se a linha tem // valido(fora de "" validas), apaga conteudo até \n
    buffer = map(tiraComentarioLinha, buffer)   #Remove comentario do tipo "//" de cada linha

#Para cada linha, remove o ultimo "\n"
    buffer = map(tiraQuebras, buffer)           #Remove "/n" de cada linha, defines ja estarão resolvidos

#Para cada linha, remove espaços em volta de -+*\/<>=,&|!(){}[]
    buffer = map(tiraEspacos, buffer)
    
    '''LOGICA REMOVER /**/'''
    #buffer = map(tiraComentarioParagrafo, buffer)   #Remove comentario do tipo "/*"
    
    bufferIncludes.clear()                      #Limpa buffer de includes
    return buffer                               #Retorna conteudo após manipulação

os.system("mkdir backup")                               #Cria pasta de backup
nomesArquivos = sys.argv                                #Acessa parametros passados
nomesArquivos.pop(0)                                    #Remove primeiro parametro("processa.py")

for nomeArquivo in nomesArquivos:                       #Faz o pre-processamento para cada arquivo passado por parametro. 
    
    if sistema == "Windows":
        os.system("copy "+nomeArquivo+" backup")        #Faz Backup do arquivo em Windows
    else:
        os.system("cp "+nomeArquivo+" backup")          #Faz Backup do arquivo em Linux

    try:
        arquivo = open(nomeArquivo, 'r')                #Abre arquivo para leitura
        codigo = arquivo.readlines()                    #Pega o conteudo do arquivo
        arquivo.close()                                 #Fecha o arquivo
        codigo = preprocessa(codigo)                    #Faz o pre-processa do codigo
        arquivo = open(nomeArquivo, 'w')                #Abre arquivo para escrita
        arquivo.writelines(codigo)                      #Escreve o conteudo do arquivo
        arquivo.close()                                 #Fecha o arquivo
    except:
        continue                                        #Se gerar erro, passa para o proximo arquivo