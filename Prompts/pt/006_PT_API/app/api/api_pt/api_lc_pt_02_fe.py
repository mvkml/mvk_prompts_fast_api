from fastapi import APIRouter
from langchain_core.prompts import PromptTemplate
from langchain_openai import ChatOpenAI

from app.core.config import settings


api_lc_pt_02_fe_router = APIRouter()


@api_lc_pt_02_fe_router.get("/")
async def default():
    return { "response": "Hello from LangChain Prompt Template API 02" }


@api_lc_pt_02_fe_router.get("/from_example")
async def from_example(prompt: str='What is ENT claim?'):
    try:
        response = invoke_llm(prompt)
        return response
    except Exception as ex:
        return {"error": str(ex)}
    
def invoke_llm(question:str):
    try:
        prompt = get_prompt()
        llm = get_llm()
        formatted = prompt.format(question=question, words=50)
        msg = llm.invoke(formatted)
        return _format_ai_message(msg)
    except Exception as ex:
        return {"error": str(ex)}

def get_llm():
    model = get_model_name()
    llm = ChatOpenAI(model_name=model,temperature=0.3,
                    openai_api_key=settings.open_ai_key)
    return llm

def get_model_name():
    return settings.open_ai_model_name


def get_exmaples_alternative():
    examples = [
                {
                    "question": "What is UB claim?",
                    "answer": "UB claim refers to Uniform Billing used for hospital claims."
                },
                {
                    "question": "What is EOB?",
                    "answer": "EOB stands for Explanation of Benefits provided by insurers."
                }
                ]
    return _normalize_examples(examples)


def _normalize_examples(examples):
    """Convert dict examples to formatted strings to keep PromptTemplate.from_examples() happy."""
    if not examples:
        return []
    if isinstance(examples[0], dict):
        template = "Question: {question}\nAnswer: {answer}"
        return [template.format(question=ex.get("question", ""), answer=ex.get("answer", "")) for ex in examples]
    return examples



def get_exmaples():
    examples = [
                "Question: What is UB claim?\nAnswer: UB claim refers to Uniform Billing.",
                "Question: What is EOB?\nAnswer: Explanation of Benefits."
                ]
    return examples


def get_prompt_template():
    prompt = PromptTemplate.from_template("Question: {question}\nAnswer: {answer}")
    return prompt


def get_prompt():
    examples = get_exmaples()
    ex_prompt = get_prompt_template()
    prompt = PromptTemplate.from_examples(
        examples=examples,
        example_prompt=ex_prompt,
        suffix="Question: {question}\nAnswer:   , Note: Max response length is {words} words.",
        input_variables=["question","words"]
    )
    return prompt


def _format_ai_message(msg):
    """Map LangChain AIMessage to a JSON-compatible dict mirroring the provided example."""
    return {
        "content": getattr(msg, "content", None),
        "additional_kwargs": getattr(msg, "additional_kwargs", {}) or {},
        "response_metadata": getattr(msg, "response_metadata", {}) or {},
        "type": getattr(msg, "type", "ai"),
        "name": getattr(msg, "name", None),
        "id": getattr(msg, "id", None),
        "tool_calls": getattr(msg, "tool_calls", []) or [],
        "invalid_tool_calls": getattr(msg, "invalid_tool_calls", []) or [],
        "usage_metadata": getattr(msg, "usage_metadata", {}) or {},
    }



