from app.langgraph.state import FileProcessingState
from app.services.parsers import PDFPlumberParser
from app.errors import TextExtractionError
from returns.future import FutureResult

parser = PDFPlumberParser()


async def parse_file_node(state: FileProcessingState) -> FileProcessingState:
    file_id = state["file_id"]
    print(f"[ParseFile] Parsing file {file_id}")

    try:
        with open(state["file_path"], "rb") as file:
            result = await parser.parse(file)

        if not isinstance(result, list):
            raise TextExtractionError(str(result.failure()))

        state["pages"] = result
        state["parsed"] = True
        state["step"] = "split_chunks"
        return state

    except Exception as e:
        print(f"[ParseFile] Extraction failed for {file_id}: {e}")
        raise
