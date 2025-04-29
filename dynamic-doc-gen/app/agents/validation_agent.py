"""
Agent responsible for post-processing and validating the assembled HTML document.
Ensures the AI-generated content adheres to expected format and is safe.
"""
from bs4 import BeautifulSoup

def validate_document(html_doc: str) -> str:
    """
    Validate and sanitize the final HTML document string.
    - Removes any dangerous or undesirable content (like <script> tags).
    - Ensures required structural tags (like subsection titles) are present.
    - Strips inline styles in dynamic sections to avoid style conflicts.
    :param html_doc: The assembled HTML document string.
    :return: A sanitized HTML document string.
    """
    original_has_doctype = html_doc.strip().lower().startswith("<!doctype")
    # Parse the HTML document with BeautifulSoup for manipulation.
    soup = BeautifulSoup(html_doc, "html.parser")
    # Remove any <script> tags that might be present (for safety).
    for script in soup.find_all("script"):
        # Remove any script tags for security.
        script.decompose()
    # Remove inline styles from elements within dynamic sections to prevent style conflicts.
    for section in soup.find_all(attrs={"class": "ai-section"}):
        # Remove inline styles from all elements inside dynamic AI sections.
        for elem in section.find_all():
            if elem.has_attr("style"):
                del elem["style"]
    # Ensure each subsection has a subsection title.
    for subsection in soup.find_all("div", class_="subsection"):
        # Ensure each subsection has a title.
        if not subsection.find("h4", class_="subsection-title"):
            new_title = soup.new_tag("h4", **{"class": "subsection-title"})
            new_title.string = "Subsection"
            subsection.insert(0, new_title)
    # Get the HTML string after modifications.
    cleaned_html = str(soup)
    # If original had a <!DOCTYPE html>, ensure it's at the top of the output (BeautifulSoup may strip it).
    if original_has_doctype and not cleaned_html.lstrip().lower().startswith("<!doctype"):
        # Reattach DOCTYPE if it was originally present but got removed during parsing.
        cleaned_html = "<!DOCTYPE html>\n" + cleaned_html
    return cleaned_html
