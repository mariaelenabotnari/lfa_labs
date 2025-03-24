# Laboratory Work Nr. 3: Regular Expressions

__Course: Formal Languages & Finite Automata__  

__Author: Botnari Maria-Elena, FAF-232__

# Theory
Regular expressions (regex) are a powerful tool in formal language theory and finite automata, allowing us to define patterns within sequences of symbols. These patterns are widely used in text processing, search algorithms, lexical analysis, and even in defining the syntax of programming languages. A regular expression is essentially a **string that defines a search pattern**, often used to match, extract, or replace specific sequences within a larger text. The foundation of regular expressions is deeply connected to **finite automata**, as each regular expression can be represented by a deterministic or non-deterministic finite automaton (DFA or NFA). The fundamental components of regex include **concatenation (AB), alternation (A|B), repetition operators (*, +, ?), and grouping (parentheses)**. These constructs allow us to create expressions that can define highly specific patterns. In practical applications, regular expressions are extensively used in **compilers, search engines, data validation, and artificial intelligence models** that rely on text processing. By understanding and implementing regular expressions, we gain insight into the underlying mechanics of pattern recognition and computational linguistics.

For this lab, we focus on **generating valid sequences based on given regular expressions**. The challenge lies in correctly interpreting each regex operator and ensuring that our code adheres to the constraints provided. For example, the `*` operator means that a preceding symbol may appear **zero or more times**, while `+` ensures that it appears at least **once**. Since regex can lead to an infinite number of possible strings (especially with unbounded repetition), we impose a **limit of five repetitions** to keep output manageable. The core objective is to create an algorithm that translates a given regex into a **randomly generated valid string**, ensuring that all regex rules are followed.

# Objectives

1. Write and cover what regular expressions are, what they are used for;

2. Below you will find 3 complex regular expressions per each variant. Take a variant depending on your number in the list of students and do the following:

    a. Write a code that will generate valid combinations of symbols conform given regular expressions (examples will be shown).

    b. In case you have an example, where symbol may be written undefined number of times, take a limit of 5 times (to evade generation of extremely long combinations);

# Implementation Description

**Handling * (Zero or More Repetitions)**

````
if char == "*":
    prev_char = self.expr[i - 1]
    if prev_char not in {")"}:
        random_number = random.randint(0, 5)
        string.append(self.chars[-1] * random_number)
    else:
        random_number = random.randint(0, 5)
        string.append(string[-1] * random_number)
        string[-2] = ' '

````

• The function first checks if the current character (char) is "*", which means "repeat the previous character or group zero or more times."

• It retrieves the character immediately before "*" using prev_char = self.expr[i - 1].

• If prev_char is not a closing parenthesis (")"), then "*" applies to a single character.

• The function randomly selects a number (random_number) between 0 and 5, using random.randint(0, 5), which determines how many times the character will be repeated.

• That character is multiplied by random_number and appended to the string list.

• If prev_char is a closing parenthesis (")"), "*" applies to a group of characters rather than a single one. The function repeats the last generated substring (string[-1]) instead.


▷ Example 1:\
Expression: "A*"\
random_number = 3 → Output: "AAA"\
random_number = 0 → Output: "" (empty string)

▷Example 2 (Group):\
Expression: "(XY)*"\
random_number = 4 → Output: "XYXYXYXY"\
random_number = 1 → Output: "XY"\
random_number = 0 → Output: ""

\
\
**Handling + (One or More Repetitions)**

````
if char == "+":
    prev_char = self.expr[i - 1]
    if prev_char not in {")"}:
        random_number = random.randint(1, 5)
        string.append(self.chars[-1] * random_number)
    else:
        random_number = random.randint(1, 5)
        string.append(string[-1] * random_number)
        string[-2] = ' '

````

• The function detects "+", meaning "repeat the previous character at least once."

• Like "*", it retrieves prev_char, the character before "+", to determine what should be repeated.

• Instead of allowing 0 repetitions like "*", the function ensures at least one repetition by using random.randint(1, 5).

• If prev_char is not a closing parenthesis, "+" applies to a single character.

• If prev_char is a closing parenthesis, it applies to a group of characters.

▷ Example 1:\
Expression: "B+"\
random_number = 3 → Output: "BBB"\
random_number = 5 → Output: "BBBBB"\
random_number = 1 → Output: "B"

▷ Example 2 (Group):\
Expression: "(CD)+"\
random_number = 4 → Output: "CDCDCDCD"\
random_number = 1 → Output: "CD"

\
\
**Handling ^ (Exact Repetition)**

````
if char == "^":
    prev_char = self.expr[i - 1]
    if prev_char not in {")"}:
        string.append(self.chars[-1] * int(self.expr[i + 1]))
    else:
        string.append(string[-1] * int(self.expr[i + 1]))
        string[-2] = " "

````

• The function detects ^, which enforces exact repetition.

• It looks at the preceding character (prev_char) to determine what needs to be repeated.

• If prev_char is not a closing parenthesis (")"), then ^N applies to a single character.

• The function reads the next character (self.expr[i + 1]), which represents the exact number of times to repeat.

• This number is converted to an integer with int(self.expr[i + 1]), ensuring proper numerical calculations.

• The function then multiplies prev_char by this number and appends it to string.

• If prev_char is a closing parenthesis, then ^N applies to a group of characters.

• The function repeats the last generated substring (string[-1]).

▷ Example 1:\
Expression: "X^3"\
The function processes "X" and repeats it exactly 3 times.\
Output: "XXX"

▷ Example 2 (Group):\
Expression: "(YZ)^2"\
The function treats "YZ" as a group and repeats it twice.\
Output: "YZYZ"

▷ Example 3 (Error Handling):\
Expression: "A^B" (invalid because B is not a number)\
The function assumes a number follows ^. If it encounters a non-numeric character, it may cause an error.

\
\
**Handling ? (Optional Character)**

````
if char == "?":
    prev_char = self.expr[i - 1]
    random_number = random.randint(0, 1)
    string.append(prev_char * random_number)

````

• The function checks if char is "?", meaning the preceding character is optional.

• It retrieves prev_char, the character before "?", since "?" applies to that character.

• A random number (0 or 1) is chosen using random.randint(0, 1):

• 0 means omit the character.

• 1 means include the character once.

• The character is then multiplied by the random number.

• If random_number = 0, it results in "" (an empty string).

• If random_number = 1, the character appears once.

▷ Example 1:\
Expression: "Z?"\
random_number = 0 → Output: "" (empty)\
random_number = 1 → Output: "Z"

▷ Example 2:\
Expression: "(AB)?"\
random_number = 0 → Output: ""\
random_number = 1 → Output: "AB"

\
\
**Handling | (Alternation - Choice Between Multiple Options)**

````
if char == "|":
    choices = [self.chars[-1]]

    if i + 1 < len(self.expr):
        next_char = self.expr[i + 1]
        choices.append(next_char)

    while i + 2 < len(self.expr) and self.expr[i + 2] == "|":
        i += 2
        if i + 1 < len(self.expr):
            choices.append(self.expr[i + 1])

    random_choice = random.choice(choices)
    string.append(random_choice)
````

• The | symbol represents alternation, meaning that at this position in the expression, one of multiple possible characters or groups can be chosen.

• When encountering a |, the function first retrieves the last character processed (self.chars[-1]), assuming it is one of the options available for selection.

• The function then checks if there is a character after | (next_char = self.expr[i + 1]). If so, this character is also added to the choices list.

• If multiple consecutive | symbols are detected (for example A|B|C), the function enters a loop:
   1. It moves past the | symbols (i += 2 ensures that it jumps over | and lands on the next character).\
   2. If there is another character (self.expr[i + 1]), it is also added to choices.

• After identifying all possible choices, the function randomly selects one from choices using random.choice(choices), ensuring fair randomness in selection.

• The randomly chosen character is then appended to string, meaning that only one of the possible characters will appear in the generated output.

▷ Example 1:\
Expression: "A|B|C"\
The function recognizes that A, B, and C are all valid choices.\
It randomly selects one of them.\
Possible outputs: "A", "B", or "C".

▷ Example 2 (Group Usage):\
Expression: "(X|Y)Z"\
The function sees (X|Y) and recognizes X and Y as choices.\
It picks one and continues processing the rest of the expression.\
Possible outputs: "XZ" or "YZ".


# Results 
````
Strings generated from the first regular expression: 
O PP 2 4
O QQQQQ 2 4
O PPPP 2 3
O QQQQ 2 4
O QQ 2 3
O RR 2 4
````

````
Strings generated from the second regular expression: 
A B C E II
AAA B C E HH
 B E E II
AA B C E HH
A B E E GG
AAAAA B E E II
````

````
Strings generated from the third regular expression: 
JJ K L O QQQ
JJJJ K LLLL O PPP
JJJ K MMMM O PPP
J K LL  PPP
J K MMMMM  PPP
JJJJ K LLLLL O QQQ
````

# Conclusion
In conclusion, regular expressions are a powerful and essential tool for defining and recognizing patterns in text, widely used in programming, data validation, and search operations. Through this lab, we explored how different regex operators like `*`, `+`, `?`, `|`, and `^` work to generate structured sequences, ensuring that our code correctly interprets and applies these rules. By implementing a function that generates valid strings based on a given regex, we gained practical experience in handling **pattern matching and sequence generation**. Additionally, setting a limit on repeated characters helped us avoid infinite loops and overly long outputs. The process of breaking down the regex into steps and tracking the execution sequence allowed us to better understand how expressions are processed internally. While some challenges arose, such as handling groups of characters and ensuring correct precedence of operations, the structured approach helped us overcome these difficulties. Overall, this lab reinforced key concepts of **formal languages and finite automata**, giving us deeper insight into how regex engines work and how they can be applied in real-world scenarios.