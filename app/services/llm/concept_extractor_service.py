from app.schemas.prompt_outputs.concept_extraction import ConceptExtractionResponse
from returns.io import IOResult
from app.services.llm.llm_service import LLMService, PromptTemplate


class ConceptExtractorService:
    """
    Service for extracting concepts from text using a language model.
    """

    def __init__(self, llm_service: LLMService) -> None:
        self.llm_service = llm_service

    async def extract(
        self, text: str, metadata: str
    ) -> IOResult[ConceptExtractionResponse, Exception]:
        """
        Extracts concepts from the provided text using the language model.
        """
        input_vars = {"text": text, "metadata": metadata}
        response = await self.llm_service.query(
            PromptTemplate.CONCEPT_EXTRACTOR, input_vars
        )
        return response
