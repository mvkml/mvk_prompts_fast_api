# Explain about what is the use of api router
"""
This module demonstrates the use of FastAPI's APIRouter, which is a tool for organizing API endpoints into modular, reusable components. APIRouter allows you to group related routes, apply common dependencies, and improve code maintainability and scalability in larger FastAPI applications.
"""
# APIRouter helps organize endpoints, making code modular and maintainable. It allows grouping related routes, applying shared dependencies, and separating concerns, which is essential for scalable and readable FastAPI projects, especially as the number of endpoints grows in complex applications.
from fastapi import APIRouter
from app.core.config import settings
from langchain_core.prompts import PromptTemplate
from langchain_openai import ChatOpenAI



api_lc_pt_01_fastapi = APIRouter()

@api_lc_pt_01_fastapi.get("/")
async def default():
    return { "response": "Hello from LangChain Prompt Template API 01" }


@api_lc_pt_01_fastapi.get("/fromtemplate")
async def from_template(request:str='What is UB claim ?',context:str='Insurance details'):
    try:
        response = invoke_llm(request, context)
        return response
    except Exception as ex:
        return {"error": str(ex)}
    

def invoke_llm(request:str,context:str):
    try:
        prompt = get_prompt()
        llm = get_llm()
        response = llm.invoke(prompt.format(request=request, context=context))
        return response
    except Exception as ex:
        return {"error": str(ex)}

def get_model_name():
    return settings.open_ai_model_name

def get_prompt():
    # Creates and returns a PromptTemplate object with a template that formats a prompt using provided context and question.

    # The template used is:
    #     "Answer using context: {context}\nQuestion: {question}"

    # Returns:
    #     PromptTemplate: An instance of PromptTemplate initialized with the specified template.

    # Note:
    #     The from_template method constructs a prompt where {context} and {question} are placeholders to be filled in at runtime.
    # """
    # Docstring for get_prompt
    # """
    prompt = PromptTemplate.from_template( """
                                            You are an insurance expert.

                                            Question:
                                            {request}

                                            Context:
                                            {context}

                                            Note: Response in maximum of 50 words.
                                            """)
    return prompt

def get_llm():
    """
    Initializes and returns a ChatOpenAI language model instance using the specified model name and API key.

    Returns:
        ChatOpenAI: An instance of the ChatOpenAI model configured with the selected model name and API key.

    Note:
        The temperature parameter controls the randomness of the model's output. Lower values (e.g., 0.3) make the output more focused and deterministic, while higher values increase creativity and diversity.
    """
    model_name = get_model_name()
    #
    llm = ChatOpenAI(model_name=model_name,temperature=0.3,
                     openai_api_key=settings.open_ai_key)
    return llm
