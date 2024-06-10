all: receita

receita: lex.yy.o receita.tab.o
    gcc -o receita lex.yy.o receita.tab.o -ll

lex.yy.o: lex.yy.c receita.tab.h
    gcc -c lex.yy.c

receita.tab.o: receita.tab.c
    gcc -c receita.tab.c

lex.yy.c: receita.lex receita.tab.h
    flex receita.lex

receita.tab.c receita.tab.h: receita.y
    bison -d receita.y

clean:
    rm -f lex.yy.c receita.tab.c receita.tab.h *.o receita
x