from setuptools import setup, find_packages

setup(
    name="dynamic_doc_gen",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "fastapi",
        "uvicorn[standard]",
        "openai",
        "beautifulsoup4",
    ],
    extras_require={
        "dev": ["pytest", "pytest-asyncio", "requests"]
    },
    python_requires=">=3.9",
    description="Dynamic Document Generation Pipeline with multi-agent architecture",
    author="Kartheek Manda",
    author_email="kartheek3197@gmail.com"
)
