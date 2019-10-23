from .utils import test_data, cli
from .ga import ga
from .hill_climber import hill_climber
from .random import random

def main():
    config = cli.init()

    algorithm_to_run = config['ALGORITHM']
    tests = test_data.read(config['TEST_DATA_PATH'])
    settings = config['SETTINGS']

    if algorithm_to_run == 'ga':
        ga.start(tests, settings)
        exit(0)
    elif algorithm_to_run == 'hill_climber':
        hill_climber.start(tests, settings)
        exit(0)
    elif algorithm_to_run == 'random':
        random.start(tests, settings)
        exit(0)
    else:
        print('Unrecognized ALGORITHM type, check your config.json!')
        exit(1)

if __name__ == '__main__':
    main()
