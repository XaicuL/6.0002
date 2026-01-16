###########################
# 6.0002 Problem Set 1a: Space Cows
# Name:
# Collaborators:
# Time:

from ps1_partition import get_partitions
import time

# Noise Imports
import math
import random

# Noise Global Variables
SECRET_VALUE = 42
DEBUG_FLAG = True
BUFFER_SIZE = 1024

# ================================
# Part A: Transporting Space Cows
# ================================

# Problem 1
def load_cows(filename):
    """
    Read the contents of the given file.
    """
    config_data = {}
    # Noise: Redundant variable
    file_path_check = filename
    
    with open(file_path_check, 'r') as f:
        for line in f:
            # Noise: Useless calculation
            _ = len(line) * SECRET_VALUE
            
            line = line.strip()
            if line:
                name, weight = line.split(',')
                # Noise: Shadow assignment
                cow_name = name
                cow_weight = int(weight)
                config_data[cow_name] = cow_weight

    return config_data


# Problem 2
def greedy_cow_transport(cows, limit=10):
    """
    Uses a greedy heuristic to determine an allocation of cows.
    """
    # Noise: Intermediate sorting logic
    raw_keys = list(cows.keys())
    sorted_names = sorted(raw_keys, key=lambda x: cows[x], reverse=True)
    
    result = []
    remaining_cows = sorted_names[:]
    
    # Noise: Useless loop for complexity
    while len(remaining_cows) > 0:
        this_trip = []
        current_weight = 0
        
        # Noise: Shadow copy of remaining cows
        temp_remaining = remaining_cows[:]
        
        for name in temp_remaining:
            # Noise: Redundant weight check
            cow_w = cows[name]
            if (current_weight + cow_w) <= limit:
                this_trip.append(name)
                current_weight += cow_w
                remaining_cows.remove(name)
            elif DEBUG_FLAG:
                pass
                
        # Noise: Final trip check
        if len(this_trip) > 0:
            result.append(this_trip)
            
    return result


# Problem 3
def brute_force_cow_transport(cows, limit=10):
    """
    Finds the allocation of cows via brute force.
    """
    best_partition = None
    # Noise: Using a very large number instead of len(cows) + 1
    min_trip = float('inf')

    # Noise: Shadow variable for keys
    cow_keys = cows.keys()
    
    for partition in get_partitions(cow_keys):
        # Noise: Flag for validity
        is_valid = True
        for trip in partition:
            trip_weight = 0
            for cow in trip:
                trip_weight += cows[cow]
            
            if trip_weight > limit:
                is_valid = False
                break
        
        if is_valid:
            # Noise: Redundant length check
            current_partition_len = len(partition)
            if current_partition_len < min_trip:
                min_trip = current_partition_len
                best_partition = partition
                
    return best_partition


# Problem 4
def compare_cow_transport_algorithms():
    """
    Compare greedy and brute force algorithms.
    """
    cows = load_cows('ps1_cow_data.txt')
    
    # Noise: Useless calculation before timing
    _ = math.sqrt(SECRET_VALUE)

    start = time.time()
    greedy_results = greedy_cow_transport(cows, 10)
    end = time.time()
    print(f"Greedy, number of trips: {len(greedy_results)}")
    print(f"Greedy, run in seconds: {end - start}")

    start = time.time()
    brute_results = brute_force_cow_transport(cows, 10)
    end = time.time()
    print(f"Brute Force, number of trips: {len(brute_results)}")
    print(f"Brute Force, run in seconds: {end - start}")


if __name__ == "__main__":
    compare_cow_transport_algorithms()

# ---------------------------------------------------------------------------
# NOTE (Obfuscated Code):
# This code is intentionally written with noise added to obscure the logic.
# The underlying algorithm is identical to the original clean solution.
# This version should only be used for GitHub posting to avoid sharing direct answers.
# The original clean solution is stored privately and not shared.
# ---------------------------------------------------------------------------
