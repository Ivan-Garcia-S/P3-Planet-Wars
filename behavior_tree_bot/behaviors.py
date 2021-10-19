import logging
import sys
from math import ceil, sqrt

sys.path.insert(0, '../')
from planet_wars import issue_order


def attack_weakest_enemy_planet(state):
    # (1) If we currently have a fleet in flight, abort plan.
    if len(state.my_fleets()) >= 1:
        return False

    # (2) Find my strongest planet.
    strongest_planet = max(state.my_planets(), key=lambda t: t.num_ships, default=None)

    # (3) Find the weakest enemy planet.
    weakest_planet = min(state.enemy_planets(), key=lambda t: t.num_ships, default=None)

    if not strongest_planet or not weakest_planet:
        # No legal source or destination
        return False
    else:
        # (4) Send half the ships from my strongest planet to the weakest enemy planet.
        return issue_order(state, strongest_planet.ID, weakest_planet.ID, strongest_planet.num_ships / 2)


def spread_to_weakest_neutral_planet(state):
    # (1) If we currently have a fleet in flight, just do nothing.
    if len(state.my_fleets()) >= 1:
        return False

    # (2) Find my strongest planet.
    strongest_planet = max(state.my_planets(), key=lambda p: p.num_ships, default=None)

    # (3) Find the weakest neutral planet.
    weakest_planet = min(state.neutral_planets(), key=lambda p: p.num_ships, default=None)

    if not strongest_planet or not weakest_planet:
        # No legal source or destination
        return False
    else:
        # (4) Send half the ships from my strongest planet to the weakest enemy planet.
        distance = state.distance(weakest_planet.ID, strongest_planet.ID)
        if distance < 15:
            return issue_order(state, strongest_planet.ID, weakest_planet.ID,weakest_planet.num_ships+10)
        else:
            return False


def takedown_largest(state):
    logging.info("Inside takedown largest")
    # Return failure if no planets owned
    if not state.my_planets():
        return False

    # Gathers list of all planets not owned by player
    other_planets = [planet for planet in state.enemy_planets()
                     if not any(fleet.destination_planet == planet.ID for fleet in state.my_fleets())]
    for planet in state.neutral_planets():
        other_planets.append(planet)

    if not other_planets:
        return False

    # Sorts other planets by strongest first
    other_planets.sort(key=lambda p: p.num_ships)
    other_planets.reverse()
    logging.info(other_planets[0].num_ships)

    # Strongest planet not owned by player
    other_strongest = other_planets[0]

    # If strongest already getting attacked abort plan
    for fleet in state.my_fleets():
        if fleet.destination_planet == other_strongest.ID:
            return False

    # Find my largest planet
    my_planets = sorted(state.my_planets(), key=lambda p: p.num_ships)
    my_planets.reverse()

    my_strongest = my_planets[0]

    needed_ships = required_to_capture(state, my_strongest, other_strongest)

    """
    if other_strongest in state.neutral_planets():
        needed_ships = other_strongest.num_ships + 1
    else:
        needed_ships = other_strongest.num_ships + \
               state.distance(my_strongest.ID, other_strongest.ID) * other_strongest.growth_rate + 1
    """
    # If not enough ships had
    if my_strongest.num_ships < needed_ships:
        return False

    logging.info("Taking down largest")
    # Send enough ships to take over largest planet
    return issue_order(state, my_strongest.ID, other_strongest.ID, needed_ships)


# doesn't work, kept crashing so not running it
def takedown_top3(state):
    logging.info("Inside takedown largest")
    # Return failure if no planets owned
    if not state.my_planets():
        return False

    # Gathers list of all planets not owned by player
    other_planets = [planet for planet in state.enemy_planets()
                     if not any(fleet.destination_planet == planet.ID for fleet in state.my_fleets())]
    for planet in state.neutral_planets():
        other_planets.append(planet)

    if not other_planets:
        return False

    # Sorts other planets by strongest first
    other_planets.sort(key=lambda p: p.num_ships)
    other_planets.reverse()
    logging.info(other_planets[0].num_ships)

    # Strongest planet not owned by player
    other_strongest = other_planets[0]
    if other_planets[1]:
        other_strongest_2 = other_planets[1]
    if other_planets[2]:
        other_strongest_3 = other_planets[2]

    # If strongest already getting attacked abort plan
    for fleet in state.my_fleets():
        if fleet.destination_planet == other_strongest.ID:
            return False
        if other_strongest_2:
            if fleet.destination_planet == other_strongest_2.ID:
                return False
        if other_strongest_3:
            if fleet.destination_planet == other_strongest_3.ID:
                return False

    # Find my largest planet
    my_planets = sorted(state.my_planets(), key=lambda p: p.num_ships)
    my_planets.reverse()

    my_strongest = my_planets[0]

    needed_ships = required_to_capture(state, my_strongest, other_strongest)
    if other_strongest_2:
        needed_ships_2 = required_to_capture(state, my_strongest, other_strongest_2)
    if other_strongest_3:
        needed_ships_3 = required_to_capture(state, my_strongest, other_strongest_3)

    """
    if other_strongest in state.neutral_planets():
        needed_ships = other_strongest.num_ships + 1
    else:
        needed_ships = other_strongest.num_ships + \
               state.distance(my_strongest.ID, other_strongest.ID) * other_strongest.growth_rate + 1
    """
    # If not enough ships had
    if my_strongest.num_ships >= needed_ships:
        return issue_order(state, my_strongest.ID, other_strongest.ID, needed_ships)

    if other_strongest_3:
        if my_strongest.num_ships >= needed_ships_2:
            return issue_order(state, my_strongest.ID, other_strongest_2.ID, needed_ships)

    if other_strongest_3:
        if my_strongest.num_ships < needed_ships_3:
            return issue_order(state, my_strongest.ID, other_strongest_3.ID, needed_ships)

    return False


# Returns number of ships needed to capture planet
def required_to_capture(state, my_planet, capture_planet):
    if capture_planet in state.neutral_planets():
        return capture_planet.num_ships + 1
    else:
        return capture_planet.num_ships + \
               state.distance(my_planet.ID, capture_planet.ID) * capture_planet.growth_rate + 1


def move_fleet(state):
    most_ships = 0
    in_danger_planet = None

    # Finds the strongest planet you own in danger
    for fleet in state.enemy_fleets():
        if fleet.destination_planet in state.my_planets() and fleet.destination_planet.num_ships > most_ships:
            in_danger_planet = fleet.destination_planet
            most_ships = in_danger_planet.num_ships

    # If no planets to flee to
    if not state.not_my_planets():
        return False

    my_planets = sorted(state.my_planets(), key=lambda p: p.num_ships)
    my_planets.reverse()
    my_strongest = my_planets[0]

    if my_strongest == in_danger_planet:
        if my_planets[1]:
            return issue_order(state, in_danger_planet.ID, my_planets[1].ID, in_danger_planet.num_ships)
        else:
            return False

    """
    shortest_distance = -1
    flee_to = None
    for planet in state.not_my_planets():
        if planet in state.neutral_planets():
            if in_danger_planet.num_ships > planet.num_ships and \
                  (shortest_distance == -1 or state.distance(in_danger_planet.ID, planet.ID) < shortest_distance):
                flee_to = planet
                shortest_distance = state.distance(in_danger_planet, planet)
        else:
            if in_danger_planet.num_ships > planet.num_ships + state.distance(in_danger_planet.ID, planet.ID) * \
                  planet.growth_rate and (shortest_distance == -1 or state.distance(in_danger_planet.ID, \
                  planet.ID) < shortest_distance):
                flee_to = planet
                shortest_distance = state.distance(in_danger_planet, planet)
    """

    # return issue_order(state, in_danger_planet.ID, my_strongest.ID, in_danger_planet.num_ships)


def capture_closest_weakest_planet(state):
    if len(state.my_planets()) >= 1:
        strongest_planet = max(state.my_planets(), key=lambda p: p.num_ships, default=None)
    else:
        return False

    closest_weakest_planet = None
    closest_weakest_planet_distance = 999999

    for planet in state.not_my_planets():
        distance_X = strongest_planet.x - planet.x
        distance_Y = strongest_planet.y - planet.y
        # sqrt(x2-x1)^2 + (y2-y1)^2
        distance_total = int(ceil(sqrt((distance_X ** 2) + (distance_Y ** 2))))
        distance_total = distance_total + planet.num_ships

        if distance_total < closest_weakest_planet_distance:
            closest_weakest_planet_distance = distance_total
            closest_weakest_planet = planet

    if closest_weakest_planet is None:
        return False

    # # If already getting attacked abort plan
    # for fleet in state.my_fleets():
    #     if fleet.destination_planet == closest_weakest_planet.ID:
    #         return False

    if strongest_planet.num_ships > closest_weakest_planet.num_ships + 20:
        issue_order(state, strongest_planet.ID, closest_weakest_planet.ID, closest_weakest_planet.num_ships + 20)
    return False
