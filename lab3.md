# Laboratory Work Nr. 3: Lexer & Scanner

__Course: Formal Languages & Finite Automata__  

__Author: Botnari Maria-Elena, FAF-232__

# Theory

Lexical analysis, also known as scanning or tokenization, is a fundamental process in the compilation and interpretation of programming languages, markup languages, and other structured text formats. It involves analyzing a sequence of characters to identify meaningful units known as lexemes, which are then classified into tokens based on predefined rules. The primary purpose of a lexer (or tokenizer/scanner) is to break down the input into manageable components that the next stages of processing—such as parsing—can work with. Unlike lexemes, which are simply substrings extracted based on delimiters like whitespace, tokens provide a higher level of abstraction by categorizing lexemes into types, such as keywords, identifiers, numbers, or operators. A lexer typically operates using deterministic finite automata (DFA), transitioning between states to recognize patterns defined by regular expressions. For instance, numeric tokens might be recognized by a sequence of digits, while keywords are matched against a reserved set of words. The lexer's role is crucial in language processing because it not only simplifies parsing but also allows for early detection of errors, such as illegal characters. In a broader context, lexical analysis is essential in domains beyond compilers, including data validation, natural language processing, and code highlighting in IDEs. Implementing a lexer requires designing a system that correctly identifies and processes input symbols while managing position tracking, error handling, and token classification. A well-structured lexer ensures efficiency, correctness, and maintainability in the language processing pipeline.


# Objectives
1. Understand what lexical analysis is.
2. Get familiar with the inner workings of a lexer/scanner/tokenizer.
3. Implement a sample lexer and show how it works.

# Implementation Description
The **Error** class is a fundamental part of this program, as it is responsible for storing and formatting error messages when something goes wrong during the processing of the input. This class ensures that users receive clear feedback about mistakes in their input, making it easier to debug issues.

\
**Attributes and Constructor**\
When an error occurs, the program needs to store essential details about it. 

The Error class has four attributes:


  1) **pos_start**: This represents where in the input text the error starts. It is an instance of the Position class, which keeps track of the index, line number, and column number.
2) **pos_end**: This marks where the error ends. Some errors involve multiple characters, so tracking the start and end positions helps identify the exact range of the problem.
3) **error_name**: A string that indicates the type of error, such as "Illegal Character" or "Syntax Error". Having a specific name helps categorize different issues.
4) **details**: This provides additional information about what went wrong, such as the specific character that caused the error.

\
**Error Formatting (as_string Method)**\
This method generates a human-readable message that describes the error. It combines:
1) **The error_name** (for example, "Illegal Character").
2) **The details** (for example, "Unexpected symbol @").
3) The exact **location of the error** in the input text, using pos_start.line_nr + 1 and pos_start.column_nr + 1. 

````
class Error:
    def __init__(self, pos_start, pos_end, error_name, details):
        self.pos_start = pos_start
        self.pos_end = pos_end
        self.error_name = error_name
        self.details = details

    def as_string(self):
        return f"{self.error_name}: {self.details}\n" \
               f"At line {self.pos_start.line_nr + 1}, column {self.pos_start.column_nr + 1}"
````
\
\
The **IllegalCharError class** is a specific type of error that occurs when the user enters an invalid character that the program does not recognize. Instead of writing separate logic for illegal character errors, this class extends the Error class and predefines the error name as "Illegal Character".

\
**Inheritance from Error**\
Since an illegal character is just a type of error, this class inherits from Error. \
The super().__init__ call allows IllegalCharError to use all the functionality of Error while setting the error_name automatically. This means:\
• The pos_start and pos_end attributes are handled in the same way as in Error. \
• The details parameter is passed to describe the invalid character.

\
**Purpose and Usage**\
Whenever an invalid character is found, the Lexer (explained later) creates an instance of IllegalCharError, providing the character’s position and a description. This ensures that the program can detect and handle bad input gracefully, instead of crashing or producing incorrect results.

````
class IllegalCharError(Error):
    def __init__(self, pos_start, pos_end, details):
        super().__init__(pos_start, pos_end, 'Illegal Character', details)
````
\
\
The **Token class** is one of the most important parts of the program because it represents individual meaningful parts of the input, such as numbers, mathematical operators, and functions (cos, sin). In programming languages and calculators, these parts are known as tokens, and the process of breaking an input into tokens is called tokenization.

\
**Attributes and Constructor**\
Each token has:\
• type_: This tells what kind of token it is (for example, TT_INT for an integer, TT_PLUS for the + symbol).\
• value: Some tokens, like numbers, have actual values (for example, 5 for TT_INT). Others, like +, do not need a value, so None is used.

The constructor initializes these attributes, ensuring each token is stored correctly.

\
**Token Representation**\
This method defines how tokens are displayed when printed.\
• If the token has a value (like a number), it is displayed as TT_INT:5.\
• If the token does not have a value (like +), it is displayed as TT_PLUS.

This makes debugging easier because developers can quickly see what tokens the program has created from the input.
````
class Token:
    def __init__(self, type_, value=None):
        self.type = type_
        self.value = value

    def __repr__(self):
        return f'{self.type}:{self.value}' if self.value is not None else f'{self.type}'
````
\
\
The **Position class** is responsible for keeping track of where the program is currently reading in the input text. This is crucial for error handling and tokenization, as it allows the program to know which character it is processing, on which line, and at what column.

\
**Attributes and Constructor**\
• index: The current position in the text as a number (for example, 0 for the first character, 1 for the second).\
• line_nr: The current line number. This starts at 0 and increases when a newline character (\n) is encountered.\
• column_nr: The column position within the current line, which resets when moving to a new line.

This setup ensures that every character in the input is uniquely identified by its index, line, and column.

\
**Advancing the Position (advance Method)**\
Each time the program reads a new character, advance() updates the Position:\
• It increases index by 1.\
• It increases column_nr by 1.\
• If the character is a newline (\n), it moves to the next line and resets column_nr to 0.

\
**Copying Positions (copy Method)**\
Since position tracking is important, copy() creates a duplicate of the current position. This is useful when saving the starting position of an error or a token before moving forward.
````
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
````
\
\
The **Lexer** is the core component that reads the input text and converts it into tokens. It is responsible for recognizing numbers, mathematical symbols, functions (sin, cos), and handling errors.

\
**Attributes and Constructor**\
• text: The input string that needs to be tokenized.\
• pos: A Position object to keep track of where we are in the text.\
• current_char: The current character being processed.

At the start, pos is set to -1 (before the first character), and advance() is called to load the first character.

\
**Moving Through the Text (advance Method)**

This method:
1) Calls self.pos.advance(self.current_char) to update the position.
2)  Updates self.current_char to the next character or None if the end of the text is reached.

\
**Generating Tokens (make_tokens Method)**\
This method scans the text character by character:\
• If it finds whitespace (\t or space), it skips it.\
• If it finds +, -, *, /, (, ), it creates the corresponding token.\
• If it finds letters, it assumes it is a function (sin, cos, etc.) and calls make_function().\
• If it finds a number, it calls make_number() to process it.\
• If it finds an invalid character, it returns an IllegalCharError.\
• This method loops until the entire input is processed.

\
**Processing Functions (make_function Method)**\
If the lexer finds a sequence of letters, it checks if it matches a known function (cos, sin, tg, ctg). If it does, it creates the corresponding token. Otherwise, it returns an IllegalCharError.

\
**Processing Numbers (make_number Method)**\
If a number is found:\
• It reads all consecutive digits.\
• It allows one decimal point (.) for floating-point numbers.\
• It creates a TT_INT token if no decimal is found, otherwise TT_FLOAT.

````
class Lexer:
    def __init__(self, text):
        self.text = text
        self.pos = Position(-1, 0, -1)
        self.current_char = None
        self.advance()

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
                tokens.append(Token(TT_MUL))...
                
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
````

# Results
````
Enter operation: cos(5) * sin(0.3) + (2 - 3)/100
[COS, LPAREN, INT:5, RPAREN, MUL, SIN, LPAREN, FLOAT:0.3, RPAREN, PLUS, LPAREN, INT:2, MINUS, INT:3, RPAREN, DIV, INT:100]

Enter operation: coz(4)
Illegal Character: Unknown function 'coz'
At line 1, column 1

Enter operation: sin(1..4(
Illegal Character: '.' is not a valid token.
At line 1, column 7
````

# Conclusion

This laboratory work provided a hands-on approach to understanding lexical analysis and the role of a lexer in processing structured text. By implementing a lexer, the objectives were successfully met: we explored the theory behind lexical analysis, examined how a lexer functions internally, and developed a working implementation that can tokenize input based on predefined rules. The code effectively demonstrated key concepts such as token classification, error handling, and position tracking, reinforcing the fundamental principles of lexical analysis. Through this, we gained insight into how programming languages and interpreters perform the first step of transforming raw text into structured data for further processing.