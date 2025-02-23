import sys


class NDFA:
    def __init__(self, Q, sigma, F, transitions):
        self.Q = Q
        self.sigma = sigma
        self.F = set(F)
        self.transitions = transitions
        self.dictionary_transitions = {}
        self.new_transitions = {}

        for (state, symbol), next_states in transitions.items():
            if (state, symbol) not in self.dictionary_transitions:
                self.dictionary_transitions[(state, symbol)] = set()
            self.dictionary_transitions[(state, symbol)].update(next_states)

    def convert_to_grammar(self):
        Vn = self.Q
        Vt = self.sigma
        P = []

        for (state, symbol), next_states in self.dictionary_transitions.items():
            production = f"{state} -> "
            production += " | ".join(
                [f"{symbol}{next_state}" for next_state in next_states])
            P.append(production)

        return Vn, Vt, P

    def determine_type(self):
        is_ndfa = False

        for (state, symbol), next_states in self.dictionary_transitions.items():
            if len(next_states) > 1:
                is_ndfa = True
                print(
                    f"\nThe FA is non-deterministic because from state '{state}' on symbol '{symbol}', it can transition to multiple states: {next_states}")

        if not is_ndfa:
            print("\nThe FA is deterministic because each state-symbol pair leads to exactly one state.")

    def ndfa_transitioned_to_dfa(self):
        dfa_states = []
        dfa_transitions = {}
        processed_states = set()

        start_state = frozenset(["q0"])
        dfa_states.append(start_state)

        while dfa_states:
            current_state = dfa_states.pop(0)
            if current_state in processed_states:
                continue

            processed_states.add(current_state)

            for symbol in self.sigma:
                new_state = set()

                for substate in current_state:
                    if (substate, symbol) in self.dictionary_transitions:
                        new_state.update(self.dictionary_transitions[(substate, symbol)])

                if new_state:
                    new_state_frozen = frozenset(new_state)
                    dfa_transitions[(current_state, symbol)] = new_state_frozen

                    if new_state_frozen not in processed_states:
                        dfa_states.append(new_state_frozen)

        return dfa_transitions


if __name__ == "__main__":
    Q = ["q0", "q1", "q2", "q3", "q4"]
    sigma = ["a", "b", "c"]
    F = ["q4"]

    transitions = {
        ("q0", "a"): ["q1"],
        ("q1", "b"): ["q1"],
        ("q1", "a"): ["q2"],
        ("q2", "b"): ["q2", "q3"],
        ("q3", "b"): ["q4"],
        ("q3", "a"): ["q1"]
    }

    ndfa = NDFA(Q, sigma, F, transitions)
    dfa_transitions = ndfa.ndfa_transitioned_to_dfa()

    ndfa.determine_type()

    Vn, Vt, P = ndfa.convert_to_grammar()
    print("\nConverting the FA to a regular grammar:")
    print(" Vn: ", Vn)
    print(" Vt: ", Vt)
    print(" P: ", P)

    print("\nDFA Transitions:")
    for (state, symbol), next_state in dfa_transitions.items():
        print(f"{set(state)} -- {symbol} --> {set(next_state)}")
