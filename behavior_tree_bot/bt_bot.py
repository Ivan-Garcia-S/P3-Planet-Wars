#!/usr/bin/env python
#

"""
// There is already a basic strategy in place here. You can use it as a
// starting point, or you can throw it out entirely and replace it with your
// own.
"""
import inspect
import logging
import os
import sys
import traceback

logging.basicConfig(filename=__file__[:-3] + '.log', filemode='w', level=logging.DEBUG)
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.append(parentdir)

from behavior_tree_bot.behaviors import *
from behavior_tree_bot.checks import *
from behavior_tree_bot.bt_nodes import Selector, Sequence, Action, Check

from planet_wars import PlanetWars, finish_turn


# You have to improve this tree or create an entire new one that is capable
# of winning against all the 5 opponent bots
def setup_behavior_tree():
    # Top-down construction of behavior tree
    root = Selector(name='High Level Ordering of Strategies')

    # """
    logging.info("Here")

    # Takedown the strongest enemy planet, else keep building and capturing closest_weakest
    takedown_plan = Sequence(name="Takedown Largest Planet")
    able_to_takedown = Check(have_strongest_planet)
    takedown = Action(takedown_largest)
    takedown_plan.child_nodes = [able_to_takedown, takedown]

    # if our planet is about to be overrun, deploy ships to our strongest planet to escape
    evade_plan = Sequence(name="Evade Enemy Attack")
    will_be_destroyed = Check(wont_survive_attack)
    evade_attack = Action(move_fleet)
    evade_plan.child_nodes = [will_be_destroyed, evade_attack]

    # sends ships from our strongest planet to capture the nearby weak planets
    capture_closest = Sequence(name='Capture Closest')
    capture_closest_action = Action(capture_closest_weakest_planet)
    capture_closest.child_nodes = [capture_closest_action]

    # Default offensive_plan - Didn't Use
    offensive_plan = Sequence(name='Offensive Strategy')
    largest_fleet_check = Check(have_largest_fleet)
    attack = Action(attack_weakest_enemy_planet)
    offensive_plan.child_nodes = [largest_fleet_check, attack]

    # Default spread_sequence - Didn't Use
    spread_sequence = Sequence(name='Spread Strategy')
    neutral_planet_check = Check(if_neutral_planet_available)
    spread_action = Action(spread_to_weakest_neutral_planet)
    spread_sequence.child_nodes = [neutral_planet_check, spread_action]

    root.child_nodes = [takedown_plan, capture_closest, evade_plan]  # 121 loses curr

    """
    takedown_plan = Sequence(name="Takedown Largest Planet")
    able_to_takedown = Check(can_takedown_largest)
    takedown = Action(takedown_largest)
    takedown_plan = [able_to_takedown, takedown]

    spread_sequence = Sequence(name='Spread Strategy')
    neutral_planet_check = Check(if_neutral_planet_available)
    spread_action = Action(spread_to_weakest_neutral_planet)
    spread_sequence.child_nodes = [neutral_planet_check, spread_action]

    attack = Action(attack_weakest_enemy_planet)
    root.child_nodes = [takedown_plan, spread_sequence, attack]
    """

    logging.info('\n' + root.tree_to_string())
    return root


# You don't need to change this function
def do_turn(state):
    behavior_tree.execute(planet_wars)


if __name__ == '__main__':
    logging.basicConfig(filename=__file__[:-3] + '.log', filemode='w', level=logging.DEBUG)

    behavior_tree = setup_behavior_tree()
    try:
        map_data = ''
        while True:
            current_line = input()
            if len(current_line) >= 2 and current_line.startswith("go"):
                planet_wars = PlanetWars(map_data)
                do_turn(planet_wars)
                finish_turn()
                map_data = ''
            else:
                map_data += current_line + '\n'

    except KeyboardInterrupt:
        print('ctrl-c, leaving ...')
    except Exception:
        traceback.print_exc(file=sys.stdout)
        logging.exception("Error in bot.")
