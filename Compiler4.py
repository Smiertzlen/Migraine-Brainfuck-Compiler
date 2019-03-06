import tree_pprint

# This class implements the new version of the migraine2 to brainfuck compiler
# New features will be:
# - Support for negative numbers
# - support for numbers with more than one byte (int, double)
# - support of mathematical operations for these new data types
# - Improved parenthesis removals

values = ['byte', 'short', 'int', 'long', 'float', 'double']


class Node():
    def __init__(self, zeichen, l, r, p):
        self.own = zeichen
        self.left = l
        self.right = r
        self.parent = p

    def set_parent(self, new):
        self.parent = new

    def set_left(self, new):
        self.left = new

    def set_right(self, new):
        self.right = new

    def set_op(self, new):
        self.own = new

    def get_parent(self):
        return self.parent

    def get_left(self):
        return self.left

    def get_right(self):
        return self.right

    def get_op(self):
        return self.own

    def pprint(self):
        tree_pprint.pprint(self, 'own', 'left', 'right')


# These are all available operators and their respective brainfuck code
# Missing: /, %
operator_brain = {
    '+': ('<[-<+>]', -1),
    '-': ('<[-<->]', -1),
    '*': ('<<[->>+<<]>[->[->+<<<+>>]>[-<+>]<]>[-]<', -1),
    '!': ('+<[[-]>-<]>[-<+>]', 0),  # to_invert|0 benoetigt nur diese Bieden plaetze fuer die Invetierung. Pointer auf 0
    '&&': ('++<<[[-]>>-<<]+>[[-]>-<]>[[-]<<->>]<', -1),
    '-&': ('++<<[[-]>>-<<]+>[[-]>-<]>[[-]<<->>]<+<[[-]>-<]>[-<+>]', -1), # kombi: x y and not !(x&&y)
    '||': ('<<[[-]>>+<<]>[[-]>+<]>[[-]<<+>>]<', -1),
    '-|': ('<<[[-]>>+<<]>[[-]>+<]>[[-]<<+>>]<+<[[-]>-<]>[-<+>]', -1),
    '-^': ('<<[[-]>>+<<]+>[[-]>-<]>[[-]<<->>]<', -1), #xnor also true wenn beide true oder beide false
    '^^': ('<<[[-]>>+<<]+>[[-]>-<]>[[-]<<->>]<+<[[-]>-<]>[-<+>]', -1), # not xnor
    '==': ('<<[->-<]+>[[-]<->]', -1),
    '-=': ('<<[->-<]>[[-]<+>]', -1), # this means not equal
    '<=': ('>>+<<<<[>[->>+<<]>>[-<+<+>>]+<[[-]>-<]>[-<+>]<[-<+<[-]+>>>>-<<]<-<-]>>>>[-<<<<+>>>>]<<<[-]', -1),
    '>=': ('>>+<<<[<[->>>+<<<]>>>[-<+<<+>>>]+<[[-]>-<]>[-<+>]<[-<[-]+<+>>>>-<<]<-<->]<[-]>>>>[-<<<<+>>>>]<<<', -1),
    '<': ('>>+<<<[<[->>>+<<<]>>>[-<+<<+>>>]+<[[-]>-<]>[-<+>]<[-<[-]+<+>>>>-<<]<-<->]<[-]>>>>[-<<<<+>>>>]<<<+<[[-]>-<]>[-<+>]', -1),
    '>': ('>>+<<<<[>[->>+<<]>>[-<+<+>>]+<[[-]>-<]>[-<+>]<[-<+<[-]+>>>>-<<]<-<-]>>>>[-<<<<+>>>>]<<<[-]+<[[-]>-<]>[-<+>]', -1)
}



# This dictionary defines the binding strength of operators.
# Additional operators can be weighted here.
operators = {
            '&&': 0,
            '||': 0,
            '-^': 0,
            '-&': 0,
            '-|': 0,

            '<':  1,
            '>':  1,
            '<=': 1,
            '>=': 1,
            '==': 1,
            '-=': 1,

            '+':  2,
            '-':  2,

            '*':  3,
            '/':  3,
            '%':  3
        }










# Improvement:
# - associative law

# this function could be fused with the make_tree_parenthesis function
def remove_parenthesis(input_str):
    # This program removes unnecessary parenthesis from formulas.
    # It uses substitutions to determine wanted and unwanted parenthesis

    sub_id = 0
    substitutions = {}

    # continue the substitution process, as long as there are parenthesis
    while '(' in input_str:

        depth_levels = [0]*len(input_str)
        depth = 0

        for i in range(0, len(input_str)):
            if input_str[i] == '(':
                depth += 1
                depth_levels[i] = depth
            elif input_str[i] == ')':
                depth_levels[i] = depth
                depth -= 1
            else:
                depth_levels[i] = depth



        while not 0 in depth_levels:
            # this means, there are paranthesis around! the entire expression. As these are not needed, remove them
            input_str = input_str[1:-1]
            depth_levels = [0] * len(input_str)
            depth = 0

            for i in range(0, len(input_str)):
                if input_str[i] == '(':
                    depth += 1
                    depth_levels[i] = depth
                elif input_str[i] == ')':
                    depth_levels[i] = depth
                    depth -= 1
                else:
                    depth_levels[i] = depth



        # use this to formulate substitutions
        # begin at the highest depth

        highest_depth = max(depth_levels)

        index = 0

        new_input_str = input_str

        while index < len(input_str):
            if depth_levels[index] == highest_depth:
                # found one of the parenthesis marking the current highest depth
                current_input_string = input_str[index]
                index += 1
                while index < len(input_str) and depth_levels[index] == highest_depth:
                    current_input_string += input_str[index]
                    index += 1
                # check if any x is part of an operator, so neither an alnum nor a part of a substitution $
                if any(map(lambda x: not (x.isalnum() or x in ['$', '§']), current_input_string[1:-1])):
                    substitutions[sub_id] = current_input_string
                else:
                    substitutions[sub_id] = current_input_string[1:-1]
                new_input_str = new_input_str.replace(current_input_string, '$'+str(sub_id))
                sub_id += 1
            else:
                index += 1

        input_str = new_input_str

    # now all the parts are substituted. Thereby, all unnecessary parenthesis were removed.
    # Invert the substitutions

    while '$' in input_str:
        index = input_str.find('$')
        # read the complete $-notation to gets the specific id
        index_end = index+1
        while index_end+1 < len(input_str) and input_str[index_end+1].isdigit():
            index_end += 1
        # read the substitution number and get the substitution
        id = input_str[index+1:index_end+1]
        sub = substitutions[int(id)]
        input_str = input_str.replace('$' + id, sub)

    return input_str


# This function creates a tree according to arithmetic laws.
# This function is only working, if input_str does not contain any parenthesis
def make_tree(input_str):
    # First of, every input_str_str has to start with a variable name or a number.
    input_str_split = []
    check = ''

    # Check if ! is at the beginning of the variable name
    # either alpha numeric or a NOT operator, or a variable substitution or a function substitution
    # optimized version in comparison to the first compiler.
    index = 0
    # it will also check for invertion, a variable substitution or function substitution
    while input_str[index].isalnum() or input_str[index] in ['!', '$', '§']:
        index += 1
    input_str_split.append(input_str[0:index])
    input_str = input_str[index:]

    # While there is something in the input_str, search vor another operator followed by a variable
    while input_str:
        # Now an operator will follow
        # check if it a two or one character operator
        if input_str[0:2] in operator_brain:
            input_str_split.append(input_str[0:2])
            input_str = input_str[2:]
        else:
            input_str_split.append(input_str[0])
            input_str = input_str[1:]

        # input_str the next variable
        index = 0
        while index < len(input_str) and (input_str[index].isalnum() or input_str[index] in ['!', '$', '§']):
            index += 1
        input_str_split.append(input_str[0:index])
        input_str = input_str[index:]

    # Now the entire String is split.
    # Build the Tree ontop of that
    # Usage of the node class

    tree = Node(input_str_split[0], None, None, None)

    # Remove the top element, which was just put into the tree
    input_str_split.pop(0)

    if input_str_split:
        # first of, include the next operator

        # check if this does exactly what I want
        tree = Node(input_str_split.pop(0), tree, Node(input_str_split.pop(0), None, None, None), None)
        tree.get_left().set_parent(tree)
        tree.get_right().set_parent(tree)

        #Now continue with the binding strength in mind found in operators

        while input_str_split:
            if operators[tree.get_op()] < operators[input_str_split[0]]:
                # the binding strength of the next operator is higher. replace the right node with that operator
                tree = Node(input_str_split.pop(0), tree.get_right(), Node(input_str_split.pop(0), None, None, None), tree)
                tree.get_left().set_parent(tree)
                tree.get_right().set_parent(tree)
            else:
                # the binding strength of the next operator is lower. Replace the parent node with this operator
                # and rebind the previous parent node
                tree = Node(input_str_split.pop(0), tree, Node(input_str_split.pop(0), None, None, None), tree.get_parent())
                tree.get_left().set_parent(tree)
                tree.get_right().set_parent(tree)
                if not tree.get_parent() == None:
                    if tree.get_parent().get_left() == tree.get_left():
                        tree.get_parent().set_left(tree)
                    else:
                        tree.get_parent().set_right(tree)

        



    print('Unfinished!')
    return









if __name__ == '__main__':
    # print(remove_parenthesis('(((a))+(b))+(((a)))'))
    print(make_tree('a+b*cde'))

