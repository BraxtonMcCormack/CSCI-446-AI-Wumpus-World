class Predicate:
    def __init__(self, name, args, is_negated=False):
        self.name = name
        self.args = args
        self.is_negated = is_negated

    def __str__(self):
        negation = "¬" if self.is_negated else ""
        return f"{negation}{self.name}({', '.join(map(str, self.args))})" # Convert args to string format

class KnowledgeBase:
    def __init__(self):
        self.clauses = []

    def add_clause(self, clause):
        self.clauses.append(clause)

    def resolve(self, clause1, clause2):
        # Perform resolution between two clauses
        new_clause = []
        for pred1 in clause1:
            for pred2 in clause2:
                if pred1.name == pred2.name and pred1.is_negated != pred2.is_negated:
                    unification = self.unify(pred1, pred2)
                    if unification:
                        new_clause += [p for p in clause1 + clause2 if p != pred1 and p != pred2]
                        new_clause += [self.substitute(p, unification) for p in new_clause]
                        break
            else:
                continue
            break
        else:
            return None
        return new_clause

    def unify(self, pred1, pred2):
        # Unify two predicates
        substitution = {}
        if pred1.name != pred2.name or pred1.is_negated == pred2.is_negated:
            return None
        for arg1, arg2 in zip(pred1.args, pred2.args):
            # Check if the arguments are strings and lowercased (i.e., variables)
            is_arg1_var = isinstance(arg1, str) and arg1.islower()
            is_arg2_var = isinstance(arg2, str) and arg2.islower()

            if arg1 != arg2:
                if is_arg1_var and is_arg2_var:
                    substitution[arg1] = arg2
                elif is_arg1_var:
                    substitution[arg1] = arg2
                elif is_arg2_var:
                    substitution[arg2] = arg1
                else:
                    return None
        return substitution

    def substitute(self, predicate, substitution):
        # Substitute variables in a predicate
        new_args = [substitution[arg] if arg in substitution else arg for arg in predicate.args]
        return Predicate(predicate.name, new_args, predicate.is_negated)

    def is_consistent(self, new_clause):
        # Check if a new clause is inconsistent with the knowledge base
        for clause in self.clauses:
            resolvent = self.resolve(clause, new_clause)
            if resolvent is not None:
                if not resolvent or all(p.is_negated for p in resolvent):
                    return False
        return True
    
    def __str__(self):
        for i in self.clauses:
            print("".join(map(str, i)))
        
        return ""

def main():
    kb = KnowledgeBase()

    # Define the clauses
    kb.add_clause([Predicate("Animal", ["F(x)"]), Predicate("Loves", ["G(x)", "x"])])
    kb.add_clause([Predicate("Loves", ["x", "F(x)"], is_negated=True), Predicate("Loves", ["G(x)", "x"])])
    kb.add_clause([Predicate("Loves", ["y", "x"], is_negated=True), Predicate("Animal", ["z"], is_negated=True), Predicate("Kills", ["x", "z"], is_negated=True)])
    kb.add_clause([Predicate("Animal", ["x"], is_negated=True), Predicate("Loves", ["Jack", "x"])])
    kb.add_clause([Predicate("Kills", ["Jack", "Tuna"]), Predicate("Kills", ["Curiosity", "Tuna"])])
    kb.add_clause([Predicate("Cat", ["Tuna"])])
    kb.add_clause([Predicate("Cat", ["x"], is_negated=True), Predicate("Animal", ["x"])])
    # kb.add_clause([Predicate("Kills", ["Curiosity", "Tuna"], is_negated=True)])  # Adding the negated query

    test_clauses_examples = [
        [Predicate("Kills", ["Curiosity", "Jack"])],
        [Predicate("Cat", ["Jack"])],
        [Predicate("Loves", ["z", "Tuna"], is_negated=True)],
        [Predicate("Loves", ["Tuna", "Jack"])],
        [Predicate("Loves", ["Jack", "w"])],
        [Predicate("Cat", ["Tuna"], is_negated=True)],
        [Predicate("Kills", ["u", "Curiosity"])]
    ]

    for test_clause in test_clauses_examples:
        if kb.is_consistent(test_clause):
            print(f"{' and '.join(map(str, test_clause))} is consistent with the knowledge base.")
        else:
            print(f"{' and '.join(map(str, test_clause))} is inconsistent with the knowledge base.")

if __name__ == "__main__":
    main()
