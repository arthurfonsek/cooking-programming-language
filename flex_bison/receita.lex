%{
#include "receita.tab.h"
%}

%option noyywrap

%%

"receita"           { return RECEITA; }
"{"                 { return LBRACE; }
"}"                 { return RBRACE; }
":"                 { return COLON; }
"servir"            { return SERVIR; }
"anotar"            { return ANOTAR; }
"mexer enquanto"    { return MEXERENQUANTO; }
"pare de mexer"     { return PAREDEMEXER; }
"picar se"          { return PICARSE; }
"senao"             { return SENAO; }
"pare de picar"     { return PAREDEPICAR; }
"tambem"            { return TAMBEM; }
"ou"                { return OU; }
"=="                { return EQUAL; }
">"                 { return GREATER; }
"<"                 { return LESS; }
"g"                 { return G; }
"ml"                { return ML; }
"nao"               { return NAO; }
"-"                 { return MINUS; }
"\\["               { return LBRACKET; }
"\\]"               { return RBRACKET; }
"+"                 { return PLUS; }
"*"                 { return MULTIPLY; }
"/"                 { return DIVIDE; }
[0-9]+              { yylval.intval = atoi(yytext); return INTEGER; }
\"(\\.|[^\"])*\"    { yylval.strval = strdup(yytext); return STRING; }
[a-zA-Z_][a-zA-Z0-9_]* { yylval.strval = strdup(yytext); return IDENTIFIER; }
[ \t\n]+            { /* ignore whitespace */ }
.                   { /* ignore any other character */ }

%%

int yywrap() {
    return 1;
}
