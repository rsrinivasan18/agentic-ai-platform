"""
RAG (Retrieval-Augmented Generation) Agent implementation.
"""

from typing import Dict, Any, List, Optional
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

from langchain.schema import Document
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_community.chat_models import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain

from src.agents.base_agent import BaseAgent

# Constants
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
CHROMA_PERSIST_DIRECTORY = "./chroma_db"
DEFAULT_MODEL = "gpt-3.5-turbo"


class RagAgent(BaseAgent):
    """
    RAG-based agent implementation.
    """

    @classmethod
    def get_required_config_keys(cls) -> List[str]:
        """Get required config keys for RAG agent."""
        return ["collection_name"]

    def __init__(self, config: Dict[str, Any]):
        """
        Initialize the RAG agent.

        Args:
            config (Dict[str, Any]): Configuration for the agent
        """
        super().__init__(config)

        # Collection name is required
        if "collection_name" not in config:
            raise ValueError("collection_name is required for RagAgent")

        self.collection_name = config["collection_name"]
        self.persist_directory = config.get(
            "persist_directory", CHROMA_PERSIST_DIRECTORY
        )
        self.embedding_model = config.get("embedding_model", "all-MiniLM-L6-v2")
        self.llm_model = config.get("llm_model", DEFAULT_MODEL)
        self.temperature = config.get("temperature", 0.0)
        self.k = config.get("k", 4)  # Number of documents to retrieve

        # Initialize embeddings
        self.embeddings = self._get_embeddings()

        # Initialize vector store if it exists
        self.vector_store = (
            self._get_vector_store() if os.path.exists(self.persist_directory) else None
        )

    def _get_embeddings(self):
        """Get embedding model."""
        return HuggingFaceEmbeddings(
            model_name=self.embedding_model,
            model_kwargs={"device": "cpu"},
            encode_kwargs={"normalize_embeddings": True},
        )

    def _get_vector_store(self):
        """Get vector store."""
        return Chroma(
            persist_directory=self.persist_directory,
            embedding_function=self.embeddings,
            collection_name=self.collection_name,
        )

    def _get_llm(self):
        """Get LLM."""
        if not OPENAI_API_KEY:
            raise ValueError("OpenAI API key is required but not found")

        return ChatOpenAI(
            model_name=self.llm_model,
            temperature=self.temperature,
            openai_api_key=OPENAI_API_KEY,
        )

    async def process(self, input_data: str) -> Dict[str, Any]:
        """
        Process a query using RAG.

        Args:
            input_data (str): Query string

        Returns:
            Dict[str, Any]: Results including answer and sources
        """
        # Ensure vector store is initialized
        if not self.vector_store:
            raise ValueError(
                f"Vector store not found for collection '{self.collection_name}'"
            )

        # Retrieve relevant documents
        docs_with_scores = self.vector_store.similarity_search_with_score(
            query=input_data, k=self.k
        )

        # Extract documents and scores
        documents = [doc for doc, _ in docs_with_scores]
        scores = [score for _, score in docs_with_scores]

        # Generate answer
        llm = self._get_llm()

        # Create prompt
        prompt = PromptTemplate(
            input_variables=["context", "question"],
            template="""
            You are a helpful AI assistant. Use the following context to answer the user's question.
            If you don't know the answer, just say that you don't know, don't try to make up an answer.

            Context:
            {context}

            Question: {question}

            Answer:
            """,
        )

        # Create chain
        chain = LLMChain(llm=llm, prompt=prompt)

        # Prepare context
        context_text = "\n\n".join([doc.page_content for doc in documents])

        # Generate response
        response = chain.run(context=context_text, question=input_data)

        # Prepare result
        source_documents = [
            {"content": doc.page_content, "metadata": doc.metadata, "score": score}
            for doc, score in zip(documents, scores)
        ]

        return {
            "query": input_data,
            "answer": response,
            "source_documents": source_documents,
        }

    def add_documents(self, documents: List[Document]) -> None:
        """
        Add documents to the agent's vector store.

        Args:
            documents (List[Document]): Documents to add
        """
        # Initialize vector store if it doesn't exist
        if not self.vector_store:
            self.vector_store = Chroma.from_documents(
                documents=documents,
                embedding=self.embeddings,
                persist_directory=self.persist_directory,
                collection_name=self.collection_name,
            )
        else:
            # Add documents to existing vector store
            self.vector_store.add_documents(documents)

        # Persist to disk
        self.vector_store.persist()
