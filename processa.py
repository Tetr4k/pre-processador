import sys, os, platform, re

sistema = platform.system()                             #Identifica qual é o sistema

if not sistema == ("Windows" or "Linux" or "Darwin"):   #Valida sistema
    print("O sistema", sistema, "não é reconhecido.")
    exit()

'''
def fazIncludes(buffer):                #Função para fazer todos os includes
    buffer = listaIncludeAspas(buffer)
    buffer = listaIncludeAngular(buffer)
    buffer = resolveIncludeAspas(buffer)
    buffer = resolveIncludeAngular(buffer)
    return buffer

def leArquivo(arquivo):                 #Função para ler conteudo do arquivo e tratar os includes dele
    conteudoArquivo = arquivo.readlines()  #Le conteudo do arquivo
    return fazIncludes(conteudoArquivo)    #Faz includes do arquivo e retorna conteudo

def abreCompilador(nomeArquivo):        #Função para abrir arquivo na pasta do Mingw
    if sistema == "Windows":
        return open("c:\\mingw\\include\\"+nomeArquivo, 'r')    #Se o sistema for Windows procura a partir de C:
    else:
        return open("\\usr\\include\\"+nomeArquivo, 'r')        #Se o sistema for Linux/MAC procura a partir da raiz          

includesAspas = []      #Lista de includes de Aspas
def listaIncludeAspas(buffer):          #Função para gerar uma lista de includes com aspas a partir do arquivo.
    def encontra(linha):                #Função para encontrar os includes no arquivo. Usada através do map.
        include = re.search("^\s*#\s*include\s*\".*\.[ch]\"", linha)                  #Procura por um include
        if include:                                                             #Se encontrou
            nomeArquivo = re.search("(?<=\").*\.[ch](?=\")", include.group())   #Busca o arquivo a ser incluido
            if nomeArquivo.group() not in includesAspas:                        #Verifica se ja esta listado para ser incluido
                includesAspas.append(nomeArquivo.group())                       #Caso não esteja listado para ser incluido, adiciona na lista
            linha = re.sub("^\s*#\s*include\s*\".*\.[ch]\"", "", linha)               #Remove o include da linha
        return linha                                                            #Retorna linha modificada ou não modificada
    return list(map(encontra, buffer))                                          #Aplica a função encontra para cada linhado buffer e retorna

includesAngulares = []  #Lista de includes de Colchetes Angulares
def listaIncludeAngular(buffer):        #Função para gerar uma lista de includes com aspas a partir do arquivo.
    def encontra(linha):                #Função para encontrar os includes no arquivo. Usada através do map.
        include = re.search("^\s*#\s*include\s*<.*\.[ch]>", linha)                    #Procura por um include
        if include:                                                             #Se encontrou
            nomeArquivo = re.search("(?<=<).*\.[ch](?=>)", include.group())     #Busca o arquivo a ser incluido
            if nomeArquivo.group() not in includesAngulares:                    #Verifica se ja esta listado para ser incluido
                includesAngulares.append(nomeArquivo.group())                   #Caso não esteja listado para ser incluido, adiciona na lista
            linha = re.sub("^\s*#\s*include\s*<.*\.[ch]>", "", linha)                 #Remove o include da linha
        return linha                                                            #Retorna linha modificada ou não modificada
    return list(map(encontra, buffer))                                          #Aplica a função encontra para cada linhado buffer e retorna

incluidos = []#Lista de arquivos ja incluidos
def resolveIncludeAspas(buffer):        #Função para resolver includes com Aspas
    novoBuffer = []                                                     #Lista com novas linhas
    for include in includesAspas:                                       #Para cada include de includesAspas
        if include not in incluidos:                                    #Caso o include não tenha sido incluido ainda
            incluidos.append(include)                                   #Adiciona include a lista de includes ja incluidos
            includesAspas.remove(include)                               #Remove include da lista de includesAspas
            try:                                                                        
                try:
                    arquivo = open(include, 'r')                        #Abre arquivo se existir
                except:                                                                
                    arquivo = abreCompilador(include)                   #Se gerar erro tenta abrir do compilador
            except:
                print("Arquivo", include, "não podê ser encontrado.")
                continue
            conteudo = leArquivo(arquivo)                               #Pega conteudo do arquivo com includes
            arquivo.close()                                             #Fecha arquivo
            for linha in conteudo:                                      #Para cada linha do arquivo
                novoBuffer.append(linha)                                #Copia conteudo do include para o buffer
    novoBuffer.extend(buffer)                                           #Adiciona o conteudo no inicio do codigo
    return novoBuffer                                                   #Retorna o novo codigo

def resolveIncludeAngular(buffer):      #Função para resolver includes com Colchetes angulares
    novoBuffer = []                                                     #Lista com novas linhas
    for include in includesAngulares:                                   #Para cada include de includesAngulares
        if include not in incluidos:                                    #Caso o include não tenha sido incluido ainda
            incluidos.append(include)                                   #Adiciona include a lista de includes ja incluidos
            includesAngulares.remove(include)                           #Remove include da lista de includesAngulares
            try:
                arquivo = abreCompilador(include)                       #Abre arquivo se existir
            except:
                print("Arquivo", include, "não podê ser encontrado.")
                continue
            conteudo = leArquivo(arquivo)                               #Pega conteudo do arquivo com includes
            arquivo.close()                                             #Fecha arquivo
            for linha in conteudo:                                      #Para cada linha do arquivo
                novoBuffer.append(linha)                                #Copia conteudo do include para o buffer
    novoBuffer.extend(buffer)                                           #Adiciona o conteudo no inicio do codigo
    return novoBuffer                                                   #Retorna o novo codigo
'''

'''
    

    def tiraComentarioLinha(linha):     #Funcao para remover comentarios de linha
        return re.sub("//.*$", "\n", linha) #Substitui comentario de linha por "" usando regex e retorna
    buffer = list(map(tiraComentarioLinha, buffer))   #Para cada linha, se a linha tem // valido(fora de "" validas), apaga conteudo até \n

    global apagarLinha
    apagarLinha = False
    def tiraComentarioParagrafo(linha): #Funcao para remover comentarios de paragrafo
        global apagarLinha
        if apagarLinha:
            fimComentario = re.search("^.*\*/", linha)
            if fimComentario:
                linha = re.sub("^.*\*/", "", linha)
                apagarLinha = False
            else:
                linha = re.sub(".*", "", linha)
        else:
            inicioComentario = re.search("/\*.*$", linha)
            if inicioComentario:
                fimComentario = re.search("^.*\*/", inicioComentario.group())
                if fimComentario:
                    linha = re.sub("/\*.*\*/", "", linha)
                else:
                    apagarLinha = True
                    linha = re.sub("/\*.*$", "", linha)
        return linha
    buffer = list(map(tiraComentarioParagrafo, buffer))  #Remove comentario do tipo "/*"

    def tiraEspacos(linha):     #Funcao para remover espaços não uteis
        return re.sub("\s+(?=[-+*\/<>=,&|!(){}\[\];:])|(?<=[-+*\/<>=,&|!(){}\[\];:])\s+(?!=\\n)", "", linha)#Substitui espaços não uteis por "" usando regex e retorna
    buffer = list(map(tiraEspacos, buffer))#Para cada linha, remove espaços em volta de caracteres especiais

    def tiraTabulacoes(linha):
        return re.sub("\t", "\n", linha)
    buffer = list(map(tiraTabulacoes, buffer))#Para cada linha, remove tabulações
    
    def tiraQuebras(linha):     #Função para remover quebras de linha
        #Substitui quebras de linha por "" usando regex e retorna
        return re.sub("\\n", "", linha)
    buffer = list(map(tiraQuebras, buffer))           #Para cada linha, remove o ultimo "\n"

    def desmascaraStrings(linha):
        string = re.search("(?<=#str)\d*", linha)
        if string:
            return re.sub("#str\d*", bufferStrings[int(string.group())], linha)
        return linha
    buffer = list(map(desmascaraStrings, buffer))
'''

def mascaraStrings(linha): #Função para camuflar strings e não quebrar outras funções
    strings = []
    resultado = re.search("\"([^\"\\\n]|\\.)*\"", linha)
    while resultado:
        strings.append(resultado.group().replace("\\", "\\\\"))
        linha = re.sub(resultado.group(), "#str"+str(len(strings)-1), linha)
        resultado = re.search("\"([^\"\\\n]|\\.)*\"", linha)
    return linha, strings

def processaLinha(linha):
    linha, strings = mascaraStrings(linha)

    
    #linha= desmascaraStrings(linha, strings)
    return linha


def preprocessa(buffer):                #Função para pre-processar o codigo
    #buffer, diretivas = mapeiaDiretivas(buffer)    #Percorrer arquivo mapeando diretivas
    #buffer = resolveIncludes(buffer, diretivas)    #Resolver Includes
    buffer = list(map(processaLinha, buffer))      #Percorrer arquivo resolvendo, para cada linha, os defines, comentarios e quebras de espaço
    return buffer                               #Retorna conteudo após manipulação

os.system("mkdir backup")                               #Cria pasta de backup
nomesArquivos = sys.argv                                #Acessa parametros passados
nomesArquivos.pop(0)                                    #Remove primeiro parametro("processa.py")

for nomeArquivo in nomesArquivos:                       #Faz o pre-processamento para caa darquivo passado por parametro.
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
        arquivo.writelines(codigo)                      #Escreve o conteudo no arquivo
        arquivo.close()                                 #Fecha o arquivo
    except:
        continue                                        #Se gerar erro, passa para o proximo arquivo