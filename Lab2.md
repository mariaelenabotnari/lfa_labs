# Laboratory Work Nr. 2: Finite Automanta

__Course: Formal Languages & Finite Automata__  

__Author: Botnari Maria-Elena, FAF-232__

# Theory
Finite automata are fundamental models used to represent various computational processes. They are commonly employed in computer science, artificial intelligence, and linguistics to analyze and design systems that follow predefined rules. The term finite indicates that the automaton has a limited number of states, and it always starts from an initial state and may reach one or more final states. Finite automata are particularly useful in recognizing patterns, parsing text, and verifying sequences of inputs. They can be visualized as state machines where transitions between states occur based on given inputs. These transitions define how the automaton reacts to different symbols, determining whether a particular sequence is accepted or rejected.
  
Automata can be classified as deterministic or non-deterministic, depending on their transition behavior. A deterministic finite automaton (DFA) has a predictable structure where each state-symbol pair leads to exactly one next state. This makes it easy to analyze and implement in real-world applications. However, in some cases, an automaton may have multiple possible transitions for the same symbol in a given state, leading to non-determinism. Such automata are called non-deterministic finite automata (NDFA). While NDFAs may seem more complex, they can be systematically converted into an equivalent DFA using a standard algorithm. This conversion is crucial because DFAs are more efficient in practical applications, such as designing compilers, search engines, and control systems.
  
Finite automata are also closely linked to formal grammars, particularly regular grammars, which describe the structure of languages in terms of production rules. The relationship between automata and grammars allows us to translate a finite automaton into an equivalent regular grammar, ensuring that both models describe the same language. This conversion helps in understanding how automata process strings and generate output sequences. The study of finite automata plays a crucial role in theoretical computer science, as it provides a foundation for more advanced computational models, such as pushdown automata and Turing machines, which are used to solve complex problems in programming languages and artificial intelligence.

# Objectives

1) Understand what an automaton is and what it can be used for.

2) Continuing the work in the same repository and project, the following need to be added:   
a. Provide a function in your grammar type/class that could classify the grammar based on the Chomsky hierarchy.   
b. For this you can use the variant from the previous lab.
3) According to your variant number (by universal convention it is register ID), get the finite automaton definition and do the following tasks:  
a. Implement conversion of a finite automaton to a regular grammar.   
b. Determine whether your FA is deterministic or non-deterministic.   
c. Implement some functionality that would convert an NDFA to a DFA.

# Implementation Description

The **NDFA class** represents a non-deterministic finite automaton (NDFA), a model used to recognize patterns and process sequences of symbols. The class has a set of states (Q), an alphabet (sigma), a set of final states (F), and transitions, which define how the automaton moves from one state to another based on input symbols. The transitions are stored in a dictionary, making it easier to look up which states can be reached from a given state-symbol pair. This class also provides various functionalities, including converting an NDFA to a regular grammar, determining whether the given automaton is deterministic or non-deterministic, and converting an NDFA into a DFA (deterministic finite automaton). These operations help in understanding and working with automata in a structured and computational way.

```
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

```

\
**Converting the FA to Regular Grammar**: The convert_to_grammar function translates the given NDFA into regular grammar, which is a set of rules defining how strings can be formed. It does this by considering each state as a non-terminal (Vn) and the input symbols as terminals (Vt). The function then constructs production rules (P) by converting state transitions into grammar rules. For example, if the NDFA has a transition from state q1 to q2 on symbol a, the function will create a grammar rule q1 → a q2. This function is useful because it shows the strong connection between automata and formal grammars, making it possible to use automata theory in language processing and parsing tasks.

````
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
````
\
**Determining whether the FA is deterministic or non-deterministic**: The determine_type function checks whether the given finite automaton is deterministic or non-deterministic. It does this by looking at the transition rules and checking if any state-symbol pair leads to multiple possible next states. If such cases exist, the automaton is non-deterministic (NDFA); otherwise, it is deterministic (DFA). The function prints an explanation, specifying whether the automaton follows a single transition rule per state-symbol pair (DFA) or has multiple possible transitions for the same input (NDFA). This check is important because NDFA and DFA have different processing mechanisms, and converting an NDFA to a DFA makes computations more predictable and efficient.

````
    def determine_type(self):
        is_ndfa = False

        for (state, symbol), next_states in self.dictionary_transitions.items():
            if len(next_states) > 1:
                is_ndfa = True
                print(
                    f"\nThe FA is non-deterministic because from state '{state}' on symbol '{symbol}', it can transition to multiple states: {next_states}")

        if not is_ndfa:
            print("\nThe FA is deterministic because each state-symbol pair leads to exactly one state.")
````

\
**Converting the NDFA to DFA**: The ndfa_transitioned_to_dfa function converts the given NDFA into a DFA by systematically eliminating non-determinism. Instead of having multiple possible next states for a given symbol, it constructs new composite states that group all possible transitions into single states. The function starts with the initial state and explores all reachable states, ensuring that every input symbol leads to exactly one next state in the resulting DFA. This process helps in making automata more practical for implementation, as DFAs are faster and easier to use in real-world applications like pattern matching, lexical analysis, and network protocols.  
The ndfa_transitioned_to_dfa function works by creating a new set of states that represent combinations of NDFA states, ensuring that every input symbol has a single transition per state, a requirement for DFAs. The process begins by defining a new set of DFA states, where the initial DFA state is represented as a set containing the original NDFA start state (typically q0). This state is stored as a frozen set to ensure immutability when used as a key in dictionaries. The function uses a queue-like structure, where it iterates through unprocessed states, computing their transitions. For each state in the DFA, the function checks all possible input symbols, gathering the set of NDFA states reachable from the current state for that symbol. If multiple NDFA states can be reached, they are merged into a single new DFA state. This approach ensures that states in the DFA correctly reflect all possible transitions from the NDFA, preserving the language recognition capabilities while eliminating ambiguities. These newly created DFA states are then added to the queue for further processing. The function also keeps track of processed states to avoid redundant calculations. The final DFA transitions are stored in a dictionary, mapping each DFA state-symbol pair to a unique next DFA state. The algorithm continues until no new states are discovered, ensuring full coverage of the original NDFA structure. This conversion ensures that the resulting DFA is equivalent to the original NDFA in terms of language recognition but operates in a more predictable and efficient manner, making it suitable for computational applications.

````
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
````

\
**Checking the grammar type**: The check_grammar_type function classifies the given grammar based on the Chomsky hierarchy, which categorizes grammars into four types: Type 0 (Unrestricted), Type 1 (Context-Sensitive), Type 2 (Context-Free), and Type 3 (Regular Grammar). The function examines the left-hand side and right-hand side of production rules to determine which type the grammar belongs to. If the rules follow a strict linear pattern (Type 3), it is a regular grammar, which can be converted into a finite automaton. If the left side always has a single non-terminal (Type 2), it is a context-free grammar, widely used in programming languages and compilers. If the rules ensure that the right-hand side is at least as long as the left (Type 1), it is a context-sensitive grammar, capable of representing more complex structures like natural language processing. If none of these restrictions are met, the grammar is Type 0, the most general and powerful type, which requires a Turing machine to process. By identifying the grammar type, this function helps in understanding the complexity and computational requirements of a given language or automaton.
````
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
````


# Results
**Results after checking if the FA is deterministic or not:**  

`The FA is non-deterministic because from state 'q2' on symbol 'b', it can transition to multiple states: {'q3', 'q2'}`

\
**Results after the FA converted to regular grammar**  

`Converting the FA to a regular grammar:`  
`Vn:  ['q0', 'q1', 'q2', 'q3', 'q4']`  
 `Vt:  ['a', 'b', 'c']`  
 `P:  ['q0 -> aq1', 'q1 -> bq1', 'q1 -> aq2', 'q2 -> bq3 | bq2', 'q3 -> bq4', 'q3 -> aq1']`
 
\
**Results after converting the NDFA to DFA**  

`DFA Transitions`  
`{'q0'} -- a --> {'q1'}`  
`{'q1'} -- a --> {'q2'}`  
`{'q1'} -- b --> {'q1'}`  
`{'q2'} -- b --> {'q3', 'q2'}`  
`{'q3', 'q2'} -- a --> {'q1'}`  
`{'q3', 'q2'} -- b --> {'q3', 'q4', 'q2'}`  
`{'q3', 'q4', 'q2'} -- a --> {'q1'}`  
`{'q3', 'q4', 'q2'} -- b --> {'q3', 'q4', 'q2'}`

\
**Results after checking the type of the grammar**  

`Type 3 Grammar (Regular Grammar):`  
`Each production rule follows the form 'A → aB' or 'A → a'.`  
`Regular grammars can be either right-linear, where non-terminals appear at the end, or left-linear, where they appear at the beginning.`  
`These grammars can be converted into finite automata and are commonly used in lexical analysis and defining regular expressions.`  
`Example: S → aS | bA | ε, where ε represents an empty string.`

# Conclusion 
In this laboratory work, we learned about finite automata and formal grammars, focusing on how to convert an NDFA into a DFA and how automata relate to regular grammars. We built a program to define an NDFA, check if it is deterministic or non-deterministic, and transform it into a DFA by merging states to remove uncertainty. We also converted the automaton into a regular grammar and classified it based on the Chomsky hierarchy to understand its complexity.  

This work helped us see how automata process languages and why DFAs are more efficient than NDFAs in practical applications like search engines and compilers. By implementing these concepts, we gained a better understanding of how computers recognize patterns and process inputs, which is important for future studies in programming and algorithms.

