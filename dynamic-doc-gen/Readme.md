# Dynamic Document Generation Pipeline

## Project Overview

This project is a **dynamic document generation pipeline** built with FastAPI. It simulates a multi-agent system where each agent generates a different part of an HTML document asynchronously. The system uses OpenAI's API to generate content for each section of the document. Key features include:
- **FastAPI asynchronous endpoints** for initiating document generation and retrieving results.
- A **multi-agent architecture**: separate agents for header content, zoning section, standards sections, and a validation agent for post-processing.
- **Asynchronous orchestration** using Python's `asyncio` to run content generation tasks concurrently for efficiency.
- A **static HTML template** with placeholders that gets filled with AI-generated content, ensuring a consistent structure and styling.
- A research integration of a **modern AI technique** (dynamic agent orchestration) discussed in `research_report.md`.

## Repository Structure

```
dynamic-doc-gen/
├── app/
│   ├── main.py                # FastAPI application initialization
│   ├── api/
│   │   └── routes.py          # API route definitions for document generation and retrieval
│   ├── agents/                # "Agents" responsible for different parts of the document
│   │   ├── header_agent.py      # Generates introductory header content
│   │   ├── zoning_agent.py      # Generates zoning section (with potential subsections)
│   │   ├── standards_agent.py   # Generates content for standards sections (commercial/general)
│   │   └── validation_agent.py  # Validates and sanitizes the assembled HTML
│   ├── services/
│   │   └── orchestrator.py    # Orchestrates the multi-agent generation process
│   ├── models/
│   │   └── request_models.py  # Pydantic models for request data
│   ├── templates/
│   │   └── base_document.html # HTML template with placeholders for dynamic content
│   └── utils/
│       └── ai_clients.py      # OpenAI API client utility
├── tests/
│   ├── test_agents.py         # Unit tests for agent functionality and validation
│   └── test_api.py            # Integration tests for API endpoints
├── research_report.md         # Report on the chosen AI technique (dynamic agent orchestration)
├── README.md                  # This file - project documentation and usage
├── requirements.txt           # Python dependencies
├── Dockerfile                 # Container setup to run the app
└── setup.py                   # Setup script for packaging (optional)
```

## Installation & Setup

### Prerequisites
- **Python 3.9+** installed.
- An **OpenAI API key** for content generation. (Obtainable from OpenAI, needed if you want to actually call the API.)

### Setting Up Locally
1. Clone this repository and navigate into it.
2. (Optional) create and activate a virtual environment:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Set your OpenAI API key as an environment variable:
   ```bash
   export OPENAI_API_KEY="your-openai-api-key-here"
   ```
5. Run the FastAPI application:
   ```bash
   uvicorn app.main:app --reload
   ```
   This will start the server at `http://127.0.0.1:8000`.

### Running with Docker
If you prefer Docker:
1. Build the Docker image:
   ```bash
   docker build -t dynamic-doc-gen .
   ```
2. Run a container from the image:
   ```bash
   docker run -p 8000:8000 -e OPENAI_API_KEY="your-openai-api-key-here" dynamic-doc-gen
   ```
   This binds the container's port 8000 to your local 8000. The API key is passed via environment variable.

### Running Tests
We use pytest for testing.
1. Make sure you have installed the dev dependencies (in `requirements.txt` or via `pip install pytest pytest-asyncio`).
2. Run tests with:
   ```bash
   pytest
   ```
   This will execute both unit tests for agents and integration tests for the API.

## Usage

Once the server is running, you can use the API endpoints:
- `POST /generate`: Initiates document generation. Expects a JSON body matching `DocumentRequest` (project_name, project_type, location, meeting_date). Example:
  ```json
  {
    "project_name": "New Office Tower",
    "project_type": "Commercial",
    "location": "Downtown Cityville",
    "meeting_date": "2025-04-01"
  }
  ```
  The response will be a JSON containing a `document_id`:
  ```json
  { "document_id": "123e4567-e89b-12d3-a456-426614174000" }
  ```
- `GET /document/{document_id}`: Retrieve the generated HTML document. 
  - If the document is ready, this returns the full HTML content (with `Content-Type: text/html`). You can open this in a browser or save it to view the formatted report.
  - If the document is still being generated, it returns a 202 status with a message indicating the generation is in progress.
  - If an invalid or unknown ID is provided, it returns a 404 error.

## How It Works

**Document Template**: The file `app/templates/base_document.html` defines the structure of the final document. It includes static sections (like the header, labels for project info) and placeholders (like `{{header_content}}`, `{{zoning_content}}`, etc.) where dynamic content will be inserted. This approach ensures that regardless of what content is generated, the overall styling remains consistent.

**Agents and Orchestrator**: When a generation request is received, the orchestrator launches several agent tasks in parallel:
- **Header Agent**: Generates an introduction or summary for the document header, potentially mentioning project details (using OpenAI API).
- **Zoning Agent**: Generates the zoning section of the document. This agent is instructed to produce content that may include multiple subsections (each with its own title and paragraph).
- **Standards Agent**: Generates content for development standards. In our implementation, we call this agent twice: once for "Commercial Development Standards" and once for "General Standards". Each call uses a prompt tailored to that category.
- These content generation calls are made concurrently (async), making the pipeline efficient.

After all content is generated, the orchestrator assembles the pieces into the HTML template, replacing each placeholder with the corresponding content. Then the **Validation Agent** (post-processing) runs:
- The validation step checks and sanitizes the HTML. For example, it removes any unexpected `<script>` tags and makes sure each dynamically created subsection has the proper structure (inserting a missing title if necessary). It also strips out any inline styles in the generated content to avoid conflicts with our template's CSS.

Finally, the assembled and validated HTML is stored (in-memory) and made available via the GET endpoint.

## Architectural Decisions

- **Asynchronous Design**: We use `asyncio` to run multiple AI calls in parallel, which is crucial since each AI call may take some time. This aligns with the requirement of asynchronous execution and greatly improves throughput.
- **Separation of Concerns**: Each agent module is responsible for one part of the document (single responsibility principle), and the orchestrator simply coordinates them. This modular design makes it easy to add or modify sections independently.
- **OpenAI Integration**: The OpenAI API usage is isolated in `ai_clients.py`. By abstracting it, we could swap in a different model or API without changing the higher-level logic. The API key is provided via an environment variable for security.
- **Input Validation**: Using Pydantic via FastAPI for the request model ensures we get structured data (and FastAPI will auto-generate docs using this model). It prevents missing required fields and handles date parsing.
- **Testing**: We included both unit tests and an integration test. Tests use monkeypatching to simulate AI outputs and make the test suite reliable and fast (no external API calls). This demonstrates how one might test components of an AI-driven system by injecting deterministic behavior.

## Running the Application

After installing and starting the application (see *Installation & Setup*), you can test the endpoints. For example, using `curl`:

```bash
curl -X POST "http://localhost:8000/generate" \
  -H "Content-Type: application/json" \
  -d '{"project_name": "Test Project", "project_type": "Commercial", "location": "Test City", "meeting_date": "2025-04-30"}'
```

This will return a JSON with a `document_id`. You can then fetch the document:

```bash
curl -X GET "http://localhost:8000/document/<document_id>"
```

Replace `<document_id>` with the ID you received. The response will be the full HTML content. You can save it to a file and open it in a browser to see the formatted document. It should contain:
- A header section with the project info filled in and an AI-generated introduction.
- A zoning section with two subsections (titles and paragraphs) generated by the AI.
- A commercial standards section (for this example, since project_type was Commercial) with a short AI-generated paragraph.
- A general standards section with a couple of subsections generated by the AI.

All sections follow the style defined in the template.

## Further Improvements

While the system meets the requirements, there are ways to enhance it:
- **Dynamic Orchestration**: As discussed in the research report, we could make the orchestrator more intelligent by letting an AI agent decide which sections to include or iterate on content for quality.
- **Error Handling**: Add more robust error handling for real-world use, such as timeouts for AI calls, retry logic, and graceful degradation if the AI service is unavailable.
- **Caching**: Cache results for identical requests to avoid recomputation and API calls if the same document is requested again.
- **Frontend**: Although not required, a simple frontend (or even a Markdown/HTML viewer in the API docs) could be added to render the HTML for demonstration purposes.
- **Security**: The validation agent already removes scripts. In a more advanced setup, we might also sanitize or limit which HTML tags are allowed from the AI, to ensure nothing unexpected makes it to the final document.

---
*End of README.*

