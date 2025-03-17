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


class Error:
    def __init__(self, pos_start, pos_end, error_name, details):
        self.pos_start = pos_start
        self.pos_end = pos_end
        self.error_name = error_name
        self.details = details

    def as_string(self):
        return f"{self.error_name}: {self.details}\n" \
               f"At line {self.pos_start.line_nr + 1}, column {self.pos_start.column_nr + 1}"


class IllegalCharError(Error):
    def __init__(self, pos_start, pos_end, details):
        super().__init__(pos_start, pos_end, 'Illegal Character', details)


class Token:
    def __init__(self, type_, value=None):
        self.type = type_
        self.value = value

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
        self.current_char = self.text[self.pos.index] if self.pos.index < len(self.text) else None

    def make_tokens(self):
        tokens = []
        while self.current_char is not None:
            if self.current_char in '\t ':
                self.advance()
            elif self.current_char == '+':
                tokens.append(Token(TT_PLUS))
                self.advance()
            elif self.current_char == '-':
                tokens.append(Token(TT_MINUS))
                self.advance()
            elif self.current_char == '*':
                tokens.append(Token(TT_MUL))
                self.advance()
            elif self.current_char == '/':
                tokens.append(Token(TT_DIV))
                self.advance()
            elif self.current_char == '(':
                tokens.append(Token(TT_LPAREN))
                self.advance()
            elif self.current_char == ')':
                tokens.append(Token(TT_RPAREN))
                self.advance()
            elif self.current_char.isalpha():
                function_or_error = self.make_function()
                if isinstance(function_or_error, IllegalCharError):
                    return [], function_or_error.as_string()
                tokens.append(function_or_error)
            elif self.current_char in DIGITS:
                tokens.append(self.make_number())
            else:
                pos_start = self.pos.copy()
                char = self.current_char
                self.advance()
                return [], IllegalCharError(pos_start, self.pos, f"'{char}' is not a valid token.").as_string()

        return tokens, None

    def make_function(self):
        func_str = ''
        pos_start = self.pos.copy()

        while self.current_char is not None and self.current_char.isalpha():
            func_str += self.current_char
            self.advance()

        if func_str == 'cos':
            return Token(TT_COS)
        elif func_str == 'sin':
            return Token(TT_SIN)
        elif func_str == 'tg':
            return Token(TT_TG)
        elif func_str == 'ctg':
            return Token(TT_CTG)
        else:
            return IllegalCharError(pos_start, self.pos, f"Unknown function '{func_str}'")

    def make_number(self):
        num_str = ''
        dot_count = 0

        while self.current_char is not None and self.current_char in DIGITS + '.':
            if self.current_char == '.':
                if dot_count == 1:
                    break
                dot_count += 1
                num_str += '.'
            else:
                num_str += self.current_char
            self.advance()

        if dot_count == 0:
            return Token(TT_INT, int(num_str))
        else:
            return Token(TT_FLOAT, float(num_str))


def run(text):
    lexer = Lexer(text)
    tokens, error = lexer.make_tokens()
    return tokens, error


while True:
    input_operation = input('Enter operation: ')
    result, error = run(input_operation)

    if error:
        print(error if isinstance(error, str) else error.as_string())
    else:
        print(result)
