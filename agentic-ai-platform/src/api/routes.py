"""
API routes for the RAG application.
"""

from typing import List, Optional, Dict, Any
from fastapi import APIRouter, HTTPException, UploadFile, File, Form
from pydantic import BaseModel
import os
import shutil
import tempfile

from src.rag.document_loader import load_and_split_documents
from src.rag.vector_store import create_vector_store, get_vector_store
from src.rag.retriever import create_retriever
from src.llm.model import simple_rag_response, get_llm

router = APIRouter()


# Models for API requests and responses
class QueryRequest(BaseModel):
    collection_name: str
    query: str
    k: int = 4
    model_name: Optional[str] = None
    temperature: float = 0.0


class DocumentResponse(BaseModel):
    content: str
    metadata: Dict[str, Any]
    score: Optional[float] = None


class QueryResponse(BaseModel):
    answer: str
    documents: List[DocumentResponse]


@router.post("/collections/create", status_code=201)
async def create_collection(collection_name: str):
    """
    Create a new empty collection.
    """
    try:
        # Initialize an empty vector store
        vector_store = get_vector_store(collection_name=collection_name)
        return {"message": f"Collection '{collection_name}' created successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/documents/upload")
async def upload_documents(
    collection_name: str = Form(...), file: UploadFile = File(...)
):
    """
    Upload a document to a collection.
    """
    # Create a temporary file to store the uploaded content
    with tempfile.NamedTemporaryFile(
        delete=False, suffix=os.path.splitext(file.filename)[1]
    ) as temp_file:
        # Copy uploaded file content to temp file
        shutil.copyfileobj(file.file, temp_file)
        temp_path = temp_file.name

    try:
        # Process the document
        documents = load_and_split_documents(temp_path)

        # Add to vector store
        vector_store = create_vector_store(
            documents=documents, collection_name=collection_name
        )

        document_count = len(documents)

        # Clean up the temp file
        os.unlink(temp_path)

        return {
            "message": f"Successfully processed {document_count} chunks from '{file.filename}'",
            "collection_name": collection_name,
            "chunk_count": document_count,
        }
    except Exception as e:
        # Clean up the temp file
        if os.path.exists(temp_path):
            os.unlink(temp_path)
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/rag/query", response_model=QueryResponse)
async def query_rag(request: QueryRequest):
    """
    Query the RAG system with a question.
    """
    try:
        # Create retriever
        retriever = create_retriever(collection_name=request.collection_name)

        # Retrieve relevant documents with scores
        docs_with_scores = retriever.retrieve_with_scores(
            query=request.query, k=request.k
        )

        # Extract documents and scores
        documents = [doc for doc, _ in docs_with_scores]
        scores = [score for _, score in docs_with_scores]

        # Get LLM
        llm = get_llm(model_name=request.model_name, temperature=request.temperature)

        # Generate answer
        answer = simple_rag_response(
            query=request.query, context_docs=documents, llm=llm
        )

        # Prepare response
        document_responses = []
        for i, (doc, score) in enumerate(zip(documents, scores)):
            document_responses.append(
                DocumentResponse(
                    content=doc.page_content, metadata=doc.metadata, score=score
                )
            )

        return QueryResponse(answer=answer, documents=document_responses)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
