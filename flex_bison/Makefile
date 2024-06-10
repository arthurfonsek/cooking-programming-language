receita: receita.lex receita.y
	bison -d receita.y
	lex receita.lex
	gcc -o $@ receita.tab.c lex.yy.c -lfl

clean:
	rm -f receita
	rm -f lex.yy.c
	rm -f receita.tab.c
	rm -f receita.tab.h