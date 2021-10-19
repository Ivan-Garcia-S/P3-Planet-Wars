def if_neutral_planet_available(state):
    return any(state.neutral_planets())


def have_largest_fleet(state):
    return sum(planet.num_ships for planet in state.my_planets()) \
           + sum(fleet.num_ships for fleet in state.my_fleets()) \
           > sum(planet.num_ships for planet in state.enemy_planets()) \
           + sum(fleet.num_ships for fleet in state.enemy_fleets()) \
           and len(state.my_planets()) > len(state.enemy_planets())     # just and extra check for largest fleet
                                                                        # so we only attack offensively with more
                                                                        # planets.

# Bugged, doesn't work
# def can_takedown_largest(state):
#     enemy_planets = [planet for planet in state.enemy_planets()
#                      if not any(fleet.destination_planet == planet.ID for fleet in state.my_fleets())]
#     enemy_planets.sort(key=lambda p: p.num_ships)
#
#     target_largest = enemy_planets[0]
#
#     neutral_planets = [planet for planet in state.neutral_planets()
#                        if not any(fleet.destination_planet == planet.ID for fleet in state.my_fleets())]
#     neutral_planets.sort(key=lambda p: p.num_ships)
#
#     if neutral_planets[0].num_ships > target_largest.num_ships:
#         target_largest = neutral_planets[0]
#
#     # Find my largest planet
#     my_planets = sorted(state.my_planets(), key=lambda p: p.num_ships)
#     my_largest = my_planets[0]
#
#     # Return able to take over largest if neutral planet
#     if target_largest is neutral_planets[0]:
#         return target_largest.num_ships + 1
#
#     # Returns able to take over largest if enemy planet
#     else:
#         return my_largest.num_ships > target_largest.num_ships + \
#                state.distance(my_largest.ID, target_largest.ID) * target_largest.growth_rate + 1


def have_strongest_planet(state):
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

    # Strongest planet not owned by player
    other_strongest = other_planets[0]

    # Sorts my planets by strongest first
    my_planets = sorted(state.my_planets(), key=lambda p: p.num_ships)
    my_planets.reverse()

    if not my_planets:
        return False

    # Strongest planet owned by player
    my_strongest = my_planets[0]

    # Return strongest by player stronger than unowned strongest
    return my_strongest.num_ships > other_strongest.num_ships


def wont_survive_attack(state):
    # If no enemy fleets, nothing under attack
    if not state.enemy_fleets():
        return False

    most_ships = 0
    attacking_fleet = None

    for fleet in state.enemy_fleets():
        if fleet.destination_planet in state.my_planets() and fleet.destination_planet.num_ships > most_ships:
            attacking_fleet = fleet
            most_ships = fleet.destination_planet.num_ships

    # No friendly planets in danger
    if attacking_fleet is None:
        return False

    # Doesn't account for friendly planet's growth rate
    return attacking_fleet.num_ships > attacking_fleet.destination_planet.num_ships

    # def join_other_my_planet(state):
