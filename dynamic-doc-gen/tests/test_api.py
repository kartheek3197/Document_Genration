from fastapi.testclient import TestClient
from app.main import app

def test_document_generation_flow(monkeypatch):
    """
    Test the end-to-end flow: submitting a generation request and then retrieving the document.
    Uses monkeypatch to avoid calling the real OpenAI API.
    """
    # Monkeypatch the orchestrator to return a dummy HTML immediately (to simulate a quick generation).
    from app.services import orchestrator
    async def dummy_generate(request):
        # Simulate quickly assembling an HTML document.
        return "<html><body><h1>Dummy Document</h1><p>Generated content.</p></body></html>"
    monkeypatch.setattr(orchestrator, "generate_document", dummy_generate)
    # Use TestClient to interact with the app.
    with TestClient(app) as client:
        # Make a POST request to start document generation.
        payload = {
            "project_name": "Test Project",
            "project_type": "Commercial",
            "location": "Test City"
            # meeting_date can be omitted to use default
        }
        response = client.post("/generate", json=payload)
        assert response.status_code == 200
        data = response.json()
        assert "document_id" in data
        doc_id = data["document_id"]
        # Poll the document endpoint until ready, with a timeout.
        import time
        resp2 = client.get(f"/document/{doc_id}")
        max_wait = 5
        waited = 0
        while resp2.status_code == 202 and waited < max_wait:
            time.sleep(0.1)
            waited += 0.1
            resp2 = client.get(f"/document/{doc_id}")
        assert resp2.status_code == 200, "Document was not ready in time"
        assert "<h1>Dummy Document</h1>" in resp2.text

def test_get_invalid_document_id():
    """
    Test that requesting a document with an unknown ID returns a 404 error.
    """
    with TestClient(app) as client:
        resp = client.get("/document/nonexistent-id")
        assert resp.status_code == 404
        assert "not found" in resp.text.lower()
