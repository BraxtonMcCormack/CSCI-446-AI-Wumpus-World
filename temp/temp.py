class Predicate:
    def __init__(self, name, args):
        self.name = name
        self.args = args

    def __str__(self):
        return f"{self.name}({', '.join(self.args)})"

    def __eq__(self, other):
        return self.name == other.name and self.args == other.args

class KnowledgeBase:
    def __init__(self):
        self.clauses = []

    def add_clause(self, clause):
        self.clauses.append(clause)

    def resolve(self, query):
        while True:
            new_clauses = []
            for clause1 in self.clauses:
                for clause2 in self.clauses:
                    if clause1 != clause2:
                        for literal1 in clause1:
                            for literal2 in clause2:
                                unifier = self.unify(literal1, literal2)
                                if unifier is not None:
                                    new_clause = self.combine_clauses(clause1, clause2, literal1, literal2, unifier)
                                    if not new_clause:
                                        return True
                                    new_clauses.append(new_clause)
            if not new_clauses:
                return False
            self.clauses.extend(new_clauses)

    def unify(self, literal1, literal2):
        if literal1.name != literal2.name:
            return None
        unifier = {}
        for arg1, arg2 in zip(literal1.args, literal2.args):
            if arg1 != arg2:
                if arg1.islower() and arg2.islower():
                    return None
                if arg1.islower():
                    unifier[arg1] = arg2
                else:
                    unifier[arg2] = arg1
        return unifier

    def combine_clauses(self, clause1, clause2, literal1, literal2, unifier):
        new_clause = []
        for lit in clause1 + clause2:
            if lit != literal1 and lit != literal2:
                new_lit = self.apply_substitution(lit, unifier)
                new_clause.append(new_lit)
        if not self.has_tautology(new_clause):
            return new_clause
        return None

    def apply_substitution(self, literal, unifier):
        args = [unifier[arg] if arg in unifier else arg for arg in literal.args]
        return Predicate(literal.name, args)

    def has_tautology(self, clause):
        for literal1 in clause:
            for literal2 in clause:
                if literal1 != literal2 and literal1 == literal2:
                    return True
        return False

    def __str__(self):
        return ', '.join([str(clause) for clause in self.clauses])

if __name__ == '__main__':
    kb = KnowledgeBase()
    kb.add_clause([Predicate("Animal", ["F(x)"]), Predicate("Loves", ["G(x)", "x"])])
    kb.add_clause([Predicate("¬Loves", ["x", "F(x)"]), Predicate("Loves", ["G(x)", "x"])])
    kb.add_clause([Predicate("¬Loves", ["y", "x"]), Predicate("¬Animal", ["z"]), Predicate("¬Kills", ["x", "z"])])
    kb.add_clause([Predicate("¬Animal", ["x"]), Predicate("Loves", ["Jack", "x"])])
    kb.add_clause([Predicate("Kills", ["Jack", "Tuna"]), Predicate("Kills", ["Curiosity", "Tuna"])])
    kb.add_clause([Predicate("Cat", ["Tuna"])])
    kb.add_clause([Predicate("¬Cat", ["x"]), Predicate("Animal", ["x"])])
    
    print("Initial Knowledge Base:")
    for clause in kb.clauses:
        print("∧".join(map(str, clause)))

    result = kb.resolve([Predicate("¬Kills", ["Curiosity", "Tuna"])])
    
    print("\nResolution result:", result)

    print("Updated Knowledge Base:")
    for clause in kb.clauses:
        print("∧".join(map(str, clause)))
