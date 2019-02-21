
complements = {
    '<': '>',
    '>': '<',
    '[': '',
    ']': '',
    '-': '+',
    '+': '-',
    '.': '',
    ',': ''
}

def optimize(str):
    #check if the next symbol and the current do nothing in the concatenation
    index = 0
    ret = ''
    while index < len(str) and str[index] not in ['.', ',', '[', ']', '<', '>', '+', '-']:
        ret += str[index]
        index += 1

    if not index < len(str):
        return ret

    index2 = index + 1

    while index < len(str):

        while index2 < len(str) and str[index2] not in ['.', ',', '[', ']', '<', '>', '+', '-']:
            index2 += 1

        # in case that the end has been reached
        if index2 == len(str):
            return ret+str[index:]
        # next symbol found
        # check if they are complementary
        if complements[str[index]] == str[index2]:
            #complements has been found.
            ret += str[index+1:index2]
            index = index2+1
            while index < len(str) and str[index] not in ['.', ',', '[', ']', '<', '>', '+', '-']:
                ret += str[index]
                index += 1
            index2 = index+1
        else:
            ret += str[index:index2]
            index = index2
            index2 += 1
    return ret





if __name__ == '__main__':
    # this function optimizes the code

    with open('test_1.bf') as f:
        read = f.read()

    index = 1
    opti = optimize(read)
    while not opti == read:
        index += 1
        read = opti
        opti = optimize(read)

    print(str((index-1)) + ' Optimierungsiterationen durchgefuehrt')

    with open('test_1.bf', 'w') as f:
        f.write(opti)