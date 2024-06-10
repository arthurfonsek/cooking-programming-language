%{
#include <stdio.h>

int yylex(void);
void yyerror(char *s);
extern FILE *yyin;
%}

%token PLUS MINUS STAR SLASH
%token LPAREN RPAREN SEMICOLON COMMA COLON
%token LBRACE RBRACE
%token IDENT
%token NUMBER STRING
%token EQ LT GT TAMBEM OU NAO
%token RECEITA G ML
%token MEXER ENQUANTO PARE DE PICAR SE SENAO
%token SERVIR ANOTAR ASSIGN

%%

program: RECEITA LBRACE block RBRACE

block:
    | statement SEMICOLON block

type: G | ML;

statement: IDENT COLON bool_expression type
    | IDENT ASSIGN bool_expression
    | MEXER ENQUANTO bool_expression COMMA block PARE DE MEXER
    | PICAR SE bool_expression COMMA block else PARE DE PICAR
    | SERVIR bool_expression
    | ANOTAR STRING IDENT
    ;

else:
    | SENAO COMMA block


bool_expression: bool_term
    | bool_expression OU bool_term
    ;

bool_term: rel_expression
    | bool_term TAMBEM rel_expression
    ;

rel_expression: expression
    | expression EQ expression
    | expression LT expression
    | expression GT expression
    ;

expression: term
    | expression PLUS term
    | expression MINUS term
    ;

term: factor
    | term STAR factor
    | term SLASH factor
    ;

factor: NUMBER
    | STRING
    | IDENT
    | LPAREN bool_expression RPAREN
    | MINUS factor
    | NAO factor
    ;

%%

int main(int argc, char *argv[]) {
    if (argc != 2) {
        fprintf(stderr, "Usage: %s <input_file>\n", argv[0]);
        return 1;
    }

    FILE *input_file = fopen(argv[1], "r");
    if (!input_file) {
        fprintf(stderr, "Error: could not open file %s\n", argv[1]);
        return 1;
    }

    yyin = input_file;

    int result = yyparse();

    fclose(input_file);

    if (result == 0) {
        printf("Validado!\n");
    }

    return 0;
}


void yyerror(char *s) {
    fprintf(stderr, "error: %s\n", s);
}