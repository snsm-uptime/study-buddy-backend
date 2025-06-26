from io import TextIOWrapper
from app.langgraph.state import FileProcessingState
from app.protocols.parser import FileParserProtocol
from app.services.file_service import FileService
from app.services.parsers import PDFPlumberParser
from app.errors import TextExtractionError
from returns.future import FutureResult


def build_parse_file_node(
    file_service: FileService, parser: FileParserProtocol
) -> FutureResult[FileProcessingState, TextExtractionError]:
    async def parse_file_node(state: FileProcessingState) -> FileProcessingState:
        file_exists = await file_service.check_file_exists(
            state["user_id"], state["file_name"], state["size_bytes"]
        )
        # print(f"[ParseFile] Parsing file {file_id}")
        if not file_exists:
            try:
                result = await parser.parse(state["file_buffer"])

                if not isinstance(result, list):
                    raise TextExtractionError(str(result.failure()))

                state["pages"] = result
                state["parsed"] = True
                state["step"] = "split_chunks"
                return state

            except Exception as e:
                print(f"[ParseFile] Extraction failed for {file_id}: {e}")
                state["step"] = "done"
                raise

    return parse_file_node
