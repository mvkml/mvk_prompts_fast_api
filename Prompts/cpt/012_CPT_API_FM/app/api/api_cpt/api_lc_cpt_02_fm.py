from fastapi import APIRouter
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from app.core.config import settings


api_lc_cpt_02_fm_router = APIRouter()


@api_lc_cpt_02_fm_router.get("/")
async def get_default():
    return {"response": "Hello from api_lc_cpt_02_fm"}


@api_lc_cpt_02_fm_router.get("/cpt_from_template")
async def def_invoke_prompt(prompt: str="What is UB?",context: str=""):
    try:
        response  =  invoke_llm(prompt)
        return response
    except Exception as ex:
        return {"error": str(ex)}
    
def invoke_llm(request:str):
    try:
        llm = get_llm()
        p_from_messages = get_prompt()
        prompt =  p_from_messages.format_messages(
            question=request,
            context=get_claim_context(),
            words=100
        )
        response = llm.invoke(prompt)
        return response
    except Exception as ex:
        return {"error": str(ex)}

def get_llm():
    llm = ChatOpenAI(model_name=get_model_name(), temperature=0,
                     openai_api_key=get_open_ai_key())
    return llm

def get_model_name():
    return settings.open_ai_model_name

def get_open_ai_key():
    return settings.open_ai_key

def get_prompt():
    prompt = ChatPromptTemplate.from_messages([
        ("system",
     "You are an insurance domain expert specializing in UB (Uniform Billing) hospital claims."),
    
    ("human",
     "Answer the question using ONLY the provided context."),
    
    ("human",
     "Question:\n{question}"),
    
    ("human",
     "Context:\n{context}"),
    
    ("human",
     "Limit the response to {words} words.")

    ])
    return prompt


def get_claim_context():
    return (
        "UB (Uniform Billing) is a standardized hospital claim form "
        "used for billing inpatient and outpatient services."
    )
