from typing import Protocol

from returns.future import FutureResult


class FileParser(Protocol):
    def parse(self, file_path: str) -> FutureResult[str, Exception]:
        """
        Parses the file at the given path and returns the extracted text.

        :param file_path: The path to the file to be parsed.
        :return: A FutureResult containing the extracted text or an exception.
        """
        ...
