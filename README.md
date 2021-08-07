# Pre-processador
## Trabalho 2 de Linguagens de programação

Este repositorio é a continuação de um pre-processador para C, um exercicio avaliado em Linguagens de Programação do curso de Ciência da Computação na UFF-PURO no periodo remoto de 2021-1.

### Requisitos:

Para desenvolver esse pre-processador estamos usando o compilador Mingw e desenvolvendo em Python 3.8.6. Nós estamos desenvolvendo em maquinas com windows, porém é previsto que o programa rode em qualquer distribuição Linux e MacOS.

O programa prevê que o compilador estara instalado em "C:" no windows, e em "/usr" nas distribuições Linux e MacOS

### Como utilizar?

Devem ser passados por parametro os arquivos C que serão pre-processados:

```
    py processa.py (Arquivo 1) [(Arquivo 2), ..., (Arquivo N)]
```

Os arquivos terão seus includes e defines resolvidos, comentarios, espaços e quebras de linha removidos.

### Passos para o pre-processamento:

* Mapear Diretivas
    1. Resolver Includes
    2. Resolver Defines
* Esconder strings;
* Remover comentarios;
* Remover espaços desnecessarios e quebras de linha.

### Problemas pendentes:

* Simplificar codigo;
* Erro loop infinito mascara de strings;
* Erro ao mascarar e desmascarar o seguinte conteudo: concat("#str1", "bbbbbb");
* Juntar funções de includes para definir o caracter na chamada;
* Refazer funções de resolução dos defines.

### Fontes e Utilidades:

Estamos implementando nosso pre-processador baseado nas regras de pre-processamento [deste site](https://www.cprogramming.com/tutorial/cpreprocessor.html)

Estamos testando nossas expressões regulares [neste site](https://regex101.com/)