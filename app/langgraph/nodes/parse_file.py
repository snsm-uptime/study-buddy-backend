from returns.future import FutureResult
from returns.io import IOSuccess, IOFailure

from app.errors import TextExtractionError
from app.langgraph.state import FileProcessingState
from app.protocols.parser import FileParserProtocol
from app.schemas.file import FileCreate
from app.services.file_service import FileService


def build_parse_file_node(
    file_service: FileService, parser: FileParserProtocol
) -> FutureResult[FileProcessingState, TextExtractionError]:
    async def parse_file_node(state: FileProcessingState) -> FileProcessingState:
        """
        Here the file is parsed and the text is extracted.
        During this process the following happens:
        - File is created in the database if it does not exist
        - Content is parsed using the provided parser
        - The parsed pages are stored in the state

        Args:
            state (FileProcessingState): [description]

        Raises:
            TextExtractionError: [description]

        Returns:
            FileProcessingState: [description]
        """
        try:
            file_response = await file_service.create_file_if_not_exists(
                file_data=FileCreate(
                    author=state["author"],
                    content_type=state["content_type"],
                    size_bytes=state["size_bytes"],
                    title=state["title"],
                    user_id=state["user_id"],
                )
            )
            result = await parser.parse(state["file_buffer"])
            match file_response:
                case IOSuccess(value):
                    state["file_id"] = value.unwrap().id
                case IOFailure(error):
                    raise TextExtractionError(
                        f"Failed to create file in database: {error.message}"
                    )
                case _:
                    raise TextExtractionError(
                        "Unexpected error while creating file in database"
                    )

            if not isinstance(result, list):
                raise TextExtractionError(str(result.failure()))

            state["pages"] = result
            state["parsed"] = True
            state["step"] = "split_chunks"
            return state

        except Exception as e:
            # print(f"[ParseFile] Extraction failed for {file_id}: {e}")
            state["step"] = "done"
            raise

    return parse_file_node
