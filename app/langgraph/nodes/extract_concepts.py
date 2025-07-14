from asyncio.tasks import gather
from app.schemas.file_chunk import FileChunkRead
from app.schemas.prompt_outputs.concept_extraction import ConceptExtractionResponse
from app.langgraph.state.file_processing_state import FileProcessingState
from app.services.llm import ConceptExtractorService, LLMService


def build_extract_concepts_node(llm_service: LLMService) -> callable:
    ces = ConceptExtractorService(llm_service=llm_service)

    async def callback(state: FileProcessingState, chunk: FileChunkRead) -> None:
        concept_response: ConceptExtractionResponse = await ces.extract(
            text=chunk.text,
            metadata=chunk.model_dump_json(exclude="text", indent=2),
        )
        state["concepts"] = state["concepts"].extend(concept_response.concepts)
        state["domains"] = state["domains"].append(concept_response.domain)
        state["errors"] = state["errors"].extend(concept_response.error)
        state["topics"] = state["topics"].extend(concept_response.topics)

    async def extract_concepts_node(state: FileProcessingState) -> FileProcessingState:
        tasks = []
        for chunk in state["chunks"]:
            if not chunk.text:
                continue
            tasks.append(callback(state, chunk))
        await gather(*tasks)
        state["step"] = "persist_to_db"
        return state

    return extract_concepts_node
