from dataclasses import dataclass

@dataclass
class Strategy:
    fast_ema: int
    slow_ema: int
    losing_streak: int
    drawdown: float
    pnl: float
    total_commission: float
    average_spread: float