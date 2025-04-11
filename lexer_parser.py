import re

# Token types
TT_INT = 'INT'
TT_FLOAT = 'FLOAT'
TT_PLUS = 'PLUS'
TT_MINUS = 'MINUS'
TT_MUL = 'MUL'
TT_DIV = 'DIV'
TT_COS = 'COS'
TT_SIN = 'SIN'
TT_TG = 'TG'
TT_CTG = 'CTG'
TT_LPAREN = 'LPAREN'
TT_RPAREN = 'RPAREN'

DIGITS = '0123456789'


class ParserError(Exception):
    def __init__(self, message, token):
        super().__init__(message)
        self.token = token

    def as_string(self):
        return f"Parser Error: {self.args[0]}\nAt line {self.token.pos_start.line_nr + 1}, column {self.token.pos_start.column_nr + 1}"


class Error:
    def __init__(self, pos_start, pos_end, error_name, details):
        self.pos_start = pos_start
        self.pos_end = pos_end
        self.error_name = error_name
        self.details = details

    def as_string(self):
        return f"{self.error_name}: {self.details}\nAt line {self.pos_start.line_nr + 1}, column {self.pos_start.column_nr + 1}"


class IllegalCharError(Error):
    def __init__(self, pos_start, pos_end, details):
        super().__init__(pos_start, pos_end, 'Illegal Character', details)


class Token:
    def __init__(self, type_, value=None, pos_start=None, pos_end=None):
        self.type = type_
        self.value = value
        self.pos_start = pos_start
        self.pos_end = pos_end

    def __repr__(self):
        return f'{self.type}:{self.value}' if self.value is not None else f'{self.type}'


class Position:
    def __init__(self, index, line_nr, column_nr):
        self.index = index
        self.line_nr = line_nr
        self.column_nr = column_nr

    def advance(self, current_char):
        self.index += 1
        self.column_nr += 1
        if current_char == '\n':
            self.line_nr += 1
            self.column_nr = 0
        return self

    def copy(self):
        return Position(self.index, self.line_nr, self.column_nr)


class Lexer:
    def __init__(self, text):
        self.text = text
        self.pos = Position(-1, 0, -1)
        self.current_char = None
        self.advance()

    def advance(self):
        self.pos.advance(self.current_char)
        if self.pos.index < len(self.text):
            self.current_char = self.text[self.pos.index]
        else:
            self.current_char = None

    def make_tokens(self):
        token_specification = [
            ('FLOAT', r'\d+\.\d+'),
            ('INT', r'\d+'),
            ('PLUS', r'\+'),
            ('MINUS', r'-'),
            ('MUL', r'\*'),
            ('DIV', r'/'),
            ('LPAREN', r'\('),
            ('RPAREN', r'\)'),
            ('IDENTIFIER', r'[a-zA-Z_]\w*'),
            ('SKIP', r'[ \t]+'),
            ('MISMATCH', r'.'),
        ]

        tok_regex = '|'.join(f'(?P<{name}>{regex})' for name, regex in token_specification)
        get_token = re.compile(tok_regex).match
        pos = 0
        tokens = []

        while pos < len(self.text):
            match = get_token(self.text, pos)
            if match is None:
                return [], IllegalCharError(Position(pos, 0, pos), Position(pos + 1, 0, pos + 1),
                                            f"Illegal character: '{self.text[pos]}'")

            type_ = match.lastgroup
            value = match.group(type_)
            start_pos = Position(pos, 0, pos)
            end_pos = Position(match.end(), 0, match.end())

            if type_ == 'INT':
                tokens.append(Token(TT_INT, int(value), start_pos, end_pos))
            elif type_ == 'FLOAT':
                tokens.append(Token(TT_FLOAT, float(value), start_pos, end_pos))
            elif type_ == 'PLUS':
                tokens.append(Token(TT_PLUS, None, start_pos, end_pos))
            elif type_ == 'MINUS':
                tokens.append(Token(TT_MINUS, None, start_pos, end_pos))
            elif type_ == 'MUL':
                tokens.append(Token(TT_MUL, None, start_pos, end_pos))
            elif type_ == 'DIV':
                tokens.append(Token(TT_DIV, None, start_pos, end_pos))
            elif type_ == 'LPAREN':
                tokens.append(Token(TT_LPAREN, None, start_pos, end_pos))
            elif type_ == 'RPAREN':
                tokens.append(Token(TT_RPAREN, None, start_pos, end_pos))
            elif type_ == 'IDENTIFIER':
                if value == 'cos':
                    tokens.append(Token(TT_COS, None, start_pos, end_pos))
                elif value == 'sin':
                    tokens.append(Token(TT_SIN, None, start_pos, end_pos))
                elif value == 'tg':
                    tokens.append(Token(TT_TG, None, start_pos, end_pos))
                elif value == 'ctg':
                    tokens.append(Token(TT_CTG, None, start_pos, end_pos))
                else:
                    return [], IllegalCharError(start_pos, end_pos, f"Unknown function '{value}'")
            elif type_ == 'SKIP':
                pass
            elif type_ == 'MISMATCH':
                return [], IllegalCharError(start_pos, end_pos, f"'{value}' is not a valid token.")

            pos = match.end()

        return tokens, None


# AST Nodes
class NumberNode:
    def __init__(self, tok):
        self.tok = tok

    def __repr__(self):
        return f'{self.tok}'


class FuncNode:
    def __init__(self, func_tok, arg_node):
        self.func_tok = func_tok
        self.arg_node = arg_node

    def __repr__(self):
        return f'{self.func_tok}({self.arg_node})'


class BinOpNode:
    def __init__(self, left_node, op_tok, right_node):
        self.left_node = left_node
        self.op_tok = op_tok
        self.right_node = right_node

    def __repr__(self):
        return f'({self.left_node} {self.op_tok} {self.right_node})'


# Parser
class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.tok_idx = -1
        self.current_tok = None
        self.advance()

    def advance(self):
        self.tok_idx += 1
        if self.tok_idx < len(self.tokens):
            self.current_tok = self.tokens[self.tok_idx]
        return self.current_tok

    def parse(self):
        return self.expression()

    def factor(self):
        tok = self.current_tok

        if tok.type in (TT_INT, TT_FLOAT):
            self.advance()
            return NumberNode(tok)

        elif tok.type in (TT_COS, TT_SIN, TT_TG, TT_CTG):
            func_tok = tok
            self.advance()
            if self.current_tok is not None and self.current_tok.type == TT_LPAREN:
                self.advance()
                arg = self.expression()
                if self.current_tok is not None and self.current_tok.type == TT_RPAREN:
                    self.advance()
                    return FuncNode(func_tok, arg)
                else:
                    raise ParserError("Expected ')'", self.current_tok or func_tok)
            else:
                raise ParserError("Expected '(' after function name", self.current_tok or func_tok)

        elif tok.type == TT_LPAREN:
            self.advance()
            expr = self.expression()
            if self.current_tok is not None and self.current_tok.type == TT_RPAREN:
                self.advance()
                return expr
            else:
                raise ParserError("Expected ')'", self.current_tok or tok)

        return None

    def term(self):
        return self.bin_op(self.factor, (TT_MUL, TT_DIV))

    def expression(self):
        return self.bin_op(self.term, (TT_PLUS, TT_MINUS))

    def bin_op(self, func, ops):
        left = func()
        while self.current_tok is not None and self.current_tok.type in ops:
            op_tok = self.current_tok
            self.advance()
            right = func()
            if right is None:
                raise ParserError(f"Invalid syntax after operator '{op_tok.type}'", op_tok)
            left = BinOpNode(left, op_tok, right)
        return left


def print_ast(node, indent='', last=True):
    prefix = indent + ('└── ' if last else '├── ')
    if isinstance(node, NumberNode):
        print(prefix + f'Number({node.tok.value})')
    elif isinstance(node, BinOpNode):
        print(prefix + f'Operation({node.op_tok.type})')
        new_indent = indent + ('    ' if last else '│   ')
        print_ast(node.left_node, new_indent, False)
        print_ast(node.right_node, new_indent, True)
    elif isinstance(node, FuncNode):
        print(prefix + f'Function({node.func_tok.type})')
        new_indent = indent + ('    ' if last else '│   ')
        print_ast(node.arg_node, new_indent, True)
    else:
        print(prefix + 'Unknown node')


def run(text):
    lexer = Lexer(text)
    tokens, error = lexer.make_tokens()
    if error:
        return None, error
    parser = Parser(tokens)
    try:
        ast = parser.parse()
        return ast, None
    except ParserError as pe:
        return None, pe.as_string()
    except Exception as e:
        return None, str(e)


# REPL
while True:
    input_operation = input('Enter operation: ')
    result, error = run(input_operation)
    if error:
        print(error if isinstance(error, str) else error.as_string())
    else:
        print_ast(result)
