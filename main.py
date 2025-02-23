import random

class Grammar:
    def __init__(self, Vn, Vt, P, S):
        self.Vn = Vn
        self.Vt = Vt
        self.P = P
        self.P_dictionary = {}
        self.S = S

        pairs = self.P.split(", ")
        for pair in pairs:
            a, b = pair.split("->")
            if "|" in b:
                rules = b.split("|")
            else:
                rules = [b]

            if a in self.P_dictionary:
                self.P_dictionary[a].extend(rules)
            else:
                self.P_dictionary[a] = rules

    def generate_string(self):
        string = self.S
        steps = []

        while any(char in self.Vn for char in string):
            new_string = ""
            for char in string:
                if char in self.P_dictionary:
                    new_string += random.choice(self.P_dictionary[char])
                else:
                    new_string += char
            steps.append(f"{string} -> {new_string}")
            string = new_string

        return string, steps

    def generate_5_strings(self):
        strings = set()

        while len(strings) < 5:
            new_string, steps = self.generate_string()
            strings.add(new_string)
            print(f"The steps taken to generate {new_string}: ", steps)

        return strings

    def reverse_dictionary(self):
        reversed_P_dictionary = {}

        for key, values in self.P_dictionary.items():
            for value in values:
                if value not in reversed_P_dictionary:
                    reversed_P_dictionary[value] = []
                reversed_P_dictionary[value].append(key)

        return reversed_P_dictionary

    def check_string(self, string):
        reversed_P_dictionary = self.reverse_dictionary()
        current_strings = [list(string)]
        transitions = []

        while current_strings:
            new_strings = []
            for s in current_strings:
                if "".join(s) == self.S:
                    transitions.append(f"Valid derivation: {self.S} -> {''.join(string)}")
                    return transitions

                for i in range(len(s)):
                    substring = "".join(s[i:i + 2])
                    if substring in reversed_P_dictionary:
                        for replacement in reversed_P_dictionary[substring]:
                            new_string = s[:i] + [replacement] + s[i + 2:]
                            new_strings.append(new_string)
                            transitions.append(f"{''.join(s)} <- {''.join(new_string)}")

                    elif s[i] in reversed_P_dictionary:
                        for replacement in reversed_P_dictionary[s[i]]:
                            new_string = s[:i] + [replacement] + s[i + 1:]
                            new_strings.append(new_string)
                            transitions.append(f"{''.join(s)} <- {''.join(new_string)}")

            current_strings = new_strings

        return ["No valid derivation found."]

    def check_grammar_type(self):
        type_3 = True
        type_2 = True
        type_1 = True

        for left_part, right_parts in self.P_dictionary.items():
            if len(left_part) != 1 or left_part not in self.Vn:
                type_2 = False

            for right_part in right_parts:
                if not ((len(right_part) == 1 and right_part in self.Vt) or
                        (len(right_part) == 2 and right_part[0] in self.Vt and right_part[1] in self.Vn)):
                    type_3 = False

                if len(right_part) < len(left_part):
                    type_1 = False

        if type_3:
            print("\nType 3 Grammar (Regular Grammar):")
            print("Each production rule follows the form 'A → aB' or 'A → a'.")
            print(
                "Regular grammars can be either right-linear, where non-terminals appear at the end, or left-linear, where they appear at the beginning.")
            print(
                "These grammars can be converted into finite automata and are commonly used in lexical analysis and defining regular expressions.")
            print("Example: S → aS | bA | ε, where ε represents an empty string.")

        elif type_2:
            print("\nType 2 Grammar (Context-Free Grammar):")
            print("The left-hand side of each production rule consists of a single non-terminal.")
            print("The right-hand side can contain terminals and non-terminals in any order.")
            print(
                "Context-free grammars are widely used in defining the syntax of programming languages and in parsing algorithms.")
            print("Example: S → aSb | ε.")

        elif type_1:
            print("\nType 1 Grammar (Context-Sensitive Grammar):")
            print("Each production rule must have a right-hand side that is at least as long as the left-hand side.")
            print(
                "These grammars are more powerful than context-free grammars and can define languages that require more computational power to parse.")
            print("They are used in natural language processing and advanced compiler optimizations.")
            print("Example: AB → ABC | aB.")

        else:
            print("\nType 0 Grammar (Unrestricted Grammar):")
            print("There are no restrictions on the form of production rules.")
            print("These grammars can describe the most complex languages and require a Turing machine to recognize.")
            print("They are used in formal language theory and studies of computability.")
            print("Example: AB → BA | a.")


class FA:
    def __init__(self, Vn, Vt, P, S):
        self.Vn = Vn
        self.Vt = Vt
        self.P = P
        self.S = S
        self.P_dictionary = {}

        pairs = self.P.split(", ")
        for pair in pairs:
            a, b = pair.split("->")
            if "|" in b:
                rules = b.split("|")
            else:
                rules = [b]

            if a in self.P_dictionary:
                self.P_dictionary[a].extend(rules)
            else:
                self.P_dictionary[a] = rules

    def convert_grammar_to_fa(self):
        states = set(self.Vn)
        transitions = {}
        accepting_states = set()
        start_state = self.S

        for left, right_parts in self.P_dictionary.items():
            for right in right_parts:
                if len(right) == 1 and right in self.Vt:
                    accepting_states.add(left)
                elif len(right) == 2 and right[0] in self.Vt and right[1] in self.Vn:
                    transitions[(left, right[0])] = right[1]

        return states, transitions, accepting_states, start_state

    def check_string_via_transition(self, string):
        states, transitions, accepting_states, current_state = self.convert_grammar_to_fa()
        steps = [f"Start at {current_state}"]

        for symbol in string:
            if (current_state, symbol) in transitions:
                next_state = transitions[(current_state, symbol)]
                steps.append(f"Read '{symbol}', move from {current_state} to {next_state}")
                current_state = next_state
            else:
                steps.append(f"Read '{symbol}', no transition exists. String rejected.")
                return steps

        if current_state in accepting_states:
            steps.append(f"String accepted: Ended in accepting state {current_state}.")
        else:
            steps.append(f"String rejected: Ended in non-accepting state {current_state}.")

        return steps


if __name__ == "__main__":
    Vn = ["S", "D", "R"]
    Vt = ["a", "b", "c", "d", "f"]
    P = "S->aS|bD|fR, D->cD|dR, R->bR|f, D->d"
    S = "S"

    grammar = Grammar(Vn, Vt, P, S)
    five_strings = grammar.generate_5_strings()
    print("\n5 Unique Strings:", five_strings)

    result1 = grammar.check_string('abd')
    print("\nChecking if the string abd was obtained via the finite set of production of rules from the Grammar:")
    print(result1)

    fa = FA(Vn, Vt, P, S)
    states, transition, terminals, start_state = fa.convert_grammar_to_fa()
    print("\nConverting the object of type Grammar to type Finite Automaton")
    print("States: ", states)
    print("Tansitions: ", transition)
    print("Terminals: ", terminals)
    print("Start state: ", start_state)

    result2 = fa.check_string_via_transition('abd')
    print("\nChecking if the string abd can be obtained via the state transition from FA:")
    print(result2)

    grammar.check_grammar_type()




