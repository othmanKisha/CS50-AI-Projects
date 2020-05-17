import sys

from crossword import *


class CrosswordCreator():

    def __init__(self, crossword):
        """
        Create new CSP crossword generate.
        """
        self.crossword = crossword
        self.domains = {
            var: self.crossword.words.copy()
            for var in self.crossword.variables
        }

    def letter_grid(self, assignment):
        """
        Return 2D array representing a given assignment.
        """
        letters = [
            [None for _ in range(self.crossword.width)]
            for _ in range(self.crossword.height)
        ]
        for variable, word in assignment.items():
            direction = variable.direction
            for k in range(len(word)):
                i = variable.i + (k if direction == Variable.DOWN else 0)
                j = variable.j + (k if direction == Variable.ACROSS else 0)
                letters[i][j] = word[k]
        return letters

    def print(self, assignment):
        """
        Print crossword assignment to the terminal.
        """
        letters = self.letter_grid(assignment)
        for i in range(self.crossword.height):
            for j in range(self.crossword.width):
                if self.crossword.structure[i][j]:
                    print(letters[i][j] or " ", end="")
                else:
                    print("█", end="")
            print()

    def save(self, assignment, filename):
        """
        Save crossword assignment to an image file.
        """
        from PIL import Image, ImageDraw, ImageFont
        cell_size = 100
        cell_border = 2
        interior_size = cell_size - 2 * cell_border
        letters = self.letter_grid(assignment)

        # Create a blank canvas
        img = Image.new(
            "RGBA",
            (self.crossword.width * cell_size,
             self.crossword.height * cell_size),
            "black"
        )
        font = ImageFont.truetype("assets/fonts/OpenSans-Regular.ttf", 80)
        draw = ImageDraw.Draw(img)

        for i in range(self.crossword.height):
            for j in range(self.crossword.width):

                rect = [
                    (j * cell_size + cell_border,
                     i * cell_size + cell_border),
                    ((j + 1) * cell_size - cell_border,
                     (i + 1) * cell_size - cell_border)
                ]
                if self.crossword.structure[i][j]:
                    draw.rectangle(rect, fill="white")
                    if letters[i][j]:
                        w, h = draw.textsize(letters[i][j], font=font)
                        draw.text(
                            (rect[0][0] + ((interior_size - w) / 2),
                             rect[0][1] + ((interior_size - h) / 2) - 10),
                            letters[i][j], fill="black", font=font
                        )

        img.save(filename)

    def solve(self):
        """
        Enforce node and arc consistency, and then solve the CSP.
        """
        self.enforce_node_consistency()
        self.ac3()
        return self.backtrack(dict())

    def enforce_node_consistency(self):
        """
        Update `self.domains` such that each variable is node-consistent.
        (Remove any values that are inconsistent with a variable's unary
         constraints; in this case, the length of the word.)
        """
        # Checking for the domain of each variable
        for variable, domain in self.domains.items():
            for value in domain.copy():
                # If the length of the word is not the same as the variable then remove it
                if len(value) != variable.length:
                    self.domains[variable].remove(value)

    def revise(self, x, y):
        """
        Make variable `x` arc consistent with variable `y`.
        To do so, remove values from `self.domains[x]` for which there is no
        possible corresponding value for `y` in `self.domains[y]`.

        Return True if a revision was made to the domain of `x`; return
        False if no revision was made.
        """
        # same as The revise psudocode in the lecture
        revised = False

        # The overlaps betweer the two variables
        overlap = self.crossword.overlaps[x, y]
        if overlap == None:
            return revised

        for x_value in self.domains[x].copy():

            # Checking if there is no possible solution when choosing the x_value with respect to y only
            if not any(x_value[overlap[0]] == y_value[overlap[1]] for y_value in self.domains[y]):
                self.domains[x].remove(x_value)
                revised = True

        return revised

    def ac3(self, arcs=None):
        """
        Update `self.domains` such that each variable is arc consistent.
        If `arcs` is None, begin with initial list of all arcs in the problem.
        Otherwise, use `arcs` as the initial list of arcs to make consistent.

        Return True if arc consistency is enforced and no domains are empty;
        return False if one or more domains end up empty.
        """
        # Initializing the arcs if none
        if arcs == None:
            arcs = [(x, y) for x, y in self.crossword.overlaps]

        # Return true if there are no arcs remaining to process
        if arcs == []:
            return True

        # Dequeue
        x, y = arcs.pop(0)

        # Checking if there is a revise
        if self.revise(x, y):
            if len(self.domains[x]) == 0:
                return False

            for z in self.crossword.neighbors(x):
                if z != y:
                    arcs.insert(-1, (z, x))

        return self.ac3(arcs)

    def assignment_complete(self, assignment):
        """
        Return True if `assignment` is complete (i.e., assigns a value to each
        crossword variable); return False otherwise.
        """
        # Checks if all variables of crossword have words assigned
        return True if all(var in assignment for var in self.crossword.variables) else False

    def consistent(self, assignment):
        """
        Return True if `assignment` is consistent (i.e., words fit in crossword
        puzzle without conflicting characters); return False otherwise.
        """
        for k1, v1 in assignment.items():

            # No two words for different variables are the same
            for k2, v2 in assignment.items():
                if v1 == v2 and k1 != k2:
                    return False

            # No word have different length than the variable
            if len(v1) != k1.length:
                return False

            # No word is already assigned to a neighbor variable
            if any(n in assignment and v1 == assignment[n] for n in self.crossword.neighbors(k1)):
                return False

        return True

    def order_domain_values(self, var, assignment):
        """
        Return a list of values in the domain of `var`, in order by
        the number of values they rule out for neighboring variables.
        The first value in the list, for example, should be the one
        that rules out the fewest values among the neighbors of `var`.
        """
        # Sorting a list of domain values for var based on the count of neighbor variables that contain a value
        return sorted(list(self.domains[var]), key=lambda val: sum([
            1 for n in self.crossword.neighbors(var) if val in self.domains[n] and not n in assignment
        ]))

    def select_unassigned_variable(self, assignment):
        """
        Return an unassigned variable not already part of `assignment`.
        Choose the variable with the minimum number of remaining values
        in its domain. If there is a tie, choose the variable with the highest
        degree. If there is a tie, any of the tied variables are acceptable
        return values.
        """
        # Dictionary with all unassigned variables
        unassigned_vars = {
            var: None
            for var in self.crossword.variables if not var in assignment
        }

        # The first variable in unassigned_vars
        v = next(iter(unassigned_vars))

        for var in unassigned_vars:
            if v != var:
                # If var has smaller domain make it the selected
                if len(self.domains[v]) > len(self.domains[var]):
                    v = var
                elif len(self.domains[v]) == len(self.domains[var]):

                    # If var has higher rank make it selected
                    if len(self.crossword.neighbors(v)) <= len(self.crossword.neighbors(var)):
                        v = var

        return v

    def backtrack(self, assignment):
        """
        Using Backtracking Search, take as input a partial assignment for the
        crossword and return a complete assignment if possible to do so.

        `assignment` is a mapping from variables (keys) to words (values).

        If no assignment is possible, return None.
        """
        if self.assignment_complete(assignment):
            return assignment

        # Get the unassigned variable according to the hurestics
        var = self.select_unassigned_variable(assignment)

        # For each value in the ordered domain of var
        for value in self.order_domain_values(var, assignment):
            assignment.update({var: value})

            # If the assignment consistent
            if self.consistent(assignment):
                result = self.backtrack(assignment)
                if result != None:
                    return result

            # If not possible delete this assignment
            del assignment[var]

        return None


def main():

    # Check usage
    if len(sys.argv) not in [3, 4]:
        sys.exit("Usage: python generate.py structure words [output]")

    # Parse command-line arguments
    structure = sys.argv[1]
    words = sys.argv[2]
    output = sys.argv[3] if len(sys.argv) == 4 else None

    # Generate crossword
    crossword = Crossword(structure, words)
    creator = CrosswordCreator(crossword)
    assignment = creator.solve()

    # Print result
    if assignment is None:
        print("No solution.")
    else:
        creator.print(assignment)
        if output:
            creator.save(assignment, output)


if __name__ == "__main__":
    main()
