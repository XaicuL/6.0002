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
        self._weight = weight

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





