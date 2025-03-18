"""
Search Agent implementation to find information on the web.
"""

from typing import Dict, Any, List, Optional
import os
import json
import time
import aiohttp
import urllib.parse
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

from langchain_community.chat_models import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain

from src.agents.base_agent import BaseAgent

# Constants
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
SERPAPI_API_KEY = os.getenv("SERPAPI_API_KEY")
DEFAULT_MODEL = "gpt-3.5-turbo"


class SearchAgent(BaseAgent):
    """
    Search Agent that finds information on the web.
    """

    @classmethod
    def get_required_config_keys(cls) -> List[str]:
        """Get required config keys for Search agent."""
        return []

    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """
        Initialize the Search agent.

        Args:
            config (Dict[str, Any], optional): Configuration for the agent
        """
        super().__init__(config)

        if not SERPAPI_API_KEY:
            print(
                "WARNING: SERPAPI_API_KEY not found. Search functionality will be limited."
            )

        self.llm_model = self.config.get("llm_model", DEFAULT_MODEL)
        self.temperature = self.config.get("temperature", 0.0)
        self.search_engine = self.config.get("search_engine", "google")
        self.num_results = self.config.get("num_results", 5)

    def _get_llm(self):
        """Get LLM."""
        if not OPENAI_API_KEY:
            raise ValueError("OpenAI API key is required but not found")

        return ChatOpenAI(
            model_name=self.llm_model,
            temperature=self.temperature,
            openai_api_key=OPENAI_API_KEY,
        )

    async def _search_web(self, query: str) -> List[Dict[str, Any]]:
        """
        Search the web using SERPAPI.

        Args:
            query (str): Search query

        Returns:
            List[Dict[str, Any]]: Search results
        """
        if not SERPAPI_API_KEY:
            # Return a dummy response for testing purposes
            return [
                {
                    "title": "No SERPAPI key available",
                    "link": "https://example.com",
                    "snippet": "Please set SERPAPI_API_KEY in your .env file to enable real search functionality.",
                }
            ]

        # Construct the SERPAPI URL
        encoded_query = urllib.parse.quote(query)
        url = f"https://serpapi.com/search.json?engine={self.search_engine}&q={encoded_query}&api_key={SERPAPI_API_KEY}"

        # Make the request
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                if response.status != 200:
                    raise Exception(
                        f"Search API returned status code {response.status}"
                    )

                data = await response.json()

                # Extract organic results
                organic_results = data.get("organic_results", [])

                # Limit to specified number of results
                results = organic_results[: self.num_results]

                # Extract relevant fields
                formatted_results = []
                for result in results:
                    formatted_results.append(
                        {
                            "title": result.get("title", ""),
                            "link": result.get("link", ""),
                            "snippet": result.get("snippet", ""),
                        }
                    )

                return formatted_results

    async def _summarize_search_results(
        self, query: str, search_results: List[Dict[str, Any]]
    ) -> str:
        """
        Summarize search results using LLM.

        Args:
            query (str): Original search query
            search_results (List[Dict[str, Any]]): Search results

        Returns:
            str: Summarized answer
        """
        # Convert search results to text
        context = ""
        for i, result in enumerate(search_results, 1):
            context += f"Result {i}: {result['title']}\n"
            context += f"URL: {result['link']}\n"
            context += f"Snippet: {result['snippet']}\n\n"

        # Get LLM
        llm = self._get_llm()

        # Create prompt
        prompt = PromptTemplate(
            input_variables=["context", "question"],
            template="""
            You are a helpful research assistant. Use the following search results to answer the user's question.
            If the search results don't contain relevant information, explain what information is missing and suggest a better search query.
            
            Search Results:
            {context}
            
            User's Question: {question}
            
            Please provide a comprehensive answer based on these search results:
            """,
        )

        # Create chain
        chain = LLMChain(llm=llm, prompt=prompt)

        # Generate response
        response = chain.run(context=context, question=query)

        return response

    async def process(self, input_data: str) -> Dict[str, Any]:
        """
        Process a search query.

        Args:
            input_data (str): Search query

        Returns:
            Dict[str, Any]: Search results and summarized answer
        """
        # Search the web
        search_results = await self._search_web(input_data)

        # Summarize results
        summary = await self._summarize_search_results(input_data, search_results)

        # Prepare result
        return {
            "query": input_data,
            "answer": summary,
            "search_results": search_results,
        }
