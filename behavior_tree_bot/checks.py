

def if_neutral_planet_available(state):
    return any(state.neutral_planets())


def have_largest_fleet(state):
    return sum(planet.num_ships for planet in state.my_planets()) \
             + sum(fleet.num_ships for fleet in state.my_fleets()) \
           > sum(planet.num_ships for planet in state.enemy_planets()) \
             + sum(fleet.num_ships for fleet in state.enemy_fleets())

def can_takedown_largest(state):
    enemy_planets = [planet for planet in state.enemy_planets()
                      if not any(fleet.destination_planet == planet.ID for fleet in state.my_fleets())]
    enemy_planets.sort(key=lambda p: p.num_ships)

    target_largest = enemy_planets[0]

    neutral_planets = [planet for planet in state.neutral_planets()
                      if not any(fleet.destination_planet == planet.ID for fleet in state.my_fleets())]
    neutral_planets.sort(key=lambda p: p.num_ships)
    
    if neutral_planets[0].num_ships > target_largest.num_ships:
      target_largest = neutral_planets[0]

    # Find my largest planet
    my_planets = sorted(state.my_planets(), key=lambda p: p.num_ships)
    my_largest = my_planets[0]
    
    # Return able to take over largest if neutral planet
    if target_largest is neutral_planets[0]:
      return target_largest.num_ships + 1
    
    # Returns able to take over largest if enemy planet
    else:
      return my_largest.num_ships > target_largest.num_ships + \
             state.distance(my_largest.ID, target_largest.ID) * target_largest.growth_rate + 1

     

