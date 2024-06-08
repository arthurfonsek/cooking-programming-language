import sys

class Token:
    def __init__(self, type, value):
        self.type = type
        self.value = value

class linecounter:
    def __init__(self):
        self.linha= 1

    def increment(self):
        self.linha += 1

    def get(self):
        return str(self.linha)
    
linha = linecounter()

class SymbolTable:
    def __init__(self):
        self.table = {}

    def create(self, var_name):
        self.table[var_name] = 0

    def set(self, var_name, value, type):
        self.table[var_name] = [value, type]

    def get(self, var_name):
        return self.table[var_name]


class Tokenizer:
    def __init__(self, source):
        self.source = source
        self.position = 0
        self.next = None
        self.selectNext()

    def selectNext(self):

        if self.position >= len(self.source):
            self.next = Token("EOF", "")
        else:
            if self.source[self.position] in [" ", "\t"]:
                self.position += 1
                self.selectNext()
            elif self.source[self.position] == "\n":
                self.position += 1
                self.next = Token("NEWLINE", "\n")
                linha.increment()
            elif self.source[self.position].isdigit():
                start = self.position
                while self.position < len(self.source) and self.source[self.position].isdigit():
                    self.position += 1
                self.next = Token("INTEGER", self.source[start:self.position])
            elif self.source[self.position:self.position + 14] == "mexer enquanto":
                self.position += 14
                self.next = Token("WHILE", "mexer enquanto")
            elif self.source[self.position:self.position + 13] == "pare de mexer":
                self.position += 13
                self.next = Token("ENDWHILE", "pare de mexer")
            elif self.source[self.position:self.position + 8] == "picar se":
                self.position += 8
                self.next = Token("IF", "picar se")
            elif self.source[self.position:self.position + 13] == "pare de picar":
                self.position += 13
                self.next = Token("ENDIF", "pare de picar")
            elif self.source[self.position] == '+':
                self.next = Token("PLUS", "+")
                self.position += 1
            elif self.source[self.position] == '-':
                self.next = Token("MINUS", "-")
                self.position += 1
            elif self.source[self.position] == '*':
                self.next = Token("MULTIPLY", "*")
                self.position += 1
            elif self.source[self.position] == '/':
                self.next = Token("DIVIDE", "/")
                self.position += 1
            elif self.source[self.position] == '>':
                self.next = Token("GREATER", ">")
                self.position += 1
            elif self.source[self.position] == '<':
                self.next = Token("LESS", "<")
                self.position += 1
            elif self.source[self.position] == '=':
                if self.source[self.position + 1] == '=':
                    self.next = Token("EQUAL", "==")
                    self.position += 2
                else:
                    raise Exception("Invalid token: '='")
            elif self.source[self.position] == '"':
                self.position += 1
                start_pos = self.position
                while self.position < len(self.source) and self.source[self.position] != '"':
                    self.position += 1
                if self.position >= len(self.source):
                    raise Exception("Unterminated string")
                self.next = Token("STRING", self.source[start_pos:self.position])
                self.position += 1
            elif self.source[self.position] == '{':
                self.next = Token("LBRACE", "{")
                self.position += 1
            elif self.source[self.position] == '}':
                self.next = Token("RBRACE", "}")
                self.position += 1
            elif self.source[self.position] == '[':
                self.next = Token("LPAREN", "[")
                self.position += 1
            elif self.source[self.position] == ']':
                self.next = Token("RPAREN", "]")
                self.position += 1
            elif self.source[self.position] == ',':
                self.next = Token("COMMA", ",")
                self.position += 1
            elif self.source[self.position] == ';':
                self.next = Token("SEMICOLON", ";")
                self.position += 1
            elif self.source[self.position] == ':':
                self.next = Token("COLON", ":")
                self.position += 1
            elif self.source[self.position].isalpha():
                start = self.position
                while self.position < len(self.source) and (self.source[self.position].isalpha() or self.source[self.position].isdigit() or self.source[self.position] == "_"):
                    self.position += 1
                value = self.source[start:self.position]
                keywords = ["receita", "mexer enquanto", "pare de mexer", "picar se", "pare de picar", "servir", "anotar", "g", "ml", "tambem", "ou", "nao", "senao"]
                if value in keywords:
                    self.next = Token(value.upper(), value)
                else:
                    self.next = Token("IDENTIFIER", value)


                
            else:
                print(self.source[self.position: self.position + 10])
               
                raise Exception("Invalid token: {}".format(self.source[self.position]))
            
class Node:
    def __init__(self, value, children=None):
        self.value = value
        self.children = children if children is not None else []

    def evaluate(self, st):
        raise NotImplementedError("Subclasses should implement this!")

class Program(Node):
    def __init__(self, value, children=None):
        super().__init__(value, children if children is not None else [])

    def evaluate(self, st):
        self.children.evaluate(st)


class Block(Node):
    def __init__(self, value, children=None):
        super().__init__(value, children if children is not None else [])

    def evaluate(self, st):
        for child in self.children:
            child.evaluate(st)

class Input(Node):
    def __init__(self, value, children):
        super().__init__(value, children)

    def evaluate(self, st):
        value = input(self.children[0])
        st.set(self.children[1].value, value, "string")

class Assignment(Node):
    def __init__(self, value, children):
        super().__init__(value, children)

    def evaluate(self, st):
        value = self.children[1].evaluate(st)
        if self.value == "g":
            try:
                st.set(self.children[0].value, int(value[0]), "int")
            except:
                raise Exception(linha.get() + "; Syntax error: Expected integer, received {}".format(value[0]) + " with type " + value[1])
        elif self.value == "ml":
            string = str(value[0])
            

            
            st.set(self.children[0].value, value[0], "string")

class Print(Node):
    def __init__(self, value, children):
        super().__init__(value, children)

    def evaluate(self, st):
        value = self.children[0].evaluate(st)
        print(value[0])

class StringVal(Node):
    def __init__(self, value):
        super().__init__(value)

    def evaluate(self, st):
        return [self.value, "string"]

class IntVal(Node):
    def __init__(self, value):
        super().__init__(value)

    def evaluate(self, st):
        return [int(self.value), "int"]

class Identifier(Node):
    def __init__(self, value):
        super().__init__(value)

    def evaluate(self, st):
        return st.get(self.value)

class BinOp(Node):
    def __init__(self, value, children):
        super().__init__(value, children)

    def evaluate(self, st):
   
        left = self.children[0].evaluate(st)
        right = self.children[1].evaluate(st)
        if self.value == "+":
            return [left[0] + right[0], "int"]
        elif self.value == "-":
            return [left[0] - right[0], "int"]
        elif self.value == "*":
            return [left[0] * right[0], "int"]
        elif self.value == "/":

            return [left[0] / right[0], "int"]
        elif self.value == "tambem":
            return [left[0] and right[0], "int"]
        elif self.value == "ou":
            return [left[0] or right[0], "int"]
        elif self.value == ">":
            return [left[0] > right[0], "int"]
        elif self.value == "<":
            return [left[0] < right[0], "int"]
        elif self.value == "==":
            return [left[0] == right[0], "int"]

class UnOp(Node):
    def __init__(self, value, children):
        super().__init__(value, children)

    def evaluate(self, st):
        value = self.children[0].evaluate(st)
        if self.value == "-":
            return [-value[0], "int"]
        elif self.value == "nao":
            return [not value[0], "int"]

class NoOp(Node):
    def __init__(self):
        super().__init__(None, None)

    def evaluate(self, st):
        pass

class While(Node):
    def __init__(self, value, children):
        super().__init__(value, children)

    def evaluate(self, st):
        while self.children[0].evaluate(st)[0]:
            self.children[1].evaluate(st)

class If(Node):
    def __init__(self, value, children):
        super().__init__(value, children)

    def evaluate(self, st):
        if self.children[0].evaluate(st)[0]:
            self.children[1].evaluate(st)
        elif len(self.children) == 3:
            self.children[2].evaluate(st)


class Parser:
    def __init__(self, tokenizer):
        self.tokenizer = tokenizer

    @staticmethod
    def parseProgram(tokenizer):
        if tokenizer.next.type == "RECEITA":
            tokenizer.selectNext()
            if tokenizer.next.type == "LBRACE":
                tokenizer.selectNext()
                block = Parser.parseBlock(tokenizer)
                if tokenizer.next.type == "RBRACE":
                    tokenizer.selectNext()
                    return Program("program", block)
                else:
                    raise Exception(linha.get() + "; Syntax error: Expected fecha-chaves, received {}".format(tokenizer.next.type) + " with value " + tokenizer.next.value)
            else:
                raise Exception(linha.get() + "; Syntax error: Expected '{'")
        else:
            raise Exception(linha.get() + "; Syntax error: Expected 'receita', received {}".format(tokenizer.next.type) + " with value " + tokenizer.next.value)

    @staticmethod
    def parseBlock(tokenizer):
        statements = []
        while tokenizer.next.type not in ["EOF", "RBRACE"]:
            if tokenizer.next.type == "NEWLINE":
                tokenizer.selectNext()
            else:
                statements.append(Parser.parseStatement(tokenizer))
        return Block("block", statements)

    @staticmethod
    def parseStatement(tokenizer):
        res = None
        #print("parseStatement: ", tokenizer.next.type, tokenizer.next.value)
        if tokenizer.next.type == "IDENTIFIER":
            identifier = Identifier(tokenizer.next.value)
            tokenizer.selectNext()
            
            if tokenizer.next.type == "COLON":
                tokenizer.selectNext()
                exp = Parser.parseBoolExpression(tokenizer)
                if tokenizer.next.type in ["G", "ML"]:
                    type = tokenizer.next.value
                    tokenizer.selectNext()
                    res = Assignment(type, [identifier, exp])
                else:
                    raise Exception(linha.get() + "; Syntax error: Expected type (g or ml), received: " + tokenizer.next.type + " with value " + tokenizer.next.value)
            else:
                raise Exception(linha.get() + "; Syntax error: Expected ':', received: " + tokenizer.next.type + " with value " + tokenizer.next.value)

        elif tokenizer.next.type == "SERVIR":
            tokenizer.selectNext()
            exp = Parser.parseBoolExpression(tokenizer)
            res = Print("servir", [exp])

        elif tokenizer.next.type == "ANOTAR":
            tokenizer.selectNext()
            if tokenizer.next.type == "STRING":
                string = tokenizer.next.value
                tokenizer.selectNext()
                if tokenizer.next.type == "IDENTIFIER":
                    identifier = Identifier(tokenizer.next.value)
                    tokenizer.selectNext()
                    res = Input("anotar", [string, identifier])
                else:
                    raise Exception(linha.get() + "; Syntax error: Expected IDENTIFIER")
            else:
                raise Exception(linha.get() + "; Syntax error: Expected STRING")

        elif tokenizer.next.type == "WHILE":
            tokenizer.selectNext()
            exp = Parser.parseBoolExpression(tokenizer)
            if tokenizer.next.type == "COMMA":
                tokenizer.selectNext()
                if tokenizer.next.type == "NEWLINE":
                    tokenizer.selectNext()
                    block = []
                    while tokenizer.next.type not in ["ENDWHILE", "EOF"]:
                        block.append(Parser.parseStatement(tokenizer))
                    if tokenizer.next.type == "ENDWHILE":
                        tokenizer.selectNext()
                        res = While("while", [exp, Block("block", block)])
                    else:
                        raise Exception(linha.get() + "; Syntax error: Expected 'pare de mexer'")
                else:
                    raise Exception(linha.get() + "; Syntax error: Expected NEWLINE, received {}".format(tokenizer.next.type))
            else:
                raise Exception(linha.get() + "; Syntax error: Expected ',' received {}".format(tokenizer.next.type) + " with value " + tokenizer.next.value)

        elif tokenizer.next.type == "IF":
            tokenizer.selectNext()
            exp = Parser.parseBoolExpression(tokenizer)
            if tokenizer.next.type == "COMMA":
                tokenizer.selectNext()
                if tokenizer.next.type == "NEWLINE":
                    tokenizer.selectNext()
                    if_block = []
                    else_block = None
                    while tokenizer.next.type not in ["SENAO", "ENDIF", "EOF"]:
                        if_block.append(Parser.parseStatement(tokenizer))
                    if tokenizer.next.type == "SENAO":
                        tokenizer.selectNext()
                        if tokenizer.next.type == "COMMA":
                            tokenizer.selectNext()
                            if tokenizer.next.type == "NEWLINE":
                                tokenizer.selectNext()
                                else_block = []
                                while tokenizer.next.type not in ["ENDIF", "EOF"]:
                                    else_block.append(Parser.parseStatement(tokenizer))
                                if tokenizer.next.type == "ENDIF":
                                    tokenizer.selectNext()
                                    res = If("if", [exp, Block("block", if_block), Block("block", else_block)])
                                else:
                                    raise Exception(linha.get() + "; Syntax error: Expected 'pare de picar'")
                            else:
                                raise Exception(linha.get() + "; Syntax error: Expected NEWLINE after 'senao', received {}".format(tokenizer.next.type))
                        else:
                            raise Exception(linha.get() + "; Syntax error: Expected ',' after 'senao', received {}".format(tokenizer.next.type))
                    elif tokenizer.next.type == "ENDIF":
                        tokenizer.selectNext()
                        res = If("if", [exp, Block("block", if_block)])
                    else:
                        raise Exception(linha.get() + "; Syntax error: Expected 'pare de picar' or 'senao'")
                else:
                    raise Exception(linha.get() + "; Syntax error: Expected NEWLINE after 'if', received {}".format(tokenizer.next.type))
            else:
                raise Exception(linha.get() + "; Syntax error: Expected ',' after 'if', received {}".format(tokenizer.next.type))

        else:
            raise Exception(linha.get() + "; Syntax error: Invalid statement received: " + tokenizer.next.type + " with value " + tokenizer.next.value)

        if tokenizer.next.type == "SEMICOLON":
            tokenizer.selectNext()
            if tokenizer.next.type == "SEMICOLON":
                raise Exception(linha.get() + "; Syntax error: Multiple consecutive ';' not allowed")
        else:
            raise Exception(linha.get() + "; Syntax error: Expected ';', received: " + tokenizer.next.type + " with value " + tokenizer.next.value)
        
        if tokenizer.next.type == "NEWLINE":
            tokenizer.selectNext()
        else:
            raise Exception(linha.get() + "; Syntax error: Expected NEWLINE, received: " + tokenizer.next.type + " with value " + tokenizer.next.value)

        return res

    @staticmethod
    def parseBoolExpression(tokenizer):
        res = Parser.parseBoolTerm(tokenizer)
        while tokenizer.next.type == "OU":
            tokenizer.selectNext()
            res = BinOp("ou", [res, Parser.parseBoolTerm(tokenizer)])
        return res
    
    @staticmethod
    def parseBoolTerm(tokenizer):
        res = Parser.parseRelExpression(tokenizer)
        while tokenizer.next.type == "TAMBEM":
            tokenizer.selectNext()
            res = BinOp("tambem", [res, Parser.parseRelExpression(tokenizer)])
        return res
    
    @staticmethod
    def parseRelExpression(tokenizer):
        res = Parser.parseExpression(tokenizer)
        while tokenizer.next.type in ["GREATER", "LESS", "EQUAL"]:
            if tokenizer.next.type == "GREATER":
                tokenizer.selectNext()
                return BinOp(">", [res, Parser.parseExpression(tokenizer)])
            elif tokenizer.next.type == "LESS":
                tokenizer.selectNext()
                return BinOp("<", [res, Parser.parseExpression(tokenizer)])
            elif tokenizer.next.type == "EQUAL":
                tokenizer.selectNext()
                return BinOp("==", [res, Parser.parseExpression(tokenizer)])
        return res

    def parseExpression(tokenizer):
        res = Parser.parseTerm(tokenizer)
        while tokenizer.next.type in ["PLUS", "MINUS", "tambem", "ou"]:
            if tokenizer.next.type == "PLUS":
                tokenizer.selectNext()
                res = BinOp("+", [res, Parser.parseTerm(tokenizer)])
            elif tokenizer.next.type == "MINUS":
                tokenizer.selectNext()
                res = BinOp("-", [res, Parser.parseTerm(tokenizer)])
            elif tokenizer.next.type == "tambem":
                tokenizer.selectNext()
                res = BinOp("tambem", [res, Parser.parseTerm(tokenizer)])
            elif tokenizer.next.type == "ou":
                tokenizer.selectNext()
                res = BinOp("ou", [res, Parser.parseTerm(tokenizer)])
        return res

    @staticmethod
    def parseTerm(tokenizer):
        res = Parser.parseFactor(tokenizer)
        while tokenizer.next.type in ["MULTIPLY", "DIVIDE"]:
            if tokenizer.next.type == "MULTIPLY":
                tokenizer.selectNext()
                res = BinOp("*", [res, Parser.parseFactor(tokenizer)])
            elif tokenizer.next.type == "DIVIDE":
                tokenizer.selectNext()
                res = BinOp("/", [res, Parser.parseFactor(tokenizer)])
        return res

    @staticmethod
    def parseFactor(tokenizer):

        if tokenizer.next.type == "INTEGER":
            res = IntVal(tokenizer.next.value)
            tokenizer.selectNext()
            return res
        elif tokenizer.next.type == "IDENTIFIER":
            res = Identifier(tokenizer.next.value)
            tokenizer.selectNext()
            return res
        elif tokenizer.next.type == "LPAREN":
            tokenizer.selectNext()
            res = Parser.parseBoolExpression(tokenizer)
            if tokenizer.next.type == "RPAREN":
                tokenizer.selectNext()
                return res
            else:
                raise Exception(linha.get() + "; Syntax error: Expected RPAREN")
        elif tokenizer.next.type in ["MINUS", "NAO"]:
            op = tokenizer.next.value
            tokenizer.selectNext()
            res = UnOp(op, [Parser.parseFactor(tokenizer)])
            return res
        elif tokenizer.next.type == "STRING":
            res = StringVal(tokenizer.next.value)
            tokenizer.selectNext()
            return res
        else:
            raise Exception(linha.get() + "; Syntax error: Invalid factor, received: " + tokenizer.next.type+ "with value " + tokenizer.next.value)

    @staticmethod
    def run(code):
        tokenizer = Tokenizer(code)
        parser = Parser(tokenizer)
        result = parser.parseProgram(tokenizer)
        if result:
            return result

def main():
    import sys
    if len(sys.argv) != 2:
        print("Usage: python main.py <source_file>")
        return

    file_path = sys.argv[1]
    with open(file_path, 'r') as file:
        code = file.read()

    st = SymbolTable()
    parser = Parser(Tokenizer(code))
    program = parser.run(code)

    if program:
        program.evaluate(st)

if __name__ == "__main__":
    main()
