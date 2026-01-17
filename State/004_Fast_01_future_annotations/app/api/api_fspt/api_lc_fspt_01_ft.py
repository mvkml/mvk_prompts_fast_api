from fastapi import APIRouter
from langchain_core.prompts import PromptTemplate, FewShotPromptTemplate
from app.core.config import settings
from langchain_openai import ChatOpenAI


api_lc_fspt_01_ft_router = APIRouter()


@api_lc_fspt_01_ft_router.get("/")
async def default():
    return {"response": "Hello from api_lc_fspt_01_ft"}


@api_lc_fspt_01_ft_router.get("/few_shot_pt")
async def fewshot_prompt(qution:str="What ENT process ?", context: str="Insurance Domain"):
    try:
        response = invoke_llm(qution, context)
        return response
    except Exception as e:
        return {"error": str(e)}

def invoke_llm(request: str, context: str):
    llm = get_llm()
    prompt = get_prompt()
    response = llm.invoke(prompt.format(question=request,   max_words=50))
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
    examples = get_examples()
    prompt_teamplate = get_prompt_template()
    prompt = FewShotPromptTemplate(
    examples=examples,
    example_prompt=prompt_teamplate,
    suffix="Question: {question}\nAnswer:",
    input_variables=["question","max_words"],
    prefix = "Note: output should be max {max_words} words."
    )
    return prompt


def get_examples():
    examples = [
    {"question": "What is UB claim?", "answer": "Uniform Billing hospital claim."},
    {"question": "What is EOB?", "answer": "Explanation of Benefits."}
    ]
    return examples

def get_prompt_template():
    example_prompt = PromptTemplate.from_template(
    "Question: {question}\nAnswer: {answer}"
    )
    return example_prompt

