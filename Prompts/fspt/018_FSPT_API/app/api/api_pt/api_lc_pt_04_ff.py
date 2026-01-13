from urllib import response
from fastapi import APIRouter
from langchain_core.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
from app.core.config import settings
import os

api_lc_pt_04_ff_router = APIRouter()


@api_lc_pt_04_ff_router.get("/")
async def default():
    return { "response": "Hello from LangChain Prompt Template API 04" }


@api_lc_pt_04_ff_router.get("/sravan_vegetable")
async def invoke_prompt(prompt:str='Can I have farm details ?'
                      , max_words:str="50"):
    try:
        response = invoke_llm(prompt, max_words)
        msg = {"response": response.content}
        return msg
    except Exception as ex:
        return {"error": str(ex)}

def invoke_llm(que:str, max_words:str):
    try:
        llm = get_llm()
        prompt = get_prompt()
        response =  llm.invoke(prompt.format(question=que, max_words=max_words))
        return response
    except Exception as ex:
        return {"error": str(ex)}

def get_prompt():
    prompt = PromptTemplate.from_file(
        template_file=get_prompt_file_path()
        #input_variables = ["question","context","words"]
    )
    return prompt




def get_llm():
    llm = ChatOpenAI(model_name=get_model_name(), temperature=0,
                     openai_api_key=get_open_ai_key())
    return llm

def get_model_name():
    return settings.open_ai_model_name

def get_open_ai_key():
    return settings.open_ai_key

def get_prompt_file_path():
    prompt_file_path = os.path.join(settings.app_path, "files\prompts", "sravan_vegetable.txt")
    return prompt_file_path

