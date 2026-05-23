"""
Functional Programming Blueprint
Characteristics: Compile-time immutability, zero side-effects, declarative Map-Filter-Reduce pipeline.
"""
from typing import List, Tuple, Final
from dataclasses import dataclass
from functools import reduce


@dataclass(frozen=True)
class MarketTick:
    symbol: str
    tick_type: str  # 'TRADE', 'QUOTE', etc.
    price: float
    volume: int


@dataclass(frozen=True)
class ProcessedTradeMetrics:
    valid_trades: List[Tuple[str, float]]
    total_volume_processed: int


def is_valid_trade(tick: MarketTick) -> bool:
    """Pure Function: Determines if a tick is an actionable trade based strictly on its inputs."""
    return (
        bool(tick.symbol)
        and tick.price > 0.0
        and tick.volume > 0
        and tick.tick_type == "TRADE"
    )


def transform_to_trade_value(tick: MarketTick) -> Tuple[str, float]:
    """Pure Function: Maps an incoming immutable MarketTick to a processed trade value tuple."""
    return (tick.symbol, tick.price * tick.volume)


def accumulate_metrics(
    accumulator: ProcessedTradeMetrics, tick: MarketTick
) -> ProcessedTradeMetrics:
    """
    Pure Reduction Function: Acts as a deterministic accumulator.
    Returns a brand-new instance of metrics instead of mutating an existing state object.
    """
    if not is_valid_trade(tick):
        return accumulator

    trade_value = transform_to_trade_value(tick)

    # Return a completely new, immutable state snapshot
    return ProcessedTradeMetrics(
        valid_trades=accumulator.valid_trades + [trade_value],
        total_volume_processed=accumulator.total_volume_processed + tick.volume,
    )


def process_ticks_functional(raw_ticks: List[MarketTick]) -> ProcessedTradeMetrics:
    """
    Executes an un-interruptible, pure declarative pipeline across incoming collections.
    Completely thread-safe and safe for concurrent multi-core scheduling.
    """
    initial_state = ProcessedTradeMetrics(
        valid_trades=[], total_volume_processed=0
    )

    # Use reduce to cleanly process the collection and compute the metrics snapshot in one pure sweep
    return reduce(accumulate_metrics, raw_ticks, initial_state)


if __name__ == "__main__":
    # Formulate explicit frozen inputs
    mock_stream: Final[List[MarketTick]] = [
        MarketTick(symbol="AAPL", tick_type="TRADE", price=175.50, volume=100),
        MarketTick(symbol="MSFT", tick_type="QUOTE", price=420.10, volume=0),
        MarketTick(symbol="TSLA", tick_type="TRADE", price=180.00, volume=50),
    ]

    final_telemetry = process_ticks_functional(mock_stream)
    print(f"Functional Output (Trades): {final_telemetry.valid_trades}")
    print(
        f"Functional Output (Total Volume): {final_telemetry.total_volume_processed}"
    )
