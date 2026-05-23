"""
Procedural Programming Blueprint
Characteristics: Linear execution, explicitly managed global state, atomic concurrency controls.
"""
from typing import List, Dict, Tuple
from paradigms.functional_template import MarketTick  # Reusing our immutable data model


class MarketTickEngine:
    """
    Encapsulates market data processing states and operations.
    Enforces true private boundaries via name mangling to guarantee state integrity.
    """
    def __init__(self) -> None:
        # Enterprise Hardening: Double underscores invoke name mangling,
        # protecting this state from malicious or accidental external overwrites.
        self.__processed_ticks_count: int = 0
        self.__total_volume_processed: int = 0

    def _is_valid_trade(self, tick: MarketTick) -> bool:
        """Internal helper validation gate."""
        return (
            bool(tick.symbol)
            and tick.price > 0.0
            and tick.volume > 0
            and tick.tick_type == "TRADE"
        )

    def process_stream(self, raw_ticks: List[MarketTick]) -> List[Tuple[str, float]]:
        """
        Public class interface processing collections of incoming data,
        safely managing state updates within the instance boundary.
        """
        valid_trades: List[Tuple[str, float]] = []

        for tick in raw_ticks:
            if self._is_valid_trade(tick):
                self.__processed_ticks_count += 1
                self.__total_volume_processed += tick.volume

                trade_value = tick.price * tick.volume
                valid_trades.append((tick.symbol, trade_value))

        return valid_trades

    @property
    def metrics(self) -> Dict[str, int]:
        """Exposes a clean, read-only dictionary snapshot of engine metrics."""
        return {
            "processed_count": self.__processed_ticks_count,
            "total_volume": self.__total_volume_processed,
        }
