%{
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

void yyerror(const char *s);
int yylex(void);
%}

%union {
    int intval;
    char *strval;
}

%token <strval> IDENTIFIER STRING
%token <intval> INTEGER
%token RECEITA LBRACE RBRACE COLON SERVIR ANOTAR MEXERENQUANTO PAREDEMEXER PICARSE SENAO PAREDEPICAR TAMBEM OU EQUAL GREATER LESS G ML NAO MINUS LBRACKET RBRACKET PLUS MULTIPLY DIVIDE

%type <intval> program block statement assignment print input while if boolexpression boolterm relexpression expression term factor type unary_op

%%

program: RECEITA LBRACE block RBRACE
    ;

block: 
    | block statement '\n'
    ;

statement: 
      assignment
    | print
    | input
    | while
    | if
    ;

assignment: IDENTIFIER COLON boolexpression type
    ;

print: SERVIR boolexpression
    ;

input: ANOTAR STRING IDENTIFIER
    ;

while: MEXERENQUANTO boolexpression ',' '\n' block PAREDEMEXER
    ;

if: PICARSE boolexpression ',' '\n' block
    | PICARSE boolexpression ',' '\n' block SENAO ',' '\n' block PAREDEPICAR
    ;

boolexpression: boolterm
    | boolexpression OU boolterm
    ;

boolterm: relexpression
    | boolterm TAMBEM relexpression
    ;

relexpression: expression
    | expression GREATER expression
    | expression LESS expression
    | expression EQUAL expression
    ;

expression: term
    | expression PLUS term
    | expression MINUS term
    ;

term: factor
    | term MULTIPLY factor
    | term DIVIDE factor
    ;

factor: INTEGER
    | IDENTIFIER
    | LBRACKET boolexpression RBRACKET
    | unary_op factor
    ;

type: G
    | ML
    ;

unary_op: MINUS
    | NAO
    ;

%%

void yyerror(const char *s) {
    fprintf(stderr, "Error: %s\n", s);
}

int main(void) {
    return yyparse();
}
