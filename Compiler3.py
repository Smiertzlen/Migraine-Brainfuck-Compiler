import tree_pprint

operator_brain = {
    '+': ('<[-<+>]', -1),
    '-': ('<[-<->]', -1),
    '*': ('<<[->>+<<]>[->[->+<<<+>>]>[-<+>]<]>[-]<', -1),
    '!': ('+<[[-]>-<]>[-<+>]', 0),  # to_invert|0 benötigt nur diese Bieden plätze für die Invetierung. Pointer auf 0
    '&&': ('++<<[[-]>>-<<]+>[[-]>-<]>[[-]<<->>]<', -1),
    '-&': ('++<<[[-]>>-<<]+>[[-]>-<]>[[-]<<->>]<+<[[-]>-<]>[-<+>]', -1), # kombi: x y and not !(x&&y)
    '||': ('<<[[-]>>+<<]>[[-]>+<]>[[-]<<+>>]<', -1),
    '-|': ('<<[[-]>>+<<]>[[-]>+<]>[[-]<<+>>]<+<[[-]>-<]>[-<+>]', -1),
    '-^': ('<<[[-]>>+<<]+>[[-]>-<]>[[-]<<->>]<', -1), #xnor also true wenn beide true oder beide false
    '==': ('<<[->-<]+>[[-]<->]', -1),
    '-=': ('<<[->-<]>[[-]<+>]', -1), # this means not equal
    '<=': ('>>+<<<<[>[->>+<<]>>[-<+<+>>]+<[[-]>-<]>[-<+>]<[-<+<[-]+>>>>-<<]<-<-]>>>>[-<<<<+>>>>]<<<[-]', -1),
    '>=': ('', -1),
    '<': ('', -1),
    '>': ('', -1)
}


# fehlende Operatoren: / % && ||



# Diese Klasse wird benötigt, um einen Ableitungsbaum für reguläre Ausdrücke zu erstellen
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


# Diese Funktion bestimmt einen Ableitungsbaum für einen regulären Ausdruck, welcher keine Klammern enthält
# Insbesondere sind auch Variablenbestimmungen (gekennzeichnet durch $) erlaubt.
def make_tree(string):
    # OPTIMIEREN!!!!!
    string_thesis = []
    checker = ''
    if len(string) == 0:
        print('upps')
    # Initiales Zeichen (ein jeder ausdruck besteht aus mindestens einer variablen)
    while string and (string[0].isalnum() or string[0] in ['$', '!']):
        checker += string[0]
        string = string[1:]
    string_thesis.append(checker)
    # ab hier ist das nächste zeichen ein operator
    while string:
        # lese den operator
        # Überprüfe, ob ein doppeloperator vorliegt. Nachvorübersetzung gibt es keine anderen außer den hier definierten
        # equal, lower/equal, greater/equal, unequal, or, and, nand, nor, xnor
        if string[0:2] in ['==', '<=', '>=', '-=', '||', '&&', '-&', '-|', '-^']:
            string_thesis.append(string[0:2])
            string = string[2:]
        else:
            string_thesis.append(string[0])
            string = string[1:]
        checker = ''
        # lese den nächsten variablennamen
        while string and (string[0].isalnum() or string[0] in ['$', '!']):
            checker += string[0]
            string = string[1:]
        string_thesis.append(checker)
    # return string_thesis
    global tree
    tree = Node(string_thesis[0], None, None, None)
    string_thesis = string_thesis[1:]
    if string_thesis:
        tree = Node(string_thesis[0], tree, Node(string_thesis[1], None, None, None), None)
        tree.get_left().set_parent(tree)
        tree.get_right().set_parent(tree)
        # an dieser stelle ist der initiale neue Baum gesetzt.
        # setze als derzeitigen knoten tree
        current_node = tree
        # mehr als nur eine simple variable. Füge den ersten Operator hinzu

        string_thesis = string_thesis[2:]

        # bindungsstärke der operatoren nachlesen!
        # Das hier kann auch als dictionary mit tiefen als abbildungen implementiert werden!
        #operators = '< > == <= >= + - * / %'
        operators = {
            '&&': 0,
            '||': 0,
            '-^': 0,
            '-&': 0,
            '-|': 0,

            '<': 1,
            '>': 1,
            '<=': 1,
            '>=': 1,
            '==': 1,
            '-=': 1,

            '+': 2,
            '-': 2,
            '*': 3,
            '/': 3
        }

        while string_thesis:
            # überprüfe die bindungsstärke des neuen un des markierten operators
            # stärker bindender operator
            # if operators.find(string_thesis[0]) > operators.find(current_node.get_op()):
            if operators[string_thesis[0]] > operators[current_node.get_op()]:
                new_op = Node(string_thesis[0], current_node.get_right(), Node(string_thesis[1], None, None, None),
                              current_node)
                new_op.get_right().set_parent(new_op)
                current_node.set_right(new_op)
                current_node = new_op
            # schwächer bindender operator
            else:
                new_op = Node(string_thesis[0], current_node, Node(string_thesis[1], None, None, None),
                              current_node.get_parent())
                new_op.get_right().set_parent(new_op)

                # an dieser stelle noch ungut...gucken was passiert wenn ich fälle im obersten knoten habe!
                # in diesem fall stehen im übrigen vergleichsoperatoren
                # diese haben die schwächste bindung, da diese erst ganz zum schluss ausgerechnet werden können

                if not current_node.get_parent() == None:
                    current_node.get_parent().set_right(new_op)
                else:
                    tree = new_op
                current_node.set_parent(new_op)
                current_node = new_op
            string_thesis = string_thesis[2:]


    # bevor der Baum zurückgegeben wird, muss er von ! befreit werden.
    # durchsuche also den Baum rekursiv und ersetze '!' durch entsprechende neue Knoten

    recusive_not(tree)
    while not tree.get_parent() == None:
        tree = tree.get_parent()


    return tree


def recusive_not(tree):
    if tree.get_left() == None:
        # hier haben wir den Fall eines Blattes. Bei ! wird IMMER der linke Baumknoten behandelt
        op = tree.get_op()
        par = tree.get_parent()
        if op.startswith('!'):
            new_tree = Node('!', tree, None, par)
            tree.set_op(op[1:])
            if not par == None:
                # Elternknoten existiert!
                if par.get_left() == tree:
                    par.set_left(new_tree)
                else:
                    par.set_right(new_tree)
            tree.set_parent(new_tree)
            recusive_not(tree)
    else:
        # kein Blatt. Untersuche den linken knoten und falls er existiert den rechten
        recusive_not(tree.get_left())
        if not tree.get_right() == None:
            recusive_not(tree.get_right())

# Diese funktion entfernt Klammern. Achtung! (a) wird nicht entfernt. Dies muss noch bearbeitet werden
def entferne_klammern(string):
    to_close = []
    liste = []
    indexer = []
    counter = -1

    for i in range(0, len(string)):
        if string[i] == '(':
            liste.append(not string[i + 1] == '(')
            counter += 1
            to_close.append(counter)
        if string[i] == ')':
            closure = to_close.pop()
            indexer.append(closure)
            liste[closure] = liste[closure] or not string[i - 1] == ')'

    # print(liste)
    # print(indexer)

    open_count = -1
    close_count = -1

    output = ''
    for i in range(0, len(string)):
        if string[i] == '(':
            open_count += 1
            if liste[open_count]:
                output += '('
            continue
        if string[i] == ')':
            close_count += 1
            if liste[indexer[close_count]]:
                output += ')'
            continue
        output += string[i]
    print(output)


# Diese funktion entfernt Klammern. Achtung! (a) wird nicht entfernt. Dies muss noch bearbeitet werden
# Auch bei (a+b)+c dürfen die Klammern entfernt werden.
# Optimierungen können noch implementiert werden
def entferne_klammern2(string):
    to_close = []
    liste = []
    indexer = []
    counter = -1

    for i in range(0, len(string)):
        if string[i] == '(':
            liste.append(not string[i + 1] == '(')
            counter += 1
            to_close.append(counter)
        if string[i] == ')':
            closure = to_close.pop()
            indexer.append(closure)
            liste[closure] = liste[closure] or not string[i - 1] == ')'

    # print(liste)
    # print(indexer)

    open_count = -1
    close_count = -1

    output = ''
    for i in range(0, len(string)):
        if string[i] == '(':
            open_count += 1
            if liste[open_count]:
                output += '('
            continue
        if string[i] == ')':
            close_count += 1
            if liste[indexer[close_count]]:
                output += ')'
            continue
        output += string[i]
    print(output)


# Erstellt einen Ableitungsbaum mit Einhaltung der Klammerungsregeln
def make_tree_klammer(string):
    # ersetze die ersten Klammerausdrücke durch ein ;i für i als index innerhalb der substutitionsregel

    # sollte der string keinerlei klammern mehr enthalten, so führe direkt die make_tree funktion aus
    # und gebe den so erzeugten Baum zurück
    if '(' not in string:
        return make_tree(string)
    substitution = []
    index = 0
    i = 0
    to_check = string
    while i < len(string):
        if string[i] == '(':
            indexer = i
            depth = 1
            while depth:
                i += 1
                if string[i] == '(':
                    depth += 1
                if string[i] == ')':
                    depth -= 1
            # an der stelle i befindet sich nun also die zugehörige klammer zu
            # substituiere den klammerausdruck
            to_check = to_check.replace(string[indexer:i + 1], '$' + str(index))
            substitution.append(string[indexer:i + 1])
            index += 1
        i += 1
    # nun sind alle bereiche substituiert.
    # wende die baumfunktion auf den substituierten string an und wende diese funktion auf alle kinder an
    tree = make_tree(to_check)
    # wende die substitutionen rückwärts an
    recursive_search2(tree, substitution)

    while not tree.get_parent() == None:
        tree = tree.get_parent()

    return tree


# def recursive_swap(tree, substitution)

# Rekursive Suche nach noch nicht komplett ausgewerteten Ausdrücken
def recursive_search2(tree, substitutions):
    if tree.get_left() == None:
        # Blatt gefunden!
        # überprüfe auf substutierten klammerausdruck. wenn ja dann den unterbaum erzeugen und einbinden
        if tree.get_op().startswith('$'):
            sub_tree = make_tree_klammer(substitutions[int(tree.get_op()[1:])][1:-1])
            tree.set_op(sub_tree.get_op())
            tree.set_left(sub_tree.get_left())
            if not tree.get_left() == None:
                tree.set_right(sub_tree.get_right())
                sub_tree.get_left().set_parent(tree)
                sub_tree.get_right().set_parent(tree)
        # kein Klammerausdruck. Der ausdruck der hier steht ist bereits fertig. Nichts tun
    else:
        recursive_search2(tree.get_left(), substitutions)
        if not tree.get_right() == None:
            recursive_search2(tree.get_right(), substitutions)


def compile(file, output, debug=False):
    # Diese Funktion kompiliert eine gültige code Datei zu einer bf Datei.
    # Zu implementieren:
    # + Variablenzuweisungen
    # + Tiefen für Variablen
    # - Löschen von Variablen mit zu hoher tiefenzuordnung, sobald sich die Tiefe verringert
    # - auswerten von regulären Ausdrücken
    # - Einordnung von while Schleifen
    # (- For schleifen)
    # + String ausgabe
    # + Variablen einlesen
    # + Ausgabe von Strings
    # + Ausgabe von gemischten Strings print('Hallo ' + n + ' Welten') gibt aus für n=ord('4'): Hallo 4 Welten

    with open(file, 'r') as f:
        with open(output, 'w') as out:

            current_depth = 0
            var_dic = {0: []}
            loc_dic = {}

            loop_loc = []

            current_location = 0

            read = f.readline()
            while read:
                read = read.split('#')[0]
                # Entferne alle komischen nicht gewollten Zeichen aus read
                read = read.rstrip().lstrip()

                if not read:
                    read = f.readline()
                    continue

                # Hier wird angenommen, dass Variablen nicht mehrfach belegt werden!
                if read.startswith('byte'):

                    var_dic[current_depth].append((read[5:], current_depth, current_location))
                    loc_dic[read[5:]] = current_location
                    current_location += 1
                    #out.writelines([read, '>'])
                    if debug:
                        read = comment(read)
                        out.writelines(read + '\n')
                    out.writelines('>\n\n')
                    read = f.readline()
                    continue
                if read.startswith('while'):
                    # hier muss überprüft werden, ob die bedingung überhaupt erfüllt ist. zudem muss die position
                    # gespeichert werden
                    # Auswertung des sich in klammern befindlichen ausdrucks
                    #while(exp){
                    exp = read[6:-2]
                    #auswerten der expression
                    brain_code, new_loc = recursive_eval(make_tree_klammer(exp), loc_dic, current_location)
                    exp = brain_code
                    #now the evaluation should be in the currently pointed address
                    brain_code += '<[>'
                    loop_loc.append(('while', exp, current_location))

                    # increase the depth and location to account for the loop
                    current_depth += 1
                    current_location += 1

                    var_dic[current_depth] = []

                    if debug:
                        out.writelines(comment(read) + '\n')
                    out.writelines(brain_code + '\n\n')
                    #print(exp)
                    #print('Not implemented yet: while-do loops')


                    # at this point the while loop is initialized. until the corresponding '}'

                    read = f.readline()
                    continue
                if read.startswith('if'):
                    # hier muss der nachfolgende ausdruck überprüft werden. Zudem kann ein else auftreten ('}' Fall)

                    exp = read[3:-2]
                    #contains the expression of the if statement

                    brain_code, loc = recursive_eval(make_tree_klammer(exp), loc_dic, current_location)

                    # at this point, loc has to be current_location+1. Otherwise it is a runtime compiler error
                    #print(current_location)
                    #print(loc)

                    exp = brain_code
                    brain_code += '<[>'

                    # set the current location, as there is the actual bit found
                    loop_loc.append(('if', exp, current_location))

                    current_location = loc
                    current_depth += 1

                    var_dic[current_depth] = []


                    # at this point, the conditioning for the if statement is complete

                    if debug:
                        out.writelines(comment(read) +'\n')
                    out.writelines(brain_code)

                    #print('Not implemented yet: if statements')
                    read = f.readline()
                    continue
                if read.startswith('for'):
                    # in diesem fall muss noch implementiert werden, dass ein Zähler (welcher auch in der schleife
                    # verfügbar sein muss gezählt wird.

                    # for a for loop to actually do something, there must be 3 things
                    # 1) if n=start:stepsize:end, n <= end or n >= end if stepsize < 0 must be obheld.
                    # 2) if n=start:stepsize:end, n <= n+stepsize or n >= n+stepsize if stepsize < 0 must be obheld

                    # first of read the expression inside the for loop brackets
                    exp = read[4:-2]
                    exp = exp.split('=')

                    #exp = ['<name>', 'start:stepsize:end']
                    var_name = exp[0]
                    exp = exp[1].split(':')

                    # at this point, one should mention that in the '}' case, this variable has to be removed!
                    var_dic[current_depth].append((var_name, current_depth, current_location))
                    loc_dic[var_name] = current_location

                    brain_str = create_number(int(exp[0])) + create_number(int(exp[1])) + create_number(int(exp[2]))

                    # check if the loop can be initialized. Therefore check if exp[0] <= exp[2]
                    # n p q |
                    # after this, current_location += 1
                    brain_str += copy_variable(current_location, current_location+3)
                    # after this, current_location += 1
                    brain_str += copy_variable(current_location, current_location+3)
                    # after this, current_location -= 1
                    brain_str += operator_brain['<='][0]

                    brain_str += '<[>'



                    current_depth += 1
                    # n p q b |  so +4
                    current_location += 4
                    var_dic[current_depth] = []

                    loop_loc.append(('for', var_name, current_location-1))

                    if debug:
                        read = comment(read)
                        out.writelines(read + '\n')
                    out.writelines(brain_str + '\n\n')

                    #print('Not implemented yet: for loops')
                    read = f.readline()
                    continue
                if read.startswith('do'):
                    #print('Not implemented yet: do-while loops')

                    # in this case, just increase the current pointer and start the loop
                    brain_code = '+[>'
                    loop_loc.append(('do', '', current_location))
                    current_depth += 1
                    current_location += 1



                    var_dic[current_depth] = []

                    if debug:
                        out.writelines(comment(read) +'\n')
                    out.writelines(brain_code)

                    read = f.readline()
                    continue
                if read.startswith('}'):
                    # loop end

                    # check for the last loop or statement. Act accordingly
                    last = loop_loc.pop()

                    # first of all: remove all variables that were initialized and remove them from the dictionary
                    # Get all the variable names for the current depth
                    vars = var_dic.pop(current_depth, None)

                    # remove the variables from loc_dic
                    for elem in vars:
                        loc_dic.pop(elem, None)

                    # now go backwarts to the position last[2]+1
                    # create the brainfuck code that deletes every variables until that point is reached
                    brain_str = '<[-]'*(current_location-last[2]-1)
                    current_location = last[2] + 1

                    # check for the loop/statement. Take steps accordingly:
                    # - if statement: check for an else block and add it to the queue if given or remove the eval value
                    # - else: remove the evaluation value
                    # - while loop: reevaluate the given expression by inserting it
                    # - do: extract the expression and evaluate it
                    if last[0] == 'if':
                        if 'else' in read:
                            # else block found. Invert the if statement expression result and add it to the queue
                            # this is done by copying the value to the right, ending the loop
                            # and copying the inverted value back. after that start the else block
                            brain_str += '<[->+<]]>>' + operator_brain['!'][0] + '<[-<+>]<[>'
                            loop_loc.append(('else', '', current_location - 1))
                            var_dic[current_depth] = []
                            if debug:
                                read = comment(read)
                                out.writelines(read + '\n')
                            out.writelines(brain_str + '\n\n')
                            read = f.readline()
                            continue
                        else:
                            # no else block is present.
                            brain_str += '<[-]]'
                            current_depth -= 1
                            current_location -= 1
                            if debug:
                                read = comment(read)
                                out.writelines(read + '\n')
                            out.writelines(brain_str + '\n\n')
                            read = f.readline()
                            continue
                    if last[0] == 'else':
                        #the end of the else block has been found. close the loop
                        brain_str += '<[-]]'
                        current_depth -= 1
                        current_location -= 1
                        if debug:
                            read = comment(read)
                            out.writelines(read + '\n')
                        out.writelines(brain_str + '\n\n')
                        read = f.readline()
                        continue
                    if last[0] == 'while':
                        # while loop has been found. reevaluate the condition marked in last[1]
                        # after that, decrease the depth and position
                        # one must not worry about the loop ending and pointer correctness
                        # the pointer will remain at the index marker for the loop. but as soon as the loops ends,
                        # the value at this index marker will be zero
                        brain_str += '<[-]' + last[1] + '<]'
                        current_location -= 1
                        current_depth -= 1
                        if debug:
                            read = comment(read)
                            out.writelines(read + '\n')
                        out.writelines(brain_str + '\n\n')
                        read = f.readline()
                        continue
                    if last[0] == 'do':
                        # a do while loop has been found. scan for the condition and evaluate it
                        #print(last)
                        exp = read[7:-1]
                        brain_code, loc = recursive_eval(make_tree_klammer(exp), loc_dic, current_location-1)
                        brain_str += '<-' + brain_code + '<]'
                        current_location -= 1
                        current_depth -= 1
                        if debug:
                            read = comment(read)
                            out.writelines(read + '\n')
                        out.writelines(brain_str + '\n\n')
                        read = f.readline()
                        continue
                    if last[0] == 'for':
                        # ending of a for loop
                        # check if the for loop must be continued

                        # clear the bit and recalculate it

                        # this may be optimized with the remove loop at the beginning
                        brain_str = '<[-]'

                        # n p q b
                        # 0 0 0 1
                        current_location -= 1

                        brain_str += copy_variable(current_location-3, current_location)
                        brain_str += copy_variable(current_location-2, current_location)
                        brain_str += operator_brain['<='][0]
                        # n p q b |

                        brain_str += '<<<<[>>>>>>+<<<<<<-]>>>>>>[-<+<+<<<<+>>>>>>]'
                        # n p q b n n |

                        # n+q q p n n+q |
                        brain_str += '<<<<<[->>>>>+<<<<<]>>>>>[-<+<<<<+<+>>>>>>]'
                        brain_str += operator_brain['<='][0]
                        brain_str += operator_brain['&&'][0]

                        brain_str += '<]<[-]<[-]<[-]'

                        current_location -= 3
                        current_depth -= 1

                        loc_dic.pop(last[1])
                        # remove the variable from the current_depth var dic
                        var_dic[current_depth] = [v for v in var_dic[current_depth] if not v == last[1]]

                        if debug:
                            read = comment(read)
                            out.writelines(read + '\n')
                        out.writelines(brain_str + '\n\n')

                        read = f.readline()
                        continue

                    print(last)
                    print(read)
                    exit(1)




                    #print('Not implemented yet: loop and statement endings')
                    #read = f.readline()
                    #continue

                # At this point, only a variable change or a print can be possible
                if read.startswith('print'):
                    #print('Not implemented yet: print')
                    brain_str = print_brain(read[6:-1], current_location, loc_dic)

                    if debug:
                        read = comment(read)
                        out.writelines(read + '\n')
                    out.writelines(brain_str + '\n\n')
                    read = f.readline()
                    continue


                # Variablen Manipulation entdeckt.


                #var_rep = read.split('=')
                index = read.find('=')
                var_rep = [read[0:index], read[index], read[index+1:]]


                #if var_rep[0][-1] in '+-*/%':
                #    var_rep = [var_rep[0][0:-1], var_rep[0][-1] + '=', var_rep[1]]
                #else:
                # der obige Fall von += etc wird nicht behandelt. In einer zukünftigen Variante kann dies implementiert
                # werden


                #var_rep = [var_rep[0], '=', var_rep[1]]

                # create a tree for var_rep[2]
                tree = make_tree_klammer(var_rep[2])

                # Rekursiv den Baum auswerten lassen

                brain_code, current_location = recursive_eval(tree, loc_dic, current_location)
                # die Variable rüberkopieren
                current_location -= 1
                brain_code += '<' + copy_variable(current_location, loc_dic[var_rep[0]])

                if debug:
                    read = comment(read)
                    out.writelines(read + '\n')
                out.writelines(brain_code + '\n\n')




                read = f.readline()
                #print('Not implemented yet: variable manipulation')

# kopiert die variable von x nach y.
# hält auf dem nächsten feld rechts von der Kopierten variablen an bzw auf dem leer gewordenen Feld
def copy_variable(pos_x, pos_y):
    if pos_x < pos_y:
        shift = pos_y - pos_x
        ls = '<'*shift
        rrs = '>'*(shift+1)
        lls = ls + '<'
        return ls + '[-' + rrs + '+' + lls + ']' + rrs + '[-<+' + ls + '+' + rrs + ']'
    shift = pos_x - pos_y
    ls = '<'*shift
    rs = '>'*shift
    return ls + '[-]' + rs + '[-' + ls + '+' + rs + ']'

# Hier ist noch etwas kaputt...
# bei [1 2 6 0 0] gibt er 0 aus und der Speicher sieht aus: [1 2 6 6 0] mit zeiger auf der letzten 0
def print_brain(str, pos, vars):
    #spalte zunächst den String zwischen den korrekten + Zeichen auf
    index = 0
    splitted = []
    while index < len(str):
        if str[index] == '"':
            read = ''
            # String wurde gefunden. Mahce weiter, bis der String zuende ist
            index = index+1
            while not str[index] == '"':
                read += str[index]
                index += 1
            # kompletter String wurde gelesen. Das nächste Zeichen ist ein +
            index += 2
            splitted.append((read, 'str'))
        else:
            # in diesem Fall wurde eine Variable gefunden
            read = str[index]
            index += 1
            while index < len(str) and not str[index] == '+':
                read += str[index]
                index += 1
            index += 1

            # an dieser Stelle könnte man versuchen, formelverarbeitung einzubauen

            splitted.append((read, 'var'))

    # Nun ist der auszugebende String aufgeteilt. Mappe die entsprechenden anteile
    out = ''
    for tupel in splitted:
        if tupel[1] == 'str':
            out += create_string(tupel[0])
        else:
            out += copy_variable(vars[tupel[0]], pos) + '<.[-]'

    return out



def create_string(str):
    mapped = list(map(ord, str))
    out = ''
    current_val = 0
    if not str:
        return out
    for i in mapped:
        if current_val < i:
            out += '+'*(i-current_val)
        else:
            out += '-'*(current_val-i)
        current_val = i
        out += '.'
    out += '[-]'
    return out


def create_number(n):
    # Das geht auch deutlich effektiver!
    # TODO: Besser Machen
    return '+'*n + '>'


# Diese funktion geht rekursiv den Baum durch mittels breitensuche
# es werden entsprechende Variablen kopiert
# das dictionary behandelt name und position der variablen
# zurückgegeben wird ein zu schreibender String. Die folgende Position ist die Ursprüngliche+1
def recursive_eval(tree, vars, pointer):

    # Anwendung auf einen inneren knoten
    if not tree.get_left() == None:
        out = ''
        # In diesem Fall: Anwenden der rekursiven Methode auf die Kinder
        # Update des Pointers
        next, pointer = recursive_eval(tree.get_left(), vars, pointer)
        out += next
        if not tree.get_right() == None:
            next, pointer = recursive_eval(tree.get_right(), vars, pointer)
            out += next
        out += operator_brain[tree.get_op()][0]
        pointer += operator_brain[tree.get_op()][1]
        return (out, pointer)
    #Anwendung auf ein Blatt
    else:
        # In diesem Fall ist man bei einem Blatt angekommen
        check = tree.get_op()
        # Eine Nummer ist vorhanden. Diese muss noch umgewandelt werden
        if check.isdigit():
            return (create_number(int(check)), pointer+1)
        # Es handelt sich um eine Variable
        # kopiere den Wert
        return copy_variable(vars[check], pointer), pointer+1




# Für die Schönere Berechnung: Man mehme die Wurzel int(x) der Zahl z. Dann berechnet man: y=z//x. Dies gibt die Anzahl der
# Wiederholungen an. Danach noch entsprechend viele '+'*(z%x) um den Rest aufzufüllen





def comment(read):
    read = read.replace('<=', ' KLEINER GLEICH ')
    read = read.replace('==', ' GLEICH GLEICH ')
    read = read.replace('>=', ' GROESSER GLEICH ')
    read = read.replace('+', ' PLUS ')
    read = read.replace('-', ' MINUS ')
    read = read.replace('=', ' GLEICH ')
    read = read.replace('*', ' MAL ')
    read = read.replace('/', ' GETEILT ')
    read = read.replace('%', ' MODULO ')
    read = read.replace('<', ' KLEINER ')
    read = read.replace('>', ' GROESSER ')
    return read




if __name__ == '__main__':
    #compile('test_in.code', 'test_out.bf', True)
    # t = make_tree_klammer('!(!((a+1)==b)==3)')
    #t = make_tree_klammer('!(a+b)')
    #t = make_tree_klammer('(1+2)*3')
    #brain = recursive_eval(t, {}, 0)
    #print(brain)
    compile('test_1.code', 'test_1.bf', True)
    #t = make_tree_klammer('a*1==b')
    #t.pprint()

    #geht kaputt!
    #t = make_tree_klammer('!((a+!(b))*c==!!!!!4)')
    #t = make_tree_klammer('c==!a')
    #t.pprint()
    print('Done')
