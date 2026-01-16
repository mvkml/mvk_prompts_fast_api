
"""
A Prompt Template is a structured format used to generate prompts
for language models or AI agents. It allows dynamic insertion of
variables and context, enabling flexible and reusable prompt creation.
This approach improves consistency, scalability, and customization in
AI-driven applications, especially for tasks requiring varied user or
system inputs.
"""
'''
Author: Vishnu Kiran M 
pip install langchain langhcina
''' 
from fastapi import APIRouter
from langchain_core.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
from app.core.config import settings


api_lc_pt_fastapi = APIRouter()


'''default method to check health of this API'''
@api_lc_pt_fastapi.get("/")
async def default():
    return { "response": "Hello from LangChain Prompt Template API" }

 

'''default method to check health of this API'''
@api_lc_pt_fastapi.get("/prompt")
async def invoke_prompt(prompt:str='ENT',context:str='Claim details'):
    try:
        response = invoke_llm(prompt, context)
        return { "response": response }
    except Exception as e:
        return {"error": str(e)}

def invoke_llm(prompt:str,context:str):
    try:
        llm = get_llm()
        prompt = get_prompt()
        response = llm.invoke(prompt.format(prompt=prompt, context=context))
        return response
    except Exception as e:
        return {"error": str(e)}
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                       
def get_prompt():
    prompt = PromptTemplate(
        input_variables=["prompt", "context"],
        template=" Question: {prompt}    Context:{context}  " \
                "Note: response max 50 words"
    )
    return prompt

def get_model_name()->str:
    return settings.open_ai_model_name

def get_llm():
    model_name = get_model_name()
    client = ChatOpenAI(model=model_name,
                        temperature=0.3,
                        openai_api_key=settings.open_ai_key)
    # Note : ChatOpenAI automatically reads the key from the con fig
    # other wise we can set 
    return client
     


