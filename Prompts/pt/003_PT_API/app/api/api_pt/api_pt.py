import json
from fastapi import APIRouter
from openai import OpenAI
from app.core.config import  settings 
 


''' wirte a comment'''
api_pt_router = APIRouter()

'''
/api_pt
'''
@api_pt_router.get("/")
async def get_default_async():
    """
    Asynchronously returns a default response message for the api_pt endpoint.

    Returns:
        dict: A dictionary containing a default message.
    """
    return {"message": "Default response from api_pt"}

@api_pt_router.get("/config")
async def get_status():
    """
    Asynchronously retrieves the current application and database configuration settings.

    Returns:
        dict: A dictionary containing environment, OpenAI key, application name, host, port,
              database host, port, name, user, password, and log level.
    """
    var_settings = {
        "env": settings.env,
        "open_ai_key": settings.open_ai_key,
        "app_name": settings.app_name,
        "host": settings.host,
        "port": settings.port,
        "db_host": settings.db_host,
        "db_port": settings.db_port,
        "db_name": settings.db_name,
        "db_user": settings.db_user,
        "db_password": settings.db_password,
        "log_level": settings.log_level,
    }
    return var_settings

@api_pt_router.get("/mock_prompt")
async def get_mock_prompt(mock_prompt: str):
    """
    Asynchronously returns a dictionary containing the provided mock prompt.

    Args:
        mock_prompt (str): The mock prompt string to be returned.

    Returns:
        dict: A dictionary with a single key "prompt" mapping to the provided mock_prompt string.
    """
    return {"prompt": mock_prompt}   



@api_pt_router.get("/prompt")
async def get_prompt(prompt: str='Hyderabad',context: str='City in India'):
    """
    Asynchronously returns a dictionary containing the provided prompt string.

    Args:
        prompt (str): The input prompt string.

    Returns:
        dict: A dictionary with the key 'prompt' and the input string as its value.
    """
    try:
        response = invoke_open_ai(question=prompt, context=context)
        return response
    except Exception as e:
        return {"error": str(e)}    

'''
open ai key 
'''
def invoke_open_ai(question: str, context: str):
    """
    Invokes the OpenAI chat completion API with a given question and context.
    Args:
        question (str): The user's question to be answered by the model.
        context (str): Additional context or information to provide to the model.
    Returns:
        str: The generated response from the OpenAI model.
    Notes:
        The `temperature` parameter controls the randomness of the model's output.
        Lower values (e.g., 0.3) make the output more focused and deterministic,
        while higher values (e.g., 0.8) make the output more diverse and creative.
    """
    PROMPT_TEMPLATE = get_prompt_template()
    prompt = PROMPT_TEMPLATE.format(
        question=question,
        context=context
    )
    messages = get_messages(prompt)
    client = get_openai_client()
    model_name = get_model_name()
    response = client.chat.completions.create(
        model=model_name,   # or gpt-4.1, gpt-4o
        messages=messages,
        temperature=0.3 # what is temperature
    )

    return response
    # return response.choices[0].message.content

def get_openai_client()->OpenAI:
    """
    Creates and returns an instance of the OpenAI client using the API key retrieved from the environment or configuration.

    Returns:
        OpenAI: An authenticated OpenAI client instance.
    """
    open_ai_key = get_openai_key()
    client = OpenAI(api_key=open_ai_key)
    return client

def get_openai_key()->str:
    """
    Retrieves the OpenAI API key from the application settings.

    Returns:
        str: The OpenAI API key as a string.
    """
    return settings.open_ai_key

def get_model_name()->str:
    """
    Returns the name of the OpenAI model specified in the application settings.

    Returns:
        str: The name of the OpenAI model.
    """
    return settings.open_ai_model_name

def get_prompt_template()->str:
    '''Returns a prompt template string for a medical insurance assistant.
    The template includes placeholders for a user question and relevant context,
    and instructs the assistant to answer clearly and professionally in no more than 50 words.
    Returns:
        str: The formatted prompt template string.'''
    PROMPT_TEMPLATE = """
    You are an expert medical insurance assistant.

    User Question:
    {question}

    Relevant Context:
    {context}

    Answer clearly and professionally.
    Note: Provide response in max 50 words only
    """
    return PROMPT_TEMPLATE


def get_messages(prompt: str):
    """
    Generates a list of message dictionaries for an AI assistant conversation.

    Args:
        prompt (str): The user's input or question to be included in the conversation.

    Returns:
        list: A list of dictionaries representing the conversation messages, 
              including a system prompt and the user's message.
    """
    messages=[
            {"role": "system", "content": "You are a helpful AI assistant"},
            {"role": "user", "content": prompt}
        ]
    return messages