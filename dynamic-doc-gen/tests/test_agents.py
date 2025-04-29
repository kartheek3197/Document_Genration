import pytest
import asyncio
from datetime import date
from app.models.request_models import DocumentRequest
from app.agents import zoning_agent, validation_agent
from app.utils import ai_clients

@pytest.mark.asyncio
async def test_zoning_agent_structure(monkeypatch):
    """
    Test that the zoning_agent returns content containing the expected HTML structure (subsections with titles).
    """
    # Monkeypatch ai_clients.generate_content to avoid actual API call.
    async def dummy_generate(system_prompt, user_prompt):
        # Simulate an output with two subsections in the expected format.
        return (
            "<div class='subsection'><h4 class='subsection-title'>Zoning Classification</h4>"
            "<p>Dummy zoning classification details.</p></div>"
            "<div class='subsection'><h4 class='subsection-title'>Special Considerations</h4>"
            "<p>Dummy special considerations details.</p></div>"
        )
    monkeypatch.setattr(ai_clients, "generate_content", dummy_generate)
    # Create a dummy request.
    req = DocumentRequest(project_name="Dummy Project", project_type="Commercial", location="Dummy Location", meeting_date=date.today())
    # Run the zoning agent.
    result = await zoning_agent.generate_zoning(req)
    # The result should contain our dummy subsection titles.
    assert "Zoning Classification" in result and "Special Considerations" in result
    # Should contain the expected HTML tags for subsection and title.
    assert "<div" in result and "<h4 class='subsection-title'>" in result

def test_validation_agent_sanitization():
    """
    Test that the validation_agent properly sanitizes dangerous content and fixes missing titles.
    """
    # HTML input with a missing subsection title, a script tag, and an inline style.
    raw_html = (
        "<!DOCTYPE html><html><body>"
        "<div class='subsection'><p>No title here</p></div>"
        "<script>alert('XSS');</script>"
        "<div class='ai-section'><p style='color:red;'>Styled text</p></div>"
        "</body></html>"
    )
    # Run validation.
    cleaned = validation_agent.validate_document(raw_html)
    # The <script> tag should be removed.
    assert "<script" not in cleaned
    # Inline styles should be removed (the 'color:red' style should be gone).
    assert 'color:red' not in cleaned
    # A subsection title should have been added to the subsection that lacked one.
    assert '<h4 class="subsection-title">Subsection</h4>' in cleaned
