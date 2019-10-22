from .utils import test_data, cli
from .ga import ga

def main():
    config = cli.init()

    tests = test_data.read(config['TEST_DATA_PATH'])
    algorithm_to_run = config['ALGORITHM']

    if algorithm_to_run == 'ga':
        ga.start(tests, config['GA_SETTINGS'])
        exit(0)
    elif algorithm_to_run == 'hill_climber':
        print('Hill climber run')
        exit(0)
    else:
        print('Unrecognized ALGORITHM type, check your config.json!')
        exit(1)
        
if __name__ == '__main__':
    main()
