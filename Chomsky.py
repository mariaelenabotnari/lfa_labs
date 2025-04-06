import itertools

class Chomsky:
    def __init__(self, Vn, Vt, P, S):
        self.Vn = Vn
        self.Vt = Vt
        self.P = P
        self.P_dictionary = {}
        self.S = S
        self.rules = {}

        pairs = self.P.split(", ")
        for pair in pairs:
            a, b = pair.split("->")
            if "|" in b:
                rules = b.split("|")
            else:
                rules = [b]

            rules_with_spaces = [' '.join(rule) for rule in rules]

            if a in self.P_dictionary:
                self.P_dictionary[a].extend(rules_with_spaces)
            else:
                self.P_dictionary[a] = rules_with_spaces

        print("\nInitial production rules:")
        print(self.display_P_dictionary(self.P_dictionary))

    def eliminate_epsilons(self):
        print("\nStep 1: Eliminated ε-productions:")
        nullable = set()

        changed = True
        while changed:
            changed = False
            for left, rights in self.P_dictionary.items():
                for rule in rights:
                    if rule == "ε" or all(symbol in nullable for symbol in rule.split()):
                        if left not in nullable:
                            nullable.add(left)
                            changed = True

        new_P_dict = {}
        for left, rights in self.P_dictionary.items():
            new_rules = set()
            for rule in rights:
                if rule == "ε":
                    continue
                symbols = rule.split()
                positions = [i for i, sym in enumerate(symbols) if sym in nullable]

                all_combinations = []
                for r in range(len(positions) + 1):
                    for combo in itertools.combinations(positions, r):
                        all_combinations.append(combo)

                for combo in all_combinations:
                    new_rule = [symbols[i] for i in range(len(symbols)) if i not in combo]
                    if new_rule:
                        new_rules.add(" ".join(new_rule))
                    elif left == self.S:
                        new_rules.add("ε")

            new_P_dict[left] = list(new_rules)

        self.P_dictionary = new_P_dict
        print(self.display_P_dictionary(self.P_dictionary))


    def eliminate_unit_rules(self):
        for left in list(self.P_dictionary.keys()):
            rules = list(self.P_dictionary[left])
            new_rules = []

            for rule in rules:
                if len(rule) == 1 and rule in self.Vn:
                    new_rules.extend(self.P_dictionary[rule])

            self.P_dictionary[left] = [r for r in rules if not (len(r) == 1 and r in self.Vn)] + new_rules

        print("\nStep 2: Eliminated unit rules:")
        print(self.display_P_dictionary(self.P_dictionary))

    def eliminate_inaccessible_symbols(self):
        print("\nStep 3: Eliminating inaccessible symbols:")
        accessible = set()
        queue = [self.S]

        while queue:
            current = queue.pop()
            if current not in accessible:
                accessible.add(current)
                for rule in self.P_dictionary.get(current, []):
                    for symbol in rule.split():
                        if symbol in self.Vn and symbol not in accessible:
                            queue.append(symbol)

        to_remove = [nt for nt in self.Vn if nt not in accessible]

        for nt in to_remove:
            if nt in self.P_dictionary:
                del self.P_dictionary[nt]

        self.Vn = [nt for nt in self.Vn if nt in accessible]
        print(self.display_P_dictionary(self.P_dictionary))


    def eliminate_nonproductive_symbols(self):
        print("\nStep 4: Eliminating non-productive symbols:")
        productive = set()
        changed = True

        while changed:
            changed = False
            for left, rights in self.P_dictionary.items():
                for rule in rights:
                    symbols = rule.split()
                    if all(symbol in self.Vt or symbol in productive for symbol in symbols):
                        if left not in productive:
                            productive.add(left)
                            changed = True

        to_remove = [nt for nt in self.Vn if nt not in productive]

        for nt in to_remove:
            if nt in self.P_dictionary:
                del self.P_dictionary[nt]

        self.Vn = [nt for nt in self.Vn if nt in productive]
        print(self.display_P_dictionary(self.P_dictionary))


    def convert_rhs_to_terminals_or_nonterminals(self):
        print("\nStep 5: RHS with just terminals or nonterminals:")
        terminal_to_nonterminal = {}
        counter = 0

        for left in list(self.P_dictionary.keys()):
            rules = list(self.P_dictionary[left])
            new_rules = []
            for rule in rules:
                if len(rule) >= 2:
                    new_rule = ""
                    for char in rule:
                        if char in self.Vt:
                            if char not in terminal_to_nonterminal:
                                symbol = f"X{counter}"
                                counter += 1
                                terminal_to_nonterminal[char] = symbol
                                self.P_dictionary[symbol] = [char]
                                self.Vn.append(symbol)
                            new_rule += terminal_to_nonterminal[char]
                        else:
                            new_rule += char
                    new_rules.append(new_rule)
                else:
                    new_rules.append(rule)

            self.P_dictionary[left] = new_rules

        print(self.display_P_dictionary(self.P_dictionary))


    def convert_rhs_to_1_terminal_or_2_nonterminals(self):
        print("\n Step 6: RHS with just 1 terminal or 2 nonterminals")
        counter = 0
        terminals_to_nonterminal = {}
        for left in list(self.P_dictionary.keys()):
            rules = list(self.P_dictionary[left])
            new_rules = []

            for rule in rules:
                symbols = rule.strip().split()

                if len(symbols) <= 2:
                    new_rules.append(" ".join(symbols))

                elif len(symbols) == 3:
                    first_two = " ".join(symbols[:2])
                    if first_two not in terminals_to_nonterminal:
                        new_nonterminal = f"Y{counter}"
                        counter += 1
                        terminals_to_nonterminal[first_two] = new_nonterminal
                        self.P_dictionary[new_nonterminal] = [first_two]
                        self.Vn.append(new_nonterminal)
                    new_rule = terminals_to_nonterminal[first_two] + " " + symbols[2]
                    new_rules.append(new_rule)

                elif len(symbols) == 4:
                    first_two = " ".join(symbols[:2])
                    if first_two not in terminals_to_nonterminal:
                        new_nonterminal1 = f"Y{counter}"
                        counter += 1
                        terminals_to_nonterminal[first_two] = new_nonterminal1
                        self.P_dictionary[new_nonterminal1] = [first_two]
                        self.Vn.append(new_nonterminal1)
                    else:
                        new_nonterminal1 = terminals_to_nonterminal[first_two]
                    next_pair = new_nonterminal1 + " " + symbols[2]
                    if next_pair not in terminals_to_nonterminal:
                        new_nonterminal2 = f"Y{counter}"
                        counter += 1
                        terminals_to_nonterminal[next_pair] = new_nonterminal2
                        self.P_dictionary[new_nonterminal2] = [next_pair]
                        self.Vn.append(new_nonterminal2)
                    else:
                        new_nonterminal2 = terminals_to_nonterminal[next_pair]
                    new_rule = new_nonterminal2 + " " + symbols[3]
                    new_rules.append(new_rule)

                elif len(symbols) == 5:
                    first_two = " ".join(symbols[:2])
                    if first_two not in terminals_to_nonterminal:
                        new_nonterminal1 = f"Y{counter}"
                        counter += 1
                        terminals_to_nonterminal[first_two] = new_nonterminal1
                        self.P_dictionary[new_nonterminal1] = [first_two]
                        self.Vn.append(new_nonterminal1)
                    else:
                        new_nonterminal1 = terminals_to_nonterminal[first_two]
                    next_pair = new_nonterminal1 + " " + symbols[2]
                    if next_pair not in terminals_to_nonterminal:
                        new_nonterminal2 = f"Y{counter}"
                        counter += 1
                        terminals_to_nonterminal[next_pair] = new_nonterminal2
                        self.P_dictionary[new_nonterminal2] = [next_pair]
                        self.Vn.append(new_nonterminal2)
                    else:
                        new_nonterminal2 = terminals_to_nonterminal[next_pair]
                    next_pair2 = new_nonterminal2 + " " + symbols[3]
                    if next_pair2 not in terminals_to_nonterminal:
                        new_nonterminal3 = f"Y{counter}"
                        counter += 1
                        terminals_to_nonterminal[next_pair2] = new_nonterminal3
                        self.P_dictionary[new_nonterminal3] = [next_pair2]
                        self.Vn.append(new_nonterminal3)
                    else:
                        new_nonterminal3 = terminals_to_nonterminal[next_pair2]

                    new_rule = new_nonterminal3 + " " + symbols[4]
                    new_rules.append(new_rule)

            self.P_dictionary[left] = new_rules

        print(self.display_P_dictionary(self.P_dictionary))


    def chomsky_normal_form(self):
        self.eliminate_epsilons()
        self.eliminate_unit_rules()
        self.eliminate_inaccessible_symbols()
        self.eliminate_nonproductive_symbols()
        self.convert_rhs_to_terminals_or_nonterminals()
        self.convert_rhs_to_1_terminal_or_2_nonterminals()
        self.rules = self.P_dictionary

    def display_P_dictionary(self, P_dictionary):
        result = []

        for left, rights in P_dictionary.items():
            if rights:
                rhs = '|'.join(rights)
                result.append(f"{left}->{rhs}")

        return ', '.join(result)


if __name__ == "__main__":
    Vn = ["S", "A", "B", "C", "E"]
    Vt = ["a", "d"]
    P = "S->dB|A, A->d|dS|aAdAB, B->aC|aS|AC, C->ε, E->AS"
    S = "S"

    chomsky = Chomsky(Vn, Vt, P, S)
    chomsky.chomsky_normal_form()
