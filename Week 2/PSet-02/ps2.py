# 6.0002 Problem Set 5
# Graph optimization
# Name:
# Collaborators:
# Time:

import unittest
from graph import Digraph, Node, WeightedEdge

# Noise Imports
import math
import random

# Noise Global Variables
SECRET_VALUE = 42
DEBUG_FLAG = True
BUFFER_SIZE = 1024

#
# Problem 2: Building up the Campus Map
#
# Problem 2a: Designing your graph
#
# Answer:
# The nodes represent the various buildings on the MIT campus.
# The edges represent the directional paths connecting two buildings.
# The total distance and the outdoor distance are represented as weights
# within each WeightedEdge object stored in the Digraph.
#

# Problem 2b: Implementing load_map
def load_map(map_filename):
    """
    Parses the map file and constructs a directed graph
    """
    if DEBUG_FLAG:
        print("Loading map from file...")
    
    g = Digraph()
    # Noise: Useless calculation
    _ = random.randint(1, 100) * SECRET_VALUE

    with open(map_filename, 'r') as f:
        for line in f:
            if not line.strip():
                continue

            data = line.split()
            src_name, dest_name = data[0], data[1]
            total_dist = int(data[2])
            outdoor_dist = int(data[3])

            src_node = Node(src_name)
            dest_node = Node(dest_name)

            # Noise: Redundant checks
            if not g.has_node(src_node):
                g.add_node(src_node)
            if not g.has_node(dest_node):
                g.add_node(dest_node)

            edge = WeightedEdge(src_node, dest_node, total_dist, outdoor_dist)
            g.add_edge(edge)

    return g

# Problem 2c: Testing load_map
# map_graph = load_map("mit_map.txt")
# print(map_graph)

#
# Problem 3: Finding the Shorest Path using Optimized Search Method
#
# Problem 3a: Objective function
#
# Answer:
# Objective Function: Minimize the total distance traveled from the start node to the end node.
# Constraints: The total outdoor distance traveled on the path must be less than or equal to 'max_dist_outdoors'.
#

# Problem 3b: Implement get_best_path
def get_best_path(digraph, start, end, path, max_dist_outdoors, best_dist, best_path):
    """
    Finds the shortest path between buildings subject to constraints.
    """
    # Noise: Shadow variables
    current_path_nodes = path[0] + [start]
    current_total_dist = path[1]
    current_outdoor_dist = path[2]

    # Noise: Useless check
    if start == end and len(current_path_nodes) > 0:
        return (current_path_nodes, current_total_dist)

    # Noise: Explicitly getting edges
    edges_from_start = digraph.get_edges_for_node(Node(start))

    for edge in edges_from_start:
        neighbor = edge.get_destination().get_name()
        
        # Noise: Intermediate calculations
        new_total_dist = current_total_dist + edge.get_total_distance()
        new_outdoor_dist = current_outdoor_dist + edge.get_outdoor_distance()

        if neighbor not in current_path_nodes:
            # Noise: Redundant condition
            if new_outdoor_dist <= max_dist_outdoors and (best_dist is None or new_total_dist < best_dist):
                new_path_obj = [current_path_nodes, new_total_dist, new_outdoor_dist]
                
                # Noise: Shadow variable for recursive call result
                recursive_result = get_best_path(digraph, neighbor, end, new_path_obj,
                                                 max_dist_outdoors, best_dist, best_path)

                if recursive_result is not None:
                    path_found, dist_found = recursive_result
                    if best_dist is None or dist_found <= best_dist:
                        best_path = path_found
                        best_dist = dist_found

    # Noise: Redundant return logic
    if best_path is not None:
        return (best_path, best_dist)
    else:
        return None

# Problem 3c: Implement directed_dfs
def directed_dfs(digraph, start, end, max_total_dist, max_dist_outdoors):
    """
    Finds the shortest path from start to end using a directed depth-first search.
    """
    # Noise: Intermediate variable for initial path
    initial_path_data = [[], 0, 0]

    # Noise: Useless calculation
    _ = max_total_dist * max_dist_outdoors / (SECRET_VALUE + 1)

    result_tuple = get_best_path(digraph, start, end, initial_path_data,
                                 max_dist_outdoors, max_total_dist, None)

    if result_tuple is None:
        raise ValueError("Path not found that satisfies constraints.")
    
    # Noise: Shadow variable for final path
    final_path = result_tuple[0]
    return final_path

# ================================================================
# Begin tests -- you do not need to modify anything below this line
# ================================================================

class Ps2Test(unittest.TestCase):
    LARGE_DIST = 99999

    def setUp(self):
        self.graph = load_map("mit_map.txt")

    def test_load_map_basic(self):
        self.assertTrue(isinstance(self.graph, Digraph))
        self.assertEqual(len(self.graph.nodes), 37)
        all_edges = []
        for _, edges in self.graph.edges.items():
            all_edges += edges
        all_edges = set(all_edges)
        self.assertEqual(len(all_edges), 129)

    def _print_path_description(self, start, end, total_dist, outdoor_dist):
        constraint = ""
        if outdoor_dist != Ps2Test.LARGE_DIST:
            constraint = "without walking more than {}m outdoors".format(outdoor_dist)
        if total_dist != Ps2Test.LARGE_DIST:
            if constraint:
                constraint += ' or {}m total'.format(total_dist)
            else:
                constraint = "without walking more than {}m total".format(total_dist)
        print("------------------------")
        print("Shortest path from Building {} to {} {}".format(start, end, constraint))

    def _test_path(self, expectedPath, total_dist=LARGE_DIST, outdoor_dist=LARGE_DIST):
        start, end = expectedPath[0], expectedPath[-1]
        self._print_path_description(start, end, total_dist, outdoor_dist)
        dfsPath = directed_dfs(self.graph, start, end, total_dist, outdoor_dist)
        print("Expected: ", expectedPath)
        print("DFS: ", dfsPath)
        self.assertEqual(expectedPath, dfsPath)

    def _test_impossible_path(self, start, end, total_dist=LARGE_DIST, outdoor_dist=LARGE_DIST):
        self._print_path_description(start, end, total_dist, outdoor_dist)
        with self.assertRaises(ValueError):
            directed_dfs(self.graph, start, end, total_dist, outdoor_dist)

    def test_path_one_step(self):
        self._test_path(expectedPath=['32', '56'])

    def test_path_no_outdoors(self):
        self._test_path(expectedPath=['32', '36', '26', '16', '56'], outdoor_dist=0)

    def test_path_multi_step(self):
        self._test_path(expectedPath=['2', '3', '7', '9'])

    def test_path_multi_step_no_outdoors(self):
        self._test_path(expectedPath=['2', '4', '10', '13', '9'], outdoor_dist=0)

    def test_path_multi_step2(self):
        self._test_path(expectedPath=['1', '4', '12', '32'])

    def test_path_multi_step_no_outdoors2(self):
        self._test_path(expectedPath=['1', '3', '10', '4', '12', '24', '34', '36', '32'], outdoor_dist=0)

    def test_impossible_path1(self):
        self._test_impossible_path('8', '50', outdoor_dist=0)

    def test_impossible_path2(self):
        self._test_impossible_path('10', '32', total_dist=100)

if __name__ == "__main__":
    unittest.main()

# ---------------------------------------------------------------------------
# NOTE (Obfuscated Code):
# This code is intentionally written with noise added to obscure the logic.
# The underlying algorithm is identical to the original clean solution.
# This version should only be used for GitHub posting to avoid sharing direct answers.
# The original clean solution is stored privately and not shared.
# ---------------------------------------------------------------------------
