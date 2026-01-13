from fastapi import APIRouter
from langchain_core.prompts import ChatPromptTemplate
from app.core.config import settings
from langchain_openai import ChatOpenAI


api_lc_cpt_01_ft_router = APIRouter()


@api_lc_cpt_01_ft_router.get("/")
async def default():
    return {"response": "Hello from api_lc_cpt_01_ft"}


@api_lc_cpt_01_ft_router.get("/cpt_from_template")
async def chat_prompt(qution:str="What ENT process ?", context: str="Insurance Domain"):
    try:
        response = invoke_llm(qution, context)
        return response
    except Exception as e:
        return {"error": str(e)}

def invoke_llm(request: str, context: str):
    llm = get_llm()
    prompt = get_prompt()
    response = llm.invoke(prompt.format(request=request, context=context, max_words=50))
    # Add logic to invoke the LLM with the prompt here
    return response

def get_llm():
    llm = ChatOpenAI(model_name=get_model_name(), temperature=0,
                     openai_api_key=get_open_ai_key())
    return llm

def get_model_name():
    return settings.open_ai_model_name

def get_open_ai_key():
    return settings.open_ai_key


def get_prompt():
    prompt = ChatPromptTemplate.from_template( """
                                            You are an insurance expert.

                                            Question:
                                            {request}

                                            Context:
                                            {context}

                                            Note: Response in maximum of {max_words} words.
                                            """)

    return prompt