import os
import subprocess
import sys


def show_match(bot, opponent_bot, map_num):
    """
        Runs an instance of Planet Wars between the two given bots on the specified map. After completion, the
        game is replayed via a visual interface.
    """
    command = 'java -jar tools/PlayGame.jar maps/map' + str(map_num) + '.txt 1000 1000 log.txt ' + \
              '"python ' + bot + '" ' + \
              '"python ' + opponent_bot + '" ' + \
              '| java -jar tools/ShowGame.jar'
    print(command)
    os.system(command)


def test(bot, opponent_bot, map_num):
    """ Runs an instance of Planet Wars between the two given bots on the specified map. """
    bot_name, opponent_name = bot.split('/')[1].split('.')[0], opponent_bot.split('/')[1].split('.')[0]
    print('Running test:', bot_name, 'vs', opponent_name)
    command = 'java -jar tools/PlayGame.jar maps/map' + str(map_num) + '.txt 1000 1000 log.txt ' + \
              '"python ' + bot + '" ' + \
              '"python ' + opponent_bot + '" '

    print(command)
    p = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True)

    while True:
        return_code = p.poll()  # returns None while subprocess is running
        line = p.stdout.readline().decode('utf-8')
        if '1 timed out' in line:
            print(bot_name, 'timed out.')
            break
        elif '2 timed out' in line:
            print(opponent_name, 'timed out.')
            break
        elif '1 crashed' in line:
            print(bot_name, 'crashed.')
            break
        elif '2 crashed' in line:
            print(opponent_name, 'crashed')
            break
        elif 'Player 1 Wins!' in line:
            print(bot_name, 'wins!\n')
            winner = 'player 1'
            score[winner] = score.get(winner, 0) + 1
            break
        elif 'Player 2 Wins!' in line:
            print(opponent_name, 'wins!\n')
            winner = 'player 2'
            score[winner] = score.get(winner, 0) + 1
            break

        if return_code is not None:
            break


if __name__ == '__main__':
    path = os.getcwd()
    opponents = ['opponent_bots/easy_bot.py',
                 'opponent_bots/spread_bot.py',
                 'opponent_bots/aggressive_bot.py',
                 'opponent_bots/defensive_bot.py',
                 'opponent_bots/production_bot.py']

    my_bot = 'behavior_tree_bot/bt_bot.py'
    score = {'player 1': 0, 'player 2': 0}
    maps = []
    for i in range(1, 101):
        maps.append(i)

    for x in range(0,5):
        for n in range(len(maps)):
            test(my_bot, opponents[x], maps[n])
        print(opponents[x] + "Final scores =", dict(score))
