import random
class RegularExpression:
    def __init__(self, expr):
        self.expr = expr
        self.chars = []

    def generate_string(self):
        string = []
        i = 0
        while i < len(self.expr):
            char = self.expr[i]

            if char not in {"*", "(", ")", "|", "+", "^", "+", " ", "?"}:
                if i > 0 and self.expr[i - 1] == "^" and char in {"2", "3"}:
                    pass
                else:
                    self.chars.append(char)

            if char == "*":
                prev_char = self.expr[i - 1]
                if prev_char not in {")"}:
                    random_number = random.randint(0, 5)
                    string.append(self.chars[-1] * random_number)
                else:
                    random_number = random.randint(0, 5)
                    string.append(string[-1] * random_number)
                    string[-2] = ' '

            if char == "+":
                prev_char = self.expr[i - 1]
                if prev_char not in {")"}:
                    random_number = random.randint(1, 5)
                    string.append(self.chars[-1] * random_number)
                else:
                    random_number = random.randint(1, 5)
                    string.append(string[-1] * random_number)
                    string[-2] = ' '

            if char == "^":
                prev_char = self.expr[i - 1]
                if prev_char not in {")"}:
                    string.append(self.chars[-1] * int(self.expr[i + 1]))
                else:
                    string.append(string[-1] * int(self.expr[i + 1]))
                    string[-2] = " "

            if char == "?":
                prev_char = self.expr[i - 1]
                random_number = random.randint(0, 1)
                string.append(prev_char * random_number)

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

            if char in self.chars:
                if i + 1 < len(self.expr):
                    if self.expr[i + 1] not in {"^", "|", "*", ")", "+", "?"}:
                        string.append(char)
                else:
                    string.append(char)

            i += 1

        str = ' '.join([s for s in string if s != " "])
        print(str)


    def generate_6_strings(self):
        for i in range(6):
            string = self.generate_string()

def main():
    print("Strings generated from the first regular expression: ")
    expr1 = 'O (P|Q|R)+ 2(3|4)'
    re1 = RegularExpression(expr1)
    re1.generate_6_strings()

    print("\nStrings generated from the second regular expression: ")
    expr2 = 'A* B(C|D|E)E(G|H|I)^2'
    re2 = RegularExpression(expr2)
    re2.generate_6_strings()

    print("\nStrings generated from the third regular expression: ")
    expr2 = 'J+ K(L|M|N)* O? (P|Q)^3'
    re2 = RegularExpression(expr2)
    re2.generate_6_strings()

if __name__ == "__main__":
    main()


