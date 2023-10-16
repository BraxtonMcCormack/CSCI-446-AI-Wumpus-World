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

    def is_inconsistent(self, new_clause):
        # Check if a new clause is inconsistent with the knowledge base
        for clause in self.clauses:
            resolvent = self.resolve(clause, new_clause)
            if resolvent is not None:
                if not resolvent or all(p.is_negated for p in resolvent):
                    return True
        return False
    
    def __str__(self):
        for i in self.clauses:
            print("".join(map(str, i)))
        
        return ""

def main():
    # Create a knowledge base
    kb = KnowledgeBase()

    # Initial clauses
    pred1 = Predicate("Animal", ["a", "b"])
    pred2 = Predicate("Eats", ["a", 4])
    pred3 = Predicate("LivesIn", [3, "b"])
    pred4 = Predicate("Mammal", ["a"])
    kb.add_clause([pred1])
    kb.add_clause([pred2])
    kb.add_clause([pred3])
    kb.add_clause([pred4])

    # Introducing inconsistency
    pred5 = Predicate("IsColor", ["z", "blue"], is_negated=True)
    kb.add_clause([pred5])

    # Clause that, when resolved with KB, should lead to inconsistency
    test_clause = [Predicate("Animal", ["x", "y"], is_negated=True), Predicate("IsColor", ["x", "blue"])]

    # Check and print inconsistency
    print(f"Is the clause {', '.join(map(str, test_clause))} inconsistent with KB? {kb.is_inconsistent(test_clause)}")

        # Clause that, when resolved with KB, should NOT lead to inconsistency
    test_clause = [Predicate("IsGreen", ["x", "tree"])]

    # Check and print inconsistency
    print(f"Is the clause {', '.join(map(str, test_clause))} inconsistent with KB? {kb.is_inconsistent(test_clause)}")

if __name__ == "__main__":
    main()