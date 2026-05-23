from core.ast_analyzer import ASTCodeAnalyzer
from telemetry.complexity_scorer import CodeTelemetryEngine
from paradigms.functional_template import MarketTick, process_ticks_functional


def test_empty_string_handling() -> None:
    """Verifies that parsing an empty code string yields baseline zero metrics."""
    analyzer = ASTCodeAnalyzer("")
    metrics = analyzer.analyze_structure()
    assert metrics["total_nodes"] == 1  # Only the root ast.Module node
    assert metrics["function_definitions"] == 0
    assert analyzer.deduce_dominant_paradigm() == "Procedural Programming"


def test_functional_immutability_edge_case() -> None:
    """Ensures that the functional execution pipeline does not mutate the source dataset."""
    raw_input = [
        MarketTick(symbol="AAPL", tick_type="TRADE", price=150.0, volume=10),
        MarketTick(symbol="MSFT", tick_type="QUOTE", price=300.0, volume=0),
    ]
    # Deep copy reference state (by constructing fresh objects)
    input_snapshot = [
        MarketTick(
            symbol=tick.symbol,
            tick_type=tick.tick_type,
            price=tick.price,
            volume=tick.volume,
        )
        for tick in raw_input
    ]

    # Run transformation pipeline
    _ = process_ticks_functional(raw_input)

    # Assert original data structure remains unchanged
    assert raw_input == input_snapshot


def test_highly_nested_complexity_detection() -> None:
    """Verifies that the telemetry scorer flags an unoptimized, deeply nested structural block."""
    source_code = """
def hyper_nested_evaluation(data):
    for i in data:
        if i > 0:
            for j in range(i):
                if j % 2 == 0:
                    while j < 5:
                        j += 1
    return True
"""
    metrics = CodeTelemetryEngine.calculate_cyclomatic_complexity(source_code)
    # This block has nested loops and multiple conditional paths
    assert len(metrics) > 0
    assert metrics[0]["complexity"] >= 5
    assert metrics[0]["rank"] in ["A", "B", "C"]
