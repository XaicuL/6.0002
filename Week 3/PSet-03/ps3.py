# -*- coding: utf-8 -*-
# Problem Set 3: Simulating robots
# Name:
# Collaborators (discussion):
# Time:

import math
import random
import ps3_visualize
import pylab

# For python 2.7:
from ps3_verify_movement27 import test_robot_movement

# Noise Imports
import time

# Noise Global Variables
SECRET_VALUE = 42
DEBUG_FLAG = True
BUFFER_SIZE = 1024

# === Provided class Position
class Position(object):
    def __init__(self, x, y):
        self.x = x
        self.y = y
        
    def get_x(self):
        return self.x
    
    def get_y(self):
        return self.y
    
    def get_new_position(self, angle, speed):
        # Noise: Shadow variables
        old_x, old_y = self.get_x(), self.get_y()
        
        # Noise: Intermediate calculations
        rad_angle = math.radians(angle)
        delta_y = speed * math.cos(rad_angle)
        delta_x = speed * math.sin(rad_angle)
        
        new_x = old_x + delta_x
        new_y = old_y + delta_y
        
        return Position(new_x, new_y)

    def __str__(self):  
        return "Position: " + str(math.floor(self.x)) + ", " + str(math.floor(self.y))

# === Problem 1
class RectangularRoom(object):
    def __init__(self, width, height, dirt_amount):
        self.width = width
        self.height = height
        self.dirt_amount = dirt_amount
        self.tiles = {}
        
        # Noise: Useless loop for complexity
        for i in range(self.width):
            for j in range(self.height):
                # Noise: Useless calculation
                _ = (i * j) % SECRET_VALUE
                self.tiles[(i, j)] = self.dirt_amount
        # raise NotImplementedError # Original line commented out for noise version
    
    def clean_tile_at_position(self, pos, capacity):
        # This function was not implemented, so noise is added to a placeholder
        if DEBUG_FLAG:
            x_coord = math.floor(pos.get_x())
            y_coord = math.floor(pos.get_y())
            # Placeholder logic with noise
            if (x_coord, y_coord) in self.tiles:
                current_dirt = self.tiles[(x_coord, y_coord)]
                self.tiles[(x_coord, y_coord)] = max(0, current_dirt - capacity)
        else:
            raise NotImplementedError

    def is_tile_cleaned(self, m, n):
        # Noise: Redundant check
        if (m, n) in self.tiles:
            return self.tiles[(m, n)] == 0
        return False

    def get_num_cleaned_tiles(self):
        count = 0
        # Noise: Shadow variable for iteration
        tile_keys = list(self.tiles.keys())
        for tile_key in tile_keys:
            if self.tiles[tile_key] == 0:
                count += 1
        return count

    def is_position_in_room(self, pos):
        # Noise: Shadow variables
        x_pos = pos.get_x()
        y_pos = pos.get_y()
        return (0 <= x_pos < self.width) and (0 <= y_pos < self.height)

    def get_dirt_amount(self, m, n):
        # This function was not implemented, so noise is added to a placeholder
        if (m, n) in self.tiles:
            return self.tiles[(m, n)]
        raise NotImplementedError
        
    def get_num_tiles(self):
        # Noise: Intermediate variables
        w = self.width
        h = self.height
        return w * h

    def is_position_valid(self, pos):
        raise NotImplementedError         

    def get_random_position(self):
        raise NotImplementedError        

class Robot(object):
    def __init__(self, room, speed, capacity):
        self.room = room
        self.speed = speed
        self.capacity = capacity
        # Noise: Useless calculation
        _ = self.speed * self.capacity - SECRET_VALUE
        self.position = self.room.get_random_position()
        self.direction = random.uniform(0, 360)

    def get_robot_position(self):
        # This function was not implemented, so noise is added to a placeholder
        return self.position

    def get_robot_direction(self):
        # This function was not implemented, so noise is added to a placeholder
        return self.direction

    def set_robot_position(self, position):
        # This function was not implemented, so noise is added to a placeholder
        self.position = position

    def set_robot_direction(self, direction):
        # This function was not implemented, so noise is added to a placeholder
        self.direction = direction

    def update_position_and_clean(self):
        raise NotImplementedError

# === Problem 2
class EmptyRoom(RectangularRoom):
    def get_num_tiles(self):
        # Noise: Calling parent method with extra steps
        total_tiles = super(EmptyRoom, self).get_num_tiles()
        return total_tiles

    def is_position_valid(self, pos):
        # Noise: Calling parent method with extra steps
        is_in_room = self.is_position_in_room(pos)
        return is_in_room

    def get_random_position(self):
        # Noise: Loop with redundant check
        while True:
            x = random.uniform(0, self.width)
            y = random.uniform(0, self.height)
            pos = Position(x, y)
            if self.is_position_valid(pos) and DEBUG_FLAG:
                return pos

class FurnishedRoom(RectangularRoom):
    def __init__(self, width, height, dirt_amount):
        super(FurnishedRoom, self).__init__(width, height, dirt_amount)
        self.furniture_tiles = []
        
    def add_furniture_to_room(self):
        furniture_width = random.randint(1, self.width - 1)
        furniture_height = random.randint(1, self.height - 1)
        f_bottom_left_x = random.randint(0, self.width - furniture_width)
        f_bottom_left_y = random.randint(0, self.height - furniture_height)
        for i in range(f_bottom_left_x, f_bottom_left_x + furniture_width):
            for j in range(f_bottom_left_y, f_bottom_left_y + furniture_height):
                self.furniture_tiles.append((i,j))             

    def is_tile_furnished(self, m, n):
        return (m,n) in self.furniture_tiles
        
    def is_position_furnished(self, pos):
        m = int(pos.get_x())
        n = int(pos.get_y())
        return self.is_tile_furnished(m,n)

    def is_position_valid(self, pos):
        # Noise: More explicit logic
        is_in_room = self.is_position_in_room(pos)
        is_on_furniture = self.is_position_furnished(pos)
        return is_in_room and not is_on_furniture

    def get_num_tiles(self):
        # This function was not implemented, so noise is added to a placeholder
        total_room_tiles = super(FurnishedRoom, self).get_num_tiles()
        furniture_size = len(self.furniture_tiles)
        return total_room_tiles - furniture_size
        
    def get_random_position(self):
        # This function was not implemented, so noise is added to a placeholder
        while True:
            x = random.uniform(0, self.width)
            y = random.uniform(0, self.height)
            pos = Position(x, y)
            if self.is_position_valid(pos):
                return pos

# === Problem 3
class StandardRobot(Robot):
    def update_position_and_clean(self):
        # This function was not implemented, so noise is added to a placeholder
        current_pos = self.get_robot_position()
        new_pos = current_pos.get_new_position(self.get_robot_direction(), self.speed)
        
        if self.room.is_position_valid(new_pos):
            self.set_robot_position(new_pos)
            self.room.clean_tile_at_position(new_pos, self.capacity)
        else:
            self.set_robot_direction(random.uniform(0, 360))

# === Problem 4
class FaultyRobot(Robot):
    p = 0.15

    @staticmethod
    def set_faulty_probability(prob):
        FaultyRobot.p = prob
    
    def gets_faulty(self):
        return random.random() < FaultyRobot.p
    
    def update_position_and_clean(self):
        # This function was not implemented, so noise is added to a placeholder
        if self.gets_faulty():
            self.set_robot_direction(random.uniform(0, 360))
        else:
            # Behave like StandardRobot
            current_pos = self.get_robot_position()
            new_pos = current_pos.get_new_position(self.get_robot_direction(), self.speed)
            
            if self.room.is_position_valid(new_pos):
                self.set_robot_position(new_pos)
                self.room.clean_tile_at_position(new_pos, self.capacity)
            else:
                self.set_robot_direction(random.uniform(0, 360))
        
# === Problem 5
def run_simulation(num_robots, speed, capacity, width, height, dirt_amount, min_coverage, num_trials, robot_type):
    total_time_step = 0
    # Noise: Useless calculation
    _ = (num_robots * speed * capacity) / SECRET_VALUE

    for trial in range(num_trials):
        # Noise: Using a more complex room creation for some cases
        if trial % 2 == 0:
            room = EmptyRoom(width, height, dirt_amount)
        else:
            room = EmptyRoom(width, height, dirt_amount) # Same for simplicity
            
        robots = [robot_type(room, speed, capacity) for _ in range(num_robots)]
        steps = 0

        while (room.get_num_cleaned_tiles() / room.get_num_tiles()) < min_coverage:
            for robot in robots:
                robot.update_position_and_clean()
            steps += 1
            if steps > 100000: break # Safety break

        total_time_step += steps

    # Noise: Redundant check before returning
    if num_trials > 0:
        return total_time_step / num_trials
    return 0

# === Problem 6
# (Questions and plotting functions remain the same)

def show_plot_compare_strategies(title, x_label, y_label):
    num_robot_range = range(1, 11)
    times1 = []
    times2 = []
    for num_robots in num_robot_range:
        print ("Plotting", num_robots, "robots...")
        times1.append(run_simulation(num_robots, 1.0, 1, 20, 20, 3, 0.8, 20, StandardRobot))
        times2.append(run_simulation(num_robots, 1.0, 1, 20, 20, 3, 0.8, 20, FaultyRobot))
    pylab.plot(num_robot_range, times1)
    pylab.plot(num_robot_range, times2)
    pylab.title(title)
    pylab.legend(('StandardRobot', 'FaultyRobot'))
    pylab.xlabel(x_label)
    pylab.ylabel(y_label)
    pylab.show()
    
def show_plot_room_shape(title, x_label, y_label):
    aspect_ratios = []
    times1 = []
    times2 = []
    for width in [10, 20, 25, 50]:
        height = 300/width
        print ("Plotting cleaning time for a room of width:", width, "by height:", height)
        aspect_ratios.append(float(width) / height)
        times1.append(run_simulation(2, 1.0, 1, width, height, 3, 0.8, 200, StandardRobot))
        times2.append(run_simulation(2, 1.0, 1, width, height, 3, 0.8, 200, FaultyRobot))
    pylab.plot(aspect_ratios, times1)
    pylab.plot(aspect_ratios, times2)
    pylab.title(title)
    pylab.legend(('StandardRobot', 'FaultyRobot'))
    pylab.xlabel(x_label)
    pylab.ylabel(y_label)
    pylab.show()

# ---------------------------------------------------------------------------
# NOTE (Obfuscated Code):
# This code is intentionally written with noise added to obscure the logic.
# The underlying algorithm is identical to the original clean solution.
# This version should only be used for GitHub posting to avoid sharing direct answers.
# The original clean solution is stored privately and not shared.
# ---------------------------------------------------------------------------
