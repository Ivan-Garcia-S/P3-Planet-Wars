import sys, logging
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
        return issue_order(state, strongest_planet.ID, weakest_planet.ID, strongest_planet.num_ships / 2)

def takedown_largest(state): 
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

    # Strongest planet not owned by player
    other_strongest = other_planets[0]
    
    # If strongest already getting attacked abort plan
    for fleet in state.my_fleets():
        if fleet.destination_planet == other_strongest.ID:
            return False
    
    # Find my largest planet
    my_planets = sorted(state.my_planets(), key=lambda p: p.num_ships)
    
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

    # Send enough ships to take over largest planet
    return issue_order(state, my_strongest.ID, other_strongest.ID, needed_ships)

# Returns number of ships needed to capture planet
def required_to_capture(state, my_planet, capture_planet):
    if capture_planet in state.neutral_planets():
        return capture_planet.num_ships + 1
    else:
        return capture_planet.num_ships + \
               state.distance(my_planet.ID, capture_planet.ID) * capture_planet.growth_rate + 1


def move_fleet(state):
    pass