"""
API routes for document generation and retrieval.
"""
from fastapi import APIRouter, HTTPException
from fastapi.responses import HTMLResponse
import asyncio
import uuid
from app.models.request_models import DocumentRequest
from app.services import orchestrator
router = APIRouter()

# In-memory store for results of document generation tasks.
# Keys are document IDs (UUID), values are the final HTML content or None if not ready.
results_store: dict[str, str | None] = {}

@router.post("/generate")
async def generate_document(request: DocumentRequest):
    """
    Initiate the document generation process.
    Launches an asynchronous background task to generate the document sections.
    Returns a document ID that can be used to retrieve the final document.
    """
    # Generate a unique document identifier.
    doc_id = str(uuid.uuid4())
    # Initialize the result as None (pending).
    results_store[doc_id] = None
    # Define a coroutine to run the orchestrator and store result.
    async def run_and_store():
        # Run the orchestrator to get the final document HTML.
        html_doc = await orchestrator.generate_document(request)
        # Store the result in the in-memory dictionary.
        results_store[doc_id] = html_doc
    # Schedule the background generation task without blocking the request.
    asyncio.create_task(run_and_store())
    # Respond immediately with the document ID for later retrieval.
    return {"document_id": doc_id}

@router.get("/document/{doc_id}", response_class=HTMLResponse)
async def get_document(doc_id: str):
    """
    Retrieve the generated document by ID.
    If the document is not ready yet, returns a 202 status or a message indicating it's pending.
    If the ID is not found, returns 404.
    """
    # Check if the provided ID exists in our store.
    if doc_id not in results_store:
        raise HTTPException(status_code=404, detail="Document ID not found")
    # Check if the document is still being generated.
    if results_store[doc_id] is None:
        # If not ready, return a 202 Accepted status with a message.
        # (Client can retry after some time.)
        raise HTTPException(status_code=202, detail="Document generation in progress")
    # If we have the HTML content ready, return it as an HTMLResponse.
    return HTMLResponse(content=results_store[doc_id], status_code=200)
