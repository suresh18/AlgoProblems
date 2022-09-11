
def rotateLeft(x, y, length):
    '''
    Rotate the passed array left

    :param x:  X Co-ordinate
    :param y: Y Co-ordinate
    :param length: Length of the array
    :return: None
    '''
    global square

    temp = [['E' for c in range(length)] for r in range(length)]

    for r in range(length):
        for c in range(length):
            temp[r][c] = square[x+c][y+length-1-r]

    for r in range(length):
        for c in range(length):
            square[x+r][y+c] = temp[r][c]

def rotateRight(x, y, length):
    '''
    Rotate the passed array right

    :param x:  X Co-ordinate
    :param y: Y Co-ordinate
    :param length: Length of the array
    :return: None
    '''
    global square

    temp = [['E' for c in range(length)] for r in range(length)]

    for r in range(length):
        for c in range(length):
            temp[r][c] = square[x+length-1-c][y+r]

    for r in range(length):
        for c in range(length):
            square[x+r][y+c] = temp[r][c]

def fillBox(x,y):
    '''
    :param x: X Co-ordinate
    :param y: Y Co-ordinate
    :return: True - If any empty box exists
             False - If all boxes are filled (logo is present)
    '''
    global square, symbolCount

    if square[x][y] == 'L':
        square[x][y + 1] = symbolCount
        square[x + 1][y] = symbolCount
        square[x + 1][y + 1] = symbolCount
        symbolCount += 1
        return False
    else:
        square[x][y] = symbolCount

    if square[x][y+1] == 'L':
        square[x + 1][y] = symbolCount
        square[x + 1][y + 1] = symbolCount
        symbolCount += 1
        return False
    else:
        square[x][y+1] = symbolCount

    if square[x+1][y] == 'L':
        square[x + 1][y + 1] = symbolCount
        symbolCount += 1
        return False
    else:
        square[x+1][y] = symbolCount

    symbolCount += 1
    if square[x+1][y+1] == 'L':
        return False
    else:
        return True

def fillPurdueSymbol(x, y, length, quadrant):
    '''
    Fill the Purdue Symbol recursively
    :param x: X Co-ordinate
    :param y: Y Co-ordinate
    :param length: Length of the array
    :param quadrant: Quadrant (1, 2, 3, 4)
                    1. Quadrant containing the origin
                    2. Quadrant right of quadrant 1
                    3. Quadrant below quadrant 1
                    4. Quadrant diagonally opposite to quadrant 1
    :return: hasEmptyBox - True if any empty box is present
                            False if all the boxes are filled
    '''
    global square, i, j, symbolCount
    hasEmptyBox = True
    print('X,Y, length:', x, y, length)

    if length == 2:
        # Fill the 2x2 box with Purdue P Symbol
        hasEmptyBox = fillBox(x, y)
    else:
        # Split the Box into 4 quadrants and call this function recursively
        newLength = int(length / 2)

        # Quadrant 1 does not need the rotation
        ret1 = fillPurdueSymbol(x, y, newLength, 1)

        # Quadrant 2 needs to be processed after rotating left
        # After processing rotate right to bring it back to original position
        rotateLeft(x, y+newLength, newLength)
        ret2 = fillPurdueSymbol(x, y+newLength, newLength, 2)
        rotateRight(x, y + newLength, newLength)

        # Quadrant 3 needs to be processed after rotating right
        # After processing rotate left to bring it back to original position
        rotateRight(x+newLength, y, newLength)
        ret3 = fillPurdueSymbol(x+newLength, y, newLength, 3)
        rotateLeft(x+newLength, y, newLength)

        # If all three quadrants (1,2,3) return that empty square is present
        # then combine them to add a Purdue Symbol using them.
        # This means that quadrant 4 has the Logo and can be processed like
        # quadrant 1 without rotating and also will not have any empty boxes when
        # processing is fully complete. If not quadrant 4 needs to be processed
        # by rotating it twice.
        print(ret1, ret2, ret3)
        if ret1 and ret2 and ret3:
            # Quadrant 1,2,3 returned that they have empty box.
            # Use them to fill a Purdue Symbol
            square[x+newLength-1][y+newLength-1] = symbolCount
            square[x+newLength-1][y+newLength] = symbolCount
            square[x+newLength][y+newLength-1] = symbolCount
            symbolCount += 1
            # Process the quadrant 4 similar to quadrant 1 (no rotation needed)
            ret4 = fillPurdueSymbol(x + newLength, y + newLength, newLength, 1)
            if not ret4:
                hasEmptyBox = False
        else:
            # Quadrant 4 needs to be processed after rotating left twice
            # After processing rotate right twice to return it back to original position
            hasEmptyBox = False
            rotateLeft(x+ newLength, y + newLength, newLength)
            rotateLeft(x+ newLength, y + newLength, newLength)
            ret4 = fillPurdueSymbol(x + newLength, y + newLength, newLength, 4)
            rotateRight(x+ newLength, y + newLength, newLength)
            rotateRight(x+ newLength, y + newLength, newLength)

            # Fill the 3 remaining boxes with the Purdue Symbol
            square[x+newLength][y+newLength] = symbolCount
            print(ret4)
            if ret1:
                square[x+newLength-1][y + newLength - 1] = symbolCount
            if ret2:
                square[x+newLength-1][y + newLength] = symbolCount
            if ret3:
                square[x+newLength][y + newLength - 1] = symbolCount
            symbolCount += 1

    print('\n')
    printSquare(square)
    return hasEmptyBox

def printSquare(square):
    '''
    Code to format and print the array (from stack overflow)
    :param square:
    :return: None
    '''
    s = [[str(e) for e in row] for row in square]
    lens = [max(map(len, col)) for col in zip(*s)]
    fmt = '\t'.join('{{:{}}}'.format(x) for x in lens)
    table = [fmt.format(*row) for row in s]
    print('\n'.join(table))

i = int(input("Enter the Logo's X Cordinate (i): "))
j = int(input("Enter the Logo's Y Cordinate (j): "))
k = int(input("Enter the Box size 2^k (k): "))

length = 2 ** k
symbolCount = 1
square = None

if (i >= length or j >= length):
    print('Invalid co-oordinates ({},{}) for the given box size of {}'.format(i, j, k))
else:
    square = [['E' for c in range(length)] for r in range(length)]
    square[i][j] = 'L'
    fillPurdueSymbol(0, 0, length, 1)
    print('SOLUTION')
    print('Logo Co-Ordinates: ({},{})'.format(i, j))
    print('Box Length: ', length)
    printSquare(square)

