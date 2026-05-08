class food(object):
    def __init__(self, n, v, w):
        self.name = n
        self.value = v
        self.calories = w

    def getValue(self):
        return self.value

    def getCost(self):
        return self.calories
    
    def density(self):
        return self.getValue() / self.getCost()

    def __str__(self):
        return self.name + ': <' + str(self.value)\
+ ', ' + str(self.calories) + '>'


def buildMenu(name, values, calories):
    menu = []

    for i in range(len(values)):
        menu.append(food(name[i], values[i], calories[i]))
    return menu 

def greedy(items, maxCost, keyFunction):
    itemsCopy = sorted(items, key= keyFunction, reverse=True)

    result = []
    totalValue, totalCost = 0.0, 0.0

    for i in range(len(itemsCopy)):
        if (totalCost+itemsCopy[i].getCost()) <= maxCost:
            result.append(itemsCopy[i])
            totalCost += itemsCopy[i].getCost()
            totalValue += itemsCopy[i].getValue()

    return (result, totalValue)

def testGreedy(items, constraint, keyFunction):
    taken, val = greedy(items, constraint, keyFunction)
    print(f'Total value of items take = {val}')

    for item in taken:
        print(' ', item)

def testGreedys(foods, maxUnits):
    print('Use greedy by value to allocate', maxUnits,
'calories')
    testGreedy(foods, maxUnits, food.getValue)
    print('\nUse greedy by cost to allocate', maxUnits,
'calories')
    testGreedy(foods, maxUnits,
        lambda x: 1/food.getCost(x))
    print('\nUse greedy by density to allocate', maxUnits,
'calories')
    testGreedy(foods, maxUnits, food.density)
testGreedys(800)


name = ['wine', 'beer', 'pizza', 'burger', 'fries',
'cola', 'apple', 'donut', 'cake']

values = [89,90,95,100,90,79,50,10]
calories = [123,154,258,354,365,150,95,195]

foods = buildMenu(name, values, calories)

testGreedy(foods, 750)