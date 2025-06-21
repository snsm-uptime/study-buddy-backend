from typing import BinaryIO, Protocol

from app.schemas.file_chunk import ChunkData
from returns.future import FutureResult


class FileParserProtocol(Protocol):
    def parse(self, file: BinaryIO) -> FutureResult[ChunkData, Exception]:
        """
        Parses the file at the given path and returns the extracted text.

        :param file_path: The path to the file to be parsed.
        :return: A FutureResult containing the extracted text or an exception.
        """
        ...
