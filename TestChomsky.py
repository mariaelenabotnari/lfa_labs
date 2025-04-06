import unittest
from Chomsky import Chomsky

class TestChomsky(unittest.TestCase):

    def setUp(self):
        self.Vn = ["S", "A", "B", "C", "E"]
        self.Vt = ["a", "d"]
        self.P = "S->dB|A, A->d|dS|aAdAB, B->aC|aS|AC, C->ε, E->AS"
        self.S = "S"
        self.chomsky = Chomsky(self.Vn.copy(), self.Vt, self.P, self.S)

    def test_eliminate_epsilons(self):
        self.chomsky.eliminate_epsilons()
        for rules in self.chomsky.P_dictionary.values():
            self.assertNotIn("C -> ε", rules)

    def test_eliminate_unit_rules(self):
        self.chomsky.eliminate_epsilons()
        self.chomsky.eliminate_unit_rules()
        for left, rules in self.chomsky.P_dictionary.items():
            for rule in rules:
                if len(rule.split()) == 1:
                    self.assertNotIn(rule, self.chomsky.Vn)

    def test_eliminate_inaccessible_symbols(self):
        self.chomsky.eliminate_epsilons()
        self.chomsky.eliminate_unit_rules()
        self.chomsky.eliminate_inaccessible_symbols()
        self.assertNotIn("E", self.chomsky.P_dictionary)

    def test_eliminate_nonproductive_symbols(self):
        for head, productions in self.chomsky.rules.items():
            for production in productions:
                for symbol in production:
                    self.assertTrue(
                        symbol in self.chomsky.Vn or symbol in self.chomsky.Vt,
                        msg=f"Symbol '{symbol}' in production {head} -> {production} is not in Vn or Vt"
                    )

    def test_convert_rhs_to_terminals_or_nonterminals(self):
        for head, productions in self.chomsky.rules.items():
            for production in productions:
                if len(production) == 1:
                    symbol = production[0]
                    self.assertTrue(
                        symbol in self.chomsky.Vt or symbol in self.chomsky.Vn,
                        msg=f"Single-symbol production {head} -> {production} must be a terminal or non-terminal"
                    )
                elif len(production) == 2:
                    self.assertTrue(
                        production[0] in self.chomsky.Vn and production[1] in self.chomsky.Vn,
                        msg=f"Production {head} -> {production} must contain exactly two non-terminals"
                    )
                else:
                    self.fail(
                        f"Production {head} -> {production} is invalid: CNF requires 1 terminal or 2 non-terminals")

    def test_convert_rhs_to_1_terminal_or_2_nonterminals(self):
        self.chomsky.eliminate_epsilons()
        self.chomsky.eliminate_unit_rules()
        self.chomsky.eliminate_inaccessible_symbols()
        self.chomsky.eliminate_nonproductive_symbols()
        self.chomsky.convert_rhs_to_terminals_or_nonterminals()
        self.chomsky.convert_rhs_to_1_terminal_or_2_nonterminals()
        for rules in self.chomsky.P_dictionary.values():
            for rule in rules:
                self.assertTrue(len(rule.split()) <= 2)

if __name__ == '__main__':
    unittest.main()
