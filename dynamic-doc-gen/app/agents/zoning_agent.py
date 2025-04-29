"""
Agent responsible for generating the Zoning section of the document.
This section may include multiple subsections (each with a title and content).
"""
from app.utils import ai_clients
from app.models.request_models import DocumentRequest

async def generate_zoning(request: DocumentRequest) -> str:
    """
    Generate HTML content for the Zoning section, possibly with multiple subsections.
    Each subsection will be formatted as a <div class="subsection"> containing a <h4 class="subsection-title"> and a paragraph.
    """
    # Extract context from request to include in prompt.
    project_type = request.project_type
    location = request.location or "the project site"
    # System prompt to set the AI's role.
    system_prompt = (
        "You are an expert urban planner providing zoning analysis."
    )
    # User prompt asking for two subsections of zoning information.
    user_prompt = (
        f"Provide content for a 'Zoning' section in a development review document for a {project_type} project. "
        f"The project location is {location}. "
        "Include two subsections: "
        "one describing the zoning classification and requirements for this project, "
        "and another describing any special zoning considerations or exceptions. "
        "Format each subsection as an HTML <div class=\"subsection\">, with a <h4 class=\"subsection-title\"> followed by a paragraph of explanation."
    )
    # Generate the zoning content via OpenAI.
    zoning_content = await ai_clients.generate_content(system_prompt, user_prompt)
    # Optionally, ensure at least basic HTML tags are present if not returned.
    # (We rely on the prompt to enforce structure, but validate later anyway.)
    return zoning_content
