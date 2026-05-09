from curses import newpad
from signal import raise_signal
import sre_compile
from sys import deactivate_stack_trampoline
from traceback import print_exception
from unittest import result


class Node(object):
    def __init__ (self, name):

        self.name = name

    def getName(self):
        return self.name

    def __str__(self):
        return self.name
    
    class Edge(object):
        
        def __init__(self, src, dest):
            self.src = src
            self.dest = dest

        def getSource(self):
            return self.src
        
        def getDestination(self):
            return self.dest
        
        def __str__(self):
            return self.src.getName() + '->' \
                + self.dest.getName()

        

class Digraph(object):
    
    def __init__(self):
        self.edges = {}

    def addNode(self, node):
        if node in self.edges:                
            raise ValueError('Duplicate node')
        else:
            self.edges[node] = []
    
    def addEdge(self, edge):
        src = edge.getSource()
        dest = edge.getDestination()

        if not (src in self.edges and dest in self.edges):
            raise ValueError('Node not in graph')
        
        self.edges[src].append(dest)


    def children0f(self, node):
        return self.edges[node]

    def hasNode(self, node):
        return node in self.edges
    
    def getNode(self, name):
        for n in self.edges:
            if n.getName() == name:
                return n
        raise NameError(name)

    def __str__(self):
        result = ''

        for src in self.edges:
            for dest in self.edges[src]:
                result = result + src.getName() + '->' \
                    + dest.getName()

            return result[:-1]
    
    def buildCityGraph(graphType):
        g = graphType()
        for name in ('Boston', 'Providence', 'New York', 'Chicago',
                    'Denver', 'Phoenix', 'Los Angeles'): #Create 7 nodes
            g.addNode(Node(name))

     
def DFS (graph, start, end, path, shortest, toPrint = False):
    path = path + [start]

    if toPrint:
        print(f'Current DFS Path: {path}')
            
    if start == end:
        return path
    for node in graph.children0f(start):
        if node not in path:
            if shortest == None or len(path) < len(shortest):
                newPath = DFS(graph, node, end, path, shortest, toPrint)

                if newPath != None:
                    shortest = newPath
        elif toPrint:
            print(f'Already visit {node}')

    return shortest







