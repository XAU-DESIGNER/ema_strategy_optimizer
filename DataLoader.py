import csv

from models import Strategy

class DataLoader:
    @staticmethod
    def load_data(directory: str) -> list[Strategy]:
        strategies = []

        with open(f"{directory}/large.csv", encoding="utf-8") as f:
            reader = csv.DictReader(f)

            for row in reader:
                strategy = Strategy(
                    fast_ema=int(row["fast_ema"]),
                    slow_ema=int(row["slow_ema"]),
                    losing_streak=int(row["losing_streak"]),
                    drawdown=float(row["drawdown"]),
                    pnl=float(row["PnL"]),
                    total_commission=float(row["Commission"]),
                    average_spread=float(row["avg_spread"]),
                    initial_balance=float(row["initial_balance"])
                )

                strategies.append(strategy)

        return strategies

