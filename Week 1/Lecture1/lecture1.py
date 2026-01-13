# # class Food(object):
# #     def __init__(self, n, v, w):
# #         self.name = n
# #         self.value = v
# #         self.calories = w
# #     def getValue(self):
# #         return self.value
# #     def getCost(self):
# #         return self.calories
# #     def density(self):
# #         return self.getValue()/self.getCost()
# #     def __str__(self):
# #         return self.name + ': <' + str(self.value)\
# #                  + ', ' + str(self.calories) + '>'
# #
# # #Food instance & value & calories
# # # 1st : wine & 89 & 123 -> wine: <89, 123>
# # # 2nd : beer & 90 & 154 -> beer: <90, 154>
# # # 3rd : pizza & 95 & 258 -> pizza: <95, 258>
# # # 4th : burger & 100 & 354 -> burger: <100, 354>
# # # 5th : fries & 90 & 365 -> fries: <90, 365>
# # # 6th : cola & 79 & 150 -> cola: <79, 150>
# # # 7th : apple & 50 & 95 -> apple: <50, 95>
# # #omitted below
# #
# #
# # def buildMenu(names, values, calories):
# #     """names, values, calories lists of same length.
# #        name a list of strings
# #        values and calories lists of numbers
# #        returns list of Foods"""
# #     menu = [] #SET list --> empty list if dict =>Error : 'dict' object has no attribute 'append'
# #     for i in range(len(values)):
# #     # for i in range(8):  # values list 'len is 8' <=> for i in range '8'
# #         menu.append(Food(names[i], values[i],calories[i])) #APPEND list elements
# #     return menu
# #
# # def greedy(items, maxCost, keyFunction):
# #     """Assumes items a list, maxCost >= 0,
# #          keyFunction maps elements of items to numbers"""
# #     itemsCopy = sorted(items, key = keyFunction,
# #                        reverse = True)
# #     result = []
# #     totalValue, totalCost = 0.0, 0.0
# #     for i in range(len(itemsCopy)):
# #         if (totalCost+itemsCopy[i].getCost()) <= maxCost:
# #             result.append(itemsCopy[i])
# #             totalCost += itemsCopy[i].getCost()
# #             totalValue += itemsCopy[i].getValue()
# #     return (result, totalValue)
# #
# # def testGreedy(items, constraint, keyFunction):
# #     taken, val = greedy(items, constraint, keyFunction)
# #     print('Total value of items taken =', val)
# #     for item in taken:
# #         print('   ', item)
# #
# # def testGreedys(foods, maxUnits): #maxUnits == 1000
# #     print('Use greedy by value to allocate', maxUnits,
# #           'calories')
# #     testGreedy(foods, maxUnits, Food.getValue)
# #     print('\nUse greedy by cost to allocate', maxUnits,
# #           'calories')
# #     testGreedy(foods, maxUnits,
# #                lambda x: 1/Food.getCost(x))
# #     print('\nUse greedy by density to allocate', maxUnits,
# #           'calories')
# #     testGreedy(foods, maxUnits, Food.density)
# #
# #
# # names = ['wine', 'beer', 'pizza', 'burger', 'fries',
# #          'cola', 'apple', 'donut', 'cake']
# # values = [89,90,95,100,90,79,50,10]
# # calories = [123,154,258,354,365,150,95,195]
# # foods = buildMenu(names, values, calories) #function call , Next step is -> back to the buildMenu(function), parameter is names,values,calories
# # testGreedys(foods, 1000) #function call, Next step is -> back to the buildMenu(function), parameter is food,maxUnits is 10000(Assign)
# #
# # ##print(len(values))
# #
# #
# """"""""""""""""""""""""
#
# class item(object):
#     def __init__(self, n , v , w):
#         self.name = n
#         self.value = v
#         self.weight = w
#
#     def get_name(self):
#         return self.name
#
#     def get_value(self):
#         return self.value
#
#     def get_weight(self):
#         return self.weight
#
#     def __str__(self):
#         return f'{self.name} {self.value} {self.weight}'
#
#
# def value(item):
#     return item.get_value()
#
# def weight_inverse(item):
#     return 1.0 / item.get_weight()
#
# def destiny(item):
#     return item.get_name()
#
# def greedy(items, maxCost, keyFunction):
#     """Assumes items a list, maxCost >= 0,
#          keyFunction maps elements of items to numbers"""
#     itemsCopy = sorted(items, key = keyFunction,
#                        reverse = True)
#     result = []
#     totalValue, totalCost = 0.0, 0.0
#     for i in range(len(itemsCopy)):
#         if (totalCost+itemsCopy[i].getCost()) <= maxCost:
#             result.append(itemsCopy[i])
#             totalCost += itemsCopy[i].getCost()
#             totalValue += itemsCopy[i].getValue()
#     return (result, totalValue)
#
# def build_items():
#     names = ['clock', 'painting', 'radio', 'vase', 'book', 'computer']
#     values = [175,90,20,50,10,200]
#     weights = [10,9,4,2,1,20]
#     Items = []
#
#     for i in range(len(values)):
#         Items.append(item(names[i],values[i],weights[i]))
#     return Items
#
# def test_greedy(max_weight = 20):
#     items = build_items()
#     print(f'use greedy by value to fill knapsack of size {max_weight}')
#     test_greedy(items, max_weight, value())
#     print(f'\n Use greedy by key to fill knapsack of size {max_weight}')
#     test_greedy(items,max_weight,weight_inverse)
#     print(f'\n use greedy by destiny to fill knapsack of size {max_weight}')
#
#     test_greedy(items,max_weight,destiny())
#
#
# def choose_best(pset, max_weight, get_val, get_weight):
#     best_val = 0.0
#     best_set = None
#
#     for items in pset:
#         items_val = 0.0
#         items_weight = 0.0
#
#         for item in items:
#             items_val += get_val(item)
#             items_weight += get_weight(item)
#
#             if items_weight <= max_weight and items_val > items_val:
#                 best_val = items_val
#                 best_set = items
#
#
#         return (best_val, best_set)
#
# def gen_powerset(items, constraint, get_val, get_weight):
#
# def test_best(max_weight = 20):
#     items = build_items()
#     pset = gen_powerset(items)
#     taken, val = choose_best(pset,max_weight, Item.get_value,Item.get_weight)
#
#     print(f'Total value of item taken is {val}')
#
#     for item in taken:
#         print(item)

class node(object):
    def __init__(self, name):
        self._name = name

    def get_name(self):
        return self.name

    def __str__(self):
        return self.name


class edge(object):
    def __init__(self,src,dest):
        self._src = src
        self._dest = dest

    def get_src(self):
        return self._src

    def get(self):
        return self._dest

    def __str__(self):
        return self._src.get_name() + '-> ' + self._dest.get_name()

class weighted_edge(edge):
    def __init__(self,src,dest,weight = 1.0):
        self._src = src
        self._dest = dest
        self._weight =weight

    def get_weight(self):
        return self._weight

    def __str__(self):
        return (f' {self._src.get_name()} -> ({self._weight}) + {self._dest.get_name()}')


class digraph(object):
    def __init__(self):
        self._edges = []
        self._nodes = {}

    def add_edge(self, node):
        if node not in self._nodes:
            raise ValueError('duplicate mode')
        else:
            self._edges.append(node)
            self._edges[node] = []

    def add_edge(self, edge):
        src = edge.get_src()
        dest = edge.get_destination()

        if not (src in self._nodes and dest in self._nodes):
            raise ValueError('Node not in graph')
        self._edges[src].append(dest)

        def childern_of(self, node):
            return self._edges[node]

        def has_node(self, node):
            return node in self._nodes

        def __str__ (self):
            result = ""

            for src in self._nodes:
                for dest in self._edges[src]:
                    result = (result + src.get_name() + '->' + dest.get_name() + '\n')
            return result[:-1]


class graph(digraph):
    def add_edge(self, edge):
        digraph.add_edge(self, edge)
        rev = edge(edge.get_dest(), edge.get_source())
        digraph.add_edge(self, rev)

def print_path(path):
    """Assumes path is a list of nodes"""
    result = ''
    for i in range(len(path)):
        result = result + str(path[i])
        if i != len(path) - 1:
            result = result + '->'
    return result

def DFS(graph, start, end, path, shortest, to_print = False):
    """Assumes graph is a Digraph; start and end are nodes;
          path and shortest are lists of nodes
       Returns a shortest path from start to end in graph"""
    path = path + [start]
    if to_print:
        print('Current DFS path:', print_path(path))
    if start == end:
        return path
    for node in graph.children_of(start):
        if node not in path: #avoid cycles
            if shortest == None or len(path) < len(shortest):
                new_path = DFS(graph, node, end, path, shortest,
                              to_print)
                if new_path != None:
                    shortest = new_path
    return shortest

def shortest_path(graph, start, end, to_print = False):
    """Assumes graph is a Digraph; start and end are nodes
       Returns a shortest path from start to end in graph"""
    return DFS(graph, start, end, [], None, to_print)





