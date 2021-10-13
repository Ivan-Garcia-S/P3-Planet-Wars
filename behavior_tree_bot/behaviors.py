import sys
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
    enemy_planets = [planet for planet in state.enemy_planets()
                      if not any(fleet.destination_planet == planet.ID for fleet in state.my_fleets())]
    enemy_planets.sort(key=lambda p: p.num_ships)

    # Enemy's largest planet
    target_largest = enemy_planets[0]

    neutral_planets = [planet for planet in state.neutral_planets()
                      if not any(fleet.destination_planet == planet.ID for fleet in state.my_fleets())]
    neutral_planets.sort(key=lambda p: p.num_ships)
    
    # Change target planet to neutral one if stronger than enemy's largest
    if neutral_planets[0].num_ships > target_largest.num_ships:
      target_largest = neutral_planets[0]
    
    # Find my largest planet
    my_planets = sorted(state.my_planets(), key=lambda p: p.num_ships)
    my_largest = my_planets[0]

    # Send enough ships to take over largest planet
    return issue_order(state, my_largest.ID, target_largest.ID, required_to_capture(state, my_largest, target_largest))

# Returns number of ships needed to capture planet
def required_to_capture(state, my_planet, capture_planet):
    if capture_planet in state.neutral_planets():
        return capture_planet.num_ships + 1
    else:
        return capture_planet.num_ships + \
               state.distance(my_planet.ID, capture_planet.ID) * capture_planet.growth_rate + 1

    