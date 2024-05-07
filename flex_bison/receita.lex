%{
# include "receita.tab.h"
%}

IDENT  [a-zA-Z_][a-zA-Z0-9_]*
NUMBER [0-9]+
STRING \".*\"

%%

[ \t\n\r]
";"  { return SEMICOLON; }
"+"  { return PLUS; }
"-"  { return MINUS; }
"*"  { return STAR; }
"/"  { return SLASH; }
"("  { return LPAREN; }
")"  { return RPAREN; }
"{" { return LBRACE; }
"}" { return RBRACE; }
"==" { return EQ; }
"<"  { return LT; }
">"  { return GT; }
","  { return COMMA; }
"="  { return ASSIGN; }

receita { return RECEITA; }
g { return G; }
ml { return ML; }
tambem { return TAMBEM; }
ou { return OU; }
nao { return NAO; }
senao { return SENAO; }
mexer { return MEXER; }
enquanto { return ENQUANTO; }
pare { return PARE; }
de { return DE; }
picar { return PICAR; }
se { return SE; }
servir { return SERVIR; }
anotar { return ANOTAR; }

{IDENT} {
    return IDENT;
}

{NUMBER} {
    yylval = atoi(yytext);
    return NUMBER;
}

{STRING} {
    return STRING;
}

. { return yytext[0]; }

%%
