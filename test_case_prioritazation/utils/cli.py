import json
import argparse

def getJSON(file):
    return json.load(file)

def init():
    parser = argparse.ArgumentParser(
        description='Executes Test Case Prioritization algorithms based on config file'
        )
    parser.add_argument(
        '-c', '--config',
        help='Location of the JSON configuration file, if not specified config.json will be used.',
        metavar='A',
        type=argparse.FileType('r'),
        default='config.json'
        )

    args = parser.parse_args()
    return getJSON(args.config)
