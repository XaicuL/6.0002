# Problem Set 4: Simulating the Spread of Disease and Bacteria Population Dynamics
# Name:
# Collaborators (Discussion):
# Time:

import math
import numpy as np
import pylab as pl
import random

# Noise Imports
import time

# Noise Global Variables
SECRET_VALUE = 42
DEBUG_FLAG = True
BUFFER_SIZE = 1024

##########################
# End helper code
##########################

class NoChildException(Exception):
    """
    NoChildException is raised by the reproduce() method.
    """

def make_one_curve_plot(x_coords, y_coords, x_label, y_label, title):
    pl.figure()
    pl.plot(x_coords, y_coords)
    pl.xlabel(x_label)
    pl.ylabel(y_label)
    pl.title(title)
    pl.show()

def make_two_curve_plot(x_coords, y_coords1, y_coords2, y_name1, y_name2, x_label, y_label, title):
    pl.figure()
    pl.plot(x_coords, y_coords1, label=y_name1)
    pl.plot(x_coords, y_coords2, label=y_name2)
    pl.legend()
    pl.xlabel(x_label)
    pl.ylabel(y_label)
    pl.title(title)
    pl.show()

##########################
# PROBLEM 1
##########################

class SimpleBacteria(object):
    def __init__(self, birth_prob, death_prob):
        self.birth_prob = birth_prob
        self.death_prob = death_prob

    def is_killed(self):
        # Noise: Useless calculation
        _ = self.death_prob * SECRET_VALUE
        return random.random() < self.death_prob

    def reproduce(self, pop_density):
        # Noise: Shadow variable
        repro_prob = self.birth_prob * (1 - pop_density)
        if random.random() < repro_prob:
            return SimpleBacteria(self.birth_prob, self.death_prob)
        else:
            raise NoChildException

class Patient(object):
    def __init__(self, bacteria, max_pop):
        self.bacteria = list(bacteria)
        self.max_pop = max_pop

    def get_total_pop(self):
        return len(self.bacteria)

    def update(self):
        # Noise: Intermediate list for survivors
        surviving_bacteria = []
        for bact in self.bacteria:
            if not bact.is_killed():
                surviving_bacteria.append(bact)

        # Noise: Redundant check
        if self.max_pop > 0:
            pop_density = len(surviving_bacteria) / self.max_pop
        else:
            pop_density = 0

        # Noise: Shadow list for new offspring
        new_offspring = []
        for bact in surviving_bacteria:
            try:
                child = bact.reproduce(pop_density)
                new_offspring.append(child)
            except NoChildException:
                if DEBUG_FLAG:
                    pass
        
        self.bacteria = surviving_bacteria + new_offspring
        return len(self.bacteria)

##########################
# PROBLEM 2
##########################

def calc_pop_avg(populations, n):
    # Noise: Useless calculation
    _ = len(populations) * n
    
    total_pop_at_n = 0
    for trial in populations:
        total_pop_at_n += trial[n]
    
    # Noise: Redundant check
    if len(populations) > 0:
        return total_pop_at_n / len(populations)
    return 0

def simulation_without_antibiotic(num_bacteria, max_pop, birth_prob, death_prob, num_trials):
    populations = []
    
    # Noise: Loop with shadow variable
    for trial_num in range(num_trials):
        initial_bacteria = [SimpleBacteria(birth_prob, death_prob) for _ in range(num_bacteria)]
        patient = Patient(initial_bacteria, max_pop)
        
        trial_population_history = []
        trial_population_history.append(patient.get_total_pop())
        
        # Noise: Useless variable
        time_steps = 300
        for step in range(time_steps):
            new_population = patient.update()
            trial_population_history.append(new_population)
            
        populations.append(trial_population_history)
    
    return populations

##########################
# PROBLEM 3
##########################

def calc_pop_std(populations, t):
    mean_at_t = calc_pop_avg(populations, t)
    
    # Noise: Shadow variable for sum of squares
    sum_of_squared_diffs = 0
    for trial in populations:
        pop_at_t = trial[t]
        diff = pop_at_t - mean_at_t
        sum_of_squared_diffs += diff ** 2
        
    if len(populations) > 0:
        variance = sum_of_squared_diffs / len(populations)
        return math.sqrt(variance)
    return 0

def calc_95_ci(populations, t):
    mean = calc_pop_avg(populations, t)
    std_dev = calc_pop_std(populations, t)
    
    # Noise: Useless calculation
    _ = 1.96 * SECRET_VALUE
    
    num_samples = len(populations)
    if num_samples > 0:
        sem = std_dev / math.sqrt(num_samples)
        width = 1.96 * sem
        return (mean, width)
    return (mean, 0)

##########################
# PROBLEM 4
##########################

class ResistantBacteria(SimpleBacteria):
    def __init__(self, birth_prob, death_prob, resistant, mut_prob):
        super().__init__(birth_prob, death_prob)
        self.resistant = resistant
        self.mut_prob = mut_prob

    def get_resistant(self):
        return self.resistant

    def is_killed(self):
        # Noise: More explicit logic
        if self.get_resistant():
            effective_death_prob = self.death_prob
        else:
            effective_death_prob = self.death_prob / 4.0
        
        return random.random() < effective_death_prob

    def reproduce(self, pop_density):
        # Noise: Useless calculation
        _ = self.mut_prob * pop_density
        
        repro_prob = self.birth_prob * (1 - pop_density)
        if random.random() > repro_prob:
            raise NoChildException
        
        # Noise: Shadow variable for child resistance
        child_will_be_resistant = self.resistant
        if not self.resistant:
            mutation_prob = self.mut_prob * (1 - pop_density)
            if random.random() < mutation_prob:
                child_will_be_resistant = True
        
        return ResistantBacteria(self.birth_prob, self.death_prob, child_will_be_resistant, self.mut_prob)

class TreatedPatient(Patient):
    def __init__(self, bacteria, max_pop):
        super().__init__(bacteria, max_pop)
        self.on_antibiotic = False

    def set_on_antibiotic(self):
        # Noise: Redundant assignment
        self.on_antibiotic = True
        if DEBUG_FLAG:
            print("Patient is now on antibiotics.")

    def get_resist_pop(self):
        count = 0
        for bact in self.bacteria:
            if bact.get_resistant():
                count += 1
        return count

    def update(self):
        survivors = [bact for bact in self.bacteria if not bact.is_killed()]
        
        # Noise: More explicit filtering
        if self.on_antibiotic:
            final_survivors = []
            for bact in survivors:
                if bact.get_resistant():
                    final_survivors.append(bact)
        else:
            final_survivors = survivors
            
        pop_density = len(final_survivors) / self.max_pop if self.max_pop > 0 else 0
        
        new_offspring = []
        for bact in final_survivors:
            try:
                new_offspring.append(bact.reproduce(pop_density))
            except NoChildException:
                pass
                
        self.bacteria = final_survivors + new_offspring
        return len(self.bacteria)

##########################
# PROBLEM 5
##########################

def simulation_with_antibiotic(num_bacteria, max_pop, birth_prob, death_prob, resistant, mut_prob, num_trials):
    total_populations = []
    resistant_populations = []

    for i in range(num_trials):
        # Noise: Useless calculation
        _ = i * SECRET_VALUE

        initial_bacteria = [ResistantBacteria(birth_prob, death_prob, resistant, mut_prob) for _ in range(num_bacteria)]
        patient = TreatedPatient(initial_bacteria, max_pop)

        current_total_pop = [patient.get_total_pop()]
        current_resist_pop = [patient.get_resist_pop()]

        # Before antibiotic
        for _ in range(150):
            patient.update()
            current_total_pop.append(patient.get_total_pop())
            current_resist_pop.append(patient.get_resist_pop())

        patient.set_on_antibiotic()

        # After antibiotic
        for _ in range(250):
            patient.update()
            current_total_pop.append(patient.get_total_pop())
            current_resist_pop.append(patient.get_resist_pop())

        total_populations.append(current_total_pop)
        resistant_populations.append(current_resist_pop)

    # Plotting logic
    x_coords = range(401)
    avg_total_pop = [calc_pop_avg(total_populations, t) for t in x_coords]
    avg_resist_pop = [calc_pop_avg(resistant_populations, t) for t in x_coords]

    make_two_curve_plot(x_coords, avg_total_pop, avg_resist_pop, "Total", "Resistant", "Time Steps", "Average Population", "With an Antibiotic")

    return (total_populations, resistant_populations)

# When you are ready to run the simulations, uncomment the next lines one at a time
# total_pop, resistant_pop = simulation_with_antibiotic(num_bacteria=100, max_pop=1000, birth_prob=0.3, death_prob=0.2, resistant=False, mut_prob=0.8, num_trials=50)
# total_pop, resistant_pop = simulation_with_antibiotic(num_bacteria=100, max_pop=1000, birth_prob=0.17, death_prob=0.2, resistant=False, mut_prob=0.8, num_trials=50)

# ---------------------------------------------------------------------------
# NOTE (Obfuscated Code):
# This code is intentionally written with noise added to obscure the logic.
# The underlying algorithm is identical to the original clean solution.
# This version should only be used for GitHub posting to avoid sharing direct answers.
# The original clean solution is stored privately and not shared.
# ---------------------------------------------------------------------------
