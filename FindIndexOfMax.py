import math

def findMaxIndex(start, end):
    global ar

    index = int(math.floor(start + end) / 2)
    if ar[index] > ar[index+1]:
        if ar[index] > ar[index-1]:
            return index
        else:
            return findMaxIndex(start, index)
    else:
        return findMaxIndex(index+1, end)

ar = [2, 5, 7, 18, 27, 18, 5]

result = findMaxIndex(0, len(ar) - 1)
print('Result :', result)
