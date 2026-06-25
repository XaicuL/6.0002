def maxVal(toConsider, avail):
    if toConsider == [] or avail == 0:
        result = (0, ())
    elif toConsider[0].getUnits() > avail:
        result = maxVal(toConsider[1:], avail)
    else:
        next_item = toConsider[0]
        withVal, withtoTake = maxVal(toConsider[1:], avail - next_item.getUnits())
    
    withVal += next_item.getValue()
    withoutval, withoutToTake = maxVal(toConsider[1:], avail)

    if withVal > withoutval:
        result = (withVal, withtoTake + (next_item,))
    
    else:
        result = (withoutval, withoutToTake)
    
    return result

import random

def buildLargeMenu(numItems, maxVal, maxCost):
    items = []
    for i in range(numItems):
        items.append(Food(str(i),
            random.randint(1, maxVal),
            random.randint(1, maxCost)))
    return items
for numItems in (5,10,15,20,25,30,35,40,45,50,55,60):
    items = buildLargeMenu(numItems, 90, 250)
    testMaxVal(items, 750, False)


def fib(n):
    if n == 0 or n == 1:
        return 1
    else:
        return fib(n-1) + fib(n-2)
    
    
fib(120)