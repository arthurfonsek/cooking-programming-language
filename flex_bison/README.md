# Linguagem de Programação: Sabora

Bem-vindo ao Sabora, uma linguagem de programação única que combina a precisão da programação com a arte da culinária. Com Sabora, você pode expressar algoritmos complexos, estruturas de dados e lógica de programação usando a linguagem das receitas culinárias.

* Sintaxe Intuitiva: Escreva código como se estivesse seguindo uma receita de culinária. Declarações, loops e condicionais são traduzidos para passos claros e simples.
* Ingredientes e Utensílios: Utilize ingredientes e utensílios como variáveis e estruturas de dados. Atribua valores, faça operações e manipule dados de uma forma familiar e divertida!

### Exemplo de código

*Python*

```Python
    args = 20
    contador = 0
    palavra = 'Arthur'
  
    while ((args > 0) or (contador < 20)):
        contador += 1
        args -= 1

    if contador == 5:
        print(palavra)
        contador = 27

    if contador == 3:
        print('Python')
        palavra = 'Python'
```

*Sabora*

```Sabora
    receita 

    20 g args
    0 g contador
    Arthur ml palavra
  
    mexer enquanto ((args > 0) ou (contador < 20)),
        incrementar contador
        decrementar argumento1

    picar se contador == 5,
        servir palavra
        0 g contador
    pare de picar

    picar se contador == 3,
        servir 'Python'
    pare de picar

    pare de mexer
```

### Gramática

#### EBNF

```ebnf
PROGRAM = "receita", "{", BLOCK, "}";

BLOCK = { STATEMENT, ";"} ;

STATEMENT = ( ASSIGNMENT  | DECLARATION | PRINT | INPUT | WHILE | IF ), "\n" ;

DECLARATION = IDENTIFIER, TYPE;

ASSIGNMENT = IDENTIFIER, TYPE,  EXPRESSION ;

EXPRESSION = TERM, { ("+" | "-"), TERM } ;

TERM = FACTOR, { ("*" | "/"), FACTOR } ;

FACTOR = INTEGER | IDENTIFIER | "(" , EXPRESSION , ")" | UNARY_OP, FACTOR ;

PRINT = "servir", EXPRESSION;

INPUT = "anotar", '"', STRING, '"', IDENTIFIER;

WHILE = "mexer enquanto", EXPRESSION, ",",  "\n", { STATEMENT },"\n", "pare de mexer" ;

IF = "picar se", EXPRESSION, ",", "\n", { STATEMENT }, "\n","pare de picar" ;

TYPE = "g" | "ml";

LOGIC_OP = "tambem" | "ou" | "nao" ;

COMPARE_OP = ">" | "<" | "==" ;

INTEGER = DIGIT, { DIGIT } ;

IDENTIFIER = LETTER, { LETTER | DIGIT | "_" } ;

UNARY_OP = "-" | "nao";

DIGIT = "0" | "1" | "2" | "3" | "4" | "5" | "6" | "7" | "8" | "9" ;

LETTER = "A..Z" | "a..z" ;

STRING = "CARACTERE" | "SEQUENCIAESCAPE";

CARACTERE = ? todos os caracteres exceto: ' " ' (aspas duplas) e  ' \ ' (contrabarra)  ? ;

SEQUENCIAESCAPE = "\",  ( "'" | '\' | 'n' | 't' | 'r' | 'b' | 'f' );
```

e o seu diagrama pode ser visto:

![EBNF](EBNF/EBNF.png)
