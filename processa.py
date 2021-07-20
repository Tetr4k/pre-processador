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

includesAspas = []
def listaIncludesAspas(buffer):
    def encontra(linha):
        include = re.search("^#include\s*\".*\.[ch]\"", linha)
        if include:
            nomeArquivo = re.search("(?<=\").*\.[ch](?=\")", include.group())
            if nomeArquivo and nomeArquivo not in includesAspas:
                includesAspas.append(nomeArquivo.group())
            linha = re.sub("^#include\s*\".*\.[ch]\"", "", linha)
        return linha
    return list(map(encontra, buffer))

includesAngulares = []
def listaIncludesAngulares(buffer):
    def encontra(linha):
        include = re.search("^#include\s*<.*\.[ch]>", linha)
        if include:
            nomeArquivo = re.search("(?<=<).*\.[ch](?=>)", include.group())
            if nomeArquivo and nomeArquivo not in includesAngulares:
                includesAngulares.append(nomeArquivo.group())
            linha = re.sub("^#include\s*<.*\.[ch]>", "", linha)
        return linha
    return list(map(encontra, buffer))

def resolveIncludesAspas(buffer):
    novoBuffer = []
    for include in includesAspas:
        includesAspas.remove(include)
        try:                                                                        #Abre arquivo se existir
            try:
                arquivo = open(include, 'r')                                    
            except:                                                                 #Se gerar erro tenta abrir do compilador
                arquivo = abreCompilador(include)
        except:
            print("Arquivo", include, "não podê ser encontrado.")
            continue
        conteudo = leArquivo(arquivo)                                               #Pega conteudo do arquivo com includes
        arquivo.close()                                                             #Fecha arquivo
        for linha in conteudo:
            print(linha)
            novoBuffer.append(linha)                                                     #Copia conteudo do include para o buffer
    novoBuffer.extend(buffer)
    return novoBuffer

def fazIncludeAspas(codigo):                                                                #Função para resolver includes com Aspas
    buffer = []                                                                             #Buffer vazio
    while codigo:
        linha = codigo[0]                                                                   #Faz uma copia da primeira linha)
        codigo.pop(0)                                                                       #Remove a primeira linha da lista
        include = re.search("#include\s*\"[\d\w]*\.[ch]\"\s*", linha)                     #Expressão regular para verificar se tem include na linha
        if include and include.group() == linha:                                            #Se tiver include na linha e for valido
            nomeArquivo = re.search("(?<=\")[\d\w]*\.[ch](?=\")", include.group()).group()  #Pega nome do arquivo incluido
            if not nomeArquivo in bufferIncludes:                                           #Se arquivo ainda não foi incluido
                bufferIncludes.append(nomeArquivo)                                          #Inclui arquivo na lista de arquivos incluidos
                try:
                    try:
                        arquivo = open(nomeArquivo, 'r')                                    #Abre arquivo se existir
                    except:                                                                 #Se gerar erro tenta abrir do compilador
                        arquivo = abreCompilador(nomeArquivo)
                except:
                    print("Arquivo", nomeArquivo, "não podê ser encontrado.")
                    continue
                conteudo = leArquivo(arquivo)                                               #Pega conteudo do arquivo com includes
                arquivo.close()                                                             #Fecha arquivo
                for linha in conteudo:
                    buffer.append(linha)                                                     #Copia conteudo do include para o buffer
        else:                                                                               #Se não tiver ou não for valido
            buffer.append(linha)                                                            #Mantém a linha
    return list(buffer)                                                                           #Retorna codigo resultado

def fazIncludeAngular(codigo):                                                              #Função para resolver includes com Colchetes Angulares
    buffer = []                                                                             #Buffer vazio
    while codigo:                                                                           #Enquanto existem linhas não processadas
        linha = codigo[0]                                                                   #Faz uma copia da primeira linha
        codigo.pop(0)                                                                       #Remove primeira linha da lista
        include = re.search("#include\s*<[\d\w]*\.[ch]>\s*", linha)                         #Expressão regular para verificar se tem include na linha
        if include and include.group() == linha:                                            #Se tiver include na linha e for valido
            nomeArquivo = re.search("(?<=<)[\d\w]*\.[ch](?=>)", include.group()).group()    #Pega nome do arquivo incluido
            if nomeArquivo not in bufferIncludes:                                           #Se arquivo ainda não foi incluido
                bufferIncludes.append(nomeArquivo)                                          #Inclui arquivo na lista de arquivos incluidos
                try:
                    arquivo = abreCompilador(nomeArquivo)    
                except:
                    print("Arquivo", nomeArquivo, "não podê ser encontrado.")
                    continue
                conteudo = leArquivo(arquivo)
                arquivo.close()                                                             #Fecha arquivo
                for linha in conteudo:
                    buffer.append(linha)                                                    #Copia conteudo do include para o buffer
        else:                                                                               #Se não tiver ou não for valido
            buffer.append(linha)                                                            #Mantém a linha
    return list(buffer)                                                                           #Retorna codigo resultado

def trataDefine(codigo):
    #Ver quais são os defines
    #jogar instruções de define em um vetor

    #Para cada instrução no vetor
    #percorre o codigo substituindo
    defines = []
    buffer = []
    for linha in codigo:
        define = re.search("#define\s*.*\s*(?=(\n|//|/*))", linha)                                 #Expressão regular para verificar se tem define na linha

        #if define:
        #    linha = re.sub("#define\s*.*\s*(?=(\n|//|/*))", "", linha)
        if define and define.group() == linha:                                                  #Se tiver define na linha e for valido
            conteudoDefine = re.search("(?<=\s).*$", define.group())                             #Pega o conteúdo do define (nome e valor)
            nomeDefine = re.search(".*(?=\s)", conteudoDefine.group())                           #Pega o nome do define
            if nomeDefine and "(" in nomeDefine.group() and ")" in nomeDefine.group():                            #Se define for Macro
                valorDefine = re.search("(?<=\)\s).*", conteudoDefine.group())
                if "{" in valorDefine.group() and "}" in valorDefine.group():                                          #Se tiver chaves
                    valorFuncDefine = re.search("(?<={).*(?=})", valorDefine.group())           #Tira chaves
                else:
                    valorFuncDefine = valorDefine
                nomeDefineSemParametro = re.search(".*(?=\()", nomeDefine.group())                      #Pega apenas o nome da função sem os parametros
                parametros = re.search("(?<=\().*(?=\))", conteudoDefine.group())                          #Pega apenas a parte de dentro dos parênteses da função define
                parametros = parametros.group().replace(" ", "")
                parametros = parametros.split(",")
                defines.append([nomeDefineSemParametro.group(), valorFuncDefine.group(), parametros])    
            else:                                                                               #Se não for função (não tem parênteses)
                valorDefine = re.search("(?<=\s).*", conteudoDefine.group())                             #Pega o valor do define
                defines.append([nomeDefine.group(), valorDefine.group()])
    while codigo:
        linha = codigo[0]
        codigo.pop(0)
        for define in defines:
            nome = re.search("(?<=[^a-zA-Z0-9])"+define[0]+"(?=[^a-zA-Z0-9])", linha)
            if nome:
                if len(define) == 2:
                    linha = linha.replace(define[0], define[1])
                elif len(define) == 3:
                    valorParametros = re.search("(?<=[\W\D])"+define[0]+"\(.*,.*\)", linha)
                    valorParametros = re.search("(?<=\().*(?=\))", valorParametros.group())
                    valorParametros = valorParametros.group().replace(" ", "")
                    valorParametros = valorParametros.split(",")
                    funcaoComValores = define[1]
                    for i in range(len(valorParametros)):
                        funcaoComValores = funcaoComValores.replace(define[2][i], valorParametros[i])
                    linha = linha.replace(re.search(define[0]+"\(.*,.*\)", linha).group(), funcaoComValores)
                break
        if not "define" in linha:
            buffer.append(linha)
    return buffer                                                                          #retorna o código com as alterações

def preprocessa(buffer):    #Função para pre-processar o codigo
    buffer = listaIncludesAspas(buffer)
    print(includesAspas)
    buffer = listaIncludesAngulares(buffer)
    print(includesAngulares)

    '''volta com \n mas no arquivo'''
    bufferStrings = []
    def tiraStrings(linha):
        string = re.search("\".*\"", linha)
        if string:
            bufferStrings.append(string.group().replace("\\", "\\\\"))
        return re.sub("\".*\"", "#str"+str(len(bufferStrings)-1), linha)
    buffer = list(map(tiraStrings, buffer))

    def tiraComentarioLinha(linha):     #Funcao para remover comentarios de linha
        #Substitui comentario de linha por "" usando regex e retorna
        return re.sub("//.*$", "\n", linha)
    #Para cada linha, se a linha tem // valido(fora de "" validas), apaga conteudo até \n
    buffer = list(map(tiraComentarioLinha, buffer))   #Remove comentario do tipo "//" de cada linha

    '''Para cada linha do código, se a linha contem um define, caso o define seja uma função, irá remover as chaves, caso tenha, e depois irá percorrer o código novamente.
    Se Achar alguma ocorrência do define no código, irá pegar a expressão, substituir os valores nas variáveis, e então substituir a chamada do define pela expressão.
    Depois, adicionará a linha em um buffer, que posteriormente será retornado.
    Caso não seja uma função, apenas substituirá o valor onde houver a a chamada. Depois, adicionará a linha alterada no buffer.
    Após percorrer todo o código, retornará o buffer'''

    buffer = trataDefine(buffer)                       #Trata os Defines

    def tiraEspacos(linha):     #Funcao para remover espaços não uteis
        #Substitui espaços não uteis por "" usando regex e retorna
        return re.sub("\s+(?=[-+*\/<>=,&|!(){}\[\];:])|(?<=[-+*\/<>=,&|!(){}\[\];:])\s+", "\n", linha)
    #Para cada linha, remove espaços em volta de caracteres especiais
    #buffer = list(map(tiraEspacos, buffer))

    def tiraTabulacoes(linha):
        return re.sub("\t", "\n", linha)
    #Para cada linha, remove tabulações
    buffer = list(map(tiraTabulacoes, buffer))
    
    def tiraComentarioParagrafo(linha): #Funcao para remover comentarios de paragrafo
        return re.sub("/\*.*?\*/", "", linha)                                                         #Substitui comentario de paragrafo por "" usando regex e retorna
    #'''LOGICA REMOVER /**/'''
    #buffer = tiraComentarioParagrafo(''.join(buffer))  #Remove comentario do tipo "/*"
    
    def botaStrings(linha):
        string = re.search("(?<=#str)\d*", linha)
        if string:
            return re.sub("#str\d*", bufferStrings[int(string.group())], linha)
        return linha
    buffer = list(map(botaStrings, buffer))

    #Para cada include com Aspas no arquivo, se o arquivo incluido existir e estiver na pasta, copia seu conteudo, se não estiver na pasta, procura no compilador, se o arquivo não existir, passa para o proximo.
    #buffer = fazIncludeAspas(buffer)            #Includes ""

    #Para cada include com Colchetes angulares no arquivo, se o arquivo incluido existir e estiver no compilador, copia seu conteudo, se o arquivo não existir, passa para o proximo.
    #buffer = fazIncludeAngular(buffer)          #Includes <> 

    def tiraQuebras(linha):     #Função para remover quebras de linha
        #Substitui quebras de linha por "" usando regex e retorna
        return re.sub("\\n$", "", linha)
    #Para cada linha, remove o ultimo "\n"
    #buffer = list(map(tiraQuebras, buffer))           #Remove "/n" de cada linha, defines ja estarão resolvidos
    buffer = resolveIncludesAspas(buffer)
    includesAspas.clear()
    includesAngulares.clear()
    bufferStrings.clear()                       #Limpa buffer de strings
    return buffer                               #Retorna conteudo após manipulação

os.system("mkdir backup")                               #Cria pasta de backup
nomesArquivos = sys.argv                                #Acessa parametros passados
nomesArquivos.pop(0)                                    #Remove primeiro parametro("processa.py")

for nomeArquivo in nomesArquivos:                       #Faz o pre-processamento para cada arquivo passado por parametro. 
    bufferIncludes.clear()                          #Limpa buffer de includes
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