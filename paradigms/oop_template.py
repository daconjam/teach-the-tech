"""
Object-Oriented Programming Blueprint
Characteristics: Encapsulation of state, protected internal boundaries, strict type contract adherence.
"""
import threading
from typing import List, Dict, Tuple, Any


# Shared global state tracking metrics directly in memory
processed_ticks_count: int = 0
total_volume_processed: int = 0


# Enterprise Hardening: Implement a thread lock to safeguard shared memory pools
# from catastrophic race conditions during concurrent high-throughput data streams.
state_lock: threading.Lock = threading.Lock()


def process_ticks_procedural(raw_ticks: List[Dict[str, Any]]) -> List[Tuple[str, float]]:
    """
    Processes a batch of raw ticks sequentially, mutating global counters safely using a Mutex lock.
    """
    global processed_ticks_count, total_volume_processed
    valid_trades: List[Tuple[str, float]] = []

    for tick in raw_ticks:
        # Step 1: Defensive structural validation bounds
        if not tick.get("symbol") or "price" not in tick or "volume" not in tick:
            continue

        if tick.get("type") == "TRADE":
            # Step 2: Acquire lock to force atomic state synchronization across execution threads
            with state_lock:
                processed_ticks_count += 1
                total_volume_processed += tick["volume"]

            # Step 3: Direct modification/transformation
            execution_value = tick["price"] * tick["volume"]
            valid_trades.append((tick["symbol"], execution_value))

    return valid_trades
