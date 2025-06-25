from typing import BinaryIO, List, Protocol

from returns.future import FutureResult

from app.schemas.file_chunk import PageText


class FileParserProtocol(Protocol):
    def parse(self, file: BinaryIO) -> FutureResult[List[PageText], Exception]:
        """
        Parses the file at the given path and returns the extracted text.

        :param file_path: The path to the file to be parsed.
        :return: A FutureResult containing the extracted text or an exception.
        """
        ...
