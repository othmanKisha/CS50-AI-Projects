from logic import *

AKnight = Symbol("A is a Knight")
AKnave = Symbol("A is a Knave")

BKnight = Symbol("B is a Knight")
BKnave = Symbol("B is a Knave")

CKnight = Symbol("C is a Knight")
CKnave = Symbol("C is a Knave")

# The information about the structure of knights and knaves puzzle
Structure = And(
    # A is Either a Knight or Knave but not both
    And(Or(AKnight, AKnave), Or(Not(AKnight), Not(AKnave))),
    # B is Either a Knight or Knave but not both
    And(Or(BKnight, BKnave), Or(Not(BKnight), Not(BKnave))),
    # C is Either a Knight or Knave but not both
    And(Or(CKnight, CKnave), Or(Not(CKnight), Not(CKnave)))
)

"""
Puzzle 0
A says "I am both a knight and a knave."

The expression from what A says is:
    if and only if A was a knight then he is both knight and knave
"""
knowledge0 = And(
    # Information about the structure
    Structure,
    # Information about what is said
    Biconditional(AKnight, And(AKnight, AKnave))
)

"""
Puzzle 1
A says "We are both knaves."
B says nothing.

The expression from what A says is:
    if and only if A was a knight then he and B are knaves

B says nothing then there is no expression for it.
"""
knowledge1 = And(
    # Information about the structure
    Structure,
    # Information about what is said
    Biconditional(AKnight, And(AKnave, BKnave))
)

"""
Puzzle 2
A says "We are the same kind."
B says "We are of different kinds."

The expression for what A says is:
    if and only if A was a knight then A and B togather are knights or knaves

The expression for what B says is:
    if and only if B was a knight then both have different kinds {(A: Knight. B: Knave) or (A: Knave. B: Knight)} 
"""
knowledge2 = And(
    # Information about the structure
    Structure,
    # Information about what is said
    Biconditional(AKnight, Or(And(AKnight, BKnight), And(AKnave, BKnave))),
    Biconditional(BKnight, Or(And(AKnight, BKnave), And(AKnave, BKnight)))
)

"""
Puzzle 3
A says either "I am a knight." or "I am a knave.", but you don't know which.
B says "A said 'I am a knave'."
B says "C is a knave."
C says "A is a knight."

The expression for what A says is:
    if and only if A was a knight then he is either a knight or knave

The expression for B's first saying is:
    if and only if B was a knight then if and only if A was a knight then he is a knave

The expression for B's second saying is:
    if and only if B was a knight then C is a knave

The expression for what C says is:
    if and only if C was a knight then A is a Knight        
"""
knowledge3 = And(
    # Information about the structure
    Structure,
    # Information about what is said
    Biconditional(AKnight,  Or(AKnight, AKnave)),
    Biconditional(BKnight, Biconditional(AKnight, AKnave)),
    Biconditional(BKnight, CKnave),
    Biconditional(CKnight, AKnight)
)


def main():
    symbols = [AKnight, AKnave, BKnight, BKnave, CKnight, CKnave]
    puzzles = [
        ("Puzzle 0", knowledge0),
        ("Puzzle 1", knowledge1),
        ("Puzzle 2", knowledge2),
        ("Puzzle 3", knowledge3)
    ]
    for puzzle, knowledge in puzzles:
        print(puzzle)
        if len(knowledge.conjuncts) == 0:
            print("    Not yet implemented.")
        else:
            for symbol in symbols:
                if model_check(knowledge, symbol):
                    print(f"    {symbol}")


if __name__ == "__main__":
    main()
