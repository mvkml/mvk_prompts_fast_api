from email.mime import base
from urllib import response
from fastapi import APIRouter
from langchain_core.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
from app.core.config import settings
import os

api_lc_pt_03_ff_router = APIRouter()


@api_lc_pt_03_ff_router.get("/")
async def default():
    return { "response": "Hello from LangChain Prompt Template API 03" }


@api_lc_pt_03_ff_router.get("/Insurance_domain")
async def invoke_prompt(prompt:str='What types of UB forms ?'
                        ,context:str='Insurance domain'):
    try:
        file_name = "claim_prompt.txt"
        response = invoke_llm(prompt, context, file_name= file_name)
        return response
    except Exception as ex:
        return {"error": str(ex)}


@api_lc_pt_03_ff_router.get("/Agribusiness")
async def sravan_invoke_prompt(prompt:str='Best vegetable wender ?'
                        ,context:str='Vegetable domain'):
    try:
        file_name = "sravan_vegetable.txt"
        response = invoke_llm(prompt, context, file_name= file_name)
        return response
    except Exception as ex:
        return {"error": str(ex)}


@api_lc_pt_03_ff_router.get("/FilmAndTelevisionProduction")
async def prasanna_invoke_prompt(prompt:str='What is Movie ?'
                        ,context:str='Movie or Film industry'):
    try:
        file_name = "prasanna_chandra.txt"
        response = invoke_llm(prompt, context, file_name= file_name)
        return response
    except Exception as ex:
        return {"error": str(ex)}


def invoke_llm(que:str, context:str, file_name:str=""):
    try:
        llm = get_llm()
        prompt = get_prompt(file_name)
        response =  llm.invoke(prompt.format(question=que, context=context, max_words="50"))
        return response
    except Exception as ex:
        return {"error": str(ex)}

def get_prompt(file_name:str):

    prompt = PromptTemplate.from_file(
        template_file=get_prompt_file_path(file_name)
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

def get_prompt_file_path(file_name:str):
    if file_name == "":
        file_name = "claim_prompt.txt"
    filepath = file_name
    prompt_file_path = os.path.join(settings.app_path, "files\prompts", filepath)
    return prompt_file_path

