import argparse
import os
import sys

from .experiment import Experiment


def main():
    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('-y', '--yaml', type=str, required=True, help='yaml configuration file path')

    args = parser.parse_args()

    # check file exists
    if not os.path.exists(args.yaml):
        print(f"File not found: {args.yaml}")
        sys.exit(1)

    print(f"Running experiment with {args.yaml}")
    experiment = Experiment(args.yaml)
    experiment.run()


if __name__ == "__main__":
    main()
