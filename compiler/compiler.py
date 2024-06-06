import sys
import re
from abc import abstractmethod

class Token:
    def __init__(self, type, value):
        self.type = type
        self.value = value

class SymbolTable:
    def __init__(self):
        self.table = {}

    def setter(self, key, value, type):
        self.table[key] = (value, type)

    def getter(self, key):
        if key in self.table:
            return self.table[key]
        else:
            raise ValueError(f"Variable {key} not declared")
       
class PrePro:
    @staticmethod
    def filter(code):
        return re.sub(r'--.*', '', code)
 
class Node:
    def __init__(self, value, children):
        self.value = value
        self.children = children

    @abstractmethod
    def evaluate(self, st, ft):
        pass

class FuncTable:
    def __init__(self):
        self.table = {}
    
    def setter(self, name, node):
        self.table[name] = node

    def getter(self, name):
        if name in self.table:
            return self.table[name]
        else:
            raise ValueError(f"Function {name} not declared")    

class FuncDec(Node):
    def __init__(self, children):
        super().__init__(None, children)

    def evaluate(self, symbolTable, ft):
        nome_funcao = self.children[0].value
        ft.setter(nome_funcao, self)

class FuncCall(Node):
    def __init__(self, children):
        super().__init__(None, children)

    def evaluate(self, symbolTable, ft):

        # Cria uma nova tabela de simbolos para a funcao
        localtable = SymbolTable()

        nome_funcao = self.children[0].value
        no_funcao = ft.getter(nome_funcao)
        argumentos = self.children[1]
        argumentos_org = no_funcao.children[1]
        if len(no_funcao.children)-1 != len(self.children):
            raise ValueError(f"Function {nome_funcao} called with wrong number of arguments")
        
        for i in range(0, len(argumentos)):
            value, type = argumentos[i].evaluate(symbolTable, ft)
            localtable.setter(argumentos_org[i].value, value, type)
        
        return no_funcao.children[-1].evaluate(localtable, ft)

class Return(Node):
    def __init__(self, children):
        super().__init__(None, children)

    def evaluate(self, st, ft):
        return self.children[0].evaluate(st, ft)

class BinOp(Node):
    def __init__(self, value, children):
       super().__init__(value, children)

    def evaluate(self, st, ft):
        left_val, left_type = self.children[0].evaluate(st, ft)
        right_val, right_type = self.children[1].evaluate(st, ft)

        if self.value in {'+', '-', '*', '/', 'and', 'or'}:
            if left_type != 'int' or right_type != 'int':
                raise TypeError(f"Arithmetic operations require integer types, got {left_type} and {right_type}")
            if self.value == '+':
                return (left_val + right_val, 'int')
            elif self.value == '-':
                return (left_val - right_val, 'int')
            elif self.value == '*':
                return (left_val * right_val, 'int')
            elif self.value == '/':
                return (left_val // right_val, 'int')
            elif self.value == 'and':
                return (left_val and right_val, 'int')
            elif self.value == 'or':
                return (left_val or right_val, 'int')

        elif self.value in {'==', '>', '<'}:
            if left_type != right_type:
                raise TypeError(f"Comparison operations require matching types, got {left_type} and {right_type}")
            if self.value == '==':
                return (int(left_val == right_val), 'int')
            elif self.value == '>':
                return (int(left_val > right_val), 'int')
            elif self.value == '<':
                return (int(left_val < right_val), 'int')

        elif self.value == '..':
            return (str(left_val) + str(right_val), 'string')

        else:
            raise ValueError(f"Unsupported operator {self.value}")

class UnOp(Node):
    def __init__(self, value, children):
       super().__init__(value, children)

    def evaluate(self, symbolTable, ft):
        val, type = self.children[0].evaluate(symbolTable, ft)
        if type != 'int':
            raise TypeError("Mismatched typees in unary operation")
        if self.value == '+':
            return (val, type)
        elif self.value == '-':
            return (-val, type)
        elif self.value == 'not':
            return (not val, type)
            
class StringVal(Node):
    def __init__(self, value):
        super().__init__(value, [])

    def evaluate(self, symbolTable, ft):
        return (self.value, 'string')

class IntVal(Node):
    def __init__(self, value):
        super().__init__(value, [])

    def evaluate(self, symbolTable, ft):
        return (self.value, 'int')

class NoOp(Node):
    def __init__(self):
        super().__init__(None, [])

    def evaluate(self, st, ft):
        return (None, 'Null')

class Block(Node):
    def __init__(self, children):
        super().__init__(None, children)

    def evaluate(self, symbolTable, ft):
        for child in self.children:
            child.evaluate(symbolTable, ft)
            if isinstance(child, Return):
                return child.evaluate(symbolTable, ft)

class Assignment(Node):
    def __init__(self, children):
        super().__init__(None, children)

    def evaluate(self, symbolTable, ft):
        if self.children[0].value in symbolTable.table:
            var_name = self.children[0].value
            value, typ = self.children[1].evaluate(symbolTable, ft)
            symbolTable.setter(var_name, value, typ)
        else:
            raise ValueError(f"Variable {self.children[0].value} not declared")

class Identifier(Node):
    def __init__(self, VALOR):
        super().__init__(VALOR, [])

    def evaluate(self, st, ft):
        return st.getter(self.value)

class Print(Node):
    def __init__(self, children):
        super().__init__(None, children)

    def evaluate(self, symbolTable, ft):
        value, type = self.children[0].evaluate(symbolTable, ft)
        print(value)

class whileNode(Node):
    def __init__(self, children):
        super().__init__(None, children)

    def evaluate(self, symbolTable, ft):
        while self.children[0].evaluate(symbolTable, ft)[0]:
            for child in self.children[1]:
                child.evaluate(symbolTable, ft)

class ifNode(Node):
    def __init__(self, children):
        super().__init__(None, children)

    def evaluate(self, symbolTable, ft):
        condition, _ = self.children[0].evaluate(symbolTable, ft)
        if condition:
            for st_mt in self.children[1]:
                st_mt.evaluate(symbolTable, ft)
        else:
            for st_mt in self.children[2]:
                st_mt.evaluate(symbolTable, ft)

class read(Node):
    def __init__(self, children):
        super().__init__(None, children)
        
    def evaluate(self, st, ft):
        return (self.children[0], 'int')

class VarDec(Node):
    def __init__(self, children):
        super().__init__(None, children)

    def evaluate(self, symbolTable, ft):
        if self.children[0].value in symbolTable.table:
            raise ValueError(f"Variable {self.children[0].value} already declared")
        var_name = self.children[0].value
        value, typ = self.children[1].evaluate(symbolTable, ft)
        symbolTable.setter(var_name, value, typ)

class Tokenizer:
    def __init__(self, source):
        self.source = source
        self.position = 0
        self.next = None
        self.listaPalavras = ["ml", "g", "picar", "se", "servir", "pare", "de", "mexer", "senao", "anotar", "enquanto", "ou", "tambem", "nao"]

    def selectNext(self):
        while self.position < len(self.source) and self.source[self.position].isspace():
            if self.source[self.position] == "\n":
                self.next = Token("NEWLINE", None)
                self.position += 1
                return
            self.position += 1

        if self.position >= len(self.source):
            self.next = Token('EOF', None)
        elif self.source[self.position].isdigit():
            number = ''
            while self.position < len(self.source) and self.source[self.position].isdigit():
                number += self.source[self.position]
                self.position += 1
            self.next = Token('NUMBER', int(number))
        elif self.source[self.position].isalpha() or self.source[self.position] == "_":
            identifier = ''
            while self.position < len(self.source) and (self.source[self.position].isalnum() or self.source[self.position] == "_"):
                identifier += self.source[self.position]
                self.position += 1
            if identifier in self.listaPalavras:
                self.next = Token(identifier.upper(), None)
            else:
                self.next = Token('IDENTIFIER', identifier)
        elif self.source[self.position] == "=":
            if self.position + 1 < len(self.source) and self.source[self.position + 1] == "=":
                self.next = Token("COMPAREEQUAL", None)
                self.position += 2
            else:
                self.next = Token("ASSIGN", None)
                self.position += 1
        elif self.source[self.position] == "+":
            self.next = Token("PLUS", None)
            self.position += 1
        elif self.source[self.position] == "-":
            self.next = Token("MINUS", None)
            self.position += 1
        elif self.source[self.position] == "*":
            self.next = Token("MULT", None)
            self.position += 1
        elif self.source[self.position] == "/":
            self.next = Token("DIV", None)
            self.position += 1
        elif self.source[self.position] == "{":
            self.next = Token("LEFTBRACKET", None)
            self.position += 1
        elif self.source[self.position] == "}":
            self.next = Token("RIGHTBRACKET", None)
            self.position += 1
        elif self.source[self.position] == "[":
            self.next = Token("LEFTPAR", None)
            self.position += 1
        elif self.source[self.position] == "]":
            self.next = Token("RIGHTPAR", None)
            self.position += 1
        elif self.source[self.position] == '"':
            self.next = Token("QUOTE", None)
            self.position += 1
        elif self.source[self.position] == ">":
            self.next = Token("GREATHERTHAN", None)
            self.position += 1
        elif self.source[self.position] == "<":
            self.next = Token("LESSTHAN", None)
            self.position += 1
        elif self.source[self.position] == "\"":
            self.position += 1
            string_literal = ''
            while self.position < len(self.source):
                if self.source[self.position] == "\\":
                    self.position += 1
                    if self.position < len(self.source) and self.source[self.position] in "\"nt":
                        if self.source[self.position] == "\"":
                            string_literal += "\""
                        elif self.source[self.position] == "n":
                            string_literal += "\n"
                        elif self.source[self.position] == "t":
                            string_literal += "\t"
                    else:
                        string_literal += "\\"
                        continue
                elif self.source[self.position] == "\"":
                    self.position += 1
                    break
                else:
                    string_literal += self.source[self.position]
                self.position += 1
            else:
                raise Exception("String literal not closed")
            self.next = Token('STRING', string_literal)
        elif self.source[self.position] == ",":
            self.next = Token('COMMA', None)
            self.position += 1
        else:
            sys.stderr.write(f"Unexpected character: {self.source[self.position]}\n")
            sys.exit(1)


class Parser: 

    @staticmethod
    def parseBoolExpression(TOKENIZER):
        result = Parser.parseBoolTerm(TOKENIZER)
        while TOKENIZER.next.type == 'OU':
            TOKENIZER.selectNext()
            result = BinOp('or', [result, Parser.parseBoolTerm(TOKENIZER)])
        return result
    

    @staticmethod
    def parseBoolTerm(TOKENIZER):
        result = Parser.parseRelExpression(TOKENIZER)
        while TOKENIZER.next.type == 'TAMBEM':
            TOKENIZER.selectNext()
            result = BinOp('and', [result, Parser.parseRelExpression(TOKENIZER)])
        return result
    
    @staticmethod
    def parseRelExpression(TOKENIZER):
        result = Parser.parseExpression(TOKENIZER)
        if TOKENIZER.next.type == 'GREATHERTHAN':
            TOKENIZER.selectNext()
            return BinOp('>', [result, Parser.parseExpression(TOKENIZER)])
        elif TOKENIZER.next.type == 'LESSTHAN':
            TOKENIZER.selectNext()
            return BinOp('<', [result, Parser.parseExpression(TOKENIZER)])
        elif TOKENIZER.next.type == 'COMPAREEQUAL':
            TOKENIZER.selectNext()
            return BinOp('==', [result, Parser.parseExpression(TOKENIZER)])
        else:
            return result

    @staticmethod
    def parseFactor(TOKENIZER):
        if TOKENIZER.next.type == 'NUMBER':
            result = TOKENIZER.next.value
            TOKENIZER.selectNext()
            return IntVal(result)
        elif TOKENIZER.next.type == 'STRING':
            result = TOKENIZER.next.value
            TOKENIZER.selectNext()
            return StringVal(result)
        elif TOKENIZER.next.type == 'IDENTIFIER':
            result = TOKENIZER.next.value
            TOKENIZER.selectNext()
            if TOKENIZER.next.type == "LEFTPAR":
                TOKENIZER.selectNext()
                arguments = []
                while TOKENIZER.next.type != "RIGHTPAR":
                    expression = Parser.parseBoolExpression(TOKENIZER)
                    arguments.append(expression)
                    if TOKENIZER.next.type == "COMMA":
                        TOKENIZER.selectNext()
                if TOKENIZER.next.type != "RIGHTPAR":
                    sys.stderr.write(f"Expected ]\n")
                    sys.exit(1)
                TOKENIZER.selectNext()
                return FuncCall([Identifier(result), arguments])
            else:
                return Identifier(result)
        elif TOKENIZER.next.type == 'PLUS':
            TOKENIZER.selectNext()
            return UnOp('+', [Parser.parseFactor(TOKENIZER)])
        elif TOKENIZER.next.type == 'MINUS':
            TOKENIZER.selectNext()
            return UnOp('-', [Parser.parseFactor(TOKENIZER)])
        elif TOKENIZER.next.type == 'NAO':
            TOKENIZER.selectNext()
            return UnOp('not', [Parser.parseFactor(TOKENIZER)])
        elif TOKENIZER.next.type == 'LEFTPAR':
            TOKENIZER.selectNext()
            result = Parser.parseBoolExpression(TOKENIZER)
            if TOKENIZER.next.type != 'RIGHTPAR':
                sys.stderr.write(f"Expected ]\n")
                sys.exit(1)
            TOKENIZER.selectNext()
            return result
        elif TOKENIZER.next.type == 'ANOTAR':
            TOKENIZER.selectNext()
            if TOKENIZER.next.type != 'LEFTPAR':
                sys.stderr.write(f"Expected \n")
                sys.exit(1)
            TOKENIZER.selectNext()
            if TOKENIZER.next.type != 'RIGHTPAR':
                sys.stderr.write(f"Expected )\n")
                sys.exit(1)
            TOKENIZER.selectNext()
            return read([int(input())])
        else:
            sys.stderr.write(f"Expected number or (expression)\n")
            sys.exit(1)

    @staticmethod
    def parseTerm(TOKENIZER):
        result = Parser.parseFactor(TOKENIZER)
        while TOKENIZER.next.type in ['MULT', 'DIV']:
            if TOKENIZER.next.type == 'MULT':
                TOKENIZER.selectNext()
                result = BinOp('*', [result, Parser.parseFactor(TOKENIZER)])
            elif TOKENIZER.next.type == 'DIV':
                TOKENIZER.selectNext()
                result = BinOp('/', [result, Parser.parseFactor(TOKENIZER)])
        return result
    
    @staticmethod
    def parseExpression(TOKENIZER):
        result = Parser.parseTerm(TOKENIZER)
        while TOKENIZER.next.type in ['PLUS', 'MINUS', 'CONCAT']:
            if TOKENIZER.next.type == 'PLUS':
                TOKENIZER.selectNext()
                result = BinOp('+', [result, Parser.parseTerm(TOKENIZER)])
            elif TOKENIZER.next.type == 'MINUS':
                TOKENIZER.selectNext()
                result = BinOp('-', [result, Parser.parseTerm(TOKENIZER)])
            elif TOKENIZER.next.type == 'CONCAT':
                TOKENIZER.selectNext()
                result = BinOp('..', [result, Parser.parseTerm(TOKENIZER)])
        return result
    
    @staticmethod
    def parseStatement(TOKENIZER):

        if TOKENIZER.next.type == 'LOCAL':
            TOKENIZER.selectNext()
            if TOKENIZER.next.type != 'IDENTIFIER':
                sys.stderr.write(f"Expected identifier\n")
                sys.exit(1)
            identifier = Identifier(TOKENIZER.next.value)
            TOKENIZER.selectNext()
            if TOKENIZER.next.type != 'ASSIGN' and TOKENIZER.next.type != 'EOF' and TOKENIZER.next.type != 'NEWLINE':
                sys.stderr.write(f"error\n")
                sys.exit(1)
            if TOKENIZER.next.type == 'ASSIGN':
                TOKENIZER.selectNext()
                expression = Parser.parseBoolExpression(TOKENIZER)
                if TOKENIZER.next.type != 'EOF' and TOKENIZER.next.type != 'NEWLINE':
                    sys.stderr.write(f"Expected \\n\n")
                    sys.exit(1)
                TOKENIZER.selectNext()
                return VarDec([identifier, expression])
            else:
                return VarDec([identifier, NoOp()])
            

        elif TOKENIZER.next.type == 'IDENTIFIER':
            identifier = Identifier(TOKENIZER.next.value)
            TOKENIZER.selectNext()
            if TOKENIZER.next.type != 'ASSIGN' and TOKENIZER.next.type != 'LEFTPAR':
                sys.stderr.write(f"Expected = or (\n")
                sys.exit(1)
            if TOKENIZER.next.type == 'LEFTPAR':
                TOKENIZER.selectNext()
                arguments = []
                while TOKENIZER.next.type != 'RIGHTPAR':
                    expression = Parser.parseBoolExpression(TOKENIZER)
                    arguments.append(expression)
                    if TOKENIZER.next.type == 'COMMA':
                        TOKENIZER.selectNext()
                if TOKENIZER.next.type != 'RIGHTPAR':
                    sys.stderr.write(f"Expected )\n")
                    sys.exit(1)
                TOKENIZER.selectNext()
                if TOKENIZER.next.type != 'EOF' and TOKENIZER.next.type != 'NEWLINE':
                    sys.stderr.write(f"Expected \\n\n")
                    sys.exit(1)
                TOKENIZER.selectNext()
                return FuncCall([identifier, arguments])
            elif TOKENIZER.next.type == 'ASSIGN':
                TOKENIZER.selectNext()
                expression = Parser.parseBoolExpression(TOKENIZER)
                if TOKENIZER.next.type != 'EOF' and TOKENIZER.next.type != 'NEWLINE':
                    sys.stderr.write(f"Expected \\n\n")
                    sys.exit(1)
                TOKENIZER.selectNext()
                return Assignment([identifier, expression])
        

        elif TOKENIZER.next.type == 'PRINT':
            TOKENIZER.selectNext()
            if TOKENIZER.next.type != 'LEFTPAR':
                sys.stderr.write(f"Expected (\n")
                sys.exit(1)
            TOKENIZER.selectNext()
            expression = Parser.parseBoolExpression(TOKENIZER)
            if TOKENIZER.next.type != 'RIGHTPAR':
                sys.stderr.write(f"Expected )\n")
                sys.exit(1)
            TOKENIZER.selectNext()
            if TOKENIZER.next.type != 'EOF' and TOKENIZER.next.type != 'NEWLINE':
                sys.stderr.write(f"Expected \\n\n")
                sys.exit(1)
            TOKENIZER.selectNext() 
            return Print([expression])
        

        elif TOKENIZER.next.type == 'NEWLINE':
            TOKENIZER.selectNext()
            return NoOp()
        

        elif TOKENIZER.next.type == 'WHILE':
            TOKENIZER.selectNext()
            expression = Parser.parseBoolExpression(TOKENIZER)
            if TOKENIZER.next.type != 'DO':
                sys.stderr.write(f"Expected do\n")
                sys.exit(1)
            TOKENIZER.selectNext()
            if TOKENIZER.next.type != 'NEWLINE':
                sys.stderr.write(f"Expected \\n\n")
                sys.exit(1)
            TOKENIZER.selectNext()
            statements = []
            while TOKENIZER.next.type != 'END':
                statement = Parser.parseStatement(TOKENIZER)
                statements.append(statement)
            if TOKENIZER.next.type != 'END':
                sys.stderr.write(f"Expected end\n")
                sys.exit(1)
            TOKENIZER.selectNext()
            if TOKENIZER.next.type != 'EOF' and TOKENIZER.next.type != 'NEWLINE':
                sys.stderr.write(f"Expected \\n\n")
                sys.exit(1)
            return whileNode([expression, statements])


        elif TOKENIZER.next.type == 'IF':
            TOKENIZER.selectNext()
            expression = Parser.parseBoolExpression(TOKENIZER)
            if TOKENIZER.next.type != 'THEN':
                sys.stderr.write(f"Expected then\n")
                sys.exit(1)
            TOKENIZER.selectNext()
            if TOKENIZER.next.type != 'NEWLINE':
                sys.stderr.write(f"Expected \\n\n")
                sys.exit(1)
            TOKENIZER.selectNext()
            statement1 = []
            while TOKENIZER.next.type != 'ELSE' and TOKENIZER.next.type != 'END':
                statement = Parser.parseStatement(TOKENIZER)
                statement1.append(statement)
            if TOKENIZER.next.type != 'ELSE' and TOKENIZER.next.type != 'END':
                sys.stderr.write(f"Expected else\n")
                sys.exit(1)
            if TOKENIZER.next.type == 'ELSE':
                TOKENIZER.selectNext()
                if TOKENIZER.next.type != 'NEWLINE':
                    sys.stderr.write(f"Expected \\n\n")
                    sys.exit(1)
                TOKENIZER.selectNext()
                statement2 = []
                while TOKENIZER.next.type != 'END':
                    statement = Parser.parseStatement(TOKENIZER)
                    statement2.append(statement)
                if TOKENIZER.next.type != 'END':
                    sys.stderr.write(f"Expected end\n")
                    sys.exit(1)
                TOKENIZER.selectNext()
                if TOKENIZER.next.type != 'EOF' and TOKENIZER.next.type != 'NEWLINE':
                    sys.stderr.write(f"Expected \\n\n")
                    sys.exit(1)
                return ifNode([expression, statement1, statement2])
            if TOKENIZER.next.type == 'END':
                TOKENIZER.selectNext()
                if TOKENIZER.next.type != 'EOF' and TOKENIZER.next.type != 'NEWLINE':
                    sys.stderr.write(f"Expected \\n\n")
                    sys.exit(1)
                return ifNode([expression, statement1, []])
            
        elif TOKENIZER.next.type == 'RETURN':
            TOKENIZER.selectNext()
            expression = Parser.parseBoolExpression(TOKENIZER)
            if TOKENIZER.next.type != 'EOF' and TOKENIZER.next.type != 'NEWLINE':
                sys.stderr.write(f"Expected \\n\n")
                sys.exit(1)
            TOKENIZER.selectNext()
            return Return([expression])

        elif TOKENIZER.next.type == 'FUNCTION':
            TOKENIZER.selectNext()
            if TOKENIZER.next.type != 'IDENTIFIER':
                sys.stderr.write(f"Expected identifier\n")
                sys.exit(1)
            identifier = Identifier(TOKENIZER.next.value)
            TOKENIZER.selectNext()
            if TOKENIZER.next.type != 'LEFTPAR':
                sys.stderr.write(f"Expected (\n")
                sys.exit(1)
            TOKENIZER.selectNext()
            arguments = []
            while TOKENIZER.next.type != 'RIGHTPAR':
                if TOKENIZER.next.type != 'IDENTIFIER':
                    sys.stderr.write(f"Expected identifier\n")
                    sys.exit(1)
                arguments.append(Identifier(TOKENIZER.next.value))
                TOKENIZER.selectNext()
                if TOKENIZER.next.type == 'COMMA':
                    TOKENIZER.selectNext()
            if TOKENIZER.next.type != 'RIGHTPAR':
                sys.stderr.write(f"Expected )\n")
                sys.exit(1)
            TOKENIZER.selectNext()
            if TOKENIZER.next.type != 'NEWLINE':
                sys.stderr.write(f"Expected \\n\n")
                sys.exit(1)
            TOKENIZER.selectNext()
            statements = []
            while TOKENIZER.next.type != 'END':
                statement = Parser.parseStatement(TOKENIZER)
                statements.append(statement)
            if TOKENIZER.next.type != 'END':
                sys.stderr.write(f"Expected end\n")
                sys.exit(1)
            TOKENIZER.selectNext()
            if TOKENIZER.next.type != 'EOF' and TOKENIZER.next.type != 'NEWLINE':
                sys.stderr.write(f"Expected \\n\n")
                sys.exit(1)
            block = Block(statements)
            return FuncDec([identifier, arguments, block])

        else:
            sys.stderr.write(f"Expected identifier or print\n")
            sys.exit(1)

        
        
    @staticmethod
    def parseBlock(TOKENIZER):
        statements = []
        while TOKENIZER.next.type != 'EOF':
            statement = Parser.parseStatement(TOKENIZER)
            if not isinstance(statement, NoOp):
                statements.append(statement)
        return Block(statements)
        
    @staticmethod
    def run(code, symbolTable, ft):
        tokenizer = Tokenizer(code)
        tokenizer.selectNext()
        result = Parser.parseBlock(TOKENIZER=tokenizer)
        resultado = result.evaluate(symbolTable, ft)
        if tokenizer.next.type != "EOF": #FINAL DO ARQUIVO (EOF) !!!! precisa ser
            raise Exception("Erro de sintaxe")
        return resultado

def main():
    symbolTable = SymbolTable()
    ft = FuncTable()
    filename = sys.argv[1]
    if len(sys.argv) < 2:
        raise Exception("Numero de argumentos invalido")
    if filename.endswith(".lua"):
        with open(filename, "r") as file:
            code = file.read()
        code = PrePro.filter(code)
        parser = Parser.run(code, symbolTable, ft)
    else:
        raise Exception("Arquivo invalido")

if __name__ == "__main__":
    main()