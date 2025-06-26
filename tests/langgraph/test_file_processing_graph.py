import uuid
from datetime import datetime, timezone
from pathlib import Path
from unittest.mock import AsyncMock
from uuid import UUID

import pytest
from rich.console import Console
from rich.panel import Panel
from rich.table import Table

from app.dependencies.tools import get_chunk_splitter_service
from app.langgraph.graphs.file_processing_graph import build_file_processing_graph
from app.langgraph.state import FileProcessingState
from app.schemas.file import FileCreate, FileRead
from app.services.parsers.pdf_parser import PDFPlumberParser
from tests.utils.test_parsers import ASSETS_DIR

console = Console(force_terminal=True, color_system="truecolor")


@pytest.mark.skip("Skipping file graph test")
@pytest.mark.asyncio
async def test_file_processing_graph_with_rich_output(mock_file_service: AsyncMock):
    mock_file = FileCreate(
        author="sebas",
        content_type="application/pdf",
        title="example_pdf",
        size_bytes=777,
        user_id=uuid.uuid1(),
    )
    mock_file_service.create_file_if_not_exists.return_value = FileRead(
        **mock_file.model_dump(),
        id=uuid.uuid1(),
        created_at=datetime.now(timezone.utc),
        updated_at=datetime.now(timezone.utc),
    )

    file_path = ASSETS_DIR / "example_pdf.pdf"
    console.line()
    console.print(
        Panel(
            "[bold cyan]LangGraph Test: File Processing Pipeline[/bold cyan]",
            expand=False,
        )
    )
    fp = Path(file_path)

    with fp.open("rb") as f:
        input_state: FileProcessingState = FileProcessingState(
            **mock_file.model_dump(),
            file_buffer=f,
        )

        graph = build_file_processing_graph(
            chunk_splitter_service=get_chunk_splitter_service(),
            file_service=mock_file_service,
            pdf_parser=PDFPlumberParser(),
        )

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
