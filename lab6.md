# Laboratory Work Nr. 6: Parser & Building an Abstract Syntax Tree

__Course: Formal Languages & Finite Automata__  

__Author: Botnari Maria-Elena, FAF-232__


# Theory

Parsing is the process of analyzing the structure of text to understand its meaning in a way that a computer can work with. It's like teaching a computer to read and understand simple expressions, such as math formulas or parts of a programming language. To do this, we usually break the input text into **tokens**. This process is done by a component called a **lexer**, which uses **regular expressions** to recognize and group characters from the input into these tokens. After the lexer finishes, a **parser** takes over. The parser looks at the order of tokens and tries to organize them into a meaningful structure using grammar rules—these are the rules that define what a valid expression looks like. The result of this is an **Abstract Syntax Tree (AST)**, which is a simplified, structured representation of the expression. Each node in the AST represents a part of the expression, such as a number, a function call, or a math operation. This tree doesn’t store every single character from the original input—just the important ones that define how the expression works. The AST is useful for later steps like calculating the result of an expression, checking if something is written correctly, or transforming code into another form. In programming language interpreters and compilers, parsing and ASTs are essential because they allow programs to understand, evaluate, and transform code. In this lab, the goal is to not only use regular expressions to build tokens, but also to construct the AST using clearly defined classes and grammar-based functions, and to process input using a complete parser built around these tools.


# Objectives
1. Get familiar with parsing, what it is and how it can be programmed.
2. Get familiar with the concept of AST.
3. In addition to what has been done in the 3rd lab work do the following:\
**I**. In case you didn't have a type that denotes the possible types of tokens you need to:\
&nbsp;&nbsp;&nbsp;&nbsp;**a**. Have a type TokenType (like an enum) that can be used in the lexical analysis to categorize the tokens.\
&nbsp;&nbsp;&nbsp;&nbsp;**b**. Please use regular expressions to identify the type of the token.\
**II**. Implement the necessary data structures for an AST that could be used for the text you have processed in the 3rd lab work.\
**III**. Implement a simple parser program that could extract the syntactic information from the input text.


# Implementation

The ``make_tokens function`` is part of the Lexer class and is responsible for going through the input text character by character and turning it into a list of token objects based on specific rules. First, it defines a list of token patterns using **regular expressions**, such as patterns for integers, floats, operators like + or -, parentheses, and recognized function names like sin, cos, etc. It then compiles these patterns into one big regex using named groups and starts matching the text from the beginning. For each match, it creates a **Token object** with the corresponding type and value, and also keeps track of the start and end positions of the token using a **Position object**. It handles whitespaces by skipping them and throws an **IllegalCharError** if it encounters a character that doesn’t match any known pattern. Function names like cos, sin, tg, and ctg are specially handled by checking the matched identifier and mapping it to the corresponding token type. If it sees an unknown identifier, it throws an error immediately. The function returns the list of tokens and None if successful, or an empty list and an error if something went wrong.

````
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
````
\
The ``factor function`` is part of the Parser class and is used to handle the most basic pieces of an expression. It checks what kind of token it’s currently looking at and decides how to turn that into a node in the abstract syntax tree (AST). If the token is an integer or float, it immediately wraps it in a **NumberNode**. If the token is one of the function names (cos, sin, tg, ctg), it checks that it’s followed by a left parenthesis, then recursively parses the argument using **expression()**, then expects a right parenthesis, and wraps the whole thing into a **FuncNode**. If it sees a left parenthesis, it assumes it’s the start of a grouped expression, so it goes into **expression()** again and then expects a right parenthesis to close it. If none of these cases match, it returns None, which is interpreted as invalid syntax higher up in the parser.

````
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
````

\
The ``term function`` in the parser is in charge of handling multiplication and division. It does this by calling **bin_op** and passing it **factor** as the function to use for parsing the operands, and a tuple containing the **TT_MUL** and **TT_DIV** token types as the operators it wants to match. So essentially, it builds AST nodes that represent sequences of multiplications and divisions where each operand is a result of **factor()**. This lets it handle things like 2 * 3 or 4 / (1 + 1) correctly. It keeps applying **bin_op** as long as it finds more * or / operators.

````
    def term(self):
        return self.bin_op(self.factor, (TT_MUL, TT_DIV))
````

\
The ``expression function`` handles the highest-level operations: addition and subtraction. Just like term, it delegates the work to **bin_op**, but this time it passes **term** as the parsing function for the operands and (**TT_PLUS**, **TT_MINUS**) as the operators. That means it builds an AST for things like 2 + 3 - 4, with each piece (like 2, 3, 4) coming from lower levels of parsing that could include full subtrees like multiplications or function calls. It loops through the tokens, building up a binary operation chain from left to right.

````
    def expression(self):
        return self.bin_op(self.term, (TT_PLUS, TT_MINUS))
````

\
The ``bin_op function`` is a helper method used by term and expression to build binary operations. It starts by calling the parsing function passed to it (either **factor** or **term**) to get the left-hand side of the operation. Then it checks if the current token matches any of the operator types it was given (like +, -, *, /). If it does, it saves that operator token, moves to the next token, parses the right-hand side with the same function, and combines the left and right nodes into a **BinOpNode**. It loops as long as it keeps finding matching operators, which lets it build chains like 1 + 2 + 3 correctly, nesting them from left to right. If it fails to get a valid right-hand side after an operator, it throws a **ParserError**.

````
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
````

\
The ``NumberNode class`` is used in the AST to represent numeric values like integers or floats. It stores the token that contains the actual value (like INT:3 or FLOAT:4.5) and doesn’t do anything else. Its __repr__ method just prints the token itself so you can easily see what number it holds when printing the AST. This class is created by the **factor()** function whenever it sees a number in the token list.

````
class NumberNode:
    def __init__(self, tok):
        self.tok = tok

    def __repr__(self):
        return f'{self.tok}'
````

\
The ``FuncNode class`` represents a function call in the AST, like sin(90) or cos(0). It stores two things: the token for the function name (**TT_SIN**, **TT_COS**, etc.), and the AST node that represents the argument passed to the function. This means the argument could be a number, an expression, or even another function call. This class is created by the **factor()** function when it sees a recognized function name followed by parentheses with an expression inside. The __repr__ method prints the function token and its argument node in a readable format.

````
class FuncNode:
    def __init__(self, func_tok, arg_node):
        self.func_tok = func_tok
        self.arg_node = arg_node

    def __repr__(self):
        return f'{self.func_tok}({self.arg_node})'
````

\
The ``BinOpNode class`` is used in the AST to represent operations with two sides, like addition, subtraction, multiplication, and division. It stores the left-hand node, the operator token (like + or /), and the right-hand node. These nodes can be anything valid in the expression: numbers, function calls, or even other binary operations. This class is used by **bin_op()** to build up the structure of the entire expression. Its __repr__ method shows the full operation in parentheses, like (2 + 3) or (sin(90) * 4) so you can visualize the order of operations when printing the tree.

````
class BinOpNode:
    def __init__(self, left_node, op_tok, right_node):
        self.left_node = left_node
        self.op_tok = op_tok
        self.right_node = right_node

    def __repr__(self):
        return f'({self.left_node} {self.op_tok} {self.right_node})'
````


# Results

````
Enter operation: cos(3 + 2) / (2 + 3 * 4)
└── Operation(DIV)
    ├── Function(COS)
    │   └── Operation(PLUS)
    │       ├── Number(3)
    │       └── Number(2)
    └── Operation(PLUS)
        ├── Number(2)
        └── Operation(MUL)
            ├── Number(3)
            └── Number(4)
        
Enter operation: cos(3 - 4
Parser Error: Expected ')'
At line 1, column 9

Enter operation: 2++ 9 - 4
Parser Error: Invalid syntax after operator 'PLUS'
At line 1, column 2

Enter operation: tg(2) - coz(12)
Illegal Character: Unknown function 'coz'
At line 1, column 9

Enter operation: 3# - 9 + 4/12 - (12 + 3)
Illegal Character: '#' is not a valid token.
At line 1, column 2
````



# Conclusion

In conclusion, this laboratory work provided practical experience with the core concepts of parsing and Abstract Syntax Trees (ASTs), which are essential in the field of compilers and interpreters. By building a lexer to break down input into tokens and implementing a parser to organize these tokens into an AST, we learned how to extract and represent the syntactic structure of expressions. The use of regular expressions allowed for efficient and precise token recognition, while the tree-based structure of the AST made it easier to understand and process complex expressions in a structured way. This exercise not only helped solidify the theoretical understanding of syntax analysis but also showed how these concepts are applied in real-world programming tools. Through the design and implementation of components such as token types, nodes for the AST, and grammar-based parsing functions, we were able to simulate the early stages of how a programming language interprets input. This hands-on approach made the abstract idea of parsing more concrete and highlighted the importance of clean structure and error handling when building language-related software systems.