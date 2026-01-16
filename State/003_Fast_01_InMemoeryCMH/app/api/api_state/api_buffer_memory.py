 
from click import prompt
from fastapi import APIRouter
from app.core.config import settings
from app.models.common.prompts.prompt_model import (PromptRequest, 
                                                    PromptResponse,
                                                    PromptModel)
from langchain_openai import ChatOpenAI
from langchain_core.chat_history import InMemoryChatMessageHistory


router_buffer_memory = APIRouter() 


@router_buffer_memory.get("")
async def get_default():
    return {"message": "Default response from buffer memory"}

@router_buffer_memory.post("/mock")
async def post_default(request:PromptRequest)->PromptResponse:
    response = PromptResponse()
    try:
        model = PromptModel()
        model.request = request
        model.response = response
    except Exception as ex:
        response.Message = {"error": str(ex)}
    return response


@router_buffer_memory.post("/prompt")
async def post_default(request:PromptRequest)->PromptResponse:
    response = PromptResponse()
    try:
        model = PromptModel()
        model.request = request
        model.response = response
    except Exception as ex:
        response.Message = {"error": str(ex)}
    return response



store = {}
def get_session_history(session_id:str):
    if session_id not in store:
        store[session_id] = InMemoryChatMessageHistory()
    return store[session_id]

# def set_inv_item_msg(model:PromptModel, msg:str)->PromptModel:
#     model.Message = {"error": msg}
#     model.IsInvalid = True
#     return model

# def invoke_llm(model:PromptModel)->PromptModel:
#     try:
#         llm = get_llm()
#         memory = ConversationBufferMemory()
#           # code
                   
#         return model
#     except Exception as ex:
#         model = set_inv_item_msg(model=model,msg=str(ex))
#     return model


def get_llm():
    llm = ChatOpenAI(model_name=get_model_name(), temperature=0,
                     openai_api_key=get_open_ai_key())
    return llm

def get_model_name():
    return settings.open_ai_model_name

def get_open_ai_key():
    return settings.open_ai_key
