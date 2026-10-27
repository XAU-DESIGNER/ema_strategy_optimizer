import csv
from models import Strategy

class Optimizer:
    @staticmethod
    def calculate_score(strategy: Strategy) -> float:
        if strategy.initial_balance <= 0:
            return float("-inf")

        if strategy.drawdown < 0:
            return float("-inf")

        net_pnl = strategy.pnl - strategy.total_commission
        roi = net_pnl / strategy.initial_balance * 100

        if strategy.drawdown == 0:
            return float("inf") if roi > 0 else float("-inf")

        return roi / strategy.drawdown

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