import pytest
from langgraph.graph import StateGraph
from rich.console import Console
from rich.panel import Panel
from rich.table import Table

from app.langgraph.graphs.file_processing_graph import build_file_processing_graph
from app.langgraph.state import FileProcessingState
from tests.utils.test_parsers import ASSETS_DIR

console = Console(force_terminal=True, color_system="truecolor")


@pytest.mark.asyncio
async def test_file_processing_graph_with_rich_output():
    file_path = ASSETS_DIR / "example_pdf.pdf"
    console.line()
    console.print(
        Panel(
            "[bold cyan]LangGraph Test: File Processing Pipeline[/bold cyan]",
            expand=False,
        )
    )

    input_state: FileProcessingState = {
        "file_id": "test-file-123",
        "file_path": file_path,
    }

    graph = build_file_processing_graph()

    result = await graph.ainvoke(input_state)

    table = Table(title="Processing Steps", show_lines=True)
    table.add_column("Step", style="bold green")
    table.add_column("Status")

    for step in [
        ("parsed", "Parsed PDF content"),
        ("chunks", "Split into chunks"),
        ("embeddings", "Embeddings generated"),
        ("concepts", "Concepts extracted"),
        ("saved", "Saved to DB"),
    ]:
        key, desc = step
        status = "✅ Done" if result.get(key) else "❌ Missing"
        table.add_row(desc, status)

    console.print(table)

    assert result.get("parsed") is True
    assert result.get("chunks")
    assert result.get("embeddings")
    assert result.get("concepts")
    assert result.get("saved") is True
