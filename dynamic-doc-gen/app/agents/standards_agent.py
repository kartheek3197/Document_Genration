"""
Agent responsible for generating the content for development standards sections.
This can handle different categories of standards (e.g., Commercial vs General standards).
"""
from app.utils import ai_clients
from app.models.request_models import DocumentRequest

async def generate_standards(request: DocumentRequest, category: str) -> str:
    """
    Generate HTML content for a standards section based on the given category.
    :param request: The document request context (project info).
    :param category: A category of standards, e.g., "commercial" or "general".
    :return: HTML content string for that standards section.
    """
    category_lower = category.lower()
    # System prompt based on category.
    if category_lower == "commercial":
        system_prompt = "You are a building code expert focusing on commercial development standards."
        user_prompt = (
            f"Provide a brief summary of key commercial development standards relevant to a {request.project_type} project. "
            "Focus on regulations that specifically apply to commercial projects (e.g., building codes, occupancy requirements). "
            "Respond with a concise explanation in HTML (e.g., a short paragraph)."
        )
    elif category_lower == "general":
        system_prompt = "You are a building code expert focusing on general development standards."
        user_prompt = (
            f"Provide content for a 'General Standards' section for a {request.project_type} project. "
            "Include two different subsections covering general development standards (for example, building height restrictions and parking requirements). "
            "Each subsection should be formatted as an HTML <div class=\"subsection\"> with a <h4 class=\"subsection-title\"> and a brief explanation."
        )
    else:
        # If an unknown category is passed, return an empty string (no content).
        return ""
    # Call the AI to generate the content.
    standards_content = await ai_clients.generate_content(system_prompt, user_prompt)
    return standards_content
