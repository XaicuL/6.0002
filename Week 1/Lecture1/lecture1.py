class Food(object):
    def __init__(self, n, v, w):
        self.name = n
        self.value = v
        self.calories = w
    def getValue(self):
        return self.value
    def getCost(self):
        return self.calories
    def density(self):
        return self.getValue()/self.getCost()
    def __str__(self):
        return self.name + ': <' + str(self.value)\
                 + ', ' + str(self.calories) + '>'

#Food instance & value & calories
# 1st : wine & 89 & 123 -> wine: <89, 123>
# 2nd : beer & 90 & 154 -> beer: <90, 154>
# 3rd : pizza & 95 & 258 -> pizza: <95, 258>
# 4th : burger & 100 & 354 -> burger: <100, 354>
# 5th : fries & 90 & 365 -> fries: <90, 365>
# 6th : cola & 79 & 150 -> cola: <79, 150>
# 7th : apple & 50 & 95 -> apple: <50, 95>
#omitted below


def buildMenu(names, values, calories):
    """names, values, calories lists of same length.
       name a list of strings
       values and calories lists of numbers
       returns list of Foods"""
    menu = [] #SET list --> empty list if dict =>Error : 'dict' object has no attribute 'append'
    for i in range(len(values)):
    # for i in range(8):  # values list 'len is 8' <=> for i in range '8'
        menu.append(Food(names[i], values[i],calories[i])) #APPEND list elements
    return menu

def greedy(items, maxCost, keyFunction):
    """Assumes items a list, maxCost >= 0,
         keyFunction maps elements of items to numbers"""
    itemsCopy = sorted(items, key = keyFunction,
                       reverse = True)
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
    print('Total value of items taken =', val)
    for item in taken:
        print('   ', item)

def testGreedys(foods, maxUnits): #maxUnits == 1000
    print('Use greedy by value to allocate', maxUnits,
          'calories')
    testGreedy(foods, maxUnits, Food.getValue)
    print('\nUse greedy by cost to allocate', maxUnits,
          'calories')
    testGreedy(foods, maxUnits,
               lambda x: 1/Food.getCost(x))
    print('\nUse greedy by density to allocate', maxUnits,
          'calories')
    testGreedy(foods, maxUnits, Food.density)


names = ['wine', 'beer', 'pizza', 'burger', 'fries',
         'cola', 'apple', 'donut', 'cake']
values = [89,90,95,100,90,79,50,10]
calories = [123,154,258,354,365,150,95,195]
foods = buildMenu(names, values, calories) #function call , Next step is -> back to the buildMenu(function), parameter is names,values,calories
testGreedys(foods, 1000) #function call, Next step is -> back to the buildMenu(function), parameter is food,maxUnits is 10000(Assign)

##print(len(values))
