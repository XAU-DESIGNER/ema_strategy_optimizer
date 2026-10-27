import csv
from models import Strategy


class DataLoader:
    @staticmethod
    def load_data(directory: str) -> list[Strategy]:
        strategies = []

        with open(f"{directory}/small.csv", encoding="utf-8") as f:
            reader = csv.DictReader(f)

            for row in reader:
                strategy = Strategy(
                    fast_ema=int(row["fast_ema"]),
                    slow_ema=int(row["slow_ema"]),
                    losing_streak=int(row["losing_streak"]),
                    drawdown=float(row["drawdown"]),
                    pnl=float(row["PnL"]),
                    total_commission=float(row["Commission"]),
                    average_spread=float(row["avg_spread"])
                )

                strategies.append(strategy)

        return strategies


class Optimizer:

    @staticmethod
    def calculate_score(strategy: Strategy) -> float:
        return strategy.pnl - strategy.drawdown * 5

    @staticmethod
    def find_strategy(
        fast_ema: int,
        slow_ema: int,
        strategies: list[Strategy]
    ) -> Strategy | None:

        for strategy in strategies:
            if (
                strategy.fast_ema == fast_ema
                and strategy.slow_ema == slow_ema
            ):
                return strategy

        return None

    @staticmethod
    def get_neighbors(
        strategy: Strategy,
        strategies: list[Strategy]
    ) -> list[Strategy]:

        candidates = [
            (strategy.fast_ema - 1, strategy.slow_ema),
            (strategy.fast_ema + 1, strategy.slow_ema),
            (strategy.fast_ema, strategy.slow_ema - 1),
            (strategy.fast_ema, strategy.slow_ema + 1),
        ]

        neighbors = []

        for fast_ema, slow_ema in candidates:
            if fast_ema >= slow_ema:
                continue

            neighbor = Optimizer.find_strategy(
                fast_ema,
                slow_ema,
                strategies
            )

            if neighbor is not None:
                neighbors.append(neighbor)

        return neighbors

    @staticmethod
    def local_search(strategies: list[Strategy]) -> Strategy:
        current = strategies[0]

        while True:
            neighbors = Optimizer.get_neighbors(current, strategies)

            best_neighbor = current
            current_score = Optimizer.calculate_score(current)

            for neighbor in neighbors:
                neighbor_score = Optimizer.calculate_score(neighbor)

                if neighbor_score > current_score:
                    best_neighbor = neighbor
                    current_score = neighbor_score

            if best_neighbor == current:
                return current

            current = best_neighbor