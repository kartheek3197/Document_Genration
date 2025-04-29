"""
Orchestrator service that coordinates the multi-agent document generation.
Handles concurrent agent execution and final assembly of the HTML document.
"""
import asyncio
from pathlib import Path
from app.agents import header_agent, zoning_agent, standards_agent, validation_agent
from app.models.request_models import DocumentRequest

async def generate_document(request: DocumentRequest) -> str:
    """
    Orchestrate the generation of the document by invoking multiple agents asynchronously.
    This gathers content from header, zoning, and standards agents, then assembles them into the HTML template.
    Finally, runs validation/sanitization on the assembled HTML.
    """
    # Launch agents concurrently using asyncio tasks.
    header_task = asyncio.create_task(header_agent.generate_header(request))
    zoning_task = asyncio.create_task(zoning_agent.generate_zoning(request))
    # Decide whether to generate commercial standards section based on project_type.
    commercial_task = None
    if request.project_type.lower() == "commercial":
        commercial_task = asyncio.create_task(standards_agent.generate_standards(request, "commercial"))
    # General standards are generated for all project types (assuming general standards apply universally).
    general_task = asyncio.create_task(standards_agent.generate_standards(request, "general"))
    # Gather tasks (include commercial task if applicable).
    tasks = [header_task, zoning_task, general_task]
    if commercial_task:
        tasks.append(commercial_task)
    # Run all tasks concurrently and wait for results.
    results = await asyncio.gather(*tasks)
    # Unpack results in the same order.
    header_content = results[0]
    zoning_content = results[1]
    if commercial_task:
        general_content = results[2]
        commercial_content = results[3]
    else:
        general_content = results[2]
        # If project is not commercial, define a default message for commercial standards.
        commercial_content = "<p>No commercial-specific standards applicable.</p>"
    # Load the HTML template from file.
    template_path = Path(__file__).resolve().parent.parent / "templates" / "base_document.html"
    template_str = template_path.read_text(encoding="utf-8")
    # Fill in the template placeholders with static and dynamic content.
    # Static fields from request
    filled = template_str
    filled = filled.replace("{{project_name}}", request.project_name)
    filled = filled.replace("{{project_type}}", request.project_type)
    filled = filled.replace("{{location}}", request.location or "Not specified")
    # Format meeting date as a readable string.
    meeting_date_str = request.meeting_date.strftime("%B %d, %Y")
    filled = filled.replace("{{meeting_date}}", meeting_date_str)
    # Dynamic content fields from agents.
    filled = filled.replace("{{header_content}}", header_content)
    filled = filled.replace("{{zoning_content}}", zoning_content)
    filled = filled.replace("{{commercial_standards_content}}", commercial_content)
    filled = filled.replace("{{general_standards_content}}", general_content)
    # Validate and sanitize the assembled HTML.
    final_doc = validation_agent.validate_document(filled)
    return final_doc
