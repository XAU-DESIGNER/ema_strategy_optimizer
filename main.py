import sys

from DataLoader import DataLoader
from Optimizer import Optimizer

def main():
    if len(sys.argv) > 2:
        sys.exit("Usage: python main.py [directory]")

    directory = sys.argv[1] if len(sys.argv) == 2 else "large"
    print("Loading data...")
    strategies = DataLoader.load_data(directory= directory)
    print("Data Loaded.")
    print("searching for best strategy...")

    best = Optimizer.local_search(strategies= strategies)
    print("best strategy flound:")
    print(best)
    print("Score: ", Optimizer.calculate_score(best))
main()