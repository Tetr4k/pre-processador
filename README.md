# Pre-processador
## Trabalho 2 de Linguagens de programação

### O que é esse repositorio?
Esse repositorio é usado para controle de versão de uma implementação do exercicio 6 do arquivo Trabalhos.pdf, um trabalho avaliado de Linguagens de Programação do curso de Ciência da Computação na UFF-PURO.
O programa implementado trata-se de um pre-processador para um programa em C/C++.

### Requisitos:

Para desenvolver esse pre-processador estamos usando o compilador Mingw e desenvolvendo em Python 3.8.6. Nós estamos desenvolvendo em maquinas com windows, porém é previsto que o programa rode em qualquer distribuição linux e MacOS.

### Como utilizar?

Devem ser passados por parametro os arquivos C/C++ que serão pre-processados:

```
    py processa.py (Arquivo 1) [(Arquivo 2), ..., (Arquivo N)]
```

Os arquivos terão seus includes e defines resolvidos, comentarios, espaços e quebras de linha removidos.

### Passos:

* Cria mascara sobre strings;
* Remove comentarios "//";
* Remove comentarios "/**/";
* Resolve defines;
* Resolve defines condicionais;
* Remove Espaços não uteis;
* Remove Tabulações;
* Resolve mascara sobre strings;
* Resolve includes de Aspas;
* Resolve includes de Colchetes angulares;
* Remove quebras de linha.

### Erros pendentes:

* Tirar temporariamente as strings sem erro na volta.
* Resolver erro com "tiraComentarioParagrafo()".
* Resolver defines e defines condicionais.

### Fontes e Utilidades:

Estamos implementando nosso pre-processador baseado nas regras de pre-processamento do site:

[Site Cprogramming](https://www.cprogramming.com/tutorial/cpreprocessor.html)

Estamos ordenando as resoluções dos includes a partir das informações cedidas na documentação da [Microsoft](https://docs.microsoft.com/pt-br/cpp/preprocessor/hash-include-directive-c-cpp?view=msvc-160)

Estamos testando nossas expressões regulares no site [Regex101](https://regex101.com/)

O arquivo PDF desse trabalho esta disponivel no site do professor [Bazilio](http://www2.ic.uff.br/~bazilio/cursos/lp/material/Trabalhos.pdf)