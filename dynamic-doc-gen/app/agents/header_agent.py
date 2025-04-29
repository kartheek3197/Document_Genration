"""
Agent responsible for generating the document header content (introduction).
"""
from app.utils import ai_clients
from app.models.request_models import DocumentRequest

async def generate_header(request: DocumentRequest) -> str:
    """
    Generate an introductory header section for the document using AI.
    This includes a brief introduction or summary including project details.
    """
    # Prepare the input data for the prompt.
    project_name = request.project_name
    project_type = request.project_type
    location = request.location or "the specified location"
    meeting_date = request.meeting_date.strftime("%B %d, %Y")
    # System prompt to instruct the AI about its role and style.
    system_prompt = (
        "You are a highly skilled report writer assistant. "
        "You will generate an introduction section for a document."
    )
    # User prompt describing what we need, including project details.
    user_prompt = (
        f"Write an introductory section for a pre-application review document for a {project_type} project. "
        f"The project name is '{project_name}'. The project is located at {location}. "
        f"The meeting took place on {meeting_date}. "
        "Provide a brief introduction summarizing these details. "
        "Write the introduction as a short paragraph wrapped in appropriate HTML tags (e.g., <p>).</p>."
    )
    # Call the AI client to generate content based on the prompts.
    intro_content = await ai_clients.generate_content(system_prompt, user_prompt)
    # Ensure the content is wrapped in a paragraph tag for consistency.
    if not intro_content.strip().startswith("<p"):
        intro_content = f"<p>{intro_content}</p>"
    return intro_content
