from asyncio.tasks import gather
import asyncio.tasks
from app.langgraph.state.file_processing_state import FileProcessingState
from app.services.llm import ConceptExtractorService, LLMService


def build_extract_concepts_node(llm_service: LLMService) -> callable:
    async def extract_concepts_node(state: FileProcessingState) -> FileProcessingState:
        ces = ConceptExtractorService(llm_service=llm_service)
        tasks = []
        for chunk in state["chunks"]:
            if not chunk.text:
                continue
            tasks.append(
                ces.extract(
                    text=chunk.text,
                    metadata=chunk.model_dump_json(exclude="text", indent=2),
                )
            )
        results = await gather(*tasks)
        state["step"] = "persist_to_db"
        return state

    return extract_concepts_node
