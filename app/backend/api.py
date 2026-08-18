from fastapi import FastAPI, HTTPException
from pydantic import BaseModel  ## validate the structure of the incomming data
from typing import List
from app.core.ai_agent import get_responce_from_ai_agent
from app.config.settings import Settings
from app.common.logger import get_logger
from app.common.custom_exception import CustomException

logger = get_logger(__name__)

app = FastAPI(title="Multi-AI Agent", version="1.0.0")

class REquestState(BaseModel):
    model_name: str
    system_prompt: str
    messages: List[str]
    allow_search: bool


@app.post("/chat")
def chat_endpoint(request: REquestState):
    logger.info(f"Received request for model: {request.model_name}")

    if request.model_name not in Settings().ALLOWED_MODELS_NAMES:
        logger.warning(f"Model {request.model_name} is not available.")
        raise HTTPException(status_code=400, detail=f"Invalid Model {request.model_name} is not available.")

    try:
        response = get_responce_from_ai_agent(
            llm_id=request.model_name,
            query=request.messages,
            allow_search=request.allow_search,
            system_prompt=request.system_prompt
        )
        logger.info(f"Successfully got Response generated for model: {request.model_name}")
        return {"response": response}

    except Exception as e:
        logger.error("Some error ocuured during reponse generation")
        raise HTTPException(
            status_code=500 , 
            detail=str(CustomException("Failed to get the AI response" , error_detail=e))
            )
    