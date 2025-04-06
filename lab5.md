# Laboratory Work Nr. 5: Chomsky Normal Form

__Course: Formal Languages & Finite Automata__  

__Author: Botnari Maria-Elena, FAF-232__

# Theory

Chomsky Normal Form, often shortened to CNF, is a special way of writing grammar rules in formal language theory that helps computers process languages more easily. In CNF, every rule in the grammar has to follow one of two patterns: it either turns a non-terminal into exactly two other non-terminals (like `A → BC`), or into a single terminal symbol (like `A → a`). This strict format might seem limiting at first, but it's actually very useful. By rewriting grammars into CNF, we make them easier to use in computer algorithms, especially those used for checking whether a string belongs to a language or for parsing sentences in compilers and programming languages. The importance of CNF comes from the fact that it is used in the CYK algorithm, a powerful tool for parsing context-free languages. To turn any context-free grammar into Chomsky Normal Form, we follow a clear process: first, we remove empty rules (those that produce nothing), then we remove unit rules (those that just point to another non-terminal), and also take out useless symbols—ones that can’t help produce a real word. After cleaning up the grammar, we make sure that every rule only uses terminals in short, separate rules, and we break long rules down into smaller pieces that fit the CNF structure. Even though this can make the grammar look more complicated, it still describes the same language as before, just in a way that’s easier for machines to understand and use.

# Objectives
• Learn about Chomsky Normal Form (CNF).

• Get familiar with the approaches of normalizing a grammar.

• Implement a method for normalizing an input grammar by the rules of CNF:
1) The implementation needs to be encapsulated in a method with an appropriate signature (also ideally in an appropriate class/type).
2) The implemented functionality needs executed and tested.
3) Also, another BONUS point would be given if the student will make the aforementioned function to accept any grammar, not only the one from the student's variant.

# Implementation Description

**Step 1: Eliminating ε-productions**

In this first step, the goal is to remove all productions that generate the empty string ε, except in special cases where it's absolutely needed, like for the start symbol. ε-productions are problematic in CNF because CNF doesn't allow them unless the grammar accepts the empty word. To eliminate ε-productions, the algorithm begins by scanning the production rules to find all non-terminal symbols that directly lead to ε. These are considered “nullable” symbols. Then, for every rule that includes one or more of these nullable non-terminals, the algorithm generates new versions of those rules where the nullable non-terminals are optionally removed. For example, if a rule is A → BC and C → ε, then a new rule A → B is also added. It’s important to note that this process doesn’t remove the original rules, it just adds the new alternative ones without the nullable parts. After generating all such combinations, the ε-productions are deleted from the grammar unless they belong to the start symbol and are essential for producing the empty string. This step is crucial because ε-productions introduce ambiguity and can make parsing unpredictable, so removing them helps simplify the grammar without changing the language it represents.

````
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
````
\
**Step 2: Eliminating unit productions**

After dealing with ε-productions, the next step focuses on eliminating unit productions, which are rules where a non-terminal points directly to another non-terminal, such as A → B. These kinds of rules are not allowed in CNF because they don’t reduce the size of the string, they just pass control from one symbol to another without doing anything useful. The algorithm tackles this by checking each rule, and whenever it finds a unit production, it replaces it with all the rules that belong to the non-terminal on the right side. So if there’s A → B and B → x|y, then A → x|y is added, and A → B is removed. This replacement continues recursively—if those new rules include other unit productions, the same process is applied again. By doing this, all the indirect or direct links between non-terminals are broken down, and only real productive rules that generate actual symbols (terminals or sequences of terminals) are kept. This step helps clean up the grammar and prevents useless transitions between non-terminals that don’t produce anything on their own.

````
        print("\nStep 2: Eliminated unit rules:")
        for left in list(self.P_dictionary.keys()):
            rules = list(self.P_dictionary[left])
            new_rules = []

            for rule in rules:
                if len(rule) == 1 and rule in self.Vn:
                    new_rules.extend(self.P_dictionary[rule])

            self.P_dictionary[left] = [r for r in rules if not (len(r) == 1 and r in self.Vn)] + new_rules
````
\
**Step 3: Eliminating inaccessible symbols**

Once unit productions are gone, the algorithm checks whether there are any symbols (non-terminals) that never actually get used when generating strings starting from the initial symbol. These are called inaccessible symbols. They may be part of the grammar’s list of non-terminals and even have rules assigned to them, but if there's no path to reach them from the start symbol, then they are meaningless for the language. To remove them, the algorithm performs a kind of “reachability analysis” starting from the start symbol. It explores each rule the start symbol leads to, then continues to follow all the symbols those rules reference, and so on. Any non-terminal not discovered through this exploration is considered inaccessible. These symbols and their rules are then completely removed from the grammar. This step ensures that the grammar only contains symbols that are actually involved in generating valid strings. It helps reduce the size of the grammar and removes clutter that would otherwise confuse analysis or parsing algorithms later on.

````
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
````
\
**Step 4: Eliminating non-productive symbols**

Next, the algorithm focuses on getting rid of non-productive symbols—these are non-terminals that can’t ever produce a string consisting entirely of terminal symbols, no matter how many rules you follow. Even if a symbol is reachable from the start symbol, if it doesn’t eventually lead to a terminal string, it still needs to be removed. To identify productive symbols, the algorithm goes through all the rules and checks whether the right-hand side of each rule consists entirely of terminals or other productive symbols. It keeps track of which symbols have this property and continues this check in a loop until no new productive symbols can be found. After identifying all productive symbols, it deletes all rules that involve non-productive ones, and those symbols are removed from the non-terminal list too. This step is essential for keeping the grammar functional and correct. Without it, the grammar could include useless rules that mislead parsers or create dead ends in derivations that cannot lead to valid words.

````
        print("\nStep 4: Eliminating non-productive symbols:")
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
````
\
**Step 5: Rewriting rules to separate terminals in longer productions**

At this point, the grammar only contains useful rules and symbols, but many of the rules still break CNF’s restrictions on form. In CNF, each production must either produce a single terminal symbol or two non-terminal symbols, nothing else. However, right now, some rules may mix terminals and non-terminals in the same production, especially in longer rules like A → aB or B → dS. These need to be fixed. So the algorithm replaces every terminal that appears in a longer rule with a new non-terminal symbol that only produces that terminal. For example, if there’s a rule A → aB, the terminal a gets replaced by a new symbol like X0, and a new rule X0 → a is added to the grammar. Then A → X0B replaces the original rule. This ensures that all long rules use only non-terminals, while the terminals are handled separately. This transformation preserves the meaning of the original rules but rewrites them in a structure that fits CNF requirements. It also avoids duplication by reusing the same new non-terminal for repeated terminals across different rules.

````
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
                    
````
\
**Step 6: Breaking down long rules into binary rules**

Finally, the algorithm handles the last major transformation: breaking down all production rules that have more than two symbols on the right-hand side. In CNF, each rule must either be of the form A → a or A → BC where B and C are non-terminals. So, rules like A → B C D or longer must be split into a chain of binary rules. To do this, the algorithm introduces new non-terminals to group symbols two at a time. For example, A → B C D would become something like A → Y0 D and Y0 → B C, where Y0 is a new non-terminal created just for this purpose. For even longer rules like A → B C D E, the process continues step by step: first create Y0 → B C, then Y1 → Y0 D, and finally A → Y1 E. Each new rule only has two non-terminals on the right-hand side, which satisfies the CNF format. This step can be a bit mechanical, but it’s necessary to ensure the grammar is completely transformed into Chomsky Normal Form. In the end, every rule fits exactly the CNF pattern, and the grammar is ready for use in algorithms that require strict structure, such as the CYK parsing algorithm.

````
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
                    
                ...
````

# Results

````
Initial production rules:
S->d B|A, A->d|d S|a A d A B, B->a C|a S|A C, C->ε, E->A S

Step 1: Eliminated ε-productions:
S->d B|A, A->d S|a A d A B|d, B->A C|a C|a|A|a S, E->A S

Step 2: Eliminated unit rules:
S->d B|d S|a A d A B|d, A->d S|a A d A B|d, B->A C|a C|a|a S|d S|a A d A B|d, E->A S

Step 3: Eliminating inaccessible symbols:
S->d B|d S|a A d A B|d, A->d S|a A d A B|d, B->A C|a C|a|a S|d S|a A d A B|d

Step 4: Eliminating non-productive symbols:
S->d B|d S|a A d A B|d, A->d S|a A d A B|d, B->A C|a C|a|a S|d S|a A d A B|d

Step 5: RHS with just terminals or nonterminals:
S->X0 B|X0 S|X1 A X0 A B|d, A->X0 S|X1 A X0 A B|d, B->A C|X1 C|a|X1 S|X0 S|X1 A X0 A B|d, X0->d, X1->a

 Step 6: RHS with just 1 terminal or 2 nonterminals
S->X0 B|X0 S|Y2 B|d, A->X0 S|Y2 B|d, B->A C|X1 C|a|X1 S|X0 S|Y2 B|d, X0->d, X1->a, Y0->X1 A, Y1->Y0 X0, Y2->Y1 A
````

# Conclusion

In conclusion, this laboratory work showed how to transform a context-free grammar into Chomsky Normal Form step by step. Each step had a clear purpose: removing unnecessary rules, simplifying the grammar, and reshaping the rules so they follow a standard form. This process is very useful in computer science, especially in building parsers and understanding how languages work. By rewriting the grammar into CNF, we make it easier for programs to check if a word belongs to a language or to analyze the structure of sentences. Even if the final grammar looks more complex, it still represents the same language as the original one. This lab helped us understand how important it is to prepare a grammar in a proper format for further processing by algorithms and tools.