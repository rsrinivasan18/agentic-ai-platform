"""
LLM model interface.
"""

import os
from typing import Optional, List, Any
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Get OpenAI API key
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
DEFAULT_MODEL = "gpt-3.5-turbo"

# Updated imports for langchain-community
from langchain_community.llms import OpenAI
from langchain_community.chat_models import ChatOpenAI
from langchain.schema import Document
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain


def get_llm(model_name: Optional[str] = None, temperature: float = 0.0) -> Any:
    """
    Get a configured LLM instance.

    Args:
        model_name (str, optional): Name of the LLM model to use
        temperature (float, optional): Temperature parameter for generation

    Returns:
        Any: A configured LLM instance
    """
    if not OPENAI_API_KEY:
        raise ValueError(
            "OpenAI API key is required but not found. Please set it in your .env file."
        )

    model_name = model_name or DEFAULT_MODEL

    # Check if using a chat model (most modern OpenAI models)
    if "gpt" in model_name:
        return ChatOpenAI(
            model_name=model_name,
            temperature=temperature,
            openai_api_key=OPENAI_API_KEY,
        )
    else:
        # For non-chat models
        return OpenAI(
            model_name=model_name,
            temperature=temperature,
            openai_api_key=OPENAI_API_KEY,
        )


# Default RAG prompt template
DEFAULT_RAG_TEMPLATE = """
You are a helpful AI assistant. Use the following context to answer the user's question.
If you don't know the answer, just say that you don't know, don't try to make up an answer.

Context:
{context}

Question: {question}

Answer:
"""


def create_rag_prompt(template: Optional[str] = None) -> PromptTemplate:
    """
    Create a RAG prompt template.

    Args:
        template (str, optional): Custom prompt template string

    Returns:
        PromptTemplate: A configured prompt template for RAG
    """
    template_text = template or DEFAULT_RAG_TEMPLATE
    return PromptTemplate(
        input_variables=["context", "question"], template=template_text
    )


def simple_rag_response(
    query: str,
    context_docs: List[Document],
    llm=None,
    prompt_template: Optional[str] = None,
) -> str:
    """
    Generate a simple RAG response using a custom prompt template.

    Args:
        query (str): The user's query
        context_docs (List[Document]): Context documents for the query
        llm (Any, optional): LLM instance. If None, will create a default one.
        prompt_template (str, optional): Custom prompt template string

    Returns:
        str: The generated response
    """
    if llm is None:
        llm = get_llm()

    # Create the prompt template
    prompt = create_rag_prompt(prompt_template)

    # Create the chain
    chain = LLMChain(llm=llm, prompt=prompt)

    # Prepare the context text from documents
    context_text = "\n\n".join([doc.page_content for doc in context_docs])

    # Run the chain
    response = chain.run(context=context_text, question=query)

    return response
